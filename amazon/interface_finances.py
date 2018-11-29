import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Finances/2015-05-01'
api_version = ['Version=2015-05-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+'/'+port_point+'?'+x+'&Signature='+y


class interface_finances:

    def __init__(self):
        pass
    #返回给定日期范围的资金/财务集合
    #参数 page(每页返回的最大结果数)  Minimum: 1 , Maximum: 100  , Default: 100  , Type: xs:int   可以为空
    #参数 start_time(查询的开始时间)   Type: xs:dateTime
    #参数 end_time(查询的结束时间) 可以为空 Type: xs:dateTime
    def ListFinancialEventGroups(execute_command):
        params = ['Action=ListFinancialEventGroups'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'page' in execute_command:
            if execute_command['page']!='':
                params.append('MaxResultsPerPage=' + quote(execute_command['page']))     #需要几页

        if 'start_time' in execute_command:
            if execute_command['start_time']!='':
                st = common_unit.conver_time(execute_command['start_time'])
                st_timeArray = quote(st)
                params.append('FinancialEventGroupStartedAfter=' + st_timeArray)   # 添加请求中包含的start_time

        if 'end_time' in execute_command:
            if execute_command['end_time']!='':
                et = common_unit.conver_time(execute_command['end_time'])
                et_timeArray = quote(et)
                params.append('FinancialEventGroupStartedBefore=' + et_timeArray)

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    #返回资金/财务集合的下一页 参数使用nexttoken

    def ListFinancialEventGroupsByNextToken(execute_command):
        params = ['Action=ListFinancialEventGroupsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params += ['NextToken=' + quote(execute_command['next_token'])]
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    #返回资金事件
    #四个参数  任意给一个 order_id \ event_group_id \ start_time \ end_time
    def ListFinancialEvents(execute_command):
        params = ['Action=ListFinancialEvents'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典

        if 'page' in execute_command:
            if execute_command['page']!= '':
                params.append('MaxResultsPerPage=' + quote(execute_command['page']))     #返回结果页数

        if 'order_id' in execute_command:
            if execute_command['order_id']!= '':
                params.append('AmazonOrderId=' + quote(execute_command['order_id']))     #订单编号

        if 'event_group_id' in execute_command:
            if execute_command['event_group_id']!='':
                params.append('FinancialEventGroupId=' + quote(execute_command['event_group_id']))  #事件组编号

        if 'start_time' in execute_command:
            if execute_command['start_time']!= '':
                st = common_unit.conver_time(execute_command['start_time'])
                st_timeArray = quote(st)
                params.append('PostedAfter=' + st_timeArray)  #开始时间

        if 'end_time' in execute_command:
            if execute_command['end_time']!= '':
                et = common_unit.conver_time(execute_command['end_time'])
                et_timeArray = quote(et)
                params.append('PostedBefore=' + et_timeArray)  #结束时间

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



    def ListFinancialEventsByNextToken(execute_command):
        params = ['Action=ListFinancialEventsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params += ['NextToken=' + quote(execute_command['next_token'])]
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        params = params.replace('=', "%3D")
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('/', "%2F")
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    # 返回 资金 这块API的操作状态
    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result