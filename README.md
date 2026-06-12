🍽️ Today's Menu
Today's Menu is a meal recommendation app that reduces decision fatigue through gamification and helps users visualize their eating habits over time.

Problem → Solution flow:
Meal decisions take too long → Decision fatigue → Gamified selection → Menu chosen → Eating habit analysis delivered


✨ Key Features
1. Filtering & Decision System

Smart Filter — Customize recommendations by calorie range, food category, dining style (delivery / home cooking), and budget.
Safety Net — Automatically resets search criteria when no results match your filters, so you never hit a dead end.

2. Gamified Recommendation Methods
Eight interactive ways to pick your next meal — no more boring scrolling:
ModeDescription🎲 RandomInstant random pick🎡 RouletteSpin-the-wheel selection🃏 Scratch CardScratch to reveal your meal🏆 World Cup1-on-1 knockout tournament🎲 DiceRoll to decide🃏 Tarot DrawDraw a card for your fate🧠 Smart RecommendAI-style picks based on your last 10 selections⚔️ Battle ModeHead-to-head menu showdown
3. Statistics & Habit Management

Recommendation History — Stores and analyzes up to 50 recent meal selections.
Calorie & Habit Analysis — Tracks daily intake against a 2,000 kcal goal; surfaces insights on preferred categories and peak meal times.
Custom Settings — Add your own menus or exclude specific items from the recommendation pool.


📊 Data
TypeDetailsSource dataKorean Food Nutrition DatabaseCollected dataMenus selected by the userUsageEating habit analysis & personalized recommendations

🔄 User Flow
Select Category → Choose Recommendation Mode → Play Game → Get Result → Confirm → Data reflected in habit analysis & recommendation feed

🚀 Getting Started
bashpip install -r requirements.txt
streamlit run app.py
Project Structure
menu_app/
├── app.py              # Main application logic
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
└── .streamlit/
    └── config.toml     # App theme & settings
