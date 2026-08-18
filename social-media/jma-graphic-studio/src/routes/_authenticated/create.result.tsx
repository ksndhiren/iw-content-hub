import { createFileRoute, Link, Navigate, useNavigate } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Download, RefreshCw, Save, Sparkles, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { useServerFn } from "@tanstack/react-start";
import { Button } from "@/components/ui/button";
import { useGeneratedStore } from "@/lib/generated-store";
import { generateImage } from "@/lib/generate.functions";
import { aspectForAssetType } from "@/lib/create-form";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { compositeDesign } from "@/lib/composite-design";
import logoWhite from "@/assets/jma-logo-white.png";

declare global {
  interface Window {
    Canva?: {
      DesignButton: {
        initialize(opts: { apiKey: string }): Promise<CanvaApi>;
      };
    };
  }
}

interface CanvaApi {
  createDesign(opts: {
    design: { type: string };
    media?: { items: Array<{ type: string; url: string; altText?: string }> };
    onDesignPublish?: (opts: { exportUrl: string }) => void;
  }): Promise<void>;
}

function canvaDesignType(assetType: string): string {
  if (["Flyer", "Handout", "Print Ad", "Catalog"].includes(assetType)) return "Poster";
  if (["Banner", "Website Ad"].includes(assetType)) return "Presentation";
  if (assetType === "Email") return "EmailNewsletter";
  return "SocialMedia";
}

export const Route = createFileRoute("/_authenticated/create/result")({
  component: ResultPage,
});

function ResultPage() {
  const result = useGeneratedStore((s) => s.result);
  const setResult = useGeneratedStore((s) => s.set);
  const { user } = useAuth();
  const generate = useServerFn(generateImage);
  const navigate = useNavigate();
  const [busy, setBusy] = useState<"regen" | "save" | "canva" | null>(null);
  const [saved, setSaved] = useState(false);
  const canvaApiRef = useRef<CanvaApi | null>(null);

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://sdk.canva.com/designbutton/v2/api.js";
    script.async = true;
    document.body.appendChild(script);
    return () => { document.body.removeChild(script); };
  }, []);

  if (!result) return <Navigate to="/create" />;

  const downloadImage = () => {
    const a = document.createElement("a");
    a.href = result.imageDataUrl;
    a.download = `${result.title.replace(/[^a-z0-9]+/gi, "-").toLowerCase() || "design"}.png`;
    a.click();
  };

  const editInCanva = async () => {
    const apiKey = import.meta.env.VITE_CANVA_API_KEY as string | undefined;
    if (!apiKey) {
      toast.error("Canva API key not configured (VITE_CANVA_API_KEY).");
      return;
    }
    if (!user) return;
    setBusy("canva");
    try {
      // Upload to Supabase to get a short-lived public URL Canva can fetch
      const res = await fetch(result.imageDataUrl);
      const blob = await res.blob();
      const path = `${user.id}/canva-tmp-${Date.now()}.png`;
      const up = await supabase.storage.from("designs").upload(path, blob, { contentType: "image/png" });
      if (up.error) throw up.error;
      const { data: signed } = await supabase.storage.from("designs").createSignedUrl(path, 60 * 60);
      if (!signed?.signedUrl) throw new Error("Could not generate a public URL for the image.");

      // Initialise (or reuse) Canva SDK
      if (!canvaApiRef.current) {
        if (!window.Canva?.DesignButton) throw new Error("Canva SDK not loaded yet - try again in a moment.");
        canvaApiRef.current = await window.Canva.DesignButton.initialize({ apiKey });
      }

      await canvaApiRef.current.createDesign({
        design: { type: canvaDesignType(result.form.assetType) },
        media: { items: [{ type: "image", url: signed.signedUrl, altText: result.title }] },
        onDesignPublish: ({ exportUrl }) => {
          toast.success("Design exported from Canva!");
          console.info("Canva export URL:", exportUrl);
        },
      });
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Could not open Canva.");
    } finally {
      setBusy(null);
    }
  };

  const regenerate = async () => {
    setBusy("regen");
    try {
      const { b64 } = await generate({
        data: {
          prompt: result.prompt,
          size: aspectForAssetType(result.form.assetType),
          sourceImageDataUrl: result.form.sourceImageDataUrl,
        },
      });
      const rawDataUrl = `data:image/png;base64,${b64}`;
      const imageDataUrl = await compositeDesign(rawDataUrl, logoWhite, result.form);
      setResult({ ...result, imageDataUrl });
      setSaved(false);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Regeneration failed");
    } finally {
      setBusy(null);
    }
  };

  const saveToLibrary = async () => {
    if (!user) return;
    setBusy("save");
    try {
      const res = await fetch(result.imageDataUrl);
      const blob = await res.blob();
      const path = `${user.id}/${Date.now()}.png`;
      const up = await supabase.storage.from("designs").upload(path, blob, { contentType: "image/png" });
      if (up.error) throw up.error;
      const { data: signed } = await supabase.storage.from("designs").createSignedUrl(path, 60 * 60 * 24 * 365 * 5);
      const { error } = await supabase.from("designs").insert({
        user_id: user.id,
        title: result.title,
        image_url: signed?.signedUrl ?? path,
        generation_prompt: result.prompt,
        form_answers: JSON.parse(JSON.stringify(result.form)),
      });
      if (error) throw error;
      setSaved(true);
      toast.success("Saved to your library");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setBusy(null);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <p className="text-sm text-muted-foreground">Result</p>
          <h1 className="text-3xl font-bold tracking-tight">{result.title}</h1>
        </div>
        <Link to="/create" className="text-sm text-muted-foreground hover:text-foreground">← Start over</Link>
      </div>

      <div className="rounded-2xl border bg-card overflow-hidden">
        <div className="relative flex max-h-[72vh] min-h-[24rem] items-center justify-center bg-muted/50 p-4 sm:p-6">
          <img
            src={result.imageDataUrl}
            alt={result.title}
            className="max-h-[calc(72vh-2rem)] w-full object-contain"
          />
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={downloadImage} className="gap-2"><Download className="h-4 w-4" /> Download</Button>
        <Button onClick={saveToLibrary} variant="outline" disabled={busy === "save" || saved} className="gap-2">
          {busy === "save" ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
          {saved ? "Saved" : "Save to Library"}
        </Button>
        <Button onClick={regenerate} variant="outline" disabled={busy === "regen"} className="gap-2">
          {busy === "regen" ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
          Regenerate
        </Button>
        <Button
          onClick={editInCanva}
          disabled={busy === "canva"}
          className="gap-2 bg-[#7D2AE8] hover:bg-[#6a22c9] text-white"
        >
          {busy === "canva" ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 4.5a7.5 7.5 0 1 1 0 15 7.5 7.5 0 0 1 0-15zm0 2.25a5.25 5.25 0 1 0 0 10.5A5.25 5.25 0 0 0 12 6.75z"/>
            </svg>
          )}
          Edit in Canva
        </Button>
        <Button onClick={() => navigate({ to: "/saved" })} variant="ghost" className="gap-2 ml-auto">
          <Sparkles className="h-4 w-4" /> View library
        </Button>
      </div>
    </div>
  );
}

