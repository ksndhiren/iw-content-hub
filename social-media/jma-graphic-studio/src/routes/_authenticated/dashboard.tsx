import { createFileRoute, Link } from "@tanstack/react-router";
import { Sparkles, Bookmark, ArrowRight } from "lucide-react";
import { useAuth } from "@/lib/auth";

export const Route = createFileRoute("/_authenticated/dashboard")({
  component: Dashboard,
});

function Dashboard() {
  const { user } = useAuth();
  const name = (user?.user_metadata?.full_name as string | undefined)?.split(" ")[0] || "there";

  return (
    <div className="space-y-10">
      <div>
        <p className="text-sm text-muted-foreground">Welcome back</p>
        <h1 className="text-4xl font-bold tracking-tight mt-1">Hi, {name} 👋</h1>
        <p className="mt-2 text-muted-foreground">What are we creating today?</p>
      </div>

      <div className="grid sm:grid-cols-2 gap-6">
        <ActionCard to="/create" title="Create" description="Start a new AI-generated design from scratch." icon={<Sparkles className="h-6 w-6" />} accent />
        <ActionCard to="/saved" title="Saved Designs" description="Browse and download your previous designs." icon={<Bookmark className="h-6 w-6" />} />
      </div>
    </div>
  );
}

function ActionCard({ to, title, description, icon, accent }: {
  to: string; title: string; description: string; icon: React.ReactNode; accent?: boolean;
}) {
  return (
    <Link
      to={to}
      className="group relative overflow-hidden rounded-2xl border bg-card p-8 transition-all hover:-translate-y-0.5 hover:shadow-lg"
    >
      {accent && <div className="absolute -top-12 -right-12 h-40 w-40 rounded-full bg-brand/30 blur-2xl" />}
      <div className="relative flex flex-col gap-6">
        <div className={`inline-flex h-12 w-12 items-center justify-center rounded-xl ${accent ? "bg-brand text-brand-foreground" : "bg-primary text-primary-foreground"}`}>
          {icon}
        </div>
        <div>
          <h2 className="text-2xl font-semibold">{title}</h2>
          <p className="mt-1 text-muted-foreground">{description}</p>
        </div>
        <div className="flex items-center text-sm font-medium text-foreground">
          Open <ArrowRight className="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" />
        </div>
      </div>
    </Link>
  );
}
