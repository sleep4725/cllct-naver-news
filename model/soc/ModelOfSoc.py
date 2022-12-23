'''
:사회
@author JunHyeon.Kim
'''
class ModelOfSoc:
    
    def __init__(self) -> None:
        self._sid1:int = 102
        self._sid1_hangl_cate:str = "사회"
        self._sid2 :dict[str, int]= {
            "사건사고": 249,
            "교육": 250,
            "노동": 251,
            "언론": 254,
            "환경": 252,
            "인권/복지": "59b",
            "식품/의료": 255,
            "지역": 256
        }