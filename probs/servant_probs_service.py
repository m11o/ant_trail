from probs.base_probs_service import BaseProbsService

class ServantProbsService(BaseProbsService):
    MODEL_PARAMS = 5.0

    def calc(self):
        if not self.ant.is_servant():
            return None

        pheromones = {
            'left': self.__left_pheromon_quantity(),
            'right': self.__right_pheromon_quantity()
        }

        return self.__calc_prob(pheromones)

    def __calc_prob(self, pheromones):
        left_prob = (self.MODEL_PARAMS + pheromones['left'])**2 / (self.MODEL_PARAMS + pheromones['left'])**2 + (self.MODEL_PARAMS + pheromones['right'])**2
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
