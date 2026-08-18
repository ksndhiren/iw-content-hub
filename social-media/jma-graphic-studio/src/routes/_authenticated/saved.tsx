import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Download, Sparkles, Trash2, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";

export const Route = createFileRoute("/_authenticated/saved")({
  component: SavedPage,
});

interface DesignRow {
  id: string;
  title: string;
  image_url: string;
  created_at: string;
}

function SavedPage() {
  const { user } = useAuth();
  const [items, setItems] = useState<DesignRow[] | null>(null);

  const load = async () => {
    if (!user) return;
    const { data, error } = await supabase
      .from("designs")
      .select("id,title,image_url,created_at")
      .order("created_at", { ascending: false });
    if (error) return toast.error(error.message);
    setItems(data ?? []);
  };

  useEffect(() => { load(); }, [user?.id]);

  const remove = async (id: string) => {
    const { error } = await supabase.from("designs").delete().eq("id", id);
    if (error) return toast.error(error.message);
    setItems((it) => (it ?? []).filter((d) => d.id !== id));
    toast.success("Deleted");
  };

  const download = async (d: DesignRow) => {
    const a = document.createElement("a");
    a.href = d.image_url;
    a.download = `${d.title.replace(/[^a-z0-9]+/gi, "-").toLowerCase() || "design"}.png`;
    a.target = "_blank";
    a.click();
  };

  return (
    <div className="space-y-8">
      <div className="flex items-end justify-between flex-wrap gap-3">
        <div>
          <p className="text-sm text-muted-foreground">Library</p>
          <h1 className="text-3xl font-bold tracking-tight">Saved Designs</h1>
        </div>
        <Link to="/create"><Button className="gap-2"><Sparkles className="h-4 w-4" /> New design</Button></Link>
      </div>

      {items === null ? (
        <div className="grid place-items-center py-20"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>
      ) : items.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((d) => (
            <div key={d.id} className="rounded-2xl border bg-card overflow-hidden group">
              <div className="aspect-square bg-muted overflow-hidden">
                <img src={d.image_url} alt={d.title} className="w-full h-full object-cover transition-transform group-hover:scale-[1.02]" />
              </div>
              <div className="p-4">
                <h3 className="font-semibold truncate">{d.title}</h3>
                <p className="text-xs text-muted-foreground">{new Date(d.created_at).toLocaleDateString()}</p>
                <div className="flex items-center gap-2 mt-3">
                  <Button size="sm" variant="outline" className="gap-1" onClick={() => download(d)}>
                    <Download className="h-3.5 w-3.5" /> Download
                  </Button>
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button size="sm" variant="ghost" className="gap-1 text-destructive hover:text-destructive">
                        <Trash2 className="h-3.5 w-3.5" /> Delete
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Delete this design?</AlertDialogTitle>
                        <AlertDialogDescription>This can't be undone.</AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={() => remove(d.id)} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                          Delete
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function EmptyState() {
  return (
    <div className="rounded-2xl border-2 border-dashed bg-card p-16 text-center">
      <div className="mx-auto h-16 w-16 rounded-2xl bg-brand/20 grid place-items-center">
        <Sparkles className="h-8 w-8 text-foreground" />
      </div>
      <h3 className="mt-4 text-xl font-semibold">No designs yet</h3>
      <p className="mt-1 text-muted-foreground">Create your first AI-generated design.</p>
      <Link to="/create" className="inline-block mt-6">
        <Button className="gap-2"><Sparkles className="h-4 w-4" /> Start creating</Button>
      </Link>
    </div>
  );
}
