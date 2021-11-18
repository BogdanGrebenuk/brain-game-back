class SetOfGames:

    def __init__(self, amount_of_stages):
        self._amount_of_stages = amount_of_stages

    @classmethod
    def default(cls):
        return cls(amount_of_stages=3)

    def get_amount_of_stages(self):
        return self._amount_of_stages
