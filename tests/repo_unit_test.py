import os
import uuid
import json
import pytest
from concard.domain import Card
from concard.repo import JsonRepo


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

    os.remove(expected_file_name)


def test_load_repo():
    repo = JsonRepo('test')
    card = Card()
    card.edit_text('hello world')
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
    delete_file(card.uid)

    assert len(new_repo.cards) == len(repo.cards)
    print(repo.cards[0].uid.__class__)

    assert isinstance(repo.cards[0].uid, uuid.UUID)
    assert repo.cards[0] == new_repo.cards[0]


def test_repo_load_multi_card():
    repo = JsonRepo('test')
    card = Card()
    card.edit_text('hello world')
    card.title = 'test title'
    card2 = Card()
    card.assign_parent(card2)

    repo.add(card)
    repo.add(card2)

    repo.save()

    new_repo = JsonRepo('test')
    new_repo.load()

    assert len(new_repo.cards) == len(repo.cards)

    delete_file(card.uid)
    delete_file(card2.uid)


def delete_file(uid):
    filename = 'files/test/' + str(uid) + ".json"
    os.remove(filename)
