def is_boom_number(number):
    """
    Check if a number is a BOOM number (divisible by 7 or contains digit 7)
    
    Parameters:
    number (int): The number to check
    
    Returns:
    bool: True if BOOM, False otherwise
    """
    # Check if divisible by 7 OR contains the digit 7
    if number % 7 == 0 or '7' in str(number):
        return True
    return False


def guessing_game():
    """Get user's guess"""
    guess = int(input("Enter your guess number: "))
    return guess


def main_menu():            
    """
    Main menu of the game
    """    
    print("Welcome to the Seven Boom Guessing Game!")
    print("Try to guess if your number is a BOOM number.")
    print("BOOM = divisible by 7 OR contains the digit 7")
    print("Good luck!\n")
    
    guess = guessing_game()
    
    if is_boom_number(guess):
        print(f"BOOM! 💥")
        print(f"{guess} is a BOOM number!")
        if guess % 7 == 0:
            print(f"  - {guess} is divisible by 7 ({guess} ÷ 7 = {guess // 7})")
        if '7' in str(guess):
            print(f"  - {guess} contains the digit 7")
    else:
        print(f"Not BOOM!")
        print(f"{guess} is not a BOOM number.")
    
    print("\nThank you for playing! Goodbye!")                
        
    return          


if __name__ == "__main__":
    main_menu() 