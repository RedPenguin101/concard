import os
import pytest
from concard.app import run


def create_card(**kwargs) -> str:
    card = {}
    for key, value in kwargs.items():
        card[key] = value
    args = {'action': 'create', 'card': card}
    response = run('test', args)
    return response['card_uid']


def read_repo(filters=None) -> list:
    args = {'action': 'read'}
    if filters:
        args['filters'] = filters
    return run('test', args)


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
    assert response['new_card']['title'] == 'updated title'
    assert response['new_card']['text'] == 'updated text'


def test_update_card_doesnt_delete_existing_params(setup_teardown):
    uid = create_card(title='test title', text='test text')

    args = {
        'action': 'update',
        'card': {'uid': str(uid), 'text': 'updated text'}
    }

    run('test', args)

    card = read_repo()['cards'][0]

    assert card['title'] == 'test title'
    assert card['text'] == 'updated text'


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
    uid = '821c9390-845f-4d95-91af-10b654bc6ab9'
    env = 'test'
    args = {
        'action': 'delete',
        'card': {
            'uid': uid
        }
    }

    response = run(env, args)

    expected = f'No card with uid "{uid}" was found in the repo'
    assert response['message'] == expected


def test_create_with_parent(setup_teardown):
    uid = create_card(title='test title', text='test text')
    second_uid = create_card(parent=str(uid))
    cards = read_repo({'uid__eq': str(second_uid)})['cards']
    assert cards[0]['parent'] == str(uid)


def test_cant_delete_card_with_children(setup_teardown):
    uid = create_card()
    create_card(parent=str(uid))

    response = run('test', {'action': 'delete', 'card': {'uid': str(uid)}})
    print(response)
    expected = 'This card has existing children cards, cannot delete'
    assert response['message'] == expected


def test_card_has_length_attr(setup_teardown):
    create_card(text='hello world')
    response = read_repo()
    print(response)
    assert not response['cards'][0]['text_exceeds_500']


def test_card_returns_exceed_500_check(setup_teardown):
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
    create_card(text=long_string)

    response = read_repo()
    print(response)
    assert response['cards'][0]['text_exceeds_500']
