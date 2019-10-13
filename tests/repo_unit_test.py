import os
import uuid
import json
import pytest
from concard.domain import Card
from concard.repo import JsonRepo


@pytest.fixture
def setup_teardown():
    yield

    directory = 'files/test/'
    for filename in os.listdir(directory):
        os.remove(directory + filename)


def test_repo_create():
    repo = JsonRepo('test')
    assert repo.env == 'test'
    assert repo.path == 'files/test/'


def test_repo_add():
    repo = JsonRepo('test')
    card = Card()
    repo.add(card)
    assert repo.cards == [card]
    assert isinstance(repo.cards[0].uid, uuid.UUID)


def test_repo_no_duplicate():
    repo = JsonRepo('test')
    card = Card()

    repo.add(card)
    with pytest.raises(Exception):
        repo.add(card)


def test_repo_save(setup_teardown):
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


def test_load_repo(setup_teardown):
    repo = JsonRepo('test')
    card = Card()
    card.text = 'hello world'
    card.title = 'test title'
    card2 = Card()
    card.assign_parent(card2)

    repo.add(card)

    assert isinstance(repo.cards[0].uid, uuid.UUID)
    print(repo.cards[0].uid.__class__)
    print(repo.cards[0].uid.__class__)

    repo.save()
    print(repo.cards[0].uid.__class__)

    new_repo = JsonRepo('test')
    new_repo.load()

    assert len(new_repo.cards) == len(repo.cards)
    print(repo.cards[0].uid.__class__)

    assert isinstance(repo.cards[0].uid, uuid.UUID)
    assert repo.cards[0] == new_repo.cards[0]


def test_repo_load_multi_card(setup_teardown):
    repo = JsonRepo('test')
    card = Card()
    card.text = 'hello world'
    card.title = 'test title'
    card2 = Card()
    card.assign_parent(card2)

    repo.add(card)
    repo.add(card2)

    repo.save()

    new_repo = JsonRepo('test')
    new_repo.load()

    assert len(new_repo.cards) == len(repo.cards)


def test_load_by_id(setup_teardown):
    repo = JsonRepo('test')
    card = Card()
    card.title = 'test title'
    id_to_fetch = str(card.uid)

    repo.add(card)
    repo.add(Card())
    repo.save()

    new_repo = JsonRepo('test')
    new_repo.load({'uid__eq': id_to_fetch})

    assert len(new_repo.cards) == 1
    assert new_repo.cards[0].title == 'test title'
