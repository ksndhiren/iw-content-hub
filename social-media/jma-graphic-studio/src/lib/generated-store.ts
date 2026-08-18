import { create } from "zustand";
import type { CreateFormState } from "./create-form";

export interface GeneratedResult {
  imageDataUrl: string;
  prompt: string;
  size: "1024x1024" | "1536x1024" | "1024x1536";
  title: string;
  form: CreateFormState;
}

interface Store {
  result: GeneratedResult | null;
  set: (r: GeneratedResult) => void;
  clear: () => void;
}

export const useGeneratedStore = create<Store>((set) => ({
  result: null,
  set: (r) => set({ result: r }),
  clear: () => set({ result: null }),
}));
