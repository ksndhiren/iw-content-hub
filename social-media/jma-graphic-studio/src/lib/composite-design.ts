import type { CreateFormState } from "./create-form";

const YELLOW       = "#f2a900";
const YELLOW_LIGHT = "#ffd266";
const YELLOW_DARK  = "#a06f00";
const WHITE        = "#ffffff";
const OFFWHITE     = "#f4ede0";
const BLACK        = "#000000";

const FONT_HEADING = '"Gotham Black", "Arial Black", Impact, sans-serif';
const FONT_BODY    = '"Articulat", "Helvetica Neue", Arial, sans-serif';

async function ensureFontsLoaded(): Promise<void> {
  const gotham    = new FontFace("Gotham Black", "url(/fonts/Gotham-Black.otf)",    { weight: "900", style: "normal" });
  const articulat = new FontFace("Articulat",    "url(/fonts/Articulat-Normal.ttf)", { weight: "400", style: "normal" });
  const [g, a] = await Promise.allSettled([gotham.load(), articulat.load()]);
  if (g.status === "fulfilled") document.fonts.add(g.value);
  if (a.status === "fulfilled") document.fonts.add(a.value);
  await document.fonts.ready;
}

function clearShadow(ctx: CanvasRenderingContext2D) {
  ctx.shadowColor = "transparent";
  ctx.shadowBlur = ctx.shadowOffsetX = ctx.shadowOffsetY = 0;
}

function roundRect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
  ctx.beginPath();
  ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function extractText(f: CreateFormState) {
  let headline = "", subHeadline = "", extra = "";
  switch (f.requestType) {
    case "Auction announcement":
      headline = (f.auctionName ?? "").toUpperCase(); subHeadline = "PUBLIC AUCTION"; break;
    case "Featured equipment":
      headline = (f.equipmentName ?? "").toUpperCase();
      subHeadline = (f.equipmentCategory ?? "").toUpperCase();
      extra = f.featureHighlight ?? ""; break;
    case "Bid reminder":
      headline = (f.auctionName ?? "").toUpperCase();
      subHeadline = "LIVE & ONLINE BIDDING"; extra = f.reminderFocus ?? ""; break;
    case "Weekly promotion":
      headline = (f.promotionHeadline ?? "").toUpperCase();
      subHeadline = (f.promotionFocus ?? "").toUpperCase(); break;
  }
  const dateTime = [f.auctionDate, f.auctionTime].filter(Boolean).join("  •  ");
  return { headline, subHeadline, extra, dateTime, location: f.auctionLocation ?? "", cta: f.callToAction ? f.callToAction.toUpperCase() : "" };
}

// Pick which word in the headline to colour yellow — prefer the middle word
function yellowWordIndex(words: string[]): number {
  if (words.length <= 1) return -1;       // 1 word: all white
  if (words.length === 2) return 1;       // 2 words: 2nd is yellow
  return Math.floor(words.length / 2);    // 3+ words: middle is yellow
}

// Wrap by words, returning lines of word indices so we can colour them
function wrapByWords(ctx: CanvasRenderingContext2D, words: string[], maxWidth: number): number[][] {
  const lines: number[][] = [];
  let currentLine: number[] = [];
  let currentWidth = 0;
  const spaceW = ctx.measureText(" ").width;
  for (let i = 0; i < words.length; i++) {
    const w = ctx.measureText(words[i]).width;
    const add = currentLine.length === 0 ? w : spaceW + w;
    if (currentLine.length > 0 && currentWidth + add > maxWidth) {
      lines.push(currentLine);
      currentLine = [i];
      currentWidth = w;
    } else {
      currentLine.push(i);
      currentWidth += add;
    }
  }
  if (currentLine.length) lines.push(currentLine);
  return lines;
}

