import abc
import json

class Repo(abc.ABC):
    def __init__(self, env: str):
        pass

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def add(self, card):
        pass

    @abc.abstractmethod
    def load(self):
        pass

class JsonRepo(Repo):
    paths = {
        'test': 'files/test/',
        'prod': 'files/',
    }

    def __init__(self, env: str):
        self.env = env
        self.path = JsonRepo.paths[env]
        self.cards = []

    def save(self):
        for card in self.cards:
            self.save_card(card)

    def save_card(self, card):
        filename = self.path + str(card.uid) + ".json"
        with open(filename, 'w') as file:
            file.write(json.dumps(card.to_dict()))

    def add(self, card):
        uids = [c.uid for c in self.cards]
        if card.uid in uids:
            raise Exception("card with that UID is already in the repository")

        self.cards.append(card)

    def load(self):
        pass