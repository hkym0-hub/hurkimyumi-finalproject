# 🍽️ Today's Menu

**Today's Menu** is a meal recommendation app that reduces decision fatigue through gamification and helps users visualize their eating habits over time.

> **Problem → Solution flow:**
> Meal decisions take too long → Decision fatigue → Gamified selection → Menu chosen → Eating habit analysis delivered

---

## ✨ Key Features

### 1. Filtering & Decision System

- **Smart Filter** — Customize recommendations by calorie range, food category, dining style (delivery / home cooking), and budget.
- **Safety Net** — Automatically resets search criteria when no results match your filters, so you never hit a dead end.

### 2. Gamified Recommendation Methods

Eight interactive ways to pick your next meal — no more boring scrolling:

| Mode | Description |
|---|---|
| 🎲 Random | Instant random pick |
| 🎡 Roulette | Spin-the-wheel selection |
| 🃏 Scratch Card | Scratch to reveal your meal |
| 🏆 World Cup | 1-on-1 knockout tournament |
| 🎲 Dice | Roll to decide |
| 🃏 Tarot Draw | Draw a card for your fate |
| 🧠 Smart Recommend | AI-style picks based on your last 10 selections |
| ⚔️ Battle Mode | Head-to-head menu showdown |

### 3. Statistics & Habit Management

- **Recommendation History** — Stores and analyzes up to 50 recent meal selections.
- **Calorie & Habit Analysis** — Tracks daily intake against a 2,000 kcal goal; surfaces insights on preferred categories and peak meal times.
- **Custom Settings** — Add your own menus or exclude specific items from the recommendation pool.

---

## 📊 Data

| Type | Details |
|---|---|
| Source data | Korean Food Nutrition Database (식품영양성분 데이터베이스) |
| Collected data | Menus selected by the user |
| Usage | Eating habit analysis & personalized recommendations |

> **Note:** While the original data source is the Korean Food Nutrition Database, the app uses a preprocessed and refined version of that data.

---

## 🔄 User Flow

```
Select Category → Choose Recommendation Mode → Play Game → Get Result → Confirm → Data reflected in habit analysis & recommendation feed
```

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Project Structure

```
menu_app/
├── app.py                    # Main application logic
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
└── data/
    ├── Detailed_Menu_Data.csv  # Preprocessed menu nutrition data
    └── presentation.pptx       # Project presentation
```
