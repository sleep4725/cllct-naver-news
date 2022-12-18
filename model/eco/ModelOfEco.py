'''
:경제 
@author JunHyeon.Kim
'''
class ModelOfEco:
    
    def __init__(self) -> None:
        self._sid1:int = 101
        self._sid1_hangl_cate:str = "경제"
        self._sid2 :dict[str, int]= {
            "금융": 259,
            "증권": 258,
            "산업/재개": 261,
            "중기/벤처": 771,
            "부동산": 260,
            "글로벌 경제": 262,
            "생활경제": 310
        }