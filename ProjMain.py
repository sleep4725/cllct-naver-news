try:
    
    import re 
    import unicodedata    
    from elasticsearch import Elasticsearch
    from concurrent.futures import ThreadPoolExecutor
    import concurrent.futures as ConcurrentFutures
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import bs4
except ImportError as error:
    print(error)

try:
    from engine.ChromeDriver import ChromeDriver
    from es.EsClient import EsClient
    from cllct.CllctOfNews import CllctOfNews
    from model.eco.ModelOfEco import ModelOfEco
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
    es_clien:Elasticsearch = EsClient.get_es_client(deploy= "local")
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
    
    news_content = str(unicodedata.normalize("NFKD",div_tag.text))\
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

def get_news_detail_information(u: str, chrome_driver: WebDriver)\
    -> dict:
    '''
    :param
    :param:
    :return:
    '''
    element :dict = {"req_url": u}
    chrome_driver.get(u)
    chrome_driver.implicitly_wait(3)
    bs_obj = BeautifulSoup(chrome_driver.page_source, "html.parser")
    
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
    
    chrome_driver.quit()
     
    return element

if __name__ == "__main__":

    o = CllctOfNews(news_category_object= ModelOfEco) 
    chrome_driver_object = ChromeDriver() 
    driver :WebDriver = chrome_driver_object.get_chrome_driver()
    
    sid2 :dict[str, int] = o._obj._sid2
    for k, v in sid2.items():
        for page in range(1, 3):
            url:list[str] = o.get_url_list(sid2=v, page=page)
            print(url)
            
            with ThreadPoolExecutor(5) as executor:
                results = [
                            executor.submit(
                                get_news_detail_information, 
                                u, chrome_driver_object.get_chrome_driver() 
                            ) for u in url
                        ]
                
                for _ in ConcurrentFutures.as_completed(results):
                    print(_.result())