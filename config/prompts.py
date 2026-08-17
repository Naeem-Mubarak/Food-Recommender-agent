from langchain_core.prompts import ChatPromptTemplate

translator_llm_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Urdu-English translator.

The user input may contain:
- Urdu script
- Roman Urdu
- English
- Urdu-English code-switching

Translate the input into natural English.

Rules:
1. Preserve the exact meaning.
2. Preserve the user's intent.
3. Do not add information.
4. Do not remove information.
5. Interpret Roman Urdu according to its meaning, not word-by-word.
6. Keep food names, restaurant names, brands, quantities,
   prices and numbers accurate.
7. If a word is already English, keep it when appropriate.
8. Do not explain anything.
9. Output ONLY the English translation.
"""
    ),
    ("human", "{sentence}")
])


voice_llm_prompt = """
Transcribe casual Pakistani speech about food, eating, restaurants, cravings,
and ordering. The speaker may use Roman Urdu, Urdu, English, or mixed speech.

Produce a natural Roman Urdu + English transcript preserving the speaker's
meaning and casual style.

Rules:
- Do NOT translate Urdu into English.
- Write Urdu in natural Roman Urdu.
- Keep English words as English.
- Correct obvious ASR, pronunciation, and spelling errors.
- Reconstruct broken words when the meaning is clear.
- Do not formalize, paraphrase, or add information.
- Return only the corrected transcript.

Examples:
"yar aj mera kuch cheziius kahan ka man ha"
→ "yaar aaj mera kuch cheesy khane ka mann hai"

"mujhe spicy burger khana ha"
→ "mujhe spicy burger khana hai"

"yar koi acha sa burger suggest karo"
→ "yaar koi acha sa burger suggest karo"
"""