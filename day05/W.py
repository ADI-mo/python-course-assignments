import random
import time
import os

# --- Configuration ---
# List of words to choose from
words_bank = ["Red", "Book", "Son", "Star", "Home", "Sea", "Tree", "Flower", "Tree", "Computer", "Ball", "Balloon"]

# Function to clear the screen (so the player can't cheat by scrolling up)
def clear_screen():
    # 'cls' is for Windows, 'clear' is for Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Main Game Logic ---
def start_game():
    sequence = [] # The list of words the player needs to remember
    score = 0
    
    clear_screen()
    print("--- Welcome to the Memory Game ---")
    print("In each round, a new word will be added to the sequence.")
    print("You must type all the words from the beginning to the end.")
    input("Press Enter to start...")

    while True: # Infinite loop until the player loses
        # 1. Pick a random new word
        new_word = random.choice(words_bank)
        sequence.append(new_word)
        
        # 2. Display phase (Memorization)
        clear_screen()
        print(f"*** Level {score + 1} ***")
        print("Get ready...")
        time.sleep(1)
        
        for word in sequence:
            clear_screen()
            # Print with spacing to center the word
            print("\n\n     >>> " + word + " <<<     \n\n") 
            time.sleep(1.2) # Show the word for 1.2 seconds
            clear_screen()  # Hide the word
            time.sleep(0.3) # Short pause in the dark

        # 3. Guessing phase
        print("Now it's your turn! Type the words in the correct order.")
        
        # Check player input against the actual sequence one by one
        for correct_word in sequence:
            user_input = input("-> ")
            
            # Case-insensitive comparison (so "Dog" and "dog" are both okay)
            if user_input.lower() != correct_word.lower():
                # If the input doesn't match - Game Over
                print("\n-------------------------")
                print("Oops! Wrong word.")
                print(f"You wrote '{user_input}', but it should be '{correct_word}'.")
                print(f"Game Over. Your final score: {score}")
                print("-------------------------")
                return # Exit the function (End game)
        
        # If the loop finished without errors - Level Complete
        score += 1
        print("Correct! Getting ready for the next level...")
        time.sleep(1)

# Run the game
start_game()        

