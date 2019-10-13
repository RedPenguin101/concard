import uuid


class Card:
    def __init__(self):
        self.uid = uuid.uuid4()

    def assign_parent(self, parent_card):
        self.parent = parent_card.uid

    def to_dict(self) -> dict:
        card_dict = self.__dict__.copy()

        card_dict['uid'] = str(card_dict['uid'])

        if 'parent' in card_dict:
            card_dict['parent'] = str(card_dict['parent'])

        return card_dict

    @classmethod
    def from_dict(cls, card_dict: dict):
        card = Card()

        for key in card_dict.keys():
            card.__dict__[key] = card_dict[key]

        if 'uid' in card_dict:
            card.uid = uuid.UUID(card.uid)

        if 'parent' in card_dict:
            card.parent = uuid.UUID(card.parent)

        return card

    def update_from_dict(self, card_dict):
        if str(self.uid) != card_dict['uid']:
            y = card_dict['uid']
            x = f'original uid {self.uid} does not match update uid {y}'
            raise Exception(x)

        del card_dict['uid']

        for key, value in card_dict.items():
            self.__dict__[key] = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        ret_val = 'Card{'

        for (key, val) in self.__dict__.items():
            ret_val += str(key) + ": " + str(val) + ", "

        ret_val += '}'
        return ret_val
