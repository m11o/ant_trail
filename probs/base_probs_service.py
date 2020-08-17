class BaseProbsService:
    def __init__(self, ant, field):
        self.ant = ant
        self.field = field

    @classmethod
    def get_instance(cls, ant, field):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(ant, field)
        else:
            cls._instance.ant = ant
            cls._instance.field = field

        return cls._instance