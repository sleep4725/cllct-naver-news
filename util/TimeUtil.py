import time 

'''
@author JunHyeon.Kim 
@date 20221208
'''
class TimeUtil:
    
    @classmethod 
    def get_cllct_time(cls)-> str:
        '''
        :param:
        :return:
        '''
        return time.strftime("%Y%m%d", time.localtime())