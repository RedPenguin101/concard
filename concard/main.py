import PyInquirer as pi
from concard.app import run


def main():
    action = True

    while action != 'Exit app':
        all_cards = run('prod', {'action': 'read'})['cards']
        selected, action = get_selection_and_action(all_cards)

        while action not in ['Go back to main', 'Exit app']:
            action, selected = perform_action(action, selected, all_cards)


def perform_action(action, selected_card, all_cards):
    if action == 'View this card':
        print_card(selected_card, all_cards)
        action = ask_for_next_action()

    if action == 'Browse children':
        children = get_children_of_selected(selected_card, all_cards)

        if not children:
            print("No children")
            action = ask_for_next_action()
        else:
            selected_card, action = get_selection_and_action(children)

    if action == 'Go to parent card':
        parent = get_parent(selected_card, all_cards)

        if parent is None:
            print("This pearl has no parent")
        else:
            selected_card = parent

        action = 'View this card'

    if action == 'Create a new child':
        response = create_child(selected_card)
        print(response)
        action = 'Go back to main'

    if action == 'Edit this card':
        response = update(selected_card)
        print(response)
        action = 'Go back to main'

    if action == 'Delete this card':
        response = delete(selected_card)
        print(response)
        action = 'Go back to main'

    return action, selected_card


def ask_for_next_action():
    return pi.prompt(ACTION_Q)['action']


def get_parent(selected_card, all_cards):
    try:
        parent = selected_card['parent']
    except IndexError:
        return None

    for new_pearl in all_cards:
        if new_pearl['uid'] == parent:
            return new_pearl

    return None


def print_card(selected_card, all_cards):
    children = get_children_of_selected(selected_card, all_cards)
    print("\n")
    print(selected_card['title'].upper())
    print(selected_card['text'])
    if selected_card.get('text_exceeds_500'):
        print(f"!!WARNING: Text length is {len(selected_card['text'])}!!")
    print("--------")
    print("Children")
    print("--------")
    for child in children:
        title = child['title']
        print(f'> {title}')
    print()


def get_children_of_selected(selected_card, all_cards):
    children_of_selection = []

    uid = selected_card['uid']

    for card in all_cards:
        if ('parent' in card) and (uid == card['parent']):
            children_of_selection.append(card)

    return children_of_selection


def create_child(selected_pearl):
    inputs_for_create = pi.prompt(CREATE_QS)
    response = run('prod', {
        'action': 'create',
        'card': {
            'title': inputs_for_create['title'],
            'text': inputs_for_create['text'],
            'parent': selected_pearl['uid']
        }
    })
    return response


def update(card):
    inputs_for_update = pi.prompt(CREATE_QS)

    card = {
            'uid': card['uid'],
    }

    if inputs_for_update['title'] != "":
        card['title'] = inputs_for_update['title']

    if inputs_for_update['text'] != "":
        card['text'] = inputs_for_update['text']

    response = run('prod', {
        'action': 'update',
        'card': card
    })
    return response


def delete(card):
    return run('prod', {
        'action': 'delete',
        'card': {'uid': card['uid']}
    })


def get_selection_and_action(card_list):
    list_questions = make_menu_question_list(card_list)

    menu_selection = pi.prompt(list_questions)

    selected_card = card_list[
        int(menu_selection['pearl_selection'][0])
    ]
    action = menu_selection['action']

    return selected_card, action


def make_menu_question_list(card_list: dict) -> list:
    questions = [
        {
            'type': 'list',
            'name': 'pearl_selection',
            'message': 'select which pearl you want',
            'choices': list_choices(card_list)
        },
        ACTION_Q
    ]

    return questions


def list_choices(full_list: dict) -> list:
    display_list = []

    for (index, card) in enumerate(full_list):
        display_list.append(f"{index}. {card['title']}")

    return display_list


CREATE_QS = [
    {
        'type': 'input',
        'name': 'title',
        'message': 'input the card title'
    },
    {
        'type': 'input',
        'name': 'text',
        'message': 'input the text of the card'
    },
]

ACTION_Q = {
    'type': 'list',
    'name': 'action',
    'message': 'What do you want to do?',
    'choices': [
        'View this card',
        'Edit this card',
        'Browse children',
        'Go to parent card',
        'Delete this card',
        'Create a new child',
        'Go back to main',
        'Exit app'
    ]
}


if __name__ == '__main__':
    main()
