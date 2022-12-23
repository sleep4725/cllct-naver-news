from dataclasses import dataclass

"""
@author JunHyeon.Kim
@date 20221223
"""
@dataclass(init=True, frozen=False)
class Template:

    news_url: str = "" 
    news_source: str = "" # 뉴스 신문사
    news_title: str = "" # 뉴스 헤드라인
    news_body: str = "" # 뉴스 내용
    news_sid1_num: int = 0 # 뉴스 카테고리-1
    news_sid1_hangl_cate: str = "" # 뉴스 카테고리-1 한글 명
    news_sid2_num: int = 0 # 뉴스 카테고리-2
    news_sid2_hangl_cate: str = "" # 뉴스 카테고리-2 한글 명
    news_cllct_detail_time: str = ""