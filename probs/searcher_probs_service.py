from probs.base_probs_service import BaseProbsService

class SearcherProbsService(BaseProbsService):
    def calc(self):
        if not self.ant.is_searcher():
            return None

        return [0.5, 0.5]