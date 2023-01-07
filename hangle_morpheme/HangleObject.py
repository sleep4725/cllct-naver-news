import os
import sys
PROJ_ROOT_PATH :str= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_PATH)

from konlpy.tag import Mecab

try:
    
    from util.Regex import Regex
except ImportError as err:
    print(err)
    exit(1)
'''
@author JunHyeon.Kim
@date 20221224
'''
class WordExtraction:
    
    @classmethod 
    def sample(cls, m_obj: Mecab, text: str):
        '''
        :param m_obj:
        :param text:
        :return:
        '''
        response = m_obj.pos(text)
        print(response)
        
    @classmethod 
    def get_compound_nng_from_xpn(cls, index: int, response: list[tuple])\
            -> tuple:
        '''
        :param index:
        :param response:
        :return:
        '''
        XPN :dict[int, list]={
                            2: [["XPN", "NNG"], 
                                ["XPN", "XR"]]
                            ,4: [["XPN", "NNG", "NNG", "XSN"], 
                                 ["XPN", "NNG", "NNB", "XSN"],
                                 ["XPN", "NR", "NNB", "XSN"],
                                 ["XPN", "SN", "NNB", "XSN"]]
                            ,5: [["XPN", "SN", "NNB", "NNG", "XSN"]]
                        }
        
        next_movement :int= 1
        result_movement :int= 1
        nn_compound_hangl :str= ""
        
        for length_v in XPN.keys():
            for hangle_tag_v in XPN[length_v]:
            
                back_position :int= index + length_v 
                if back_position > len(response): 
                    """이동하려는 위치가 전체 사이즈를 벗어나는 경우"""
                    pass
                else:
                    hangl_str :str= " ".join([e[1] for e in response[index: index+length_v]])
                    xpn_str :str= " ".join(hangle_tag_v)

                    if xpn_str == hangl_str:
                        nn_compound_hangl += "".join([e[0] for e in response[index: index+length_v]])                    
                        if index + length_v + next_movement < len(response):
                            hangl_tag :str= response[index + length_v + next_movement][1]  

                            if hangl_tag == "XSN":
                                nn_compound_hangl = nn_compound_hangl + response[index + length_v + next_movement][0]
                                result_movement = length_v + next_movement                                
                                break
                            else: 
                                result_movement = length_v
                                break
                        else: 
                            pass
                    else: 
                        pass
        
        return nn_compound_hangl, result_movement
    
    @classmethod 
    def get_compound_nng_from_nnp(cls, index: int, response: list[tuple])\
            -> tuple:
        '''
        '''
        next_movement :int= 1
        tmp_movement :int= index + next_movement 
        
        result_movement :int= 0
        nn_compound_hangl :str= ""
        
        while True:
            if tmp_movement > len(response): 
                break
            if response[tmp_movement][1] == "NNG":
                nn_compound_hangl += response[tmp_movement][0]
                tmp_movement += next_movement
                result_movement += 1
            else:
                # response[tmp_movement + next_movement][1] != "NNG": 
                result_movement += 1
                break
        
        return nn_compound_hangl, result_movement  
    
    @classmethod
    def get_compound_nng_from_nng(cls, index: int, response: list[tuple])\
            -> tuple:
        '''
        NNG + NNG + VV + ETN : 불우이웃돕기(불우/NNG+이웃/NNG+돕/VV+기/ETN)
        
        NNG + VV + ETN : 글쓰기(글/NNG+쓰/VV+기/ETN)
        NNG + MM + NNG : 국내총생산(국내/NNG+총/MM+생산/NNG)
        NNG + (VV + ETM) + NNG : 눈코뜰새(눈코/NNG+뜨/VV+ㄹ/ETM+새/NNG)
        
        :param response:
        :return:
        '''
        NNG :dict[int, list]={
                            3: [["NNG", "VV", "ETN"],
                                ["NNG", "MM", "NNG"]]
                            ,4: [["NNG", "NNG", "VV", "ETN"]], 
                        }
        
        next_movement :int= 1
        tmp_movement :int= index + next_movement 
        
        result_movement :int= 0
        nn_compound_hangl :str= ""
        
        is_true :bool= False
        
        for length_v in NNG.keys():
            for hangle_tag_v in NNG[length_v]:
            
                back_position :int= index + length_v 
                if back_position > len(response): 
                    """이동하려는 위치가 전체 사이즈를 벗어나는 경우
                    """
                    pass
                else:
                    """이동하려는 위치가 전체 사이즈를 벗어나지 않는 경우
                    """
                    hangl_str :str= " ".join([e[1] for e in response[index: back_position]])
                    xpn_str :str= " ".join(hangle_tag_v)

                    if xpn_str == hangl_str:
                        nn_compound_hangl += "".join([e[0] for e in response[index + 1: back_position]])                    
                        is_true = True
                        result_movement += length_v
                        print("----------------------------------------")
                        break
                    else: 
                        pass
        
        if not is_true:
            while True:
                if tmp_movement >= len(response): 
                    break
                if response[tmp_movement][1] == "NNG" and len(response[tmp_movement][0]) > 1:
                    nn_compound_hangl += response[tmp_movement][0]
                    tmp_movement += next_movement
                    result_movement += 1
                else:
                    # response[tmp_movement + next_movement][1] != "NNG": 
                    result_movement += 1
                    break
        
        return nn_compound_hangl, result_movement 
    
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
    
    @classmethod
    def ex_compound_word(cls, m_obj: Mecab, text: str)\
            -> list[str]:
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
            
            if response[mov_index][1] == "XPN":
                ''' XPN : 체언접두사
                '''
                nn_compound_hangl, move = WordExtraction.get_compound_nng_from_xpn(index= mov_index, response= response)
                result_compound_word.append(str(nn_compound_hangl).strip())
                mov_index += move
            elif response[mov_index][1] == "NNG" and len(response[mov_index][0]) > 1:
                ''' NNG
                '''
                nng_word :str= response[mov_index][0]
                nn_compound_hangl, move = WordExtraction.get_compound_nng_from_nng(index= mov_index, response= response)
                nng_word += nn_compound_hangl
                result_compound_word.append(str(nng_word).strip())
                if move == 0:
                    mov_index += 1
                else:
                    mov_index += move
            elif response[mov_index][1] == "NNP":
                nnp_word :str= response[mov_index][0]
                nn_compound_hangl, move = WordExtraction.get_compound_nng_from_nng(index= mov_index, response= response)
                nnp_word += nn_compound_hangl
                result_compound_word.append(str(nnp_word).strip())
                if move == 0:
                    mov_index += 1
                else:
                    mov_index += move 
            else:
                mov_index += 1 
        
        compound_word_list :list[str]= list(set([w for w in list(set(result_compound_word)) if len(w) > 2]))
        return compound_word_list
        
class HangleObject:
    
    @classmethod 
    def get_hangle_client(cls)\
            -> Mecab:
        '''
        :param:
        :return:
        '''
        m_obj = Mecab()
        return m_obj