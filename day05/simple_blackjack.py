import random

def print_instructions():
    print("""
    Welcome to Blackjack! 🃏
    
    Here are the rules:
    1. The goal is to get a score close to 21, but not over 21.
    2. Number cards (2-10) are worth their number.
    3. Face cards (J, Q, K) are worth 10.
    4. Ace (A) is worth 11 or 1 (if you go over 21).
    5. The computer dealer must take cards until they have at least 17.
    6. If you go over 21, you lose immediately (Bust).
    
    Good luck! 🍀
    ----------------------------------------------------------
    """)

def deal_card():
    # I used 11 for Ace, and 10 for J, Q, K
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    # Pick a random card from the list
    card = random.choice(cards)
    return card

def calculate_score(cards):
    # Calculate sum of cards
    score = sum(cards)
    
    # Check if we have an Ace (11) and the score is over 21
    if score > 21 and 11 in cards:
        # Change Ace from 11 to 1 so we don't lose
        cards.remove(11)
        cards.append(1)
        score = sum(cards)
        
    return score

def play_game():
    user_cards = []
    computer_cards = []
    is_game_over = False

    # Give 2 cards to me and 2 to the computer
    for i in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    # My turn to play
    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        
        print(f"   Your cards: {user_cards}, current score: {user_score}")
        print(f"   Computer's first card: {computer_cards[0]}")

        # Check if the game should end
        if user_score == 21 or computer_score == 21 or user_score > 21:
            is_game_over = True
        else:
            # Ask if I want another card
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True

    # Computer's turn
    # The computer must take a card if score is less than 17
    while computer_score != 21 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"   Your final hand: {user_cards}, final score: {user_score}")
    print(f"   Computer's final hand: {computer_cards}, final score: {computer_score}")
    
    # Decide who won
    if user_score > 21:
        print("You went over 21. You lose 😭")
    elif computer_score > 21:
        print("Opponent went over. You win! 😁")
    elif user_score > computer_score:
        print("You win! 😃")
    elif computer_score > user_score:
        print("You lose 😤")
    else:
        print("It's a draw 🙃")

# This ensures the game only runs if executed directly, not when imported for testing
if __name__ == "__main__":
    # Show instructions once at the start
    print_instructions()

    # Start the game loop
    while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
        play_game()