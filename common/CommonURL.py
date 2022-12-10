from urllib.parse import urlencode
'''
@author JunHyeon.Kim
@date 20221208
'''
class CommonURL:
    
    def __init__(self) -> None:
        self._base_url: str = "https://news.naver.com/main/list.naver"
        self._base_param: str = urlencode({
            "mode": "LS2D"
            ,"mid": "shm"
        })
        
        self._headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }