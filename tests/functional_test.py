import os
import pytest
from concard.app import run


@pytest.fixture
def setup_teardown():
    yield

    directory = 'files/test/'
    for filename in os.listdir(directory):
        os.remove(directory + filename)


def test_create(setup_teardown):
    env = 'test'
    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)

    assert response['message'] == 'Card created'
    assert 'card_uid' in response


def test_create_and_retrieve_one_card(setup_teardown):
    env = 'test'
    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)
    expected_uid = response['card_uid']

    args = {
        'action': 'read',
    }

    read_response = run(env, args)

    assert 'cards' in read_response
    assert read_response['cards'][0]['title'] == 'test title'
    assert read_response['cards'][0]['text'] == 'test text'
    assert read_response['cards'][0]['uid'] == expected_uid


def test_retrieve_multi_card(setup_teardown):
    env = 'test'

    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)
    first_uid = response['card_uid']

    args['card']['title'] = '2nd test'
    args['card']['text'] = '2nd test'
    response = run(env, args)
    second_uid = response['card_uid']

    args = {
        'action': 'read',
    }

    read_response = run(env, args)

    assert len(read_response['cards']) == 2
    uids = [c['uid'] for c in read_response['cards']]
    assert first_uid in uids
    assert second_uid in uids


def test_retrieve_by_uid(setup_teardown):
    env = 'test'
    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)
    target_uid = response['card_uid']

    args = {
        'action': 'create',
        'card': {'title': 'not this one'}
    }

    run(env, args)

    args = {
        'action': 'read',
        'filters': {
            'uid__eq': str(target_uid)
        }
    }

    read_response = run(env, args)

    assert len(read_response['cards']) == 1


def test_edit_card(setup_teardown):
    env = 'test'
    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)
    target_uid = response['card_uid']
    print(target_uid)

    args = {
        'action': 'update',
        'card': {
            'uid': str(target_uid),
            'title': 'updated title',
            'text': 'updated text'
        }
    }

    response = run(env, args)

    assert response['message'] == 'Card updated'
    assert response['old_card']['title'] == 'test title'
    assert response['old_card']['text'] == 'test text'
    assert response['new_card']['title'] == 'updated title'
    assert response['new_card']['text'] == 'updated text'


def test_delete(setup_teardown):
    env = 'test'
    args = {
        'action': 'create',
        'card': {'title': 'test title', 'text': 'test text'}
    }

    response = run(env, args)
    target_uid = response['card_uid']
    print(target_uid)

    args = {
        'action': 'delete',
        'card': {
            'uid': str(target_uid),
        }
    }

    response = run(env, args)

    assert response['message'] == 'Card deleted'
    assert response['uid'] == str(target_uid)

    assert len(run(env, {'action': "read"})['cards']) == 0


def test_delete_of_no_card(setup_teardown):
    env = 'test'
    args = {
        'action': 'delete',
        'card': {
            'uid': 'I will fail'
        }
    }

    response = run(env, args)

    assert response['message'] == 'No card with uid "I will fail" was found in the repo'
