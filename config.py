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




dishes = [
    (1, 1, "Chicken Karahi", 4, 550, "non-veg", 7, 4.5),
    (2, 1, "Chapli Kebab", 3, 400, "non-veg", 6, 4.2),
    (3, 1, "Daal Chawal", 1, 250, "veg", 7, 4.0),
    (4, 1, "Seekh Kebab", 3, 380, "non-veg", 6, 4.1),
    (5, 1, "Mutton Pulao", 3, 600, "non-veg", 6, 4.3),
    (6, 2, "Kung Pao Chicken", 4, 600, "non-veg", 7, 4.3),
    (7, 2, "Veg Fried Rice", 1, 350, "veg", 7, 3.9),
    (8, 2, "Chili Garlic Noodles", 5, 450, "veg", 5, 4.6),
    (9, 2, "Manchurian", 3, 420, "veg", 5, 4.2),
    (10, 2, "Sweet and Sour Chicken", 2, 550, "non-veg", 6, 4.0),
    (11, 3, "Margherita Pizza", 1, 700, "veg", 4, 4.4),
    (12, 3, "Pepperoni Pizza", 3, 850, "non-veg", 3, 4.1),
    (13, 3, "Pasta Alfredo", 1, 650, "veg", 4, 4.0),
    (14, 3, "Spicy Arrabiata Pasta", 4, 600, "veg", 5, 4.2),
    (15, 3, "Garlic Bread", 1, 250, "veg", 3, 4.3),
    (16, 4, "Zinger Burger", 3, 500, "non-veg", 3, 4.7),
    (17, 4, "Broast (2pc)", 2, 450, "non-veg", 3, 4.5),
    (18, 4, "French Fries", 1, 200, "veg", 2, 4.2),
    (19, 4, "Chicken Wrap", 2, 400, "non-veg", 4, 4.1),
    (20, 4, "Loaded Fries", 3, 350, "non-veg", 2, 4.4),
    (21, 5, "Zinger Burger", 3, 550, "non-veg", 3, 4.6),
    (22, 5, "Hot Wings", 4, 450, "non-veg", 3, 4.5),
    (23, 5, "Krunch Burger", 3, 500, "non-veg", 3, 4.3),
    (24, 5, "Popcorn Chicken", 3, 400, "non-veg", 3, 4.4),
    (25, 5, "Twister", 2, 480, "non-veg", 4, 4.2),
    (26, 6, "Nihari", 4, 450, "non-veg", 6, 4.5),
    (27, 6, "Haleem", 3, 400, "non-veg", 6, 4.6),
    (28, 6, "Biryani", 4, 350, "non-veg", 6, 4.7),
    (29, 6, "Palak Paneer", 2, 300, "veg", 8, 4.1),
    (30, 6, "Chana Chaat", 2, 200, "veg", 8, 4.0),
    (31, 7, "Cheese Burger", 2, 450, "non-veg", 3, 4.2),
    (32, 7, "Club Sandwich", 2, 350, "veg", 5, 4.0),
    (33, 7, "Loaded Nachos", 3, 400, "veg", 3, 4.3),
    (34, 7, "Fried Chicken", 4, 500, "non-veg", 3, 4.4),
    (35, 7, "Milkshake Combo", 1, 550, "veg", 4, 4.5),
    (36, 8, "Protein Shake", 1, 350, "veg", 9, 4.3),
    (37, 8, "Fruit Smoothie", 1, 300, "veg", 9, 4.5),
    (38, 8, "Oats Bowl", 1, 250, "veg", 9, 4.2),
    (39, 8, "Grilled Chicken Salad", 2, 450, "non-veg", 9, 4.6),
    (40, 8, "Green Detox Juice", 1, 280, "veg", 10, 4.1),
    (41, 9, "Peshawari Karahi", 5, 600, "non-veg", 6, 4.7),
    (42, 9, "Spicy Tikka Boti", 4, 500, "non-veg", 6, 4.5),
    (43, 9, "Bhindi Masala", 3, 300, "veg", 7, 4.0),
    (44, 9, "Spicy Roast Chicken", 4, 550, "non-veg", 6, 4.6),
    (45, 9, "Masala Fish", 4, 500, "non-veg", 6, 4.3),
    (46, 10, "Gulab Jamun", 1, 200, "veg", 3, 4.6),
    (47, 10, "Ras Malai", 1, 250, "veg", 3, 4.5),
    (48, 10, "Kheer", 1, 220, "veg", 4, 4.3),
    (49, 10, "Chocolate Cake", 1, 400, "veg", 2, 4.7),
    (50, 10, "Ice Cream Sundae", 1, 350, "veg", 2, 4.8),
]



restaurants = [
    (1, "Spice Villa", "Pakistani"),
    (2, "Golden Dragon", "Chinese"),
    (3, "Pizza Point", "Italian"),
    (4, "Karachi Broast", "Fast Food"),
    (5, "KFC", "Fast Food"),
    (6, "Food Masala", "Desi Food"),
    (7, "Yumms", "Fast Food"),
    (8, "Health is Wealth", "Healthy Milk Shakes"),
    (9, "Roasters", "Traditional Spicy Food"),
    (10,"Candy land", "Sweet Dishes")
]


users=[
    (2, 'Naeem'),
    (4, 'Sameer')
]

orders = [
    (2, 1, 1, 'Chicken Karahi', 4, 550, 'non-veg', 7),
    (2, 1, 2, 'Chapli Kebab', 3, 400, 'non-veg', 6),
    (2, 2, 6, 'Kung Pao Chicken', 4, 600, 'non-veg', 7),
    (2, 2, 9, 'Manchurian', 3, 420, 'veg', 5),
    (2, 4, 16, 'Zinger Burger', 3, 500, 'non-veg', 3),
    (4, 1, 3, 'Daal Chawal', 1, 250, 'veg', 7),
    (4, 3, 11, 'Margherita Pizza', 1, 700, 'veg', 4),
    (4, 6, 26, 'Nihari', 4, 450, 'non-veg', 6),
    (4, 8, 36, 'Protein Shake', 1, 350, 'veg', 9),
    (4, 10, 46, 'Gulab Jamun', 1, 200, 'veg', 3),
]