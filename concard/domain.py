import uuid

class Card:
    def __init__(self):
        self.uid = uuid.uuid4()

    def assign_parent(self, parent_card):
        self.parent = parent_card.uid

    def edit_text(self, text: str):
        self.text = text

    def to_dict(self):
        dic = self.__dict__
        dic['uid'] = str(dic['uid'])
        if 'parent' in dic:
            dic['parent'] = str(dic['parent'])

        return dic