# 🍽️ Today's Menu

A menu recommendation web application designed to solve the daily dilemma of "What should I eat?". Beyond simple lists, this app incorporates various gamification elements to turn the decision-making process into an enjoyable experience.

## ✨ Key Features

### 1. Filtering & Decision System
* **Smart Filter**: Customize recommendations by setting calorie range, food type, dining style (delivery/cooking), and budget.
* **Safety Net**: Automatically resets search criteria if no results match your filters, ensuring a seamless user experience without dead ends.

### 2. Gamified Recommendation Methods
Stop the boring scrolling and choose your meal using eight interactive methods:
* **Engagement**: 🎲 Random, 🎡 Roulette, 🃏 Scratch Card, 🏆 World Cup (1:1 Tournament).
* **Utility**: 🎲 Dice, 🃏 Tarot Card Draw, 🧠 Smart Recommendations (based on last 10 entries), ⚔️ Battle Mode.

### 3. Statistics & Management
* **Recommendation History**: Stores and analyzes up to 50 of your recent meal selections.
* **Calorie & Habit Analysis**: Track your daily intake against a 2,000 kcal goal, and view insights on your preferred food categories and peak meal times.
* **Custom Settings**: Add your own menus or exclude specific items from the recommendation pool.

---

## 🚀 How to Run

### Local Execution
```bash
pip install -r requirements.txt
streamlit run app.py

## menu_app
├── app.py              # Main application logic
├── requirements.txt    # List of dependency packages
├── README.md           # Project documentation
└── .streamlit/
    └── config.toml     # App theme and settings
