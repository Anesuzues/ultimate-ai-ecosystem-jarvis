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

## Implemented (Iteration 2 — 2026-04-25, "P1 + P2")
**P1**
- ✅ **Streaming LLM replies** via SSE — new `POST /api/chat/stream` endpoint emits `meta` → `chunk` (3-token windows, 25ms throttle) → `done` events. Frontend consumes via `fetch` + `ReadableStream` (async generator).
- ✅ **Tool execution per category** (prompt-level): system prompt now instructs the model to format per category — research as structured analysis with sources, coding as fenced code blocks, build as goal/stack/architecture/steps/risks, content as deliverable-ready, general as conversational.
- ✅ **Markdown rendering** with `react-markdown` + `remark-gfm` + `rehype-highlight` + `highlight.js` (github-dark) — verified Python syntax highlighting in JARVIS bubbles.

**P2**
- ✅ **Voice input** (Whisper STT) — `POST /api/voice/transcribe` accepts multipart audio, frontend uses `MediaRecorder` (audio/webm). Mic button with recording-state indicator.
- ✅ **Voice output** (OpenAI TTS, voice "nova", model tts-1) — `POST /api/voice/tts` returns `audio/mpeg`. Frontend toggle (`voice-out-toggle`) auto-plays JARVIS replies via `<audio>` blob URLs when enabled.
- ✅ **Multi-turn context** — backend pre-loads last 10 messages from MongoDB and prepends them to the user's new message before LLM call. Verified via test that a second message references the first.
- ✅ **Emergent Google Auth** — `POST /api/auth/session` exchanges Emergent session_id for our cookie + DB-backed `user_sessions`. `GET /api/auth/me`, `POST /api/auth/logout`. Sessions and messages now scoped by `user_id`. Frontend has `/login` screen, `AuthCallback` for `#session_id=` fragment, user chip + logout in header. Cookies are `httpOnly`, `secure`, `samesite="none"`.
- ✅ **Export conversation** — `GET /api/sessions/{id}/export?format=md|json` with proper `Content-Disposition`. Frontend download icon per session.

**Testing**: 22/22 backend pytest passed + 7/8 frontend Playwright passed. The 1 frontend "failure" is mic recording in headless Chromium (no audio device) — app code verified correct, untestable in CI only.

## Backlog (Prioritized)
**P1**
- Real code execution sandbox for `coding` category (currently just renders code; no execution)
- Web-search MCP for `research` category to ground answers in real-time data with citations

**P2**
- Anonymous-user isolation: currently anonymous chats share a single bucket — give each browser session a separate guest UUID
- Push-to-talk hotkey + waveform animation while recording
- Per-user customizable voice (alloy/nova/onyx/echo/shimmer/etc.)
- Conversation search across history

**P3**
- Mobile polish (bottom sheet for sessions on small screens)
- Rate limiting / per-user quotas on `/api/chat/*`
- Theme switcher + customizable accent color
- Light client-side telemetry (which categories are most-used)
- WebSocket replacement for SSE if reconnect/back-pressure becomes an issue

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
