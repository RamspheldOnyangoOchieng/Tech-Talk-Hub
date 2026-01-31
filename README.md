# AI-Fundamentals-Class

## Traveling Salesman Route Optimization

This project implements a solution to the Traveling Salesman Problem (TSP) using real-world geographical data from Kenya. The implementation includes:

- Route optimization between multiple cities
- Real-time distance calculations using OpenRouteService API
- Interactive map visualization with animated car movement
- Detailed route analysis and distance reporting

### Features

- Calculates all possible routes between cities
- Finds the shortest route using real driving distances
- Visualizes the route on an interactive map
- Shows animated car movement along the optimized route
- Displays detailed distance information for each possible route

### Requirements

- Python 3.x
- Required packages:
  - folium
  - openrouteservice
  - matplotlib
  - numpy
  - pandas

### Usage

1. Install the required packages:
```bash
pip install folium openrouteservice matplotlib numpy pandas
```

2. Run the script:
```bash
python TravelingSalesMan_RouteOptimization.py
```

3. View the results:
- Check the console output for route analysis
- Open 'optimized_route_map.html' in a web browser to see the interactive visualization

### Current Implementation

The current implementation includes routes between:
- Nairobi
- Meru
- Nyeri
- Nandi
- Kericho

### Algorithm Used

This project solves the Traveling Salesman Problem using a brute-force approach. It generates all possible permutations of the intermediate towns (excluding the start/end city, Nairobi) and calculates the total driving distance for each complete route (starting and ending in Nairobi). The route with the shortest total distance is then identified as the optimal route.

This method guarantees finding the absolute shortest route but becomes computationally expensive as the number of towns increases due to the factorial growth of permutations.

The program calculates the optimal route starting and ending in Nairobi, considering real driving distances between cities.

---

## 📚 Educational Coding Projects

A collection of interactive coding projects designed for students from **Grade 1 to Grade 12**. Each project is tailored to the appropriate skill level and teaches fundamental programming concepts through fun, hands-on activities.

### 🎮 Grade 1-3 (Beginners)

Simple, visual, and interactive projects using HTML/CSS/JavaScript:

| Project | Description | File |
|---------|-------------|------|
| **Move the Character** | Use arrow keys to move a character while avoiding monsters that chase you! Features multiple monsters with teleportation abilities. | `Grade_1-3/move_character.html` |
| **Play the Drum** | Interactive drum kit - click or press keys to play different drum sounds. | `Grade_1-3/play_the_drum.html` |
| **Tic Tac Toe** | Classic two-player Tic Tac Toe game with a colorful interface. | `Grade_1-3/tic_tac_toe.html` |

### 🧮 Grade 4-6 (Intermediate)

Projects introducing logic, math operations, and user interaction:

| Project | Description | File |
|---------|-------------|------|
| **Calculator** | A functional calculator with basic arithmetic operations and a modern UI. | `Grade_4-6/calculator.html` |
| **Quiz Game** | Interactive quiz game with multiple-choice questions and score tracking. | `Grade_4-6/quiz_game.html` |
| **Score Counter** | Keep track of scores for games or activities with increment/decrement buttons. | `Grade_4-6/score_counter.html` |
| **Mystery Number (No JS)** | Learn how CSS can handle game logic using radio buttons and selectors. | `Grade_4-6/guess_number_nofilter.html` |

### 🐍 Grade 7-9 (Python Introduction)

Introduction to Python programming with text-based games:

| Project | Description | File |
|---------|-------------|------|
| **Guess the Number** | A number guessing game where the computer picks a random number and gives hints. | `Grade_7-9/guess_number.py` |
| **Maze Escape** | A fun maze game using Turtle graphics. Find the gold treasure while avoiding walls! | `Grade_7-9/maze_escape.py` |
| **Number Quest** | Gamified UI version of Guess the Number with high scores and difficulty levels. | `Grade_7-9/guess_number_ui.html` |
| **Advanced Tic Tac Toe** | Enhanced Tic Tac Toe with better visuals and game logic. | `Grade_7-9/tic_tac_toe_advanced.html` |

### 🌐 Grade 10-12 (Advanced)

Complex web applications with forms, layouts, and data management:

| Project | Description | File |
|---------|-------------|------|
| **Registration Form** | A complete user registration form with validation and modern styling. | `Grade_10-12/registration_form.html` |
| **Expense Tracker** | Track income and expenses with a dynamic interface and balance calculation. | `Grade_10-12/expense_tracker.html` |
| **Flexbox Game** | Learn CSS Flexbox through an interactive puzzle game. | `Grade_10-12/flexbox_game.html` |

### 🚀 How to Run

1. **HTML Projects**: Simply open the `.html` file in any web browser.
2. **Python Projects**: Run with Python 3:
   ```bash
   python Grade_7-9/guess_number.py
   ```

### 🎯 Learning Objectives

- **Grade 1-3**: Introduction to cause-and-effect, basic interactivity
- **Grade 4-6**: Logic, arithmetic operations, user input handling
- **Grade 7-9**: Variables, loops, conditionals, functions in Python
- **Grade 10-12**: Web development, forms, CSS layouts, JavaScript DOM manipulation

---

## 📁 Other Files

| File | Description |
|------|-------------|
| `calculator.py` | Python-based calculator |
| `me.py` | Personal Python script |
| `todolist.py` | Python to-do list application |

---

*This repository is part of the Tech Talk Hub initiative for teaching programming concepts.*
