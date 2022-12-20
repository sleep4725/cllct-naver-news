'''
:생활/문화
@author JunHyeon.Kim
@date 20221220
'''
class ModelOfCul:
    
    def __init__(self) -> None:
        self._sid1:int = 103
        self._sid1_hangl_cate:str = "생활_문화"
        self._sid2 :dict[str, int]= {
            "건강정보": 241,
            "자동차/시승기": 239,
            "도로/교통": 240,
            "여행/레저": 237,
            "음식/맛집": 238,
            "패션/뷰티": 376,
            "공연/전시": 242,
            "책": 243,
            "종교": 244,
            "날씨": 248
        }