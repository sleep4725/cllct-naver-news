import mecab

'''
@author JunHyeon.Kim
@date 20221224
'''
class WordExtraction:
    
    @classmethod 
    def sample(cls, m_obj: mecab.MeCab, text: str):
        '''
        :param m_obj:
        :param text:
        :return:
        '''
        m_obj.pos(text)
    
    @classmethod 
    def get_nng_from_xpn(cls, index: int, response: list[tuple]):
        '''
        '''
        XPN :list[list]= [["XPN", "NNG"], ["XPN", "XR"]]

        for x in XPN:
            ''''''
            length_v :int= len(x)
            back_position :int= index + length_v 
            if back_position > len(response): pass
            [e for e in response[index: index+length_v]]
     
     
    @classmethod
    def get_nng_add_nng(cls, index: int, response: list[tuple])\
            -> bool:
        '''
        파생명사] 명사(NNG)-접미사(XSN/SN)
        :param response:
        :return:
        '''
        jump :int= index + 1
        result_jump :int= 0
        while True:
            if jump > len(response) -1: break
            else:
                if response[jump][1] == "NNG":
                    result_jump += 1
                    jump += 1
                else:
                    break 
    
    @classmethod 
    def get_compound_num_xpn(cls, index: int, response: list[tuple]):
        '''
        (XPN)+NNG+(XSN) :  비과학적(비/XPN+과학/NNG+적/XSN),   신제품(신/XPN+제품/NNG), 책들(책/NNG+들/XSN )
        (XPN)+XR+(XSN) :  불확실성(불/XPN+확실/XR+성/XS), 저돌적(저돌/XR+적/XSN), 복잡성(복잡/XR+성/XSN)
        (XPN)+NNG+NNG+(XSN) : 비영리단체들(비/XPN+영리/NNG+단체/NNG+들/XSN), 초국적기업(초/XPN+국적/NNG+기업/NNG),  
                                    택시기사들(택시/NNG+기사/NNG+들/XSN)
        (XPN)+NNG+NNB+(XSN) : 무의식간(무/XPN+의식/NNG+간/NNB),  고전주의자들(고전주의/NNG+자/NNB+들/XSN),  
                                    좌우측(좌우/NNG+측/NNB)
        (XPN)+NNG+NNG+NNB+(XSN) : 비영리단체간(비/XPN+영리/NNG+단체/NNG+간/NNB), 다음주중(다음/NNG+주/NNG+중/NNB)
        (XPN)+NR+NNB+(XSN) : 제일차간(제/XPN+일/NR+차/NNB), 사년생(사/NR+년/NNB+생/XSN), 백일(백/NR+일/NNB)
        NR+NNB+NNG : 일년동안(일/NR+년/NNB+동안/NNG)
        (XPN)+SN+NNB+NNG+(XSN) : 제2차대전(제/XPN+2/SN+차/NNB+대전/NNG), 5년임기제(5/SN+년/NNB+임기/NNG+제/XSN)
        (XPN)+SN+NNB+(XSN)  : 제1차적(제/XPN+1/SN+차/NNB+적/XSN), 제1권(제/XPN+1/SN+권/NNB), 5시경(5/SN+시/NNB+경/XSN)
        :param index:
        :param response:
        :return: 
        '''
        NNG_TAG_LIST :list[str]= ["XPN", "XPN NNG"]
        XR_TAG_LIST :list[str]= ["XPN"]
        NNB_TAG_LIST :list[str]= ["XPN NNG"]
        
        mov_index :int= index+1
        compound_char :str= "XPN"
        
        if response[mov_index][1] == "NNG" and compound_char in NNG_TAG_LIST:
            compound_char = compound_char + f" {response[mov_index][1]}" 
            mov_index += 1
        elif response[mov_index][1] == "XR" and compound_char in XR_TAG_LIST:
            compound_char = compound_char + f" {response[mov_index][1]}" 
            mov_index += 1 
        
    
    @classmethod
    def ex_compound_word(cls, m_obj: mecab.MeCab, text: str):
        '''
        :param m_obj:
        :param text:
        :return
        '''
        result_compound_word: list[str] = list()
        
        response :list[tuple]= m_obj.pos(text)
        
        lst_index :int= len(response)
        mov_index :int= 0
        
        while True:
            if mov_index == lst_index: break 
            print (mov_index, response[mov_index])
            
            if response[mov_index][1] == "NNG":
                is_ok :bool= WordExtraction.get_nng_add_nng(index=mov_index, response=response)
            elif response[mov_index][1] == "XPN":
                ''' XPN : 체언접두사
                '''
                
            else:
                mov_index += 1
        
        compound_word_list :list[str]= list(set(result_compound_word))
        print(compound_word_list)

class HangleObject:
    
    @classmethod 
    def get_hangle_client(cls)\
            ->mecab.MeCab:
        '''
        :param:
        :return:
        '''
        m_obj = mecab.MeCab()
        return m_obj
        
if __name__ == "__main__":
    o = HangleObject.get_hangle_client()
    t = '''[서울=뉴시스]윤정민 기자 = 지난 상반기에 법원 허가가 필요한 '통신사실확인자료' 제공 건수와 '통신제한조치' 협조 건수는 지난해 같은 기간에 비해 늘었지만 검·경찰, 국정원 등 수사기관에 제공된 '통신자료' 건수는 줄어든 것으로 나타났다.

23일 과학기술정보통신부는 78개 전기통신사업자(기간통신 50개사, 부가통신 28개사)가 제출한 '22년 상반기 통신자료 및 통신사실확인자료 제공, 통신제한조치 협조 현황'을 집계해 발표했다.

'통신자료'는 이용자 성명, 주민등록번호, 주소, 가입 및 해지일자, 전화번호, 아이디(ID) 등 통신서비스 이용자의 기본 인적사항이다. '통신사실확인자료'는 통화 내용이 아닌 상대방 전화번호, 통화 일시 및 통화시간 등의 통화사실과, 인터넷 로그기록·접속지 자료(IP Address) 및 발신기지국 위치추적자료 등이다.

이용자 인적사항인 통신자료는 수사기관 등이 보이스피싱이나 납치 피해자 확인 등 신속한 범죄 수사를 위해 전기통신사업법에 따라 공문으로 요청해 전기통신사업자로부터 취득되는 자료다.

통신자료가 지난 상반기 수사기관에 제출된 건수는 전화번호 수 기준 212만6건으로 전년 동기 대비 17.2%(43만9433건) 줄었다. 이중 검찰과 경찰이 받아간 자료는 각각 55만9774건, 149만4927건으로 총 205만4701건이다.

하지만 법원 허가가 필요한 통신사실확인자료와 통신제한조치 건수는 증가했다.

상대방 전화번호 등 통신사실확인자료는 통신비밀보호법이 정한 요건 및 절차에 따라 해당 자료가 필요한 수사기관 등이 법원의 허가를 받아야만 전기통신사업자로부터 취득할 수 있다.

통신사실확인자료가 지난 상반기 수사기관에 제출된 건수는 전화번호 수 기준으로 30만2015건으로 전년 동기 대비 25.3%(6만1032건) 늘었다. 이중 검찰과 경찰이 받아간 자료는 각각 4만4871건, 25만4421건으로 총 29만9292건이다.'''
    WordExtraction.ex_compound_word(o, t)