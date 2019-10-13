import uuid


class Card:
    def __init__(self):
        self.uid = uuid.uuid4()

    def assign_parent(self, parent_card):
        self.parent = parent_card.uid

    def to_dict(self):
        dic = self.__dict__.copy()

        dic['uid'] = str(dic['uid'])

        if 'parent' in dic:
            dic['parent'] = str(dic['parent'])

        return dic

    @classmethod
    def from_dict(cls, dic):
        card = Card()

        for key in dic.keys():
            card.__dict__[key] = dic[key]

        if 'uid' in dic:
            card.uid = uuid.UUID(card.uid)

        if 'parent' in dic:
            card.parent = uuid.UUID(card.parent)

        return card

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
