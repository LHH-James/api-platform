import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit
from urllib.parse import unquote



headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Feeds/2009-01-01'
api_version = ['Version=2009-01-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y



class interface_feeds:
    def __init__(self):
        pass

    def SubmitFeed(execute_command):
        params = ['Action=SubmitFeed'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params += ['FeedType=_POST_PRODUCT_DATA_']
        request_content = open('./amazon/submit_xml_string.txt', 'r').read()
        request_content = bytes(request_content, 'utf-8')
        # print(type(request_content))
        # print(common_unit.get_md5(request_content))
        params += ['ContentMD5Value=' + quote(common_unit.get_md5(request_content)).replace('/', '%2F')]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, request_content, headers=headers)
        result = common_unit.xmltojson(r.text)
        # print(result)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def GetFeedSubmissionList(execute_command):
        params = ['Action=GetFeedSubmissionList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'submission_id_list' in execute_command:
            if execute_command['submission_id_list'] != '':
                id_list = execute_command['submission_id_list'].split(',')
                submission_id_list = []
                for i in id_list:
                    submission_id_list.append('FeedSubmissionIdList.Id.' + str(id_list.index(i) + 1) + '=' + i)
                params+=submission_id_list

        if 'max_count' in execute_command:
            if execute_command['max_count'] != '':
                params.append('MaxCount=' + execute_command['max_count'])


        if 'feed_type' in execute_command:
            if execute_command['feed_type'] != '':
                feed_list = execute_command['feed_type'].split(',')
                feed_type_list = []
                for i in feed_list:
                    feed_type_list.append('FeedTypeList.Type.' + str(feed_list.index(i) + 1) + '=' + i)
                params+=feed_type_list

        if 'feed_process_status' in execute_command:
            if execute_command['feed_process_status'] != '':
                feed_status_list = execute_command['feed_process_status'].split(',')
                status_list = []
                for i in feed_status_list:
                    status_list.append('FeedProcessingStatusList.Status.' + str(feed_status_list.index(i) + 1) + '=' + i)
                params += status_list

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                st = common_unit.conver_time(execute_command['start_time'])
                st = quote(st)
                params.append('SubmittedFromDate=' + st)

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                et = common_unit.conver_time(execute_command['end_time'])
                et = quote(et)
                params.append('SubmittedToDate=' + et)



        params = params + default_params + ['MaxCount=99']
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def GetFeedSubmissionListByNextToken(execute_command):
        params = ['Action=GetFeedSubmissionListByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params.append('NextToken=' + execute_command['next_token'])
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def GetFeedSubmissionCount(execute_command):
        params = ['Action=GetFeedSubmissionCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'feed_type' in execute_command:
            if execute_command['feed_type'] != '':
                feed_list = execute_command['feed_type'].split(',')
                feed_type_list = []
                for i in feed_list:
                    feed_type_list.append('FeedTypeList.Type.' + str(feed_list.index(i) + 1) + '=' + i)
                params+=feed_type_list

        if 'feed_process_status' in execute_command:
            if execute_command['feed_process_status'] != '':
                feed_status_list = execute_command['feed_process_status'].split(',')
                status_list = []
                for i in feed_status_list:
                    status_list.append('FeedProcessingStatusList.Status.' + str(feed_status_list.index(i) + 1) + '=' + i)
                params += status_list

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                st = common_unit.conver_time(execute_command['start_time'])
                st = quote(st)
                params.append('SubmittedFromDate=' + st)

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                et = common_unit.conver_time(execute_command['end_time'])
                et = quote(et)
                params.append('SubmittedToDate=' + et)

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



    def CancelFeedSubmissions(execute_command):
        params = ['Action=CancelFeedSubmissions'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)

        if 'submission_id_list' in execute_command:
            if execute_command['submission_id_list'] != '':
                id_list = execute_command['submission_id_list'].split(',')
                submission_id_list = []
                for i in id_list:
                    submission_id_list.append('FeedSubmissionIdList.Id.' + str(id_list.index(i) + 1) + '=' + i)
                params+=submission_id_list

        if 'feed_type' in execute_command:
            if execute_command['feed_type'] != '':
                feed_list = execute_command['feed_type'].split(',')
                feed_type_list = []
                for i in feed_list:
                    feed_type_list.append('FeedTypeList.Type.' + str(feed_list.index(i) + 1) + '=' + i)
                params+=feed_type_list

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                st = common_unit.conver_time(execute_command['start_time'])
                st = quote(st)
                params.append('SubmittedFromDate=' + st)

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                et = common_unit.conver_time(execute_command['end_time'])
                et = quote(et)
                params.append('SubmittedToDate=' + et)

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def GetFeedSubmissionResult(execute_command):
        params = ['Action=GetFeedSubmissionResult'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'submission_id' in execute_command:
            if execute_command['submission_id'] != '':
                params += ['FeedSubmissionId=' + execute_command['submission_id']]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        # print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        # error_result = common_unit.catch_exception(result)  # 异常处理
        # if error_result != '':
        #     result = error_result
        return result

    



    

