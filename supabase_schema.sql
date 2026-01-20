-- Supabase schema for SDG-4 AI Tutor
-- Tables: learners, sessions, progress, events
-- Notes: avoid storing PII; use `external_user_id` for optional mapping to external identifiers

-- Enable pgcrypto for gen_random_uuid()
create extension if not exists pgcrypto;

-- Learners table: stores non-sensitive learner metadata and skill/profile JSON
create table if not exists learners (
  id uuid primary key default gen_random_uuid(),
  external_user_id text unique, -- optional external id (not PII)
  language_preference text default 'en',
  skill_levels jsonb default '{}'::jsonb, -- e.g. {"Algebra": 0.6}
  metadata jsonb default '{}'::jsonb, -- general non-sensitive metadata
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
create index if not exists idx_learners_external_user_id on learners(external_user_id);

-- Sessions table: per-interaction session tracking
create table if not exists sessions (
  id uuid primary key default gen_random_uuid(),
  learner_id uuid references learners(id) on delete set null,
  started_at timestamptz default now(),
  last_activity timestamptz,
  session_metadata jsonb default '{}'::jsonb
);
create index if not exists idx_sessions_learner_id on sessions(learner_id);

-- Progress table: stores progress metrics, mastery estimates and counts
create table if not exists progress (
  id uuid primary key default gen_random_uuid(),
  learner_id uuid references learners(id) on delete set null,
  session_id uuid references sessions(id) on delete set null,
  topic text,
  mastery_level numeric check (mastery_level >= 0 and mastery_level <= 1),
  interaction_count integer default 0,
  details jsonb default '{}'::jsonb, -- e.g. {"last_answers": [...], "confidence_scores": [...]}
  created_at timestamptz default now()
);
create index if not exists idx_progress_learner_id on progress(learner_id);
create index if not exists idx_progress_topic on progress(topic);

-- Events table: event-driven payloads (webhooks, system events)
create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  event_type text not null,
  learner_id uuid references learners(id) on delete set null,
  session_id uuid references sessions(id) on delete set null,
  payload jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  processed boolean default false
);
create index if not exists idx_events_event_type on events(event_type);
create index if not exists idx_events_learner_id on events(learner_id);

-- Optional helper: keep updated_at current on learners
create or replace function update_updated_at_column()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_learners_updated_at on learners;
create trigger trg_learners_updated_at
  before update on learners
  for each row
  execute procedure update_updated_at_column();

-- Security note: Do not store names, birthdates, or other PII here.
