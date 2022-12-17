'''
:경제 
@author JunHyeon.Kim
'''
class ModelOfEco:
    
    def __init__(self) -> None:
        self._sid1:int = 101
        self._sid2 :dict[str, int]= {
            "금융": 259,
            "증권": 258,
            "산업/재개": 261
        }