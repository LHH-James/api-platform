import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Recommendations/2013-04-01'
api_version = ['Version=2013-04-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


class interface_recommendations:
    def __init__(self):
        pass   

    def GetLastUpdatedTimeForRecommendations(execute_command):
        params = ['Action=GetLastUpdatedTimeForRecommendations']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result
    
    def ListRecommendations(execute_command):
        params = ['Action=ListRecommendations']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'recommend_category' in execute_command:
            if execute_command['recommend_category']!='':
                params+=['RecommendationCategory='+quote(execute_command['recommend_category'])]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def ListRecommendationsByNextToken(execute_command):
        params = ['Action=ListRecommendationsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params += ['NextToken=' + execute_command['next_token']]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)
        print(url)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


