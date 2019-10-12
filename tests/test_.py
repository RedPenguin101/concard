from concard.domain import Card

def test_card_create():
    card = Card()
    card.title = "Hello World"