// Draw text with two-pass shadow: glow + crisp drop shadow
function drawTextStack(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, sz: number, color: string, glow: string) {
  ctx.save();
  ctx.shadowColor = glow; ctx.shadowBlur = Math.round(sz * 0.45);
  ctx.fillStyle = color; ctx.fillText(text, x, y);
  ctx.restore();
  ctx.save();
  ctx.shadowColor = "rgba(0,0,0,0.92)";
  ctx.shadowBlur    = Math.round(sz * 0.10);
  ctx.shadowOffsetX = Math.round(sz * 0.03);
  ctx.shadowOffsetY = Math.round(sz * 0.06);
  ctx.fillStyle = color; ctx.fillText(text, x, y);
  ctx.restore();
}

// Smart logo corner: score four corners by darkness + uniformity
function pickLogoCorner(ctx: CanvasRenderingContext2D, W: number, H: number, lw: number, lh: number, pad: number) {
  const samples = [
    { x: pad,         y: pad,         tag: "tl" as const },
    { x: W - lw - pad, y: pad,         tag: "tr" as const },
    { x: pad,         y: H - lh - pad, tag: "bl" as const },
    { x: W - lw - pad, y: H - lh - pad, tag: "br" as const },
  ];
  let best = samples[3]; let bestScore = -Infinity;
  for (const s of samples) {
    try {
      const data = ctx.getImageData(s.x, s.y, lw, lh).data;
      let lumSum = 0, lumSq = 0, n = data.length / 4;
      for (let i = 0; i < data.length; i += 4) {
        const l = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
        lumSum += l; lumSq += l * l;
      }
      const mean = lumSum / n;
      const variance = lumSq / n - mean * mean;
      const score = (255 - mean) - variance * 0.04;
      if (score > bestScore) { bestScore = score; best = s; }
    } catch { /* getImageData can fail on tainted canvas; fallback br */ }
  }
  return best;
}

