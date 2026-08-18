/**
 * Composites the JMA logo onto a generated image.
 * Scores the 4 corners by darkness + uniformity and places the logo in the best fit.
 */
export function compositeLogoOnImage(imageDataUrl: string, logoSrc: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const baseImg = new Image();
    baseImg.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = baseImg.width;
      canvas.height = baseImg.height;
      const ctx = canvas.getContext("2d");
      if (!ctx) return reject(new Error("Canvas 2D not available"));
      ctx.drawImage(baseImg, 0, 0);

      const logoImg = new Image();
      logoImg.onload = () => {
        const W = canvas.width;
        const H = canvas.height;

        // Logo: 18% of canvas width, aspect-correct
        const logoW = Math.round(W * 0.18);
        const logoH = Math.round(logoW * (logoImg.naturalHeight / logoImg.naturalWidth));
        const pad = Math.round(W * 0.04);

        const candidates = [
          { x: pad,              y: pad },               // top-left
          { x: W - logoW - pad,  y: pad },               // top-right
          { x: pad,              y: H - logoH - pad },   // bottom-left
          { x: W - logoW - pad,  y: H - logoH - pad },  // bottom-right
        ];

        const { data: pixels } = ctx.getImageData(0, 0, W, H);

        function luminance(x: number, y: number): number {
          const i = (Math.round(y) * W + Math.round(x)) * 4;
          return 0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2];
        }

        function scoreRegion(rx: number, ry: number, rw: number, rh: number): number {
          const step = Math.max(2, Math.floor(Math.min(rw, rh) / 10));
          const samples: number[] = [];
          for (let y = ry; y < ry + rh; y += step) {
            for (let x = rx; x < rx + rw; x += step) {
              if (x < W && y < H) samples.push(luminance(x, y));
            }
          }
          if (!samples.length) return Infinity;
          const avg = samples.reduce((a, b) => a + b, 0) / samples.length;
          const variance = samples.reduce((a, b) => a + (b - avg) ** 2, 0) / samples.length;
          // Lower score = darker (good for white logo) + more uniform (less cluttered)
          return avg * 0.7 + Math.sqrt(variance) * 0.3;
        }

        let best = candidates[0];
        let bestScore = Infinity;
        for (const c of candidates) {
          const s = scoreRegion(c.x, c.y, logoW, logoH);
          if (s < bestScore) { bestScore = s; best = c; }
        }

        ctx.globalAlpha = 0.92;
        ctx.drawImage(logoImg, best.x, best.y, logoW, logoH);
        ctx.globalAlpha = 1;

        resolve(canvas.toDataURL("image/png"));
      };
      logoImg.onerror = () => reject(new Error("Failed to load logo"));
      logoImg.src = logoSrc;
    };
    baseImg.onerror = () => reject(new Error("Failed to load base image"));
    baseImg.src = imageDataUrl;
  });
}
