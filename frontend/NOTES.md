# Frontend integration notes

## Running this

```bash
cp .env.example .env      # adjust VITE_WS_URL if your backend runs elsewhere
npm install
npm run dev
```

Start your FastAPI backend first (`uvicorn app.main:app --reload` from `backend/`),
then open the Vite dev server URL it prints.

## What was verified against the real backend before building this

- Single websocket endpoint: `/agent`. No other routes exist or are assumed.
- The server speaks first the moment the socket opens - the client never
  sends anything until it receives the first audio turn.
- Two interrupt types send a JSON text frame *before* their audio:
  - `'Select dish'` -> JSON array of recommended dishes (rendered as the table)
  - `'confirmation'` -> JSON object of the selected dish (rendered as the card)
  All other interrupt types send audio only.
- Every turn after that is binary audio in, binary audio out - one full
  WAV clip per turn, not a live streaming transcript in either direction.
  This is a real constraint of the backend's Whisper-based STT: it needs a
  complete utterance, not partial audio. The mic button reflects this
  honestly - press to start, press again to stop and send - rather than
  pretending to support fully hands-free continuous listening.

## Known gap, not fixed on the frontend side

When the graph finishes (order confirmed), the backend's while loop just
exits - it does not currently send an explicit "done" message. This
frontend falls back to treating a clean `onclose` with no pending error as
"complete." If you add an explicit completion message on the backend later,
wire it into `useVoiceAgent.js`'s `onmessage` handler for a cleaner signal.

## Where to look if something needs changing

- `src/hooks/useVoiceAgent.js` - all websocket, mic, and audio-playback logic,
  every integration point commented inline.
- `src/components/VoiceOrb.jsx` - the frequency visualization; reads real
  analyser data, nothing here is a random/fake animation.
- `tailwind.config.js` - the color/type tokens if you want to adjust the look.
