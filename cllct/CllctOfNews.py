import os
import sys 
PROJ_ROOT_DIR : str = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_DIR)

try:
    
    import requests
    from bs4 import BeautifulSoup
    import bs4
except ImportError as err:
    print(err)
    
try:
    
    from common.CommonURL import CommonURL
    from util.TimeUtil import TimeUtil
    from model.eco.ModelOfEco import ModelOfEco
except ImportError as err:
    print(err)
    
'''
네이버 뉴스
-------------------------
@author JunHyeon.Kim 
@date 20221208
'''
class CllctOfNews(CommonURL):
    
    def __init__(self, news_category_object: object) -> None:
        CommonURL.__init__(self)
        self._obj: news_category_object = news_category_object()
        self._cllct_time: str = TimeUtil.get_cllct_time()
             
    def get_url_list(self, sid2: int, page: int)\
        -> list[str]:
        '''
        :param sid2:
        :param page:
        :return:
        '''
        url_list: list[str] = []
        print(self._obj._sid1)
        req_url: str = \
                        f"{self._base_url}" +\
                        f"?" +\
                        f"{self._base_param}" +\
                        f"&sid1={self._obj._sid1}" +\
                        f"&sid2={sid2}" +\
                        f"&date={self._cllct_time}" +\
                        f"&page={page}"

        print(f"req_url: {req_url}")
        
        response :requests.models.Response = requests.get(req_url, headers= self._headers)
        if response.status_code == 200:
            bs_object :bs4.element.Tag = BeautifulSoup(response.text, "html.parser")                    
            ul_tag :bs4.element.Tag =  bs_object.select_one("ul.type06_headline")
            li_tags_list :bs4.element.ResultSet = ul_tag.select("li")
            
            for li_tag in li_tags_list:
                li_tag :bs4.element.Tag = li_tag
                a_tag :bs4.element.Tag = li_tag.select_one("dl > dt > a")
                href_url :str = a_tag.attrs["href"]
                url_list.append(href_url)
            
            return url_list
        
        else:
            ''''''
            return []

          
                
                