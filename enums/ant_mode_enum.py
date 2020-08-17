from enum import Enum

class AntModeEnum(Enum):
    Searcher = 0    # 餌を探すアリ
    Returnee = 1    # 餌場から最短距離で戻るアリ
    Servant = 2     # フェロモンの誘引に従って進むアリ
