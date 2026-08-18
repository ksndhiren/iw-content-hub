import { Outlet, createFileRoute, useLocation, useNavigate } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import { ArrowLeft, ArrowRight, Loader2, Sparkles, Upload, X } from "lucide-react";
import { toast } from "sonner";
import { useServerFn } from "@tanstack/react-start";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  AUDIENCE_OPTIONS,
  AUCTION_LOCATION_OPTIONS,
  AUCTION_TIME_OPTIONS,
  CALL_TO_ACTION_OPTIONS,
  EQUIPMENT_CATEGORIES,
  emptyForm,
  PRINT_TYPES,
  WEB_TYPES,
  aspectForAssetType,
  buildPrompt,
  summaryTitle,
  type CreateFormState,
  type AssetNeed,
  type RequestType,
  type Audience,
  type Objective,
} from "@/lib/create-form";
import { generateImage } from "@/lib/generate.functions";
import { useGeneratedStore } from "@/lib/generated-store";
import { compositeDesign } from "@/lib/composite-design";
import logoWhite from "@/assets/jma-logo-white.png";

export const Route = createFileRoute("/_authenticated/create")({
  component: CreatePage,
});

const STEPS = ["Request details", "Creative brief", "Source image", "Review"];

function CreatePage() {
  const location = useLocation();
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<CreateFormState>(emptyForm);
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();
  const setResult = useGeneratedStore((s) => s.set);
  const generate = useServerFn(generateImage);

  if (location.pathname !== "/create") {
    return <Outlet />;
  }

  const update = <K extends keyof CreateFormState>(k: K, v: CreateFormState[K]) =>
    setForm((f) => ({ ...f, [k]: v }));

  const next = () => {
    const err = validateStep(step, form);
    if (err) return toast.error(err);
    setStep((s) => Math.min(STEPS.length - 1, s + 1));
  };
  const back = () => setStep((s) => Math.max(0, s - 1));

  const handleGenerate = async () => {
    setBusy(true);
    try {
      const prompt = buildPrompt(form);
      const size = aspectForAssetType(form.assetType);
      const { b64 } = await generate({
        data: {
          prompt,
          size,
          sourceImageDataUrl: form.sourceImageDataUrl,
        },
      });
      const rawDataUrl = `data:image/png;base64,${b64}`;
      const imageDataUrl = await compositeDesign(rawDataUrl, logoWhite, form);
      setResult({
        imageDataUrl,
        prompt,
        size,
        title: summaryTitle(form),
        form,
      });
      navigate({ to: "/create/result" });
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Generation failed";
      toast.error(msg);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-8">
      <Stepper step={step} />

      <div className="bg-card border rounded-2xl p-6 sm:p-10">
        {step === 0 && <StepRequest form={form} update={update} />}
        {step === 1 && <StepBrief form={form} update={update} />}
        {step === 2 && <StepSource form={form} update={update} />}
        {step === 3 && <StepReview form={form} />}
      </div>

      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={back} disabled={step === 0 || busy}>
          <ArrowLeft className="h-4 w-4 mr-1" /> Back
        </Button>
        {step < STEPS.length - 1 ? (
          <Button onClick={next}>
            Continue <ArrowRight className="h-4 w-4 ml-1" />
          </Button>
        ) : (
          <Button onClick={handleGenerate} disabled={busy} size="lg" className="bg-brand text-brand-foreground hover:bg-brand/90">
            {busy ? <><Loader2 className="h-4 w-4 mr-2 animate-spin" /> Generating…</> : <><Sparkles className="h-4 w-4 mr-2" /> Generate Output</>}
          </Button>
        )}
      </div>
    </div>
  );
}

function Stepper({ step }: { step: number }) {
  return (
    <div>
      <div className="flex items-center justify-between text-xs font-medium text-muted-foreground mb-3">
        <span>Step {step + 1} of {STEPS.length}</span>
        <span>{STEPS[step]}</span>
      </div>
      <div className="grid grid-cols-4 gap-2">
        {STEPS.map((_, i) => (
          <div key={i} className={`h-1.5 rounded-full ${i <= step ? "bg-brand" : "bg-muted"}`} />
        ))}
      </div>
    </div>
  );
}

function Field({ label, required, children, hint }: { label: string; required?: boolean; children: ReactNode; hint?: string }) {
  return (
    <div className="space-y-2">
      <Label className="text-sm">{label}{required && <span className="text-brand"> *</span>}</Label>
      {children}
      {hint && <p className="text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}

function StepRequest({ form, update }: { form: CreateFormState; update: <K extends keyof CreateFormState>(k: K, v: CreateFormState[K]) => void }) {
  const types = form.assetNeed === "Print Need" ? PRINT_TYPES : form.assetNeed === "Web Need" ? WEB_TYPES : [];
  return (
    <div className="grid sm:grid-cols-2 gap-6">
      <Field label="Requestor information" required>
        <Input placeholder="Name, team, or department" value={form.requestor} onChange={(e) => update("requestor", e.target.value)} />
      </Field>
      <Field label="Date of request" required>
        <Input type="date" value={form.requestDate} onChange={(e) => update("requestDate", e.target.value)} />
      </Field>
      <Field label="What kind of design asset are you requesting?" required>
        <Select value={form.assetNeed} onValueChange={(v) => { update("assetNeed", v as AssetNeed); update("assetType", ""); }}>
          <SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="Print Need">Print Need</SelectItem>
            <SelectItem value="Web Need">Web Need</SelectItem>
          </SelectContent>
        </Select>
      </Field>
      <Field label="Asset type" required>
        <Select value={form.assetType} onValueChange={(v) => update("assetType", v)} disabled={!form.assetNeed}>
          <SelectTrigger><SelectValue placeholder={form.assetNeed ? "Select" : "Pick a need first"} /></SelectTrigger>
          <SelectContent>
            {types.map((t) => <SelectItem key={t} value={t}>{t}</SelectItem>)}
          </SelectContent>
        </Select>
      </Field>
    </div>
  );
}

function StepBrief({ form, update }: { form: CreateFormState; update: <K extends keyof CreateFormState>(k: K, v: CreateFormState[K]) => void }) {
  const toggleAudience = (value: Audience, checked: boolean) => {
    const next = checked ? [...form.audience, value] : form.audience.filter((item) => item !== value);
    update("audience", next);
  };

  return (
    <div className="space-y-6">
      <Field label="Description of request" required>
        <Textarea rows={4} placeholder="Describe what the design should communicate and any important context."
          value={form.description} onChange={(e) => update("description", e.target.value)} />
      </Field>
      <div className="grid sm:grid-cols-2 gap-6">
        <Field label="Business objective" required>
          <Select value={form.objective} onValueChange={(v) => update("objective", v as Objective)}>
            <SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger>
            <SelectContent>
              {["Drive registrations","Increase bidding activity","Promote an upcoming auction","Highlight featured equipment","Attract consignors","Build brand awareness"].map((o) =>
                <SelectItem key={o} value={o}>{o}</SelectItem>)}
            </SelectContent>
          </Select>
        </Field>
        <Field label="Type of request" required>
          <Select value={form.requestType} onValueChange={(v) => update("requestType", v as RequestType)}>
            <SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger>
            <SelectContent>
              {["Auction announcement","Featured equipment","Bid reminder","Weekly promotion"].map((o) =>
                <SelectItem key={o} value={o}>{o}</SelectItem>)}
            </SelectContent>
          </Select>
        </Field>
        <Field label="Target audience" required hint="Choose all audience groups this creative should speak to.">
          <div className="grid grid-cols-2 gap-3 rounded-xl border p-4">
            {AUDIENCE_OPTIONS.map((option) => (
              <label key={option} className="flex items-center gap-2 text-sm">
                <Checkbox
                  checked={form.audience.includes(option)}
                  onCheckedChange={(checked) => toggleAudience(option, !!checked)}
                />
                <span>{option}</span>
              </label>
            ))}
          </div>
        </Field>
      </div>

      {form.requestType && (
        <div className="border-t pt-6 grid sm:grid-cols-2 gap-6">
          {form.requestType === "Auction announcement" && (<>
            <Field label="Auction name" required><Input value={form.auctionName ?? ""} onChange={(e) => update("auctionName", e.target.value)} placeholder="Brooklyn Spring Equipment Auction" /></Field>
            <Field label="Auction date" required><Input type="date" value={form.auctionDate ?? ""} onChange={(e) => update("auctionDate", e.target.value)} /></Field>
            <Field label="Auction time" required>
              <Select value={form.auctionTime ?? ""} onValueChange={(v) => update("auctionTime", v)}>
                <SelectTrigger><SelectValue placeholder="Select time" /></SelectTrigger>
                <SelectContent>
                  {AUCTION_TIME_OPTIONS.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}
                </SelectContent>
              </Select>
            </Field>
            <Field label="Auction location" required>
              <Select value={form.auctionLocation ?? ""} onValueChange={(v) => update("auctionLocation", v)}>
                <SelectTrigger><SelectValue placeholder="Select location" /></SelectTrigger>
                <SelectContent>
                  {AUCTION_LOCATION_OPTIONS.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}
                </SelectContent>
              </Select>
            </Field>
          </>)}
          {form.requestType === "Featured equipment" && (<>
            <Field label="Equipment category" required>
              <Select value={form.equipmentCategory ?? ""} onValueChange={(v) => update("equipmentCategory", v)}>
                <SelectTrigger><SelectValue placeholder="Select category" /></SelectTrigger>
                <SelectContent>
                  {EQUIPMENT_CATEGORIES.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}
                </SelectContent>
              </Select>
            </Field>
            <Field label="Equipment name" required><Input value={form.equipmentName ?? ""} onChange={(e) => update("equipmentName", e.target.value)} placeholder="Liebherr LTM 1300" /></Field>
            <Field label="Feature highlight" required><Input value={form.featureHighlight ?? ""} onChange={(e) => update("featureHighlight", e.target.value)} placeholder="All terrain crane" /></Field>
          </>)}
          {form.requestType === "Bid reminder" && (<>
            <Field label="Auction name" required><Input value={form.auctionName ?? ""} onChange={(e) => update("auctionName", e.target.value)} /></Field>
            <Field label="Auction date" required><Input type="date" value={form.auctionDate ?? ""} onChange={(e) => update("auctionDate", e.target.value)} /></Field>
            <Field label="Auction time" required>
              <Select value={form.auctionTime ?? ""} onValueChange={(v) => update("auctionTime", v)}>
                <SelectTrigger><SelectValue placeholder="Select time" /></SelectTrigger>
                <SelectContent>
                  {AUCTION_TIME_OPTIONS.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}
                </SelectContent>
              </Select>
            </Field>
            <Field label="Reminder focus" required><Input value={form.reminderFocus ?? ""} onChange={(e) => update("reminderFocus", e.target.value)} placeholder="Last chance to register and bid" /></Field>
          </>)}
          {form.requestType === "Weekly promotion" && (<>
            <Field label="Promotion headline" required><Input value={form.promotionHeadline ?? ""} onChange={(e) => update("promotionHeadline", e.target.value)} placeholder="This week at Jeff Martin" /></Field>
            <Field label="Promotion focus" required><Input value={form.promotionFocus ?? ""} onChange={(e) => update("promotionFocus", e.target.value)} placeholder="New featured lots and active bidding" /></Field>
          </>)}
          <Field label="Call to action" required>
            <Select value={form.callToAction ?? ""} onValueChange={(v) => update("callToAction", v)}>
              <SelectTrigger><SelectValue placeholder="Select call to action" /></SelectTrigger>
              <SelectContent>
                {CALL_TO_ACTION_OPTIONS.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}
              </SelectContent>
            </Select>
          </Field>
        </div>
      )}
    </div>
  );
}

function StepSource({ form, update }: { form: CreateFormState; update: <K extends keyof CreateFormState>(k: K, v: CreateFormState[K]) => void }) {
  const onFile = (file: File) => {
    if (!file.type.startsWith("image/")) return toast.error("Please upload an image file.");
    if (file.size > 8 * 1024 * 1024) return toast.error("Image must be smaller than 8 MB.");
    const reader = new FileReader();
    reader.onload = () => {
      update("noSourceImage", false);
      update("sourceImageDataUrl", reader.result as string);
      update("sourceImageName", file.name);
    };
    reader.readAsDataURL(file);
  };
  return (
    <div className="space-y-4">
      <Field label="Upload the main image" required={!form.noSourceImage} hint="JPG or PNG up to 8 MB. This is the visual reference for the AI.">
        <label className="flex items-center gap-2 text-sm">
          <Checkbox
            checked={form.noSourceImage}
            onCheckedChange={(checked) => {
              const enabled = !!checked;
              update("noSourceImage", enabled);
              if (enabled) {
                update("sourceImageDataUrl", undefined);
                update("sourceImageName", undefined);
              }
            }}
          />
          <span>I don't have an image</span>
        </label>
        {form.sourceImageDataUrl ? (
          <div className="flex items-center gap-4 p-4 border rounded-xl">
            <img src={form.sourceImageDataUrl} alt="Source" className="h-24 w-24 object-cover rounded-md border" />
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{form.sourceImageName}</p>
              <p className="text-xs text-muted-foreground">Ready to use.</p>
            </div>
            <Button variant="ghost" size="icon" onClick={() => { update("sourceImageDataUrl", undefined); update("sourceImageName", undefined); }}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        ) : !form.noSourceImage ? (
          <label className="flex flex-col items-center justify-center gap-2 p-10 border-2 border-dashed rounded-xl cursor-pointer hover:bg-muted/40 transition">
            <Upload className="h-8 w-8 text-muted-foreground" />
            <span className="text-sm font-medium">Click to upload an image</span>
            <span className="text-xs text-muted-foreground">PNG or JPG</span>
            <input type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files?.[0] && onFile(e.target.files[0])} />
          </label>
        ) : (
          <div className="rounded-xl border border-dashed p-8 text-center text-sm text-muted-foreground">
            OpenAI will generate the hero image from your brief and equipment category.
          </div>
        )}
      </Field>
    </div>
  );
}

function StepReview({ form }: { form: CreateFormState }) {
  const rows: Array<[string, string | undefined]> = [
    ["Asset request", form.assetNeed],
    ["Asset type", form.assetType],
    ["Description", form.description],
    ["Business objective", form.objective],
    ["Type of request", form.requestType],
    ["Target audience", form.audience.join(", ")],
    ["Auction name", form.auctionName],
    ["Auction date", form.auctionDate],
    ["Auction time", form.auctionTime],
    ["Auction location", form.auctionLocation],
    ["Equipment category", form.equipmentCategory],
    ["Equipment name", form.equipmentName],
    ["Feature highlight", form.featureHighlight],
    ["Reminder focus", form.reminderFocus],
    ["Promotion headline", form.promotionHeadline],
    ["Promotion focus", form.promotionFocus],
    ["Call to action", form.callToAction],
  ].filter(([, v]) => v) as Array<[string, string]>;
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold">Ready to generate</h3>
        <p className="text-sm text-muted-foreground">Review your brief and click Generate Output to create the design.</p>
      </div>
      <div className="grid sm:grid-cols-[200px_1fr] gap-x-6 gap-y-3 text-sm">
        {rows.map(([k, v]) => (
          <div key={k} className="contents">
            <div className="text-muted-foreground">{k}</div>
            <div className="font-medium text-foreground">{v}</div>
          </div>
        ))}
        {form.sourceImageDataUrl && (
          <>
            <div className="text-muted-foreground">Source image</div>
            <img src={form.sourceImageDataUrl} alt="" className="h-24 w-24 object-cover rounded-md border" />
          </>
        )}
        {form.noSourceImage && (
          <>
            <div className="text-muted-foreground">Source image</div>
            <div className="font-medium text-foreground">OpenAI-generated from brief only</div>
          </>
        )}
      </div>
    </div>
  );
}

function validateStep(step: number, f: CreateFormState): string | null {
  if (step === 0) {
    if (!f.requestor) return "Add requestor information.";
    if (!f.requestDate) return "Pick a date.";
    if (!f.assetNeed) return "Choose Print or Web.";
    if (!f.assetType) return "Pick an asset type.";
  }
  if (step === 1) {
    if (!f.description) return "Add a description.";
    if (!f.objective) return "Pick a business objective.";
    if (!f.requestType) return "Pick a request type.";
    if (f.audience.length === 0) return "Pick at least one target audience.";
    if (!f.callToAction) return "Add a call to action.";
    const map: Record<string, Array<keyof CreateFormState>> = {
      "Auction announcement": ["auctionName","auctionDate","auctionTime","auctionLocation"],
      "Featured equipment": ["equipmentCategory","equipmentName","featureHighlight"],
      "Bid reminder": ["auctionName","auctionDate","auctionTime","reminderFocus"],
      "Weekly promotion": ["promotionHeadline","promotionFocus"],
    };
    for (const k of map[f.requestType] ?? []) {
      if (!f[k]) return `Fill in all ${f.requestType.toLowerCase()} fields.`;
    }
  }
  if (step === 2 && !f.noSourceImage && !f.sourceImageDataUrl) return "Upload a source image or choose 'I don't have an image'.";
  return null;
}
