try:
    
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import Bulk    
    from concurrent.futures import ThreadPoolExecutor
except ImportError as error:
    print(error)

try:
    from es.EsClient import EsClient
    from cllct.CllctOfNews import CllctOfNews
    from model.eco.ModelOfEco import ModelOfEco
except ImportError as error:
    print(error)

""""""
def bulk_indexing(action: list[dict]):
    '''Elasticsearch Bulk insert
    :param:
    :return:
    '''
    es_clien:Elasticsearch = EsClient.get_es_client(deploy= "local")
    es_client.close()
    
def get_news_detail_information(u: str):
    '''
    :param:
    :return:
    '''
    print(u)

if __name__ == "__main__":

    o = CllctOfNews(news_category_object= ModelOfEco) 
    sid2 :dict[str, int] = o._obj._sid2
    for k, v in sid2.items():
        for page in range(1, 11):
            url:list[str] = o.get_url_list(sid2=v, page=page)
        
            with ThreadPoolExecutor() as executor:
                results = [executor.submit(get_news_detail_information, u) for u in url]  