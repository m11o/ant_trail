from probs.base_probs_service import BaseProbsService
from probs.concerns.calc_pheromones_prob_service import CalcPheromonesProbService


class ServantProbsService(BaseProbsService):
    MODEL_PARAMS = 5.0
    MODEL_EXPONENT = 2.0

    def calc(self):
        if not self.ant.is_servant():
            return None

        calculator = CalcPheromonesProbService(self.ant, self.field)
        probs = calculator.calc()

        if calculator.ONLY_LEFT_PROB == probs or calculator.ONLY_RIGHT_PROB == probs:
            return probs

        # 餌場に向かう場合には、フェロモン濃度が低い方向に向かっていくため
        left = 1 - probs[0]
        right = 1 - probs[1]

        return [left, right]
