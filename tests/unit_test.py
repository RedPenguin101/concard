import json
import pytest
from concard.domain import Card
from concard.repo import JsonRepo

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
    card.edit_text('hello world')
    card.assign_parent(card2)

    dic = card.to_dict()
    expected = {
        'uid': str(card.uid),
        'text': card.text,
        'parent': str(card.parent),
    }

    assert dic == expected


def test_repo_create():
    repo = JsonRepo('test')
    assert repo.env == 'test'
    assert repo.path == 'files/test/'


def test_repo_add():
    repo = JsonRepo('test')
    card = Card()
    repo.add(card)
    assert repo.cards == [card]


def test_repo_no_duplicate():
    repo = JsonRepo('test')
    card = Card()

    repo.add(card)
    with pytest.raises(Exception):
        repo.add(card)    


def test_repo_save():
    repo = JsonRepo('test')
    card = Card()

    repo.add(card)
    repo.save()

    expected_file_name = repo.path + str(card.uid) + ".json"
    expected_dict = {
        'uid': str(card.uid),
    }

    with open(expected_file_name) as file:
        data = json.loads(file.read())

    assert data == expected_dict
        