# 🍽️ Today's Menu

A gamified menu recommendation web application designed to reduce the stress of choosing what to eat. Instead of endlessly scrolling through delivery apps or asking friends for suggestions, users can enjoy interactive game-based recommendation systems and build personalized eating habits through their meal selections.

## 🎯 Project Goal

Many people experience decision fatigue when choosing meals every day.

This project aims to:

* Reduce menu selection stress through gamification.
* Make the decision-making process more enjoyable.
* Collect user meal choices and visualize eating habits.
* Provide personalized menu recommendations based on accumulated data.

### Problem Solving Flow

Menu Decision Takes Too Long
➡️ Decision Fatigue
➡️ Gamified Recommendation System
➡️ Faster Menu Selection
➡️ Meal Choice Data Collection
➡️ Eating Habit Analysis & Personalized Recommendations

---

## ✨ Key Features

### 1. Smart Menu Filtering

Users can customize recommendations using various conditions:

* Calorie range
* Food category
* Dining style (delivery or cooking)
* Budget range

#### Safety Net System

If no menu matches the selected filters, the system automatically resets the search criteria to ensure recommendations are always available.

---

### 2. Gamified Recommendation Methods

Instead of a simple random list, users can choose meals through interactive mini-games.

#### Engagement-Based Methods

* 🎲 Random Selection
* 🎡 Roulette Wheel
* 🃏 Scratch Card
* 🏆 Menu World Cup Tournament

#### Utility-Based Methods

* 🎲 Dice Roll
* 🃏 Tarot Card Draw
* 🧠 Smart Recommendation
* ⚔️ Battle Mode

Each method offers a unique experience while leading users toward a final menu choice.

---

### 3. User Habit Tracking & Analytics

#### Meal Adoption System

When a user accepts a recommended menu, it is recorded as an actual meal choice.

This data is then used to:

* Analyze eating habits
* Generate personalized recommendation feeds
* Track food preferences over time

#### Statistics Dashboard

* Recent recommendation history (up to 50 entries)
* Daily calorie tracking
* Favorite food category analysis
* Peak meal-time analysis

---

### 4. Custom Menu Management

Users can:

* Add custom menus
* Exclude unwanted menus
* Personalize their recommendation pool

---

## 📊 Data Utilization

### External Data

* Korean Food Composition Database (Food Safety Korea)
* Food calorie and nutritional information

### Collected User Data

* Adopted menu selections
* Recommendation history
* Food preference patterns

### Data Usage

* Display calorie information for recommended menus
* Analyze user eating habits
* Generate personalized menu recommendations

---

## 🔄 User Flow

1. Select menu category
2. Choose recommendation method
3. Play the recommendation game
4. Receive menu result
5. Accept the menu
6. Save meal data
7. Update habit analysis and recommendation feed

---

## 🚀 How to Run

### Local Execution

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```text
menu_app
├── app.py              # Main application logic
├── requirements.txt    # Dependency packages
├── README.md           # Project documentation
└── .streamlit/
    └── config.toml     # Streamlit configuration
```
