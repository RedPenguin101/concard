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
    assert repo.cards_in_memory == [card]
    assert isinstance(repo.cards_in_memory[0].uid, uuid.UUID)


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
    repo.save()

    new_repo = JsonRepo('test')
    new_repo.load()

    assert len(new_repo.cards_in_memory) == 1

    assert new_repo.cards_in_memory[0] == card


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

    assert len(new_repo.cards_in_memory) == 2


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

    assert len(new_repo.cards_in_memory) == 1
    assert new_repo.cards_in_memory[0].title == 'test title'


def create_and_save_card(title, text=None):
    repo = JsonRepo('test')
    card = Card()
    card.title = title
    if text:
        card.text = text

    uid = str(card.uid)

    repo.add(card)
    repo.save()

    print('created and saved card with uid ' + uid)

    return uid


def test_memory_empties_on_save(setup_teardown):
    repo = JsonRepo('test')
    card = Card()
    repo.add(card)
    repo.save()
    assert len(repo.cards_in_memory) == 0


def test_delete_mem_empties_on_save(setup_teardown):
    uid = create_and_save_card('test title')
    repo = JsonRepo('test')
    repo.delete(uid)
    repo.save()
    assert len(repo.cards_to_delete) == 0


def test_delete_deletes(setup_teardown):
    uid = create_and_save_card('test title')

    repo = JsonRepo('test')
    repo.delete(uid)
    repo.save()

    test_repo = JsonRepo('test')
    test_repo.load()

    assert len(test_repo.cards_in_memory) == 0


def test_delete_non_existant_card_fails(setup_teardown):
    uid = str(uuid.uuid4())

    repo = JsonRepo('test')
    repo.delete(uid)

    with pytest.raises(FileNotFoundError):
        repo.save()


@pytest.mark.skip
def test_cant_delete_card_with_children(setup_teardown):
    card1 = Card()
    card2 = Card()

    card2.assign_parent(card1)

    repo = JsonRepo('test')
    repo.add(card1)
    repo.add(card2)
    repo.save()

    uid = card1.uid
    repo.delete(uid)

    with pytest.raises(Exception):
        repo.save()
