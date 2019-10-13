import json
import os
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
        self.cards_to_delete: List[str] = []

    def save(self):
        for card in self.cards_in_memory:
            self.save_card(card)

        self.cards_in_memory = []

        for uid in self.cards_to_delete:
            if self.card_has_children(uid):
                raise ValueError(f"Card with uid {uid} has existing children, can't delete")

            filename = self.path + str(uid) + ".json"
            print('deleting file ' + filename)
            os.remove(filename)

        self.cards_to_delete = []

    def card_has_children(self, uid: str) -> bool:
        pass

    def save_card(self, card: Card):
        filename = self.path + str(card.uid) + ".json"
        print('saving card ' + str(card))
        with open(filename, 'w') as file:
            file.write(json.dumps(card.to_dict()))

    def add(self, card: Card):
        uids = [c.uid for c in self.cards_in_memory]

        if card.uid in uids:
            raise Exception("card with that UID is already in the repository")

        self.cards_in_memory.append(card)

    def load(self, filters=None):
        # TODO: Make this functional, return list
        filenames = os.listdir(self.path)

        if not filters:
            for filename in filenames:
                if filename.endswith('.json'):
                    self.cards_in_memory.append(load_card(self.path + filename))

        elif 'uid__eq' in filters:
            target = filters['uid__eq'] + '.json'
            if target in filenames:
                card = load_card(self.path + target)
                self.cards_in_memory.append(card)

    def delete(self, uid: str):
        self.cards_to_delete.append(uid)


def load_card(filename):
    with open(filename, 'r') as file:
        return Card.from_dict(json.loads(file.read()))
