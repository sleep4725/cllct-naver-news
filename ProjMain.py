try:
    
    import os 
    import sys 
    import re 
    import requests
    import unicodedata    
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    from concurrent.futures import ThreadPoolExecutor
    import concurrent.futures as ConcurrentFutures
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import bs4
except ImportError as error:
    print(error)

#PROJ_ROOT_PATH :str = os.path.abspath(os.path.dirname(__file__))
#print(PROJ_ROOT_PATH)
#sys.path.append(PROJ_ROOT_PATH)

try:
    
    from engine.ChromeDriver import ChromeDriver
    from es.EsClient import EsClient
    from es.EsOption import EsOption
    from cllct.CllctOfNews import CllctOfNews
    from model.eco.ModelOfEco import ModelOfEco
    from model.pol.ModelOfPol import ModelOfPol
    from common.CommonURL import CommonURL
except ImportError as error:
    print(error)

"""
@author JunHyeon.Kim
@date 20221217토
"""
def bulk_indexing(action: list[dict]):
    '''Elasticsearch Bulk insert
    :param:
    :return:
    '''
    es_client:Elasticsearch = EsClient.get_es_client(deploy= "local")
    try:
        
        bulk(client= es_client, actions= action)
    except:
        print("bulk insert error")
        exit(1)
    
    es_client.close()

def get_media_body(news_body: bs4.element.Tag)\
    -> str:
    '''
    '''
    div_tag :bs4.element.Tag= news_body.select_one(
        "div#newsct_article.newsct_article._article_body" + 
        " > " +
        "div#dic_area.go_trans._article_content"
    )
    
    news_content= div_tag.text\
        .replace("\n", "")\
        .replace("\t", "")
    news_content_v: str = re.sub(' +', ' ', news_content)    
    return news_content_v

def get_media_title(news_title: bs4.element.Tag)\
    -> str:
    '''
    :param:
    :return:
    '''
    span_tag: bs4.element.Tag= news_title.select_one(
        "h2#title_area.media_end_head_headline" + 
        " > " + 
        "span"
    )

    return str(span_tag.text).strip()
    
def get_media_source(news_source: bs4.element.Tag)\
    -> str:
    '''
    :param news_source:
    :return:
    '''
    img_tag :bs4.element.Tag= news_source.select_one(
        "a.media_end_head_top_logo" + 
        " > " + 
        "img"
    )
    
    return str(img_tag.attrs["title"]).strip()

def get_news_detail_information(u: str, url_header: dict[str, str])\
    -> dict:
    '''
    :param
    :param:
    :return:
    '''
    element :dict = {"req_url": u["url"]}
    
    response = requests.get(u["url"], headers= url_header) 
    bs_obj = BeautifulSoup(response.text, "html.parser")
    
    newsct :bs4.element.Tag= bs_obj.select_one("div#ct.newsct")
    news_header :bs4.element.Tag= newsct.select_one("div.media_end_head.go_trans")
    news_source :bs4.element.Tag= news_header.select_one("div.media_end_head_top")
    news_title :bs4.element.Tag= news_header.select_one("div.media_end_head_title")
    news_body :bs4.element.Tag= newsct.select_one("div#contents.newsct_body")
    
    news_source_v :str= get_media_source(news_source= news_source) # 뉴스 출처
    news_title_v :str= get_media_title(news_title= news_title) # 뉴스 타이틀
    news_body_v :str= get_media_body(news_body=news_body)
    
    element["news-source"] = news_source_v    
    element["news-title"] = news_title_v
    element["news-body"] = news_body_v
    element["news-sid1_num"] = u["sid1"]
    element["news-sid1_hangl_cate"] = u["sid1_hangl_cate"]
    element["news-sid2_num"] = u["sid2"]
    element["news-sid2_hangl_cate"] = u["sid2_hangl_cate"]
    element["news-cllct_detail_time"] = u["detail_cllct_time"]
    
    #chrome_driver.quit()
     
    return element

## -----------------------------
# PROJ MAIN FUNCTION
## -----------------------------
if __name__ == "__main__":

    argument = sys.argv
    
    if len(argument) != 2: exit(1)
    
    common_url = CommonURL()
    news_category_obj = None 
    if argument[1] not in ["ModelOfEco", "ModelOfPol"]:
        print("ModelOfEco, ModelOfPol")
        exit(1)
    if argument[1] == "ModelOfEco": news_category_obj = ModelOfEco
    elif argument[1] == "ModelOfPol": news_category_obj = ModelOfPol
     
    o = CllctOfNews(news_category_object= news_category_obj) 
    es_client_obj = EsOption()
    
    sid2 :dict[str, int] = o._obj._sid2
    for k, v in sid2.items():
        for page in range(1, 2):
            url:list[dict] = o.get_url_list(
                sid2=v, 
                page=page, 
                sid2_hangl_cate=k)
            
            with ThreadPoolExecutor(5) as executor:
                results = [
                            executor.submit(
                                get_news_detail_information, 
                                u,common_url._headers 
                            ) for u in url
                        ]

                actions :list[dict] = []
                for result_element in ConcurrentFutures.as_completed(results):
                    element:dict = result_element.result()
                    actions_element = {
                        "_index": es_client_obj._news_index,
                        "_id": 
                            element["news-sid1_hangl_cate"] +
                            "_" +
                            element["news-sid2_hangl_cate"] +
                            "_" + 
                            element["news-source"] +
                            "_" +
                            element["news-title"]
                            ,    
                        "_source": element
                    }
                    actions.append(actions_element)
                
                bulk_indexing(action= actions)