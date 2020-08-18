from probs.base_probs_service import BaseProbsService
from probs.concerns.calc_pheromones_prob_service import CalcPheromonesProbService

class ReturneeProbsService(BaseProbsService):
    GREATER_PROP = 0.7
    LESS_PROP = 0.3
    EQUAL_PROP = 0.5

    def calc(self):
        if not self.ant.is_returnee():
            return None

        if self.ant.is_on_pheromone(self.field) and not self.ant.was_searcher():
            return CalcPheromonesProbService(self.ant, self.field).calc()

        weights = []
        next_positions = self.ant.next_positions()
        for position in next_positions:
            difference = self.__calc_step_difference(position)
            weight = 1.0 - self.__calc_step_weight() * difference
            weights.append(weight)

        if weights[0] > weights[1]:
            return [self.GREATER_PROP, self.LESS_PROP]
        elif weights[0] < weights[1]:
            return [self.LESS_PROP, self.GREATER_PROP]
        elif weights[0] == weights[1]:
            return [self.EQUAL_PROP, self.EQUAL_PROP]

    def __calc_step_weight(self):
        return 1.0 / max(self.field.X, self.field.Y)

    def __calc_step_difference(self, position):
        diff_x = abs(position[0] - self.field.nest_field.nest_position[0])
        diff_y = abs(position[1] - self.field.nest_field.nest_position[1])

        return max([diff_x, diff_y])
