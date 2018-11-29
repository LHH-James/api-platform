import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit
import datetime
from test_file import test_common

headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Orders/2013-09-01'
api_version = ['Version=2013-09-01']
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


class interface_orders:

    def __init__(self):
        pass


    def ListOrders(execute_command):
        if common_unit.test_access_param(execute_command)!=-1:
            result = common_unit.read_xmlfile('test_file/order_list.xml')
            result = eval(result)
            test_common.get_test_order_list(execute_command, result)
        else:
            params = ['Action=ListOrders'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            params[-1] = 'MarketplaceId.Id.1=' + params[-1].split('=')[1]
            if 'create_time' in execute_command:
                if execute_command['create_time'] != '':
                    ct = common_unit.conver_time(execute_command['create_time'])
                    c_time = quote(ct)
                    params += ['CreatedAfter=' + c_time]
                else:
                    params += ['CreatedAfter=' + quote('1970-01-01T00:00:00')]
            if 'end_time' in execute_command:
                if execute_command['end_time'] != '':
                    # params += ['CreatedBefore=' + quote(execute_command['end_time'] + 'T00:00:00')]
                    et = common_unit.conver_time(execute_command['end_time'])
                    e_time = quote(et)
                    params += ['CreatedBefore=' + e_time]
                else:
                    delay = datetime.datetime.now() - datetime.timedelta(days=1)
                    e_time = delay.strftime('%Y-%m-%dT%H:%M:%S')
                    params += ['CreatedBefore=' + quote(e_time)]
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    #下一页
    def ListOrdersByNextToken(execute_command):
        if common_unit.test_access_param(execute_command)!=-1:
            result = common_unit.read_xmlfile('test_file/order_list_next.xml')
        else:
            params = ['Action=ListOrdersByNextToken']+api_version+['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            if 'next_token' in execute_command:
                if execute_command['next_token']!='':
                    next_token = execute_command['next_token']
                    params+=['NextToken='+quote(next_token)]
            params += default_params
            params = sorted(params)
            params = '&'.join(params)
            params = params.replace('+', '%2B')
            params = params.replace('/', '%2F')
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            signature = signature.replace('=', '%3D')
            signature = signature.replace('/', '%2F')
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result

 
    #订单明细
    def ListOrderItems(execute_command):
        if common_unit.test_access_param(execute_command)!=-1:
            result = common_unit.read_xmlfile('test_file/order_item_list.xml')
            result = eval(result)
            test_common.get_test_orderitem_list(execute_command, result)
        else:
            params = ['Action=ListOrderItems']+api_version+['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])

            params += common_unit.make_access_param(execute_command)
            if 'order_id' in execute_command:
                if execute_command['order_id']!='':
                    params += [str('AmazonOrderId='+quote(execute_command['order_id']))]
            params += default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key']))) # 计算字符串的加密签名
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            result = common_unit.xmltojson(r.text)
            # print(attribute_content)
            # print(type(attribute_content))
            # result = write_order_item_into_database(execute_command,attribute_content)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    #订单明细下一页
    def ListOrderItemsByNextToken(execute_command):
        if common_unit.test_access_param(execute_command)!=-1:
            result = common_unit.read_xmlfile('test_file/order_item_list_next.xml')
        else:
            params = ['Action=ListOrderItemsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += default_params
            params += common_unit.make_access_param(execute_command)
            if 'next_token' in execute_command:
                if execute_command['next_token'] != '':
                    params += ['NextToken=' + execute_command['next_token']]
            params = sorted(params)
            params = '&'.join(params)
            params = params.replace('+', "%2B")
            params = params.replace('/', "%2F")
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            signature = signature.replace('=', '%3D')
            signature = signature.replace('/', '%2F')
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result




    def GetOrder(execute_command):
        if common_unit.test_access_param(execute_command)!=-1:
            result = common_unit.read_xmlfile('test_file/get_order.xml')
            result = eval(result)
            test_common.get_test_order(execute_command, result)
        else:
            params = ['Action=GetOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'order_id' in execute_command:
                if execute_command['order_id'] != '':
                    order_id_list = execute_command['order_id'].split(',')
                    order_param_list = []
                    for i in order_id_list:
                        order_param_list.append('AmazonOrderId.Id.'+str(order_id_list.index(i)+1)+'='+i)
                    params+=order_param_list
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
