export function compositeDesign(imageDataUrl: string, logoSrc: string, form: CreateFormState): Promise<string> {
  return new Promise((resolve, reject) => {
    ensureFontsLoaded().then(() => {
      const baseImg = new Image();
      baseImg.onload = () => {
        const logoImg = new Image();
        logoImg.onload = () => {
          const canvas = document.createElement("canvas");
          canvas.width = baseImg.width; canvas.height = baseImg.height;
          const ctx = canvas.getContext("2d");
          if (!ctx) return reject(new Error("Canvas 2D not available"));

          ctx.drawImage(baseImg, 0, 0);

          const W   = canvas.width;
          const H   = canvas.height;
          const pad = Math.round(W * 0.060);

          // ── DRAMATIC GRADIENT OVERLAYS ────────────────────────────
          const headerH   = Math.round(H * 0.52);
          const footerTop = Math.round(H * 0.58);

          const hGrad = ctx.createLinearGradient(0, 0, 0, headerH);
          hGrad.addColorStop(0,    "rgba(0,0,0,0.96)");
          hGrad.addColorStop(0.55, "rgba(0,0,0,0.82)");
          hGrad.addColorStop(0.85, "rgba(0,0,0,0.20)");
          hGrad.addColorStop(1,    "rgba(0,0,0,0)");
          ctx.fillStyle = hGrad;
          ctx.fillRect(0, 0, W, headerH);

          const fGrad = ctx.createLinearGradient(0, footerTop, 0, H);
          fGrad.addColorStop(0,    "rgba(0,0,0,0)");
          fGrad.addColorStop(0.25, "rgba(0,0,0,0.80)");
          fGrad.addColorStop(1,    "rgba(0,0,0,0.97)");
          ctx.fillStyle = fGrad;
          ctx.fillRect(0, footerTop, W, H - footerTop);

          // ── SIDE ACCENT BARS (yellow, fading vertically) ──────────
          const sideBarW = Math.max(4, Math.round(W * 0.008));
          const sideBarL = ctx.createLinearGradient(0, 0, 0, H);
          sideBarL.addColorStop(0,    YELLOW);
          sideBarL.addColorStop(0.25, "rgba(242,169,0,0.55)");
          sideBarL.addColorStop(0.50, "rgba(242,169,0,0)");
          sideBarL.addColorStop(0.75, "rgba(242,169,0,0.55)");
          sideBarL.addColorStop(1,    YELLOW);
          ctx.fillStyle = sideBarL;
          ctx.fillRect(0,            0, sideBarW, H);
          ctx.fillRect(W - sideBarW, 0, sideBarW, H);

          // ── FULL-WIDTH HAIRLINE TOP + BOTTOM ──────────────────────
          const hair = Math.max(2, Math.round(H * 0.0025));
          ctx.fillStyle = YELLOW;
          ctx.fillRect(0, 0,        W, hair);
          ctx.fillRect(0, H - hair, W, hair);

          const { headline, subHeadline, extra, dateTime, location, cta } = extractText(form);

          // ── HEADER TEXT ───────────────────────────────────────────
          const textPadL = pad + sideBarW;
          const maxTextW = W - textPadL - pad - sideBarW;
          let   curY     = Math.round(H * 0.048) + hair;

          // Headline (centred horizontally, with one yellow word)
          let headlineEndY = curY;
          if (headline) {
            const words = headline.split(" ");
            const yIdx  = yellowWordIndex(words);

            // Pick a size that fits height-wise too
            const maxHeadlineH = Math.round(headerH * 0.72) - curY;
            let sz = Math.round(W * 0.118);
            let lines: number[][];
            do {
              ctx.font = `900 ${sz}px ${FONT_HEADING}`;
              lines = wrapByWords(ctx, words, maxTextW);
              if (lines.length * Math.round(sz * 1.0) <= maxHeadlineH) break;
              sz -= 4;
            } while (sz > 28);

            const lineH = Math.round(sz * 1.00);
            const spaceW = ctx.measureText(" ").width;

            ctx.font = `900 ${sz}px ${FONT_HEADING}`;
            ctx.textBaseline = "top";
            ctx.textAlign    = "center";

            for (const line of lines) {
              // measure line width with spaces
              let lineW = 0;
              for (let j = 0; j < line.length; j++) {
                lineW += ctx.measureText(words[line[j]]).width;
                if (j < line.length - 1) lineW += spaceW;
              }
              // Draw each word with its colour, sliding x cursor
              let cursorX = W / 2 - lineW / 2;
              for (let j = 0; j < line.length; j++) {
                const w = words[line[j]];
                const isYellow = line[j] === yIdx;
                const ww = ctx.measureText(w).width;
                // Use textAlign = left for per-word drawing
                ctx.textAlign = "left";
                drawTextStack(
                  ctx, w, cursorX, curY, sz,
                  isYellow ? YELLOW : WHITE,
                  isYellow ? "rgba(242,169,0,0.30)" : "rgba(242,169,0,0.10)"
                );
                cursorX += ww + spaceW;
              }
              ctx.textAlign = "center";
              curY += lineH;
            }
            headlineEndY = curY;
            ctx.textAlign = "left";
          }

          // Sub-headline: "— PUBLIC AUCTION —"
          if (subHeadline) {
            const sz = Math.round(W * 0.034);
            ctx.font = `900 ${sz}px ${FONT_HEADING}`;
            ctx.textBaseline = "top";
            ctx.letterSpacing = "0.18em";
            const wText = ctx.measureText(subHeadline).width;
            const dashLen = Math.round(W * 0.07);
            const dashGap = Math.round(sz * 0.6);
            const totalW  = dashLen + dashGap + wText + dashGap + dashLen;
            const startX  = (W - totalW) / 2;
            const yPos    = headlineEndY + Math.round(H * 0.012);
            const lineY   = yPos + Math.round(sz * 0.55);

            // Left dash
            const dashH = Math.max(2, Math.round(H * 0.0035));
            const lGrad = ctx.createLinearGradient(startX, 0, startX + dashLen, 0);
            lGrad.addColorStop(0, "rgba(242,169,0,0)");
            lGrad.addColorStop(1, YELLOW);
            ctx.fillStyle = lGrad;
            ctx.fillRect(startX, lineY, dashLen, dashH);

            // Right dash
            const rX = startX + dashLen + dashGap + wText + dashGap;
            const rGrad = ctx.createLinearGradient(rX, 0, rX + dashLen, 0);
            rGrad.addColorStop(0, YELLOW);
            rGrad.addColorStop(1, "rgba(242,169,0,0)");
            ctx.fillStyle = rGrad;
            ctx.fillRect(rX, lineY, dashLen, dashH);

            // Sub-headline text (off-white, letter-spaced)
            ctx.save();
            ctx.shadowColor = "rgba(0,0,0,0.85)"; ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
            ctx.fillStyle = OFFWHITE;
            ctx.fillText(subHeadline, startX + dashLen + dashGap, yPos);
            ctx.restore();
            ctx.letterSpacing = "0";
            clearShadow(ctx);

            headlineEndY = yPos + sz * 1.4;
          }

          // Extra text (optional)
          if (extra) {
            const sz = Math.round(W * 0.030);
            ctx.save();
            ctx.shadowColor = "rgba(0,0,0,0.85)"; ctx.shadowBlur = 7; ctx.shadowOffsetY = 2;
            ctx.font = `400 ${sz}px ${FONT_BODY}`;
            ctx.fillStyle = "rgba(255,255,255,0.85)"; ctx.textBaseline = "top";
            ctx.textAlign = "center";
            ctx.fillText(extra, W / 2, headlineEndY + Math.round(H * 0.01));
            ctx.restore();
            clearShadow(ctx);
            ctx.textAlign = "left";
          }

          // ── FOOTER ────────────────────────────────────────────────
          const ctaFontSz = Math.round(W * 0.058);
          const ctaBtnH   = Math.round(ctaFontSz * 2.0);
          const ctaBtnW   = Math.round(W * 0.70);
          const ctaBtnX   = (W - ctaBtnW) / 2;
          const ctaBtnY   = H - Math.round(H * 0.075) - ctaBtnH;
          const ctaR      = Math.round(ctaBtnH * 0.16);

          // Location + date stacked above CTA, centred
          const dateFontSz = Math.round(W * 0.048);
          const locFontSz  = Math.round(W * 0.030);
          let infoBottomY  = ctaBtnY - Math.round(H * 0.025);

          if (location) {
            ctx.save();
            ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 10; ctx.shadowOffsetY = 2;
            ctx.font = `400 ${locFontSz}px ${FONT_BODY}`;
            ctx.fillStyle = "rgba(255,255,255,0.85)";
            ctx.textBaseline = "bottom"; ctx.textAlign = "center";
            ctx.fillText(location, W / 2, infoBottomY);
            ctx.restore();
            clearShadow(ctx);
            infoBottomY -= Math.round(locFontSz * 1.7);
          }

          if (dateTime) {
            // Yellow glow + crisp date, centred
            ctx.save();
            ctx.shadowColor = "rgba(242,169,0,0.45)"; ctx.shadowBlur = Math.round(dateFontSz * 0.5);
            ctx.font = `900 ${dateFontSz}px ${FONT_HEADING}`;
            ctx.fillStyle = YELLOW;
            ctx.textBaseline = "bottom"; ctx.textAlign = "center";
            ctx.fillText(dateTime, W / 2, infoBottomY);
            ctx.restore();

            ctx.save();
            ctx.shadowColor = "rgba(0,0,0,0.80)"; ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
            ctx.font = `900 ${dateFontSz}px ${FONT_HEADING}`;
            ctx.fillStyle = YELLOW;
            ctx.textBaseline = "bottom"; ctx.textAlign = "center";
            ctx.fillText(dateTime, W / 2, infoBottomY);
            ctx.restore();
            clearShadow(ctx);
            infoBottomY -= Math.round(dateFontSz * 1.0);
          }

          // Thin yellow fading rule above date stack, centred
          const ruleW = Math.round(W * 0.30);
          const ruleH2 = Math.max(2, Math.round(H * 0.003));
          const ruleY  = infoBottomY - Math.round(H * 0.005);
          const rgrad = ctx.createLinearGradient(W / 2 - ruleW / 2, 0, W / 2 + ruleW / 2, 0);
          rgrad.addColorStop(0,   "rgba(242,169,0,0)");
          rgrad.addColorStop(0.5, YELLOW);
          rgrad.addColorStop(1,   "rgba(242,169,0,0)");
          ctx.fillStyle = rgrad;
          ctx.fillRect(W / 2 - ruleW / 2, ruleY, ruleW, ruleH2);

          // CTA button — centred, big, with gradient + glow + arrow
          if (cta) {
            // Outer glow
            ctx.save();
            ctx.shadowColor = "rgba(242,169,0,0.6)";
            ctx.shadowBlur = Math.round(ctaBtnH * 1.0);
            ctx.shadowOffsetY = Math.round(ctaBtnH * 0.18);
            ctx.fillStyle = YELLOW;
            roundRect(ctx, ctaBtnX, ctaBtnY, ctaBtnW, ctaBtnH, ctaR); ctx.fill();
            ctx.restore();
            clearShadow(ctx);

            // Gradient fill
            const btnGrad = ctx.createLinearGradient(ctaBtnX, ctaBtnY, ctaBtnX, ctaBtnY + ctaBtnH);
            btnGrad.addColorStop(0,    YELLOW_LIGHT);
            btnGrad.addColorStop(0.50, YELLOW);
            btnGrad.addColorStop(1,    YELLOW_DARK);
            ctx.fillStyle = btnGrad;
            roundRect(ctx, ctaBtnX, ctaBtnY, ctaBtnW, ctaBtnH, ctaR); ctx.fill();

            // Top shine
            const btnShine = ctx.createLinearGradient(ctaBtnX, ctaBtnY, ctaBtnX, ctaBtnY + ctaBtnH * 0.48);
            btnShine.addColorStop(0, "rgba(255,255,255,0.32)");
            btnShine.addColorStop(1, "rgba(255,255,255,0)");
            ctx.fillStyle = btnShine;
            roundRect(ctx, ctaBtnX + 2, ctaBtnY + 2, ctaBtnW - 4, ctaBtnH * 0.48, ctaR); ctx.fill();

            // Inner darker stroke for definition
            ctx.save();
            ctx.lineWidth = Math.max(2, Math.round(ctaBtnH * 0.025));
            ctx.strokeStyle = "rgba(0,0,0,0.25)";
            roundRect(ctx, ctaBtnX + 1, ctaBtnY + 1, ctaBtnW - 2, ctaBtnH - 2, ctaR);
            ctx.stroke();
            ctx.restore();

            // CTA text
            ctx.save();
            ctx.shadowColor = "rgba(0,0,0,0.25)"; ctx.shadowBlur = 4; ctx.shadowOffsetY = 1;
            ctx.font = `900 ${ctaFontSz}px ${FONT_HEADING}`;
            ctx.fillStyle = BLACK;
            ctx.textBaseline = "middle"; ctx.textAlign = "center";
            ctx.fillText(cta, W / 2, ctaBtnY + ctaBtnH / 2);
            ctx.textAlign = "left"; ctx.textBaseline = "top";
            ctx.restore();
            clearShadow(ctx);
          }

          // ── LOGO (smart corner placement) ─────────────────────────
          const logoW = Math.round(W * 0.16);
          const logoH = Math.round(logoW * (logoImg.naturalHeight / logoImg.naturalWidth));
          const corner = pickLogoCorner(ctx, W, H, logoW, logoH, Math.round(W * 0.035));

          ctx.save();
          ctx.shadowColor = "rgba(0,0,0,0.85)";
          ctx.shadowBlur = Math.round(logoW * 0.15);
          ctx.shadowOffsetY = 4;
          ctx.globalAlpha = 0.96;
          ctx.drawImage(logoImg, corner.x, corner.y, logoW, logoH);
          ctx.restore();
          clearShadow(ctx);
          ctx.globalAlpha = 1;

          resolve(canvas.toDataURL("image/png"));
        };
        logoImg.onerror = () => reject(new Error("Failed to load logo"));
        logoImg.src = logoSrc;
      };
      baseImg.onerror = () => reject(new Error("Failed to load base image"));
      baseImg.src = imageDataUrl;
    }).catch(reject);
  });
}
