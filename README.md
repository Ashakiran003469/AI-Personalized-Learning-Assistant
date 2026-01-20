# SDG4 AI Tutor Prototype

This repository contains a minimal prototype of an AI-powered personalized learning assistant aligned with SDG-4 (Quality Education). It includes:

- Backend: FastAPI + LangGraph-style agent pipeline (prototype)
- Frontend: React (Vite) single-page chat UI
- Storage: Supabase integration with local JSON fallback

Requirements
- Python 3.10+
- Node 18+

Backend setup
1. cd backend
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. Set environment variables (optional): `SUPABASE_URL`, `SUPABASE_KEY`, `OPENAI_API_KEY`
6. Run: `uvicorn app.main:app --reload --port 8000`

Frontend setup
1. cd frontend
2. npm install
3. npm run dev

Notes
- The LangGraph agent is implemented as a sequential pipeline in `backend/app/agent.py` and follows the required node flow.
- Supabase is optional — if not configured the app writes to `backend/data/` as a fallback so you can prototype offline.
- This is a prototype focusing on modularity, explainability, and accessibility for low-resource environments.

Ethical & Privacy Notes
- The system avoids collecting sensitive personal data by design.
- Data stored in Supabase or local fallback is limited to learning progress metrics and non-identifying session info.
- See `ETHICS.md` for a short policy.
