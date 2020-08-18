class CalcPheromonesProbService:
    MODEL_PARAMS = 5.0
    MODEL_EXPONENT = 2.0

    ONLY_LEFT_PROB = [1.0, 0.0]
    ONLY_RIGHT_PROB = [0.0, 1.0]

    def __init__(self, ant, field):
        self.ant = ant
        self.field = field

    def calc(self):
        pheromones = {
            'left': self.__left_pheromon_quantity(),
            'right': self.__right_pheromon_quantity()
        }

        return self.__calc_prob(pheromones)

    def __calc_prob(self, pheromones):
        if pheromones['left'] == 0:
            return self.ONLY_RIGHT_PROB
        elif pheromones['right'] == 0:
            return self.ONLY_LEFT_PROB

        left_prob = (self.MODEL_PARAMS + pheromones['left'])**self.MODEL_EXPONENT / ((self.MODEL_PARAMS + pheromones['left'])**self.MODEL_EXPONENT + (self.MODEL_PARAMS + pheromones['right'])**self.MODEL_EXPONENT)
        right_prob = 1 - left_prob

        return [left_prob, right_prob]

    def __left_pheromon_quantity(self):
        position = self.ant.next_left_position()
        if not bool(position):
            return 0

        return self.field.pheromone_quantity(position[0], position[1])

    def __right_pheromon_quantity(self):
        position = self.ant.next_right_position()
        if not bool(position):
            return 0

        return self.field.pheromone_quantity(position[0], position[1])
