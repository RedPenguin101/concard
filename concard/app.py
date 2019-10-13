from concard.domain import Card
from concard.repo import JsonRepo


def run(env, crud_args) -> dict:
    action = crud_args['action']
    if action == 'create':
        return create_card_command(env, crud_args['card'])

    if action == 'read':
        return read_cards_command(env, crud_args.get('filters'))

    if action == 'update':
        return update_card_command(env, crud_args['card'])

    return {'message': 'Invalid action'}


def create_card_command(env, card_dict):
    repo = JsonRepo(env)
    card = Card.from_dict(card_dict)
    repo.add(card)
    repo.save()
    return {'message': 'Card created', 'card_uid': str(card.uid)}


def read_cards_command(env, filters=None):
    repo = JsonRepo(env)
    repo.load(filters)
    return {'cards': [card.to_dict() for card in repo.cards]}


def update_card_command(env, card_dict):
    updated_card = Card.from_dict(card_dict)

    repo = JsonRepo(env)
    repo.load({'uid__eq': str(updated_card.uid)})

    old_card = repo.cards[0]
    repo.cards = [updated_card]
    repo.save()

    return {
        'message': 'Card updated',
        'old_card': old_card.to_dict(),
        'new_card': updated_card.to_dict(),
    }
