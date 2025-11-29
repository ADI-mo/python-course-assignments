import pytest
from simple_blackjack import calculate_score, deal_card

# --- Tests for calculate_score ---

def test_calculate_score_simple():
    """Test a simple hand without Aces."""
    hand = [10, 5]
    assert calculate_score(hand) == 15

def test_calculate_score_blackjack():
    """Test a Blackjack hand (Ace + 10)."""
    hand = [11, 10]
    assert calculate_score(hand) == 21

def test_calculate_score_ace_conversion():
    """Test that Ace (11) converts to 1 to prevent bust."""
    # 11 + 10 + 5 = 26 (Bust) -> converts Ace to 1 -> 1 + 10 + 5 = 16
    hand = [11, 10, 5]
    assert calculate_score(hand) == 16

def test_calculate_score_multiple_aces():
    """Test logic with two Aces."""
    # 11 + 11 = 22 (Bust) -> converts one Ace to 1 -> 11 + 1 = 12
    hand = [11, 11]
    assert calculate_score(hand) == 12

def test_calculate_score_bust():
    """Test a hand that busts (goes over 21) without Aces."""
    hand = [10, 10, 5]
    assert calculate_score(hand) == 25

# --- Tests for deal_card ---

def test_deal_card_range():
    """Test that deal_card returns a valid card value."""
    card = deal_card()
    valid_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert card in valid_cards

def test_deal_card_is_integer():
    """Test that the returned card is an integer."""
    card = deal_card()
    assert isinstance(card, int)