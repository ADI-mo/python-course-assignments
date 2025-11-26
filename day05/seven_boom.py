"""
Seven Boom Game
The game goes through numbers from 1 to a number chosen by the user.
Any number divisible by 7 or containing the digit 7 prints "BOOM!"
"""

def is_boom_number(number):
    """
    Check if a number is a "boom" number - divisible by 7 or contains the digit 7
    
    Parameters:
    number (int): The number to check
    
    Returns:
    bool: True if it's a boom number, False otherwise
    """
    # Check if the number is divisible by 7
    if number % 7 == 0:
        return True
    
    # Check if the number contains the digit 7
    if '7' in str(number):
        return True
    
    return False


def play_seven_boom(max_number):
    """
    Play Seven Boom game up to a certain number
    
    Parameters:
    max_number (int): The maximum number in the game
    """
    print(f"\n{'='*40}")
    print(f"  Seven Boom Game: 1 to {max_number}")
    print(f"{'='*40}\n")
    
    boom_count = 0  # Count BOOM numbers
    
    for num in range(1, max_number + 1):
        if is_boom_number(num):
            print(f"{num}: BOOM! 💥")
            boom_count += 1
        else:
            print(num)
    
    print(f"\n{'='*40}")
    print(f"  Total: {boom_count} BOOM numbers!")
    print(f"{'='*40}\n")


def play_seven_boom_interactive():
    """
    Interactive version of the game - player guesses if the number is BOOM
    """
    import random
    
    print("\n" + "="*50)
    print("  Welcome to Seven Boom - Guessing Mode!")
    print("="*50)
    print("\nRules:")
    print("- I will show you a number")
    print("- You need to guess if it's a BOOM number (divisible by 7 or contains 7)")
    print("- Answer 'yes' or 'no' (or y/n)")
    print("="*50 + "\n")
    
    score = 0
    rounds = 5
    
    for round_num in range(1, rounds + 1):
        # Pick a random number between 1 and 100
        number = random.randint(1, 100)
        
        print(f"\nRound {round_num}/{rounds}")
        print(f"The number is: {number}")
        
        # Get answer from player
        while True:
            answer = input("Is this BOOM? (yes/no or y/n): ").strip().lower()
            if answer in ['y', 'n', 'yes', 'no']:
                break
            print("Please enter 'yes' or 'no'")
        
        # Convert answer to True/False
        user_thinks_boom = answer in ['y', 'yes']
        
        # Check the correct answer
        is_actually_boom = is_boom_number(number)
        
        # Check if player was correct
        if user_thinks_boom == is_actually_boom:
            print("✓ Correct! 🎉")
            score += 1
            if is_actually_boom:
                print(f"  {number} is indeed BOOM (divisible by 7 or contains 7)")
            else:
                print(f"  {number} is indeed not BOOM")
        else:
            print("✗ Wrong! 😞")
            if is_actually_boom:
                print(f"  {number} is BOOM!")
                # Explain why
                if number % 7 == 0:
                    print(f"  Because {number} ÷ 7 = {number // 7}")
                if '7' in str(number):
                    print(f"  Because {number} contains the digit 7")
            else:
                print(f"  {number} is not BOOM")
    
    print("\n" + "="*50)
    print(f"  Game Over! Score: {score}/{rounds}")
    if score == rounds:
        print("  Perfect! 🏆")
    elif score >= rounds * 0.6:
        print("  Good job! 👍")
    else:
        print("  Keep practicing! 💪")
    print("="*50 + "\n")


def main():
    """
    Main menu of the game
    """
    while True:
        print("\n" + "="*50)
        print("  Seven Boom Game")
        print("="*50)
        print("\nChoose game mode:")
        print("1. Display all BOOM numbers up to a certain number")
        print("2. Interactive guessing game")
        print("3. Exit")
        print("="*50)
        
        choice = input("\nYour choice (1/2/3): ").strip()
        
        if choice == '1':
            while True:
                try:
                    max_num = int(input("\nUp to what number? (e.g., 50): "))
                    if max_num > 0:
                        play_seven_boom(max_num)
                        break
                    else:
                        print("Please enter a positive number")
                except ValueError:
                    print("Please enter a valid number")
        
        elif choice == '2':
            play_seven_boom_interactive()
        
        elif choice == '3':
            print("\nThanks for playing! Goodbye! 👋\n")
            break
        
        else:
            print("\nInvalid choice. Please choose 1, 2, or 3")


if __name__ == "__main__":
    main()
