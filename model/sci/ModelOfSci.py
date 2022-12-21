'''
:IT/과학
@author JunHyeon.Kim
@date 20221221
'''
class ModelOfSci:
    
    def __init__(self) -> None:
        self._sid1:int = 105
        self._sid1_hangl_cate:str = "IT_과학"
        self._sid2 :dict[str, int]= {
            "모바일": 731,
            "인터넷/SNS": 226,
            "통신/뉴미디어": 227,
            "IT 일반": 230,
            "보안/해킹": 732,
            "컴퓨터": 283,
            "게임/리뷰": 229
        }