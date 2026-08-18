"""Canva Connect API — OAuth 2.0 + PKCE flow and design autofill wrapper."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from dotenv import load_dotenv

load_dotenv()

CANVA_CLIENT_ID = os.getenv("CANVA_CLIENT_ID")
CANVA_CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET")
CANVA_REDIRECT_URI = os.getenv("CANVA_REDIRECT_URI", "http://127.0.0.1:3000/callback")

CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize"
CANVA_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
CANVA_API_BASE = "https://api.canva.com/rest/v1"

TOKEN_FILE = Path(__file__).resolve().parent.parent / ".canva_tokens.json"

# ---------------------------------------------------------------------------
# PKCE helpers
# ---------------------------------------------------------------------------

def _generate_code_verifier() -> str:
    """Generate a random code verifier (43-128 chars, URL-safe)."""
    return secrets.token_urlsafe(64)[:128]


def _generate_code_challenge(verifier: str) -> str:
    """SHA-256 hash the verifier, then base64url-encode it."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


# ---------------------------------------------------------------------------
# Token persistence
# ---------------------------------------------------------------------------

def _save_tokens(tokens: dict) -> None:
    """Save tokens to disk (access_token, refresh_token, expires_at)."""
    tokens["saved_at"] = time.time()
    if "expires_in" in tokens:
        tokens["expires_at"] = time.time() + tokens["expires_in"]
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))


def _load_tokens() -> dict | None:
    """Load saved tokens from disk."""
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return None


def get_access_token() -> str | None:
    """Return a valid access token, refreshing if needed."""
    tokens = _load_tokens()
    if not tokens:
        return None

    # Refresh if expired (with 5 min buffer)
    if tokens.get("expires_at", 0) < time.time() + 300:
        tokens = _refresh_token(tokens["refresh_token"])
        if not tokens:
            return None

    return tokens.get("access_token")


# ---------------------------------------------------------------------------
# OAuth callback server
# ---------------------------------------------------------------------------

class _OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Tiny HTTP handler that captures the authorization code."""

    auth_code: str | None = None
    state_received: str | None = None

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/callback":
            if "code" in params:
                _OAuthCallbackHandler.auth_code = params["code"][0]
                _OAuthCallbackHandler.state_received = params.get("state", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<html><body><h2>Canva authorization successful!</h2>"
                    b"<p>You can close this tab and return to the terminal.</p>"
                    b"</body></html>"
                )
            else:
                error = params.get("error", ["unknown"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    f"<html><body><h2>Authorization failed: {error}</h2></body></html>".encode()
                )
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default HTTP log noise."""
        pass


# ---------------------------------------------------------------------------
# Auth flow
# ---------------------------------------------------------------------------

def authorize() -> dict:
    """Run the full OAuth 2.0 + PKCE flow interactively.

    Opens a browser for the user to authorize, captures the callback,
    and exchanges the code for tokens.

    Returns:
        Token dict with access_token, refresh_token, expires_in.
    """
    if not CANVA_CLIENT_ID or not CANVA_CLIENT_SECRET:
        raise ValueError("CANVA_CLIENT_ID and CANVA_CLIENT_SECRET must be set in .env")

    # Parse port from redirect URI
    parsed_redirect = urlparse(CANVA_REDIRECT_URI)
    port = parsed_redirect.port or 3000

    # PKCE
    code_verifier = _generate_code_verifier()
    code_challenge = _generate_code_challenge(code_verifier)
    state = secrets.token_urlsafe(32)

    # Build authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": CANVA_CLIENT_ID,
        "redirect_uri": CANVA_REDIRECT_URI,
        "scope": "design:content:read design:content:write design:meta:read asset:read asset:write profile:read",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    auth_url = f"{CANVA_AUTH_URL}?{urlencode(auth_params)}"

    # Start callback server
    server = HTTPServer(("127.0.0.1", port), _OAuthCallbackHandler)
    server.timeout = 120  # 2 min timeout

    print(f"\n{'='*60}")
    print("CANVA AUTHORIZATION")
    print(f"{'='*60}")
    print(f"\nOpening browser for Canva authorization...")
    print(f"If it doesn't open, visit this URL manually:\n")
    print(auth_url)
    print(f"\nWaiting for authorization (timeout: 2 minutes)...")
    print(f"{'='*60}\n")

    webbrowser.open(auth_url)

    # Wait for callback
    _OAuthCallbackHandler.auth_code = None
    _OAuthCallbackHandler.state_received = None

    while _OAuthCallbackHandler.auth_code is None:
        server.handle_request()

    server.server_close()
    auth_code = _OAuthCallbackHandler.auth_code

    # Validate state
    if _OAuthCallbackHandler.state_received != state:
        raise ValueError("State mismatch — possible CSRF attack. Aborting.")

    # Exchange code for tokens
    tokens = _exchange_code(auth_code, code_verifier)
    _save_tokens(tokens)
    print("Canva authorization successful! Tokens saved.")
    return tokens


