# Voice-Driven Mood-Based Ordering Agent

A voice-first agent that recommends food based on mood, budget, and order
history — not a search box, a conversation. Built with LangGraph, FastAPI,
and a React frontend, backed by Groq (speech-to-text and text-to-speech)
and Gemini (reasoning and structured extraction).

## Architecture

![Agent workflow](assets/agent_architecture.gif)

<details>
<summary><strong>View interactive architecture diagram</strong></summary>

```mermaid
flowchart LR
    start(["__start__"]):::pillNode --> data_receiver["data_receiver<br/>receives voice / text input"]:::coreNode
    data_receiver -.->|"invalid input"| data_receiver
    data_receiver -.-> check_user["check_user<br/>routes new vs. returning user"]:::coreNode

    check_user -.->|"existing user"| history_loader["history_loader<br/>loads past order history"]:::branchNode
    check_user -.->|"new user"| new_user["new_user<br/>creates a new user record"]:::branchNode
    new_user --> check_user

    history_loader --> order_collection["order_collection<br/>gathers the food order"]:::coreNode
    order_collection --> check_order_completness["check_order_completness<br/>validates order details"]:::coreNode

    check_order_completness -.->|"complete"| recommendations["recommendations<br/>suggests mood-based dishes"]:::branchNode
    check_order_completness -.->|"incomplete"| complete_info["complete_info<br/>asks for missing details"]:::branchNode
    complete_info --> check_order_completness

    recommendations --> select_item["select_item<br/>user picks a food item"]:::coreNode
    select_item --> order_confirmation["order_confirmation<br/>confirms the final order"]:::coreNode
    order_confirmation -.->|"change item"| select_item
    order_confirmation -.-> update_db["update_db<br/>saves order to database"]:::coreNode
    update_db --> end_(["__end__"]):::pillNode

    classDef pillNode fill:#F1EFE8,stroke:#888780,color:#2C2C2A
    classDef coreNode fill:#EEEDFE,stroke:#7F77DD,color:#26215C
    classDef branchNode fill:#E1F5EE,stroke:#5DCAA5,color:#04342C
```

</details>

A static PNG export of the graph is also available in [`assets/`](assets/).

## How a conversation works

1. **Identify** — the agent asks for a name and ID. Returning users are
   recognized and their order history loads; new users are assigned an ID
   on the spot (shown on screen, not just spoken, since numbers are easy
   to mishear).
2. **Collect the order** — the user describes what they want in their own
   words ("something spicy, budget around 900"). Missing details (taste,
   spice level, budget) trigger a follow-up question instead of guessing.
3. **Recommend** — the agent narrates and displays a short list of dishes,
   filtered against the menu and ranked using the user's past orders.
4. **Select & confirm** — the user picks a dish by voice, the agent reads
   it back for confirmation, and the order is written to the database.

Every pause in that flow (asking for a name, asking for missing order
details, asking for confirmation) is a LangGraph `interrupt()` — the graph
genuinely pauses mid-execution and resumes exactly where it left off once
the next voice input arrives, rather than restarting the conversation.

## Tech stack

**Backend**
- FastAPI + a single WebSocket endpoint (audio in, audio out, per turn)
- LangGraph for the conversation state machine and human-in-the-loop pauses
- PostgreSQL (via `AsyncPostgresSaver`) for graph checkpointing
- SQLite for restaurant, menu, user, and order data
- Groq Whisper for speech-to-text, Groq Orpheus for text-to-speech
- Gemini (via LangChain) for structured extraction and recommendation reasoning

**Frontend**
- React + Vite + Tailwind CSS
- Native WebSocket + MediaRecorder for capture, no fixed recording window
- Web Audio API (`AnalyserNode`) driving a real frequency visualization off
  the actual playing/captured audio — not a decorative animation

## Project structure

```
├── assets/            architecture diagrams
├── backend/
│   ├── app/            FastAPI entry point, the WebSocket endpoint
│   ├── graph/           LangGraph nodes, schemas, and the compiled graph
│   ├── database/        SQLite schema, seed data, and query helpers
│   ├── models/           Groq/Gemini client wrappers (STT, TTS, extraction)
│   └── config/           environment loading, prompts, sample data
└── frontend/
    └── src/
        ├── hooks/         useVoiceAgent - all websocket/audio logic
        └── components/    the orb, recommendation table, status UI
```

## Running it locally

**Backend**
```bash
cd backend
cp .env.example .env   # fill in GROQ_API_KEY, GOOGLE_API_KEY, DATABASE_URL
uv sync
uv run python -m uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
cp .env.example .env   # VITE_WS_URL, defaults to ws://localhost:8000/agent
npm install
npm run dev
```

Open the printed Vite URL, click **Start ordering**, and allow microphone
access.

## Known limitations

- English only — the Whisper/Orpheus models in use here don't support
  Urdu, so mixed Roman Urdu/English speech works inconsistently.
- One complete audio clip per turn, not a live streaming transcript — a
  real constraint of batch-based STT, not a frontend shortcut.
- No production deployment config yet; this is built and tested for local
  development.

## License

See [`LICENSE`](LICENSE).
