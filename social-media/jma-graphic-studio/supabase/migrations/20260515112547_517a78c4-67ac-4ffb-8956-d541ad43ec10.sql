
-- designs table
CREATE TABLE public.designs (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL DEFAULT 'Untitled design',
  image_url TEXT NOT NULL,
  generation_prompt TEXT NOT NULL,
  form_answers JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.designs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own designs"
  ON public.designs FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own designs"
  ON public.designs FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own designs"
  ON public.designs FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own designs"
  ON public.designs FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE INDEX designs_user_created_idx ON public.designs(user_id, created_at DESC);

-- storage bucket (private)
INSERT INTO storage.buckets (id, name, public)
VALUES ('designs', 'designs', false);

-- storage RLS: each user can only touch files under their own user-id folder
CREATE POLICY "Users can read their own design files"
  ON storage.objects FOR SELECT
  TO authenticated
  USING (bucket_id = 'designs' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can upload their own design files"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'designs' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can delete their own design files"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (bucket_id = 'designs' AND auth.uid()::text = (storage.foldername(name))[1]);
