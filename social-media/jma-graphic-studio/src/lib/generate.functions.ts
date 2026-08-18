import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { requireSupabaseAuth } from "@/integrations/supabase/auth-middleware";

const inputSchema = z.object({
  prompt: z.string().min(10).max(4000),
  size: z.enum(["1024x1024", "1536x1024", "1024x1536"]),
  sourceImageDataUrl: z.string().optional(),
});

export const generateImage = createServerFn({ method: "POST" })
  .middleware([requireSupabaseAuth])
  .inputValidator((input) => inputSchema.parse(input))
  .handler(async ({ data }) => {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) throw new Error("Image generation is not configured.");

    const model = process.env.OPENAI_IMAGE_MODEL || "gpt-image-1";
    const quality = process.env.OPENAI_IMAGE_QUALITY || "low";

    // No source image: use /generations (text-to-image)
    // Source image uploaded: use /edits (image-to-image reference)
    if (!data.sourceImageDataUrl) {
      return generateWithGenerations(apiKey, data, { model, quality });
    }

    const res = await generateWithEdits(apiKey, data, { model, quality });

    if (!res.ok) {
      let msg = `Image generation failed (${res.status})`;
      try {
        const j = (await res.json()) as { error?: { message?: string; code?: string } };
        if (j.error?.code === "content_policy_violation") {
          msg = "Your prompt was rejected by the safety filter. Please rephrase and try again.";
        } else if (j.error?.message) {
          msg = j.error.message;
        }
      } catch { /* ignore */ }
      throw new Error(msg);
    }

    const json = (await res.json()) as { data: Array<{ b64_json?: string; url?: string }> };
    let b64 = json.data?.[0]?.b64_json;

    if (!b64) {
      const imageUrl = json.data?.[0]?.url;
      if (!imageUrl) throw new Error("No image returned by the model.");
      const imageRes = await fetch(imageUrl);
      if (!imageRes.ok) throw new Error(`Failed to download generated image (${imageRes.status})`);
      b64 = Buffer.from(await imageRes.arrayBuffer()).toString("base64");
    }

    return { b64, size: data.size };
  });

async function generateWithGenerations(
  apiKey: string,
  data: z.infer<typeof inputSchema>,
  opts: { model: string; quality: string },
): Promise<{ b64: string; size: string }> {
  const res = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      model: opts.model,
      prompt: data.prompt,
      n: 1,
      size: data.size,
      quality: opts.quality,
    }),
  });

  if (!res.ok) {
    let msg = `Image generation failed (${res.status})`;
    try {
      const j = (await res.json()) as { error?: { message?: string; code?: string } };
      if (j.error?.code === "content_policy_violation") {
        msg = "Your prompt was rejected by the safety filter. Please rephrase and try again.";
      } else if (j.error?.message) {
        msg = j.error.message;
      }
    } catch { /* ignore */ }
    throw new Error(msg);
  }

  const json = (await res.json()) as { data: Array<{ b64_json?: string; url?: string }> };
  let b64 = json.data?.[0]?.b64_json;

  if (!b64) {
    const imageUrl = json.data?.[0]?.url;
    if (!imageUrl) throw new Error("No image returned by the model.");
    const imageRes = await fetch(imageUrl);
    if (!imageRes.ok) throw new Error(`Failed to download generated image (${imageRes.status})`);
    b64 = Buffer.from(await imageRes.arrayBuffer()).toString("base64");
  }

  return { b64, size: data.size };
}

async function generateWithEdits(
  apiKey: string,
  data: z.infer<typeof inputSchema>,
  opts: { model: string; quality: string }
) {
  const match = data.sourceImageDataUrl!.match(/^data:(image\/[\w.+-]+);base64,(.+)$/);
  if (!match) throw new Error("The uploaded source image could not be read.");
  const [, mimeType, base64] = match;
  const bytes = Buffer.from(base64, "base64");
  const ext = mimeType.includes("png") ? "png" : mimeType.includes("webp") ? "webp" : "jpg";

  const formData = new FormData();
  formData.append("model", opts.model);
  formData.append("prompt", data.prompt);
  formData.append("size", data.size);
  formData.append("quality", opts.quality);
  formData.append("image[]", new Blob([bytes], { type: mimeType }), `source.${ext}`);
  formData.append("input_fidelity", "high");

  return fetch("https://api.openai.com/v1/images/edits", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}` },
    body: formData,
  });
}
