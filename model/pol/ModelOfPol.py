'''
:정치
@author JunHyeon.Kim
'''
class ModelOfPol:
    
    def __init__(self) -> None:
        self._sid1:int = 100
        self._sid1_hangl_cate:str = "정치"
        self._sid2 :dict[str, int]= {
            "대통령실": 264,
            "국회/정당": 265,
            "북한": 268,
            "행정": 266,
            "국방/외교": 267
        }