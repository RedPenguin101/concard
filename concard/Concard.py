from concard.repo import JsonRepo


class Concard:
    def __init__(self, env):
        self.env = env

    def create_card_command(self, card):
        repo = JsonRepo(self.env)
        repo.add(card)
        repo.save()
        return card.uid

    def read_cards_command(self):
        pass

    def update_card_command(self):
        pass

    def delete_card_command(self):
        pass
