#!/usr/bin/env python3
"""
Meta Business Suite API Automation
Handles posting to Instagram, Facebook, and Threads for Internwise campaign.
Requires: Page Access Token, Page ID, Instagram Business Account ID
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

@dataclass
class PostConfig:
    """Configuration for a single post"""
    post_id: int
    date: str  # Format: "2026-04-14"
    time: str  # Format: "14:00" (2:00 PM)
    type: str  # "carousel" or "single_image"
    image_files: List[str]  # List of image file paths
    caption: str
    platforms: List[str]  # ["instagram", "facebook", "threads"]
    hashtags: str

class MetaBusinessSuiteAPI:
    """Handles all Meta API interactions"""

    def __init__(self, page_access_token: str, page_id: str, instagram_business_account_id: str):
        """
        Initialize Meta API client

        Args:
            page_access_token: Facebook Page Access Token
            page_id: Facebook Page ID
            instagram_business_account_id: Instagram Business Account ID (linked to FB page)
        """
        self.page_access_token = page_access_token
        self.page_id = page_id
        self.instagram_business_account_id = instagram_business_account_id
        self.api_version = "v19.0"  # Current Meta API version
        self.base_url = f"https://graph.instagram.com/{self.api_version}"
        self.facebook_base_url = f"https://graph.facebook.com/{self.api_version}"

    def _make_request(self, method: str, url: str, data: Dict = None, files: Dict = None) -> Dict:
        """
        Make HTTP request to Meta API

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full API endpoint URL
            data: JSON data for POST requests
            files: Files for multipart upload

        Returns:
            Response JSON
        """
        params = {"access_token": self.page_access_token}

        try:
            if method == "POST":
                response = requests.post(url, params=params, json=data, files=files, timeout=30)
            elif method == "GET":
                response = requests.get(url, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise

    def upload_image(self, image_path: str, is_carousel_item: bool = False) -> str:
        """
        Upload image to Instagram/Facebook

        Args:
            image_path: Path to PNG image file
            is_carousel_item: Whether this is part of a carousel

        Returns:
            Image/Media ID
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}

            if is_carousel_item:
                # Upload as carousel item
                url = f"{self.base_url}/{self.instagram_business_account_id}/media"
                data = {"media_type": "IMAGE"}
            else:
                # Upload as single image
                url = f"{self.base_url}/{self.instagram_business_account_id}/media"
                data = {"media_type": "IMAGE"}

            result = self._make_request("POST", url, data=data, files=files)
            return result.get('id')

    def create_carousel_post(self, image_ids: List[str], caption: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Create carousel post on Instagram

        Args:
            image_ids: List of uploaded image IDs
            caption: Post caption with hashtags
            schedule_time: ISO 8601 datetime to schedule post (optional)

        Returns:
            Post creation response with post ID
        """
        data = {
            "media_type": "CAROUSEL",
            "children": image_ids,
            "caption": caption,
            "user_tags": []
        }

        if schedule_time:
            data["scheduled_publish_time"] = schedule_time

        url = f"{self.base_url}/{self.instagram_business_account_id}/media"
        result = self._make_request("POST", url, data=data)

        if "id" in result:
            # Now publish the container
            publish_result = self._publish_container(result['id'], schedule_time is None)
            return publish_result
        return result

    def create_single_image_post(self, image_id: str, caption: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Create single image post on Instagram

        Args:
            image_id: Uploaded image ID
            caption: Post caption with hashtags
            schedule_time: ISO 8601 datetime to schedule post (optional)

        Returns:
            Post creation response with post ID
        """
        data = {
            "media_type": "IMAGE",
            "image_url": f"https://graph.instagram.com/{self.api_version}/{image_id}?fields=media_url&access_token={self.page_access_token}",
            "caption": caption,
            "user_tags": []
        }

        if schedule_time:
            data["scheduled_publish_time"] = schedule_time

        url = f"{self.base_url}/{self.instagram_business_account_id}/media"
        result = self._make_request("POST", url, data=data)

        if "id" in result:
            # Now publish the container
            publish_result = self._publish_container(result['id'], schedule_time is None)
            return publish_result
        return result

    def _publish_container(self, media_id: str, publish_immediately: bool = True) -> Dict:
        """
        Publish a media container (carousel or single image)

        Args:
            media_id: Media container ID
            publish_immediately: Whether to publish now or keep as draft

        Returns:
            Publication response
        """
        url = f"{self.base_url}/{media_id}/publish"
        data = {} if publish_immediately else {}

        return self._make_request("POST", url, data=data)

    def post_to_facebook(self, image_url: str, caption: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Post image to Facebook page

        Args:
            image_url: URL of image to post
            caption: Post caption
            schedule_time: ISO 8601 datetime to schedule post (optional)

        Returns:
            Post creation response with post ID
        """
        data = {
            "source": image_url,
            "caption": caption,
            "published": not schedule_time,
        }

        if schedule_time:
            # Convert to Unix timestamp
            dt = datetime.fromisoformat(schedule_time.replace('Z', '+00:00'))
            data["scheduled_publish_time"] = int(dt.timestamp())

        url = f"{self.facebook_base_url}/{self.page_id}/feed"
        return self._make_request("POST", url, data=data)

    def post_to_threads(self, image_url: str, caption: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Post to Threads via Instagram Graph API

        Args:
            image_url: URL of image to post
            caption: Post caption
            schedule_time: ISO 8601 datetime to schedule post (optional)

        Returns:
            Post creation response with post ID
        """
        # Threads posts are created via Instagram Graph API with media_type="THREADS_IMAGE"
        data = {
            "image_url": image_url,
            "caption": caption,
            "media_type": "THREADS_IMAGE"
        }

        if schedule_time:
            data["scheduled_publish_time"] = schedule_time

        url = f"{self.base_url}/{self.instagram_business_account_id}/media"
        return self._make_request("POST", url, data=data)


class PostScheduler:
    """Manages post scheduling and batch uploads"""

    # Campaign posts configuration
    POSTS = [
        {
            "post_id": 1,
            "date": "2026-04-14",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_comeback",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Comeback Carousel"
        },
        {
            "post_id": 2,
            "date": "2026-04-15",
            "time": "14:00",
            "type": "single_image",
            "file_prefix": "tipcard_cv_mistakes",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "CV Mistakes Tip Card"
        },
        {
            "post_id": 3,
            "date": "2026-04-16",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_star_method",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "STAR Method Carousel"
        },
        {
            "post_id": 4,
            "date": "2026-04-17",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_chatgpt_prompts",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "ChatGPT Prompts Carousel"
        },
        {
            "post_id": 5,
            "date": "2026-04-18",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_ikigai",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Ikigai Carousel"
        },
        {
            "post_id": 6,
            "date": "2026-04-21",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_networking",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Networking 101 Carousel"
        },
        {
            "post_id": 7,
            "date": "2026-04-22",
            "time": "14:00",
            "type": "single_image",
            "file_prefix": "tipcard_confidence",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Confidence Tip Card"
        },
        {
            "post_id": 8,
            "date": "2026-04-23",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_ai_jobs",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "AI Jobs Carousel"
        },
        {
            "post_id": 9,
            "date": "2026-04-24",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_wealth",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Wealth Carousel"
        },
        {
            "post_id": 10,
            "date": "2026-04-25",
            "time": "14:00",
            "type": "carousel",
            "file_prefix": "carousel_campaign_close",
            "platforms": ["instagram", "facebook", "threads"],
            "title": "Campaign Close Carousel"
        },
    ]

    def __init__(self, tools_dir: str, campaigns_dir: str):
        """
        Initialize scheduler

        Args:
            tools_dir: Path to tools directory containing carousel/tipcard scripts
            campaigns_dir: Path to campaigns directory with outputs
        """
        self.tools_dir = Path(tools_dir)
        self.campaigns_dir = Path(campaigns_dir)

    def get_image_paths(self, post_config: Dict) -> Tuple[List[str], str]:
        """
        Get image paths and caption for a post

        Args:
            post_config: Post configuration dict

        Returns:
            Tuple of (image_paths, caption)
        """
        post_id = post_config["post_id"]
        file_prefix = post_config["file_prefix"]
        post_type = post_config["type"]

        # Generate images by running the carousel/tipcard script
        script_path = self.tools_dir / f"{file_prefix}.py"

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Run the script to generate images
        import subprocess
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(self.tools_dir)
        )

        if result.returncode != 0:
            print(f"Error running {file_prefix}: {result.stderr}")
            raise RuntimeError(f"Failed to generate images for post {post_id}")

        # Find generated images
        output_dir = self.campaigns_dir / f"wk{self._get_week(post_config['date'])}-day{self._get_day(post_id)}-{file_prefix.replace('carousel_', '').replace('tipcard_', '')}"

        # Look for existing output directory structure
        output_dirs = list(self.campaigns_dir.glob(f"*{file_prefix.replace('carousel_', '').replace('tipcard_', '')}*"))

        if not output_dirs:
            raise FileNotFoundError(f"No output directory found for {file_prefix}")

        output_dir = output_dirs[-1]  # Use most recent

        # Get image files
        if post_type == "carousel":
            image_paths = sorted([str(p) for p in output_dir.glob("slide_*.png")])
        else:  # single_image
            image_paths = [str(p) for p in output_dir.glob("*.png")]

        # Get caption from copy.md
        copy_file = output_dir / "copy.md"
        caption = ""
        if copy_file.exists():
            with open(copy_file, 'r') as f:
                content = f.read()
                # Extract caption (usually after "### Caption" section)
                if "### Caption" in content:
                    caption = content.split("### Caption")[1].strip()
                elif "### Instagram / Facebook / LinkedIn / Threads" in content:
                    caption = content.split("### Instagram / Facebook / LinkedIn / Threads")[1].split("###")[0].strip()

        return image_paths, caption

    def _get_week(self, date_str: str) -> int:
        """Get week number from date"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.month == 4:
            if date.day <= 18:
                return 1
            else:
                return 2
        return 1

    def _get_day(self, post_id: int) -> int:
        """Get day number (cycles 1-5 per week)"""
        return ((post_id - 1) % 5) + 1

    def schedule_all_posts(self, api: MetaBusinessSuiteAPI, dry_run: bool = False) -> Dict:
        """
        Schedule all posts for the campaign

        Args:
            api: MetaBusinessSuiteAPI instance
            dry_run: If True, only show what would be posted without actually posting

        Returns:
            Schedule summary
        """
        scheduled = []
        errors = []

        for post_config in self.POSTS:
            try:
                print(f"\n📅 Processing Post {post_config['post_id']}: {post_config['title']}")

                # Get images and caption
                image_paths, caption = self.get_image_paths(post_config)

                # Calculate scheduled time
                date_str = post_config['date']
                time_str = post_config['time']
                scheduled_time = f"{date_str}T{time_str}:00+01:00"  # UK timezone (BST/GMT+1)

                print(f"   Images: {len(image_paths)} file(s)")
                print(f"   Scheduled: {scheduled_time}")
                print(f"   Platforms: {', '.join(post_config['platforms'])}")
                print(f"   Caption preview: {caption[:100]}...")

                if dry_run:
                    scheduled.append({
                        "post_id": post_config['post_id'],
                        "title": post_config['title'],
                        "status": "DRY_RUN",
                        "scheduled_time": scheduled_time
                    })
                    continue

                # Upload images
                image_ids = []
                for image_path in image_paths:
                    image_id = api.upload_image(image_path, is_carousel_item=post_config['type'] == 'carousel')
                    image_ids.append(image_id)
                    print(f"   ✓ Uploaded: {Path(image_path).name}")
                    time.sleep(0.5)  # Rate limiting

                # Create posts based on type
                if post_config['type'] == 'carousel':
                    # Instagram carousel
                    if 'instagram' in post_config['platforms']:
                        result = api.create_carousel_post(image_ids, caption, scheduled_time)
                        print(f"   ✓ Instagram carousel scheduled (ID: {result.get('id', 'N/A')})")

                elif post_config['type'] == 'single_image':
                    # Single image post
                    if 'instagram' in post_config['platforms']:
                        result = api.create_single_image_post(image_ids[0], caption, scheduled_time)
                        print(f"   ✓ Instagram post scheduled (ID: {result.get('id', 'N/A')})")

                # Facebook posts
                if 'facebook' in post_config['platforms'] and image_ids:
                    # Get image URL from first image
                    fb_result = api.post_to_facebook(
                        image_url=image_paths[0],
                        caption=caption,
                        schedule_time=scheduled_time
                    )
                    print(f"   ✓ Facebook post scheduled (ID: {fb_result.get('id', 'N/A')})")

                # Threads posts (via Instagram API)
                if 'threads' in post_config['platforms'] and image_ids:
                    threads_result = api.post_to_threads(
                        image_url=image_paths[0],
                        caption=caption,
                        schedule_time=scheduled_time
                    )
                    print(f"   ✓ Threads post scheduled (ID: {threads_result.get('id', 'N/A')})")

                scheduled.append({
                    "post_id": post_config['post_id'],
                    "title": post_config['title'],
                    "status": "SCHEDULED",
                    "scheduled_time": scheduled_time,
                    "image_count": len(image_ids)
                })

            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
                errors.append({
                    "post_id": post_config['post_id'],
                    "title": post_config['title'],
                    "error": str(e)
                })

        return {
            "total_posts": len(self.POSTS),
            "scheduled": len(scheduled),
            "errors": len(errors),
            "posts": scheduled,
            "error_details": errors
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Meta Business Suite automation for Internwise")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted without actually posting")
    parser.add_argument("--test-credentials", action="store_true", help="Test API credentials")
    parser.add_argument("--schedule", action="store_true", default=True, help="Schedule posts")

    args = parser.parse_args()

    # Get credentials from environment or prompt
    page_access_token = os.getenv("META_PAGE_ACCESS_TOKEN")
    page_id = os.getenv("META_PAGE_ID")
    instagram_business_account_id = os.getenv("META_INSTAGRAM_BUSINESS_ACCOUNT_ID")

    if not all([page_access_token, page_id, instagram_business_account_id]):
        print("\n⚠️  Missing Meta API credentials!")
        print("\nPlease set these environment variables:")
        print("  META_PAGE_ACCESS_TOKEN - Your Facebook Page Access Token")
        print("  META_PAGE_ID - Your Facebook Page ID")
        print("  META_INSTAGRAM_BUSINESS_ACCOUNT_ID - Your Instagram Business Account ID")
        print("\nOr add them to .env file in the project root")
        print("\n📖 Setup guide:")
        print("  1. Go to https://developers.facebook.com/apps")
        print("  2. Create/select your app")
        print("  3. Add Instagram Graph API product")
        print("  4. Generate Page Access Token with these permissions:")
        print("     - instagram_business_management")
        print("     - pages_manage_metadata")
        print("     - pages_read_engagement")
        print("     - pages_manage_posts")
        print("     - pages_read_user_content")
        return

    # Initialize API
    api = MetaBusinessSuiteAPI(page_access_token, page_id, instagram_business_account_id)

    # Test credentials
    if args.test_credentials:
        print("🔐 Testing Meta API credentials...")
        try:
            # Try to fetch page info
            url = f"https://graph.facebook.com/v19.0/{page_id}"
            result = api._make_request("GET", url)
            if "name" in result:
                print(f"✓ Credentials valid!")
                print(f"  Page: {result['name']}")
                print(f"  Page ID: {page_id}")
                print(f"  Instagram Account ID: {instagram_business_account_id}")
            else:
                print(f"✗ Invalid credentials")
        except Exception as e:
            print(f"✗ Error: {e}")
        return

    # Initialize scheduler
    tools_dir = "/Users/abhishekutkarsha/Claude/IW social media/tools"
    campaigns_dir = "/Users/abhishekutkarsha/Claude/IW social media/campaigns/outputs"
    scheduler = PostScheduler(tools_dir, campaigns_dir)

    # Schedule posts
    print("\n🚀 Internwise Campaign - Meta Business Suite Automation")
    print("=" * 60)

    if args.dry_run:
        print("📋 DRY RUN MODE - No posts will be created")

    result = scheduler.schedule_all_posts(api, dry_run=args.dry_run)

    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY")
    print("=" * 60)
    print(f"Total posts to schedule: {result['total_posts']}")
    print(f"Successfully scheduled: {result['scheduled']}")
    print(f"Errors: {result['errors']}")

    if result['error_details']:
        print("\n❌ ERRORS:")
        for error in result['error_details']:
            print(f"  Post {error['post_id']} ({error['title']}): {error['error']}")

    # Save results
    output_file = "/Users/abhishekutkarsha/Claude/IW social media/scheduling_results.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Results saved to: {output_file}")


if __name__ == "__main__":
    main()
