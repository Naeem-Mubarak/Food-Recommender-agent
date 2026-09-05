# Voice-Driven Mood-Based Ordering Agent

A voice-first (text as optional) agent that recommends food based on mood, budget, and order
history — not a search box, a conversation.

## Architecture

![Agent workflow](assets/agent_architecture.gif)

A static PNG snapshot of the same graph is available at
[`assets/agent_architecture.png`](assets/agent_architecture.png).

## How a conversation works

1. **Identify** — the agent asks for a name and ID. Returning users are
   recognized and their order history loads; new users are assigned an ID
   on the spot (shown on screen, not just spoken, since numbers are easy
   to mishear).
2. **Collect the order** — the user describes what they want, by voice or
   by typing ("something spicy, budget around 900"). Missing details
   (taste, budget) trigger a follow-up question instead of guessing.
3. **Recommend** — the agent narrates and displays up to two dishes,
   filtered against the menu (spice, sweetness, budget, cuisine) and
   ranked using the user's past orders.
4. **Select, reject, or retry** — the user picks a dish, or rejects both.
   Rejected dishes are remembered and excluded from the next round of
   suggestions. After three rejections, the agent asks the user to
   describe their order again from scratch rather than looping forever.
5. **Confirm** — the agent reads back the selected dish for confirmation,
   and the order is written to the database.

Every pause in that flow (asking for a name, asking for missing order
details, asking for confirmation, asking for a fresh pick after a
rejection) is a LangGraph `interrupt()` (human-in-the-loop) — the graph
genuinely pauses mid-execution and resumes exactly where it left off once
the next input arrives, rather than restarting the conversation.

## Input and output

- **Input** — voice (recorded, no fixed duration) or typed text, switchable
  at any point in the conversation via a toggle in the UI.
- **Output** — always spoken. The agent's reply is synthesized to audio
  regardless of which input mode the user is in.

## Tech stack

**Backend**
- FastAPI + a single WebSocket endpoint (per-turn audio/text in, audio out)
- LangGraph for the conversation state machine and human-in-the-loop pauses
- PostgreSQL (via `AsyncPostgresSaver`) for graph checkpointing (session memory)
- SQLite for restaurant, menu, user, and order data
- Groq Whisper for speech-to-text, Groq Orpheus for text-to-speech
- Gemini (via LangChain) for open-ended extraction (name, order details,
  budget) where the input is genuinely free-form; 
  history formatting run as plain filtering/scoring logic where the
  underlying data is already structured, to keep API usage to what
  actually needs language understanding

**Frontend**
- React + Vite + Tailwind CSS
- Native WebSocket + MediaRecorder for voice capture, no fixed recording window
- Web Audio API (`AnalyserNode`) driving a real frequency visualization off
  the actual playing/captured audio — not a decorative animation

## Project structure

├── assets/ architecture diagrams
├── backend/
│ ├── app/ FastAPI entry point, the WebSocket endpoint
│ ├── graph/ LangGraph nodes, schemas, and the compiled graph
│ ├── database/ SQLite schema, seed data, and query helpers
│ ├── models/ Groq/Gemini client wrappers (STT, TTS, extraction)
│ └── config/ environment loading, prompts, sample data
└── frontend/
└── src/
├── hooks/ useVoiceAgent - websocket, audio, and text input logic
└── components/ the orb, recommendation table, input toggle, status UI




## Running it locally

**Backend**
```bash
cd backend
cp .env.example .env   # fill in GROQ_API_KEY, GOOGLE_API_KEY, DATABASE_URL
uv sync
uv run python -m database.table_creation   # sets up + seeds the SQLite db
uv run python -m uvicorn app.main:app --reload --ws wsproto --ws-max-size 20000000 --ws-ping-interval 20 --ws-ping-timeout 3600
```

**Frontend**
```bash
cd frontend
cp .env.example .env   # VITE_WS_URL, defaults to ws://localhost:8000/agent
npm install
npm run dev
```

Open the printed Vite URL, click **Start ordering**, and choose voice or text.

## Known limitations

- English only — the Whisper/Orpheus models in use here don't support
  Urdu, so mixed Roman Urdu/English speech works inconsistently.
- Voice input is one complete clip per turn, not a live streaming
  transcript — a real constraint of batch-based STT, not a shortcut.
  Kokoro was the other alternative for streaming but due to latency issues we didn't
  use that
- No production deployment config yet; this is built and tested for local
  development.
- Note: Data is AI generated so there might be some porblems in the rating of spice level and sweet level of the dishes so don't worry about that.

## License

See [`LICENSE`](LICENSE).