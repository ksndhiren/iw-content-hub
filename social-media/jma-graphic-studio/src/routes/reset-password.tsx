import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/reset-password")({
  component: ResetPassword,
});

function ResetPassword() {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <div className="min-h-screen grid place-items-center px-6 bg-background">
      <form
        className="w-full max-w-sm space-y-4 bg-card border rounded-2xl p-8"
        onSubmit={async (e) => {
          e.preventDefault();
          if (password.length < 6) return toast.error("Password must be at least 6 characters");
          setBusy(true);
          const { error } = await supabase.auth.updateUser({ password });
          setBusy(false);
          if (error) return toast.error(error.message);
          toast.success("Password updated");
          navigate({ to: "/dashboard" });
        }}
      >
        <h1 className="text-2xl font-bold">Set a new password</h1>
        <div className="space-y-2">
          <Label>New password</Label>
          <Input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <Button type="submit" className="w-full" disabled={busy}>{busy ? "Saving…" : "Update password"}</Button>
      </form>
    </div>
  );
}
