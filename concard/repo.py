import json
import os
import uuid
from typing import List

from concard.domain import Card


class JsonRepo():
    paths = {
        'test': 'files/test/',
        'prod': 'files/',
    }

    def __init__(self, env: str):
        self.env = env
        self.path = JsonRepo.paths[env]
        self.cards_in_memory: List[Card] = []
        self.cards_to_delete: List[uuid.UUID] = []

    def save(self):
        for card in self.cards_in_memory:
            self.save_card(card)

        self.cards_in_memory = []

        for uid in self.cards_to_delete:
            if self.card_has_children(uid):
                raise ValueError(f"Card with uid {uid} has existing children, can't delete")

            filename = self.path + str(uid) + ".json"
            os.remove(filename)

        self.cards_to_delete = []

    def card_has_children(self, uid: uuid.UUID) -> bool:
        all_cards: List[Card] = self.get_cards_from_repo()

        for card in all_cards:
            if hasattr(card, 'parent') and card.parent == uid:
                return True

        return False

    def save_card(self, card: Card):
        filename = self.path + str(card.uid) + ".json"
        with open(filename, 'w') as file:
            file.write(json.dumps(card.to_dict()))

    def add(self, card: Card):
        uids = [c.uid for c in self.cards_in_memory]

        if card.uid in uids:
            raise Exception("card with that UID is already in the repository")

        self.cards_in_memory.append(card)

    def load(self, filters=None):
        self.cards_in_memory = self.get_cards_from_repo(filters)

    def get_cards_from_repo(self, filters=None) -> List[Card]:
        filenames = os.listdir(self.path)
        memory = []

        if not filters:
            for filename in filenames:
                if filename.endswith('.json'):
                    memory.append(load_card(self.path + filename))

        elif 'uid__eq' in filters:
            target = filters['uid__eq'] + '.json'
            if target in filenames:
                card = load_card(self.path + target)
                memory.append(card)

        return memory

    def delete(self, uid_str: str):
        try:
            uid = uuid.UUID(uid_str)
        except Exception:
            raise ValueError(f'value passed {uid_str} is not a valid UUID')
        self.cards_to_delete.append(uid)


def load_card(filename):
    with open(filename, 'r') as file:
        return Card.from_dict(json.loads(file.read()))
