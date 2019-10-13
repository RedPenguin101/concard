import uuid
from concard.domain import Card


def test_card_create():
    card = Card()
    card.title = "Hello World"

    assert card.uid


def test_card_create_with_parent():
    card1 = Card()
    card2 = Card()

    card1.assign_parent(card2)

    assert card1.parent == card2.uid


def test_edit_card_body():
    card = Card()
    card.edit_text('text')
    assert card.text == 'text'


def test_card_to_dict():
    card = Card()
    card2 = Card()
    card.title = 'test title'
    card.edit_text('hello world')
    card.assign_parent(card2)

    dic = card.to_dict()
    expected = {
        'uid': str(card.uid),
        'title': card.title,
        'text': card.text,
        'parent': str(card.parent),
    }

    assert dic == expected


def test_from_dict():
    uid = uuid.uuid4()
    p_uid = uuid.uuid4()

    dic = {
        'uid': str(uid),
        'text': 'hello world',
        'title': 'test title',
        'parent': str(p_uid),
    }

    card = Card.from_dict(dic)

    assert card.uid == uid
    assert card.parent == p_uid
    assert card.text == 'hello world'
    assert card.title == 'test title'

def test_equality():
    uid = uuid.uuid4()
    p_uid = uuid.uuid4()

    card = Card.from_dict({
        'uid': str(uid),
        'text': 'hello world',
        'title': 'test title',
        'parent': str(p_uid),
    })

    assert card == card
