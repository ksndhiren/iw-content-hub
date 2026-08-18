// Shared types + state for the multi-step create wizard.

export type AssetNeed = "Print Need" | "Web Need";
export type RequestType = "Auction announcement" | "Featured equipment" | "Bid reminder" | "Weekly promotion";
export type Audience = "Buyers" | "Bidders" | "Consignors" | "Dealers" | "Contractors" | "General audience";
export type Objective =
  | "Drive registrations"
  | "Increase bidding activity"
  | "Promote an upcoming auction"
  | "Highlight featured equipment"
  | "Attract consignors"
  | "Build brand awareness";

export const PRINT_TYPES = ["Flyer", "Handout", "Banner", "Catalog", "Print Ad"] as const;
export const WEB_TYPES = ["Social Media", "Email", "Website Ad"] as const;
export const AUDIENCE_OPTIONS: Audience[] = ["Buyers", "Bidders", "Consignors", "Dealers", "Contractors", "General audience"];
export const EQUIPMENT_CATEGORIES = [
  "All Terrain Cranes",
  "Crawler Cranes",
  "Hydraulic Truck Cranes",
  "Truck Cranes",
  "Rough Terrain Cranes",
  "Carry Deck Cranes",
  "Crane Trucks",
  "Ancillary Crane Equipment",
  "Heavy Transportation Equipment",
  "Heavy Haul Trucks",
  "Heavy Commercial Trucks",
  "Utility Equipment",
  "Grapple / Digger Derrick Trucks",
  "Trailers",
  "Bumper Pull Trailers",
  "Gooseneck Trailers",
  "Lowboy Trailers",
  "Step Deck Trailers",
  "Flatbed Trailers",
  "Van & Reefer Trailers",
  "Excavators",
  "Backhoes",
  "Dozers",
  "Crawler Tractors",
  "Wheel Loaders",
  "Multi-Terrain Loaders",
  "Skip Loaders",
  "Motor Scrapers",
  "Motor Graders",
  "Skid Steers",
  "Articulated Dump Trucks",
  "Rigid Frame Haul Trucks",
  "Paving / Compaction Equipment",
  "Forestry Equipment",
  "Aerial Lifts",
  "Forklifts",
  "Concrete Equipment",
  "Agricultural Equipment",
  "Farm Equipment",
  "Farm Implements",
  "Mining Equipment",
  "Tractors",
  "Generators",
  "Welders",
  "Air Compressors",
  "Pumps",
  "Industrial Equipment",
  "Engines",
  "Attachments",
  "Parts",
  "Tires",
  "Passenger Vehicles",
  "Pickups",
  "Motorcycles",
  "RVs & Campers",
  "Boats",
  "Attachments & Support Equipment",
  "Service Trucks & Pickup Trucks",
  "Other Heavy Equipment",
] as const;
export const CALL_TO_ACTION_OPTIONS = [
  "Register to Bid",
  "Bid Now",
  "View Inventory",
  "Browse Lots",
  "Consign Today",
  "Learn More",
  "Contact Our Team",
  "Join the Auction",
] as const;
export const AUCTION_TIME_OPTIONS = [
  "6:00 AM",
  "7:00 AM",
  "8:00 AM",
  "9:00 AM",
  "10:00 AM",
  "11:00 AM",
  "12:00 PM",
  "1:00 PM",
  "2:00 PM",
  "3:00 PM",
  "4:00 PM",
  "5:00 PM",
  "6:00 PM",
] as const;
export const AUCTION_LOCATION_OPTIONS = [
  "Brooklyn (Hattiesburg), Mississippi",
  "Pelzer, South Carolina",
  "Kissimmee, Florida",
  "Stanton (Midland), Texas",
  "Houston (Splendora), Texas",
  "Glencoe, Minnesota",
  "Loudon, New Hampshire",
  "Clayton, Indiana",
  "Various Locations",
] as const;

export interface CreateFormState {
  // Step 1
  requestor: string;
  requestDate: string;
  assetNeed: AssetNeed | "";
  assetType: string;
  // Step 2
  description: string;
  objective: Objective | "";
  requestType: RequestType | "";
  audience: Audience[];
  // type-specific
  auctionName?: string;
  auctionDate?: string;
  auctionTime?: string;
  auctionLocation?: string;
  equipmentCategory?: string;
  equipmentName?: string;
  featureHighlight?: string;
  reminderFocus?: string;
  promotionHeadline?: string;
  promotionFocus?: string;
  callToAction?: string;
  // Step 3
  sourceImageDataUrl?: string;
  sourceImageName?: string;
  noSourceImage: boolean;
}

export const emptyForm: CreateFormState = {
  requestor: "",
  requestDate: new Date().toISOString().slice(0, 10),
  assetNeed: "",
  assetType: "",
  description: "",
  objective: "",
  requestType: "",
  audience: [],
  noSourceImage: false,
};

export function aspectForAssetType(type: string): "1024x1024" | "1536x1024" | "1024x1536" {
  if (["Banner", "Website Ad"].includes(type)) return "1536x1024";
  if (["Flyer", "Handout", "Print Ad", "Catalog", "Social Media"].includes(type)) return "1024x1536";
  return "1024x1024";
}

export function buildPrompt(f: CreateFormState): string {
  const parts: string[] = [];

  if (f.sourceImageDataUrl) {
    parts.push(`SOURCE IMAGE RULE: The uploaded equipment photograph is the primary hero visual. Preserve the exact machine, paint color, and viewing angle. Design the layout around it.`);
  }

  parts.push(`Create a high-quality hero image for a heavy-equipment auction ${f.assetType.toLowerCase()}. This is the hero image only — not the full poster layout. Focus on a strong equipment composition with dramatic lighting and clean negative space for text overlays that will be added later.`);
  parts.push(`Brand palette: black (#0d0d0d), white, and yellow (#f2a900) only.`);

  const sceneType: Record<string, string> = {
    "Auction announcement": "public auction event announcement",
    "Featured equipment": "equipment feature showcase",
    "Bid reminder": "live bidding event",
    "Weekly promotion": "weekly promotional campaign",
  };
  parts.push(`Scene context: ${sceneType[f.requestType] ?? "auction event"}. Concept: ${f.description}`);

  if (f.equipmentCategory && !f.sourceImageDataUrl) parts.push(`Equipment type: ${f.equipmentCategory}.`);
  if (f.equipmentName && !f.sourceImageDataUrl) parts.push(`Feature this machine: ${f.equipmentName}.`);

  parts.push(`Visual direction: premium auction-marketing aesthetic — gritty editorial energy, charcoal/black textured background, yellow accent lighting, dramatic cinematic lighting on the equipment.`);
  parts.push(`Composition: solid dark zone covering the top 28% of the image, equipment hero in the center 44% with dramatic lighting, solid dark zone covering the bottom 28%. All equipment fully inside the canvas with no cropping.`);

  if (f.sourceImageDataUrl) {
    parts.push(`Use the uploaded photo as the equipment hero. Preserve machine type, color, and angle exactly.`);
  } else if (f.noSourceImage) {
    parts.push(`Generate a photorealistic equipment hero matching the scene context.`);
  }

  parts.push(`Do not generate any text, letters, numbers, logos, watermarks, dates, call-to-action buttons, or poster copy inside the image. The final design text and logo will be added separately in post-production.`);

  return parts.join(" ");
}

export function summaryTitle(f: CreateFormState): string {
  if (f.auctionName) return f.auctionName;
  if (f.equipmentName) return f.equipmentName;
  if (f.promotionHeadline) return f.promotionHeadline;
  return f.assetType || "Untitled design";
}