def _exchange_code(code: str, code_verifier: str) -> dict:
    """Exchange authorization code for access + refresh tokens."""
    # Basic auth header with client_id:client_secret
    credentials = base64.b64encode(
        f"{CANVA_CLIENT_ID}:{CANVA_CLIENT_SECRET}".encode()
    ).decode()

    resp = requests.post(
        CANVA_TOKEN_URL,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": CANVA_REDIRECT_URI,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _refresh_token(refresh_token: str) -> dict | None:
    """Use a refresh token to get a new access token."""
    credentials = base64.b64encode(
        f"{CANVA_CLIENT_ID}:{CANVA_CLIENT_SECRET}".encode()
    ).decode()

    try:
        resp = requests.post(
            CANVA_TOKEN_URL,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=30,
        )
        resp.raise_for_status()
        tokens = resp.json()
        _save_tokens(tokens)
        return tokens
    except requests.RequestException as e:
        print(f"Token refresh failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Canva API helpers
# ---------------------------------------------------------------------------

def _api_headers() -> dict:
    """Return authorization headers for Canva API calls."""
    token = get_access_token()
    if not token:
        raise ValueError("No valid Canva token. Run `authorize()` first.")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def list_designs(limit: int = 10) -> dict:
    """List the user's Canva designs."""
    resp = requests.get(
        f"{CANVA_API_BASE}/designs",
        headers=_api_headers(),
        params={"limit": limit},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_design(design_id: str) -> dict:
    """Get details for a specific design."""
    resp = requests.get(
        f"{CANVA_API_BASE}/designs/{design_id}",
        headers=_api_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def autofill_design(brand_template_id: str, data: dict, title: str | None = None) -> dict:
    """Create a new design by autofilling a brand template.

    Args:
        brand_template_id: The Canva brand template ID.
        data: Dict mapping template field names to their values.
              Text fields: {"type": "text", "text": "value"}
              Image fields: {"type": "image", "asset_id": "id"}
        title: Optional title for the new design.

    Returns:
        Dict with the new design details.
    """
    payload = {
        "brand_template_id": brand_template_id,
        "data": data,
    }
    if title:
        payload["title"] = title

    resp = requests.post(
        f"{CANVA_API_BASE}/autofills",
        headers=_api_headers(),
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def get_autofill_job(job_id: str) -> dict:
    """Check the status of an autofill job."""
    resp = requests.get(
        f"{CANVA_API_BASE}/autofills/{job_id}",
        headers=_api_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def upload_asset(file_path: str, name: str | None = None) -> dict:
    """Upload an image asset to Canva.

    Args:
        file_path: Local path to the image file.
        name: Optional display name for the asset.

    Returns:
        Dict with asset_id and other metadata.
    """
    token = get_access_token()
    if not token:
        raise ValueError("No valid Canva token. Run `authorize()` first.")

    file_path_obj = Path(file_path)
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml",
    }
    content_type = mime_types.get(file_path_obj.suffix.lower(), "image/png")

    # Step 1: Create the upload job
    metadata = {"name_base64": base64.b64encode((name or file_path_obj.stem).encode()).decode()}

    resp = requests.post(
        f"{CANVA_API_BASE}/asset-uploads",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
            "Asset-Upload-Metadata": json.dumps(metadata),
        },
        data=file_path_obj.read_bytes(),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def export_design(design_id: str, format: str = "png") -> dict:
    """Export a Canva design to a file format.

    Args:
        design_id: The design to export.
        format: Export format — "png", "jpg", "pdf", "mp4".

    Returns:
        Dict with export job details including download URL when ready.
    """
    payload = {
        "design_id": design_id,
        "format": {"type": format},
    }
    resp = requests.post(
        f"{CANVA_API_BASE}/exports",
        headers=_api_headers(),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_export_job(job_id: str) -> dict:
    """Check the status of an export job and get download URL."""
    resp = requests.get(
        f"{CANVA_API_BASE}/exports/{job_id}",
        headers=_api_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def wait_for_job(job_type: str, job_id: str, max_wait: int = 60) -> dict:
    """Poll a job until it completes.

    Args:
        job_type: "autofills" or "exports"
        job_id: The job ID to poll.
        max_wait: Maximum seconds to wait.

    Returns:
        Final job status dict.
    """
    get_fn = get_autofill_job if job_type == "autofills" else get_export_job
    start = time.time()
    while time.time() - start < max_wait:
        result = get_fn(job_id)
        status = result.get("job", {}).get("status", result.get("status"))
        if status in ("success", "completed", "failed"):
            return result
        time.sleep(2)
    raise TimeoutError(f"Job {job_id} did not complete within {max_wait}s")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "auth":
        authorize()
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        token = get_access_token()
        if token:
            designs = list_designs()
            print(json.dumps(designs, indent=2))
        else:
            print("Not authenticated. Run: python tools/canva_api.py auth")
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        tokens = _load_tokens()
        if tokens:
            expires_at = tokens.get("expires_at", 0)
            remaining = max(0, expires_at - time.time())
            print(f"Authenticated: Yes")
            print(f"Token expires in: {int(remaining // 60)} minutes")
        else:
            print("Authenticated: No")
            print("Run: python tools/canva_api.py auth")
    else:
        print("Usage:")
        print("  python tools/canva_api.py auth     — Run OAuth flow")
        print("  python tools/canva_api.py status   — Check token status")
        print("  python tools/canva_api.py list     — List your designs")
