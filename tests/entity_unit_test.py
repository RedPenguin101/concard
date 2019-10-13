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


def test_card_to_dict():
    card = Card()
    card2 = Card()
    card.title = 'test title'
    card.text = 'hello world'
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


def test_update_from_dict():
    card = Card()
    card.title = 'old title'
    card.text = 'old text'

    card_dict = {
        'uid': str(card.uid),
        'title': 'new title'
    }

    card.update_from_dict(card_dict)

    assert card.title == 'new title'
    assert card.text == 'old text'


def test_text_length_max_500():
    card = Card()
    card.title = 'title'

    long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                   'Integer iaculis interdum diam vitae dapibus. Praesent '
                   'et dapibus eros, rutrum feugiat velit. Proin placerat '
                   'orci dignissim, eleifend dui quis, aliquet tellus. '
                   'Vestibulum ante ipsum primis in faucibus orci luctus et '
                   'ultrices posuere cubilia Curae; Cras vel tincidunt '
                   'velit. Fusce nulla erat, malesuada eu ultrices pulvinar,'
                   ' fringilla viverra nisi. Donec non rutrum velit, sed '
                   'rutrum mi. Praesent consequat, tellus eget sagittis '
                   'ornare, augue justo molestie mi, vel accumsan risus '
                   'turpis id est. Donec congue hendrerit urna, nec aliquet '
                   'quam hendrerit at. Integer eget dui nec arcu venenatis '
                   'viverra nec nec justo. Praesent.')

    card.text = long_string
    assert card.text_exceeds_500()


def test_length_check_no_text():
    card = Card()
    assert not card.text_exceeds_500()
