Simple Python Blackjack 🃏

A simple, text-based implementation of the classic Blackjack card game in Python. This project includes the game logic and a suite of unit tests to ensure everything works correctly.

Prerequisites

Python 3.x: Make sure you have Python installed on your computer. You can download it from python.org.

Installation

Clone or Download the project files into a folder (e.g., blackjack_game).

Install Dependencies: The game itself uses standard Python libraries, but to run the tests, you need pytest.

Open your terminal or command prompt and run:

pip install pytest


How to Play the Game

To start the game, navigate to the project folder in your terminal and run the main script:

python simple_blackjack.py


Game Rules

Goal: Get a score closer to 21 than the dealer without going over 21.

Card Values:

Number cards (2-10): Face value.

Face cards (J, Q, K): 10 points.

Ace (A): 11 or 1 point (automatically adjusts to prevent busting).

Dealer Rules: The computer dealer must hit until their score is at least 17.

How to Run the Tests

This project includes automated tests to verify the scoring logic and card dealing. We use pytest to run them.

Open your terminal in the project folder.

Run the following command:

pytest


You should see output indicating that the tests passed (e.g., 7 passed in 0.05s).

Files in this Project

simple_blackjack.py: The main game code.

test_blackjack.py: The test file containing unit tests for the game logic.

README.md: This instruction file.

Acknowledgments

Gemini AI: Used to assist in writing the pytest test suite, refactoring/improving the game code, and generating this README.
