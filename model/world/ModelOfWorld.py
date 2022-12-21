'''
:세계
@author JunHyeon.Kim
@date 20221221
'''
class ModelOfWorld:
    
    def __init__(self) -> None:
        self._sid1:int = 104
        self._sid1_hangl_cate:str = "세계"
        self._sid2 :dict[str, int]= {
            "아시아/호주": 231,
            "미국/중남미": 232,
            "유럽": 233,
            "중동/아프리카": 234
        }