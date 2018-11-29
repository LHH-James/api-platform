import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit

headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Reports/2009-01-01'
api_version = ['Version=2009-01-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+'/'+port_point+'?'+x+'&Signature='+y


#报告

class interface_reports:

    def __init__(self):
        pass
    

    #创建一个报告请求和提交请求亚马逊MWS
    def RequestReport(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            result = common_unit.read_xmlfile('test_file/requestReport.xml')
        else:
            params = ['Action=RequestReport'] + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            access_params = common_unit.make_access_param(execute_command)
            market_place_id = access_params[-1].split('=')[1]
            access_params += ['MarketplaceIdList.Id.1='+market_place_id]
            params = params + access_params # 获取包含认证参数的字典
            if 'report_type' in execute_command:
                if execute_command['report_type'] != '':
                    params.append('ReportType=' + quote(execute_command['report_type']))

            if 'start_time' in execute_command:
                s = execute_command['start_time']
                if s != '':
                    st = common_unit.conver_time(s)
                    st = quote(st)
                    params.append('StartDate=' + st)

            if 'end_time' in execute_command:
                e = execute_command['end_time']
                if e!= '':
                    et = common_unit.conver_time(e)
                    et = quote(et)
                    params.append('EndDate=' + et)

            params = params + default_params
            params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
            params = '&'.join(params)  # 对请求身进行分割
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key']))) # 计算字符串的加密签名
            signature = signature.replace('/', '%2F')
            url = connect_url(params, signature)  # 拼接请求字符串
            # print(url)
            r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            # print(r.text)
            error_result = common_unit.catch_exception(result)     #异常处理
            if error_result!='':
                result = error_result
        return result




    #返回一个请求报告的列表  用参数ReportRequestId 请求
    def GetReportRequestList(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            result = common_unit.read_xmlfile('test_file/getReportRequestList.xml')
        else:
            params = ['Action=GetReportRequestList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'report_request_id' in execute_command:
                if execute_command['report_request_id'] != '':
                    request_id_list = execute_command['report_request_id'].split(',')
                    request_list = []
                    for i in request_id_list:
                        request_list.append('ReportRequestIdList.Id.' + str(request_id_list.index(i) + 1) + '=' + i)
                    params += request_list

            if 'report_type' in execute_command:
                if execute_command['report_type'] != '':
                    report_list = execute_command['report_type'].split(',')
                    report_type_list = []
                    for i in report_list:
                        report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                    params+=report_type_list

            if 'process_status' in execute_command:
                if execute_command['process_status'] != '':
                    process_status_list = execute_command['process_status'].split(',')
                    process_list = []
                    for i in process_status_list:
                        process_list.append('ReportProcessingStatusList.Status.' + str(process_status_list.index(i) + 1) + '=' + i)
                    params+=process_list

            if 'max_count' in execute_command:
                if execute_command['max_count'] != '':
                    params.append('MaxCount=' + quote(execute_command['max_count']))

            if 'start_time' in execute_command:
                if execute_command['start_time'] != '':
                    st = common_unit.conver_time(execute_command['start_time'])
                    st = quote(st)
                    params.append('RequestedFromDate=' + st)  #开始时间

            if 'end_time' in execute_command:
                if execute_command['end_time'] != '':
                    et = common_unit.conver_time(execute_command['end_time'])
                    et = quote(et)
                    params.append('RequestedToDate=' + et)  #结束时间

            params = params + default_params
            params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
            params = '&'.join(params)  # 对请求身进行分割
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
            url = connect_url(params, signature)  # 拼接请求字符串
            r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            # print(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result

        return result


    #下一页
    def GetReportRequestListByNextToken(execute_command):
        params = ['Action=GetReportRequestListByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params.append('NextToken=' + quote(execute_command['next_token']))  # 取上一个接口 NextToken的返回值
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('=', '%3D')
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    #返回已提交给亚马逊MWS进行处理的报告请求计数
    def GetReportRequestCount(execute_command):
        params = ['Action=GetReportRequestCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典

        if 'process_status' in execute_command:
            if execute_command['process_status'] != '':
                process_status_list = execute_command['process_status'].split(',')
                process_list = []
                for i in process_status_list:
                    process_list.append('ReportProcessingStatusList.Status.' + str(process_status_list.index(i) + 1) + '=' + i)
                params+=process_list

        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                params.append('RequestedFromDate=' + quote(execute_command['start_time'] + 'T00:00:00'))  # 开始时间

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                params.append('RequestedToDate=' + + quote(execute_command['end_time'] + 'T00:00:00'))  # 结束时间


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

    #取消一个或多个报告请求
    def CancelReportRequests(execute_command):
        params = ['Action=CancelReportRequests'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_request_id' in execute_command:
            if execute_command['report_request_id'] != '':
                request_id_list = execute_command['report_request_id'].split(',')
                request_list = []
                for i in request_id_list:
                    request_list.append('ReportRequestIdList.Id.' + str(request_id_list.index(i) + 1) + '=' + i)
                params += request_list

        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

        if 'process_status' in execute_command:
            if execute_command['process_status'] != '':
                process_status_list = execute_command['process_status'].split(',')
                process_list = []
                for i in process_status_list:
                    process_list.append('ReportProcessingStatusList.Status.' + str(process_status_list.index(i) + 1) + '=' + i)
                params+=process_list

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                params.append('RequestedFromDate=' + quote(execute_command['start_time'] + 'T00:00:00')) #开始时间

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                params.append('RequestedToDate=' + + quote(execute_command['end_time'] + 'T00:00:00'))  #结束时间

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

    #返回在前90天中创建的报告列表
    #request_id  传list进来
    def GetReportList(execute_command):
        params = ['Action=GetReportList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'max_count' in execute_command:
            if execute_command['max_count'] != '':
                params.append('MaxCount=' + quote(execute_command['max_count']))

        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

        if 'ac_knowledge' in execute_command:
            if execute_command['ac_knowledge'] != '':
                params.append('Acknowledged=' + quote(execute_command['ac_knowledge']))

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                params.append('AvailableFromDate=' + quote(execute_command['start_time'] + 'T00:00:00')) #开始时间

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                params.append('AvailableToDate=' + + quote(execute_command['end_time'] + 'T00:00:00'))  #结束时间

        if 'report_request_id' in execute_command:
            if execute_command['report_request_id'] != '':
                # params.append('ReportRequestIdList.Id.1=' + quote(execute_command['report_request_id']))
                request_id_list = execute_command['report_request_id'].split(',')
                request_list = []
                for i in request_id_list:
                    request_list.append('ReportRequestIdList.Id.' + str(request_id_list.index(i) + 1) + '=' + i)
                params += request_list

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

    #上一个接口的下一页
    def GetReportListByNextToken(execute_command):
        params = ['Action=GetReportListByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params.append('NextToken=' + quote(execute_command['next_token']).replace('/','%2F'))  # 取上一个接口 NextToken的返回值

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

    #返回报告的数量,在过去的90天了，_DONE_ 状态,可供下载
    def GetReportCount(execute_command):
        params = ['Action=GetReportCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

        if 'acknowledged' in execute_command:
            if execute_command['acknowledged'] != '':
                params.append('Acknowledged=' + quote(execute_command['acknowledged']))

        if 'start_time' in execute_command:
            if execute_command['start_time'] != '':
                params.append('AvailableFromDate=' + quote(execute_command['start_time'] + 'T00:00:00')) #开始时间

        if 'end_time' in execute_command:
            if execute_command['end_time'] != '':
                params.append('AvailableToDate=' + quote(execute_command['end_time'] + 'T00:00:00'))  #结束时间

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


    #返回报告的内容以及返回的报告主体的Content-MD5头
    def GetReport(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            result = common_unit.report_content
        else:
            params = ['Action=GetReport'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'report_id' in execute_command:
                if execute_command['report_id'] != '':
                    params.append('ReportId=' + quote(execute_command['report_id']))
            params = params + default_params
            params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
            params = '&'.join(params)  # 对请求身进行分割
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
            url = connect_url(params, signature)  # 拼接请求字符串
            r = requests.post(url, headers=headers)  # 发起请求
            # print(r)
            # print(r.text)
            # print(r.content)
            result = common_unit.read_file(r.text)
            # result = common_unit.xmltojson(r.content)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result



    #创建，更新或删除指定报告类型的报告请求计划
    def ManageReportSchedule(execute_command):
        params = ['Action=ManageReportSchedule'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                params.append('ReportType=' + quote(execute_command['report_type']))

        if 'schedule' in execute_command:
            if execute_command['schedule'] != '':
                params.append('Schedule=' + quote(execute_command['schedule']))

        if 'schedule_date' in execute_command:
            if execute_command['schedule_date'] != '':
                params.append('ScheduleDate=' + quote(execute_command['schedule_date']))

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



    #返回计划提交给亚马逊MWS进行处理的订单报告请求列表
    def GetReportScheduleList(execute_command):
        params = ['Action=GetReportScheduleList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

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

    #返回计划提交给亚马逊MWS的订单报告请求计数
    def GetReportScheduleCount(execute_command):
        params = ['Action=GetReportScheduleCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_type' in execute_command:
            if execute_command['report_type'] != '':
                report_list = execute_command['report_type'].split(',')
                report_type_list = []
                for i in report_list:
                    report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
                params+=report_type_list

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

    #更新一个或多个报告的确认状态
    #参数 acknowledged 只有两种状态  true or false
    def UpdateReportAcknowledgements(execute_command):
        params = ['Action=UpdateReportAcknowledgements'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'report_id' in execute_command:
            if execute_command['report_id'] != '':
                report_id_list = execute_command['report_id'].split(',')
                report_list = []
                for i in report_id_list:
                    report_list.append('ReportIdList.Id.' + str(report_id_list.index(i) + 1) + '=' + i)
                params += report_list

        if 'acknowledged' in execute_command:
            if execute_command['acknowledged'] != '':
                params.append('Acknowledged=' + quote(execute_command['acknowledged']))  # true or false

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




