import { createFileRoute, Link, Navigate, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Checkbox } from "@/components/ui/checkbox";
import logoWhite from "@/assets/jma-logo-white.png";
import logoDark from "@/assets/jma-logo.png";

export const Route = createFileRoute("/auth")({
  component: AuthPage,
});

function AuthPage() {
  const { session, loading } = useAuth();
  const [mode, setMode] = useState<"login" | "signup" | "forgot">("login");
  const [sentEmail, setSentEmail] = useState<string | null>(null);

  if (loading) return <div className="min-h-screen grid place-items-center text-sm text-muted-foreground">Loading…</div>;
  if (session) return <Navigate to="/dashboard" />;

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background">
      <div className="hidden lg:flex flex-col justify-between p-12 bg-primary text-primary-foreground">
        <img src={logoWhite} alt="JMA" className="h-14 w-auto self-start" />
        <div>
          <h1 className="text-4xl font-bold leading-tight">AI-powered graphics for every auction.</h1>
          <p className="mt-4 text-primary-foreground/70 max-w-md">
            Generate on-brand flyers, social posts and email creative in seconds - built for the JMA team.
          </p>
        </div>
        <div className="text-xs text-primary-foreground/50">© Jeff Martin Auctioneers</div>
      </div>

      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md">
          <img src={logoDark} alt="JMA" className="lg:hidden h-10 mb-6" />
          {sentEmail ? (
            <CheckInbox email={sentEmail} onBack={() => { setSentEmail(null); setMode("login"); }} />
          ) : (
            <Tabs value={mode} onValueChange={(v) => setMode(v as typeof mode)}>
              <TabsList className="grid grid-cols-3 w-full">
                <TabsTrigger value="login">Log in</TabsTrigger>
                <TabsTrigger value="signup">Sign up</TabsTrigger>
                <TabsTrigger value="forgot">Reset</TabsTrigger>
              </TabsList>
              <TabsContent value="login"><LoginForm onForgot={() => setMode("forgot")} onSignup={() => setMode("signup")} /></TabsContent>
              <TabsContent value="signup"><SignupForm onSent={(e) => setSentEmail(e)} /></TabsContent>
              <TabsContent value="forgot"><ForgotForm onSent={(e) => setSentEmail(e)} /></TabsContent>
            </Tabs>
          )}
        </div>
      </div>
    </div>
  );
}

function CheckInbox({ email, onBack }: { email: string; onBack: () => void }) {
  return (
    <div className="text-center space-y-4">
      <div className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-brand/20 text-2xl">✉️</div>
      <h2 className="text-2xl font-bold">Check your inbox</h2>
      <p className="text-muted-foreground">We sent a link to <span className="font-medium text-foreground">{email}</span>.</p>
      <Button variant="outline" onClick={onBack} className="w-full">Back to log in</Button>
    </div>
  );
}

function LoginForm({ onForgot, onSignup }: { onForgot: () => void; onSignup: () => void }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);
  const [busy, setBusy] = useState(false);

  return (
    <form
      className="space-y-4 mt-6"
      onSubmit={async (e) => {
        e.preventDefault();
        setBusy(true);
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        setBusy(false);
        if (error) return toast.error(error.message);
        navigate({ to: "/dashboard" });
      }}
    >
      <div>
        <h2 className="text-2xl font-bold">Welcome back</h2>
        <p className="text-sm text-muted-foreground">Sign in to keep creating.</p>
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input id="password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div className="flex items-center justify-between text-sm">
        <label className="flex items-center gap-2">
          <Checkbox checked={remember} onCheckedChange={(v) => setRemember(!!v)} /> Remember me
        </label>
        <button type="button" onClick={onForgot} className="text-foreground hover:underline">Forgot password?</button>
      </div>
      <Button type="submit" className="w-full" disabled={busy}>{busy ? "Signing in…" : "Sign in"}</Button>
      <p className="text-sm text-center text-muted-foreground">
        New here? <button type="button" onClick={onSignup} className="text-foreground font-medium hover:underline">Create an account</button>
      </p>
    </form>
  );
}

function SignupForm({ onSent }: { onSent: (email: string) => void }) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [busy, setBusy] = useState(false);

  return (
    <form
      className="space-y-4 mt-6"
      onSubmit={async (e) => {
        e.preventDefault();
        if (password !== confirm) return toast.error("Passwords do not match");
        if (password.length < 6) return toast.error("Password must be at least 6 characters");
        setBusy(true);
        const { error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: { full_name: fullName },
            emailRedirectTo: `${window.location.origin}/dashboard`,
          },
        });
        setBusy(false);
        if (error) return toast.error(error.message);
        onSent(email);
      }}
    >
      <div>
        <h2 className="text-2xl font-bold">Create your account</h2>
        <p className="text-sm text-muted-foreground">Start designing in minutes.</p>
      </div>
      <div className="space-y-2">
        <Label>Full name</Label>
        <Input required value={fullName} onChange={(e) => setFullName(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label>Email</Label>
        <Input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label>Password</Label>
        <Input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label>Confirm password</Label>
        <Input type="password" required value={confirm} onChange={(e) => setConfirm(e.target.value)} />
      </div>
      <Button type="submit" className="w-full" disabled={busy}>{busy ? "Creating account…" : "Create account"}</Button>
    </form>
  );
}

function ForgotForm({ onSent }: { onSent: (email: string) => void }) {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <form
      className="space-y-4 mt-6"
      onSubmit={async (e) => {
        e.preventDefault();
        setBusy(true);
        const { error } = await supabase.auth.resetPasswordForEmail(email, {
          redirectTo: `${window.location.origin}/reset-password`,
        });
        setBusy(false);
        if (error) return toast.error(error.message);
        onSent(email);
      }}
    >
      <div>
        <h2 className="text-2xl font-bold">Reset password</h2>
        <p className="text-sm text-muted-foreground">We'll email you a reset link.</p>
      </div>
      <div className="space-y-2">
        <Label>Email</Label>
        <Input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <Button type="submit" className="w-full" disabled={busy}>{busy ? "Sending…" : "Send reset link"}</Button>
    </form>
  );
}
