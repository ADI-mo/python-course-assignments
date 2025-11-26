"""
Advanced Number Guessing Game
Features:
- Multiple difficulty levels
- Smart hints system
- Score tracking
- Limited attempts
- Statistics tracking
"""

import random
import time


class GuessingGame:
    """Advanced number guessing game with multiple features"""
    
    def __init__(self):
        self.score = 0
        self.games_played = 0
        self.games_won = 0
        self.total_attempts = 0
        self.best_score = float('inf')
        
    def get_difficulty(self):
        """
        Get difficulty level from user
        
        Returns:
        tuple: (max_number, max_attempts, hint_frequency)
        """
        print("\n" + "="*50)
        print("  Choose Difficulty Level")
        print("="*50)
        print("1. Easy   - Number 1-50,  10 attempts, hints every 2 guesses")
        print("2. Medium - Number 1-100, 7 attempts,  hints every 3 guesses")
        print("3. Hard   - Number 1-200, 5 attempts,  hints every 4 guesses")
        print("4. Expert - Number 1-500, 4 attempts,  no hints!")
        print("="*50)
        
        while True:
            choice = input("\nYour choice (1-4): ").strip()
            if choice == '1':
                return (50, 10, 2)
            elif choice == '2':
                return (100, 7, 3)
            elif choice == '3':
                return (200, 5, 4)
            elif choice == '4':
                return (500, 4, 0)
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def generate_hint(self, target, guess, attempt_num):
        """
        Generate smart hints based on the guess
        
        Parameters:
        target (int): The target number
        guess (int): The user's guess
        attempt_num (int): Current attempt number
        
        Returns:
        str: A helpful hint
        """
        difference = abs(target - guess)
        
        # Temperature-based hints
        if difference == 0:
            return "🎯 PERFECT!"
        elif difference <= 5:
            return "🔥 On fire! You're VERY close!"
        elif difference <= 10:
            return "♨️ Hot! Getting warmer!"
        elif difference <= 20:
            return "🌡️ Warm... you're in the area"
        elif difference <= 50:
            return "❄️ Cool... still far away"
        else:
            return "🧊 Ice cold! Way off!"
    
    def give_special_hints(self, target, attempts_left):
        """
        Give special mathematical hints
        
        Parameters:
        target (int): The target number
        attempts_left (int): Remaining attempts
        """
        hints = []
        
        # Hint about odd/even
        if target % 2 == 0:
            hints.append("The number is EVEN")
        else:
            hints.append("The number is ODD")
        
        # Hint about divisibility
        for divisor in [3, 5, 7]:
            if target % divisor == 0:
                hints.append(f"The number is divisible by {divisor}")
                break
        
        # Hint about prime numbers
        if self.is_prime(target):
            hints.append("The number is PRIME")
        
        # Hint about digits
        if target >= 10:
            digits = [int(d) for d in str(target)]
            digit_sum = sum(digits)
            hints.append(f"Sum of digits: {digit_sum}")
        
        # Hint about range (when desperate)
        if attempts_left <= 2:
            lower = (target // 10) * 10
            upper = lower + 10
            hints.append(f"💡 BONUS HINT: Number is between {lower} and {upper}")
        
        print("\n📌 Special Hints:")
        for hint in hints[:2]:  # Give max 2 hints at a time
            print(f"   • {hint}")
    
    def is_prime(self, n):
        """Check if a number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def play_round(self):
        """Play one round of the game"""
        print("\n" + "="*60)
        print("  🎮 NEW GAME STARTING...")
        print("="*60)
        
        # Get difficulty settings
        max_number, max_attempts, hint_frequency = self.get_difficulty()
        
        # Generate random target number
        target = random.randint(1, max_number)
        
        print(f"\n🎯 I'm thinking of a number between 1 and {max_number}")
        print(f"🎲 You have {max_attempts} attempts to guess it!")
        
        if hint_frequency > 0:
            print(f"💡 You'll get special hints every {hint_frequency} guesses")
        else:
            print("⚠️  Expert mode: NO HINTS!")
        
        print("\n" + "-"*60)
        
        attempts = 0
        guesses = []
        start_time = time.time()
        
        while attempts < max_attempts:
            attempts += 1
            print(f"\n📍 Attempt {attempts}/{max_attempts}")
            
            # Show previous guesses
            if guesses:
                print(f"Previous guesses: {', '.join(map(str, sorted(guesses)))}")
            
            # Get user input
            try:
                guess = int(input("Enter your guess: "))
                
                if guess < 1 or guess > max_number:
                    print(f"⚠️  Please enter a number between 1 and {max_number}")
                    attempts -= 1  # Don't count invalid attempts
                    continue
                
                if guess in guesses:
                    print("⚠️  You already guessed that number!")
                    attempts -= 1  # Don't count repeated guesses
                    continue
                
                guesses.append(guess)
                
            except ValueError:
                print("⚠️  Invalid input! Please enter a number.")
                attempts -= 1  # Don't count invalid attempts
                continue
            
            # Check if correct
            if guess == target:
                elapsed_time = time.time() - start_time
                print("\n" + "="*60)
                print("  🎉 CONGRATULATIONS! YOU WON! 🎉")
                print("="*60)
                print(f"✓ You guessed the number {target} correctly!")
                print(f"✓ Attempts used: {attempts}/{max_attempts}")
                print(f"✓ Time taken: {elapsed_time:.1f} seconds")
                
                # Calculate score (fewer attempts and less time = higher score)
                round_score = (max_attempts - attempts + 1) * 100 + int(50 - elapsed_time)
                round_score = max(round_score, 10)  # Minimum score
                
                print(f"✓ Round score: {round_score} points")
                
                self.score += round_score
                self.games_won += 1
                self.total_attempts += attempts
                
                if attempts < self.best_score:
                    self.best_score = attempts
                    print(f"🏆 NEW BEST SCORE! (fewest attempts: {attempts})")
                
                return True
            
            # Give temperature hint
            hint = self.generate_hint(target, guess, attempts)
            print(f"\n{hint}")
            
            # Tell if higher or lower
            if guess < target:
                print("⬆️  The target number is HIGHER")
            else:
                print("⬇️  The target number is LOWER")
            
            # Give special hints at intervals
            if hint_frequency > 0 and attempts % hint_frequency == 0 and attempts < max_attempts:
                self.give_special_hints(target, max_attempts - attempts)
        
        # Game over - no attempts left
        print("\n" + "="*60)
        print("  ❌ GAME OVER - No attempts left!")
        print("="*60)
        print(f"The number was: {target}")
        print(f"Your guesses were: {', '.join(map(str, sorted(guesses)))}")
        
        self.total_attempts += attempts
        return False
    
    def show_statistics(self):
        """Display game statistics"""
        if self.games_played == 0:
            print("\nNo games played yet!")
            return
        
        print("\n" + "="*60)
        print("  📊 GAME STATISTICS")
        print("="*60)
        print(f"Total games played: {self.games_played}")
        print(f"Games won: {self.games_won}")
        print(f"Games lost: {self.games_played - self.games_won}")
        
        if self.games_played > 0:
            win_rate = (self.games_won / self.games_played) * 100
            print(f"Win rate: {win_rate:.1f}%")
        
        print(f"Total score: {self.score}")
        
        if self.games_played > 0:
            avg_attempts = self.total_attempts / self.games_played
            print(f"Average attempts per game: {avg_attempts:.1f}")
        
        if self.best_score != float('inf'):
            print(f"Best game (fewest attempts): {self.best_score}")
        
        print("="*60)
    
    def play(self):
        """Main game loop"""
        print("\n" + "="*60)
        print("  🎮 WELCOME TO ADVANCED NUMBER GUESSING GAME! 🎮")
        print("="*60)
        print("\nGuess the secret number with smart hints and limited attempts!")
        
        while True:
            print("\n" + "="*60)
            print("  MAIN MENU")
            print("="*60)
            print("1. 🎯 Play New Game")
            print("2. 📊 View Statistics")
            print("3. 🚪 Exit")
            print("="*60)
            
            choice = input("\nYour choice (1-3): ").strip()
            
            if choice == '1':
                self.games_played += 1
                won = self.play_round()
                
                if won:
                    print(f"\n💰 Total score: {self.score} points")
                
            elif choice == '2':
                self.show_statistics()
            
            elif choice == '3':
                print("\n" + "="*60)
                print("  Thanks for playing! 👋")
                if self.games_played > 0:
                    print(f"  Final score: {self.score} points")
                    print(f"  Games won: {self.games_won}/{self.games_played}")
                print("="*60 + "\n")
                break
            
            else:
                print("\n⚠️  Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Run the game"""
    game = GuessingGame()
    game.play()


if __name__ == "__main__":
    main()
