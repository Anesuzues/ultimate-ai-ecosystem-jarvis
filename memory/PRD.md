# JARVIS — Product Requirements Document

## Original Problem
User shared the GitHub repo `Anesuzues/ultimate-ai-ecosystem-jarvis` for review. The repo claimed to be the "most advanced AI development system ever created" with 35+ specialist agents and 5 integrated AI systems, but in reality was ~1,000 disorganized files: a keyword-matching router with hard-coded f-string "responses", empty bridge files, vendored third-party projects, and broken `requirements.txt`. User asked: "fix everything to start working" and chose the simplest path.

## Solution Architecture
Built a **clean, simplified JARVIS app from scratch** at `/app/`:

- **Backend** (`/app/backend/server.py`): FastAPI on port 8001
  - Real LLM-powered intelligent router (Emergent LLM key + `gpt-4o-mini`) replacing the keyword matcher
  - Single LLM call returns JSON `{category, title, response}` — categories: research / coding / build / content / general
  - MongoDB persistence (sessions + messages)
  - Routes: `/api/health`, `/api/status`, `/api/chat`, `/api/sessions`, `/api/sessions/{id}/messages`, `DELETE /api/sessions/{id}`

- **Frontend** (`/app/frontend/src/App.js`): React 18 + Tailwind + craco
  - JARVIS HUD aesthetic: obsidian background, electric cyan + warning amber accents
  - Rajdhani heading font, IBM Plex Mono body font
  - 5-card status dashboard (Router / Memory / Knowledge / Voice / Network)
  - Sessions sidebar with auto-titled conversations
  - Chat panel with category badges, prompt suggestions, optimistic UI, scanline overlay

- **Legacy code** parked at `/app/legacy/` (kept for reference, not used).

## User Personas
- **Solo developer / hobbyist** experimenting with AI assistant patterns and wanting a working JARVIS-style chat with real intelligent routing.

## Core Static Requirements
1. Accept natural-language commands and produce useful, in-character JARVIS replies.
2. Classify each request via real LLM into 5 task categories.
3. Persist conversation history per session.
4. Display real-time-feeling system status dashboard.
5. Theme must be premium, futuristic, distinctive (no purple AI-slop).

## Implemented (Iteration 1 — 2026-04-25)
- ✅ FastAPI backend with 6 endpoints, all returning Pydantic-typed responses, no `_id` leakage
- ✅ Emergent LLM integration via `emergentintegrations` (`gpt-4o-mini`)
- ✅ MongoDB persistence (sessions + messages collections)
- ✅ React frontend with JARVIS HUD theme + scanline overlay + corner brackets
- ✅ Conversation list with auto-generated titles, delete, new-chat
- ✅ Prompt suggestion chips on empty state
- ✅ Optimistic UI for sending + animated thinking indicator
- ✅ `data-testid` on every interactive element
- ✅ Tested end-to-end by `testing_agent_v3`: 13/13 backend tests, full frontend E2E flow passing

## Backlog (Prioritized)
**P1**
- Streaming LLM responses (SSE/WebSocket) instead of waiting for full reply
- Real "tool execution" per category (e.g. `coding` → run code in sandbox, `research` → web-search MCP, `content` → render markdown nicely)
- Proper markdown rendering for JARVIS output (currently plain text)

**P2**
- Voice input + TTS (the "Voice Synthesis" card is in standby — wire it up with Whisper + OpenAI TTS)
- Multi-turn context: pass last N messages back to LLM (currently each `/api/chat` is fresh-context per the LlmChat session_id)
- Authentication (Emergent Google Auth) so sessions are per-user
- Export conversation as Markdown / JSON

**P3**
- Theme switcher (current dark HUD is the only theme)
- Mobile polish (currently desktop-first)
- Rate limiting on `/api/chat`

## Tech Stack
| Layer | Tech |
|---|---|
| Backend | FastAPI + uvicorn + motor (async Mongo) + emergentintegrations |
| LLM | OpenAI `gpt-4o-mini` via Emergent Universal Key |
| DB | MongoDB |
| Frontend | React 18 + craco + Tailwind 3 + axios + lucide-react |
| Fonts | Rajdhani (headings), IBM Plex Mono (body) |
| Theme | Obsidian #05050B + Electric Cyan #00E5FF + Warning Amber #FF9100 |

## Service Layout
- Backend on `:8001`, all routes prefixed `/api`
- Frontend on `:3000`, calls `${REACT_APP_BACKEND_URL}/api/...`
- Both managed by supervisor

## Next Tasks
1. Add streaming responses (P1)
2. Wire `coding` category to real sandbox execution
3. Add user auth + per-user sessions
