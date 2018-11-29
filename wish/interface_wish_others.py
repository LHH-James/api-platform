#coding=utf-8
import sys
sys.path.append('../')
import requests
from wish import wish_common

#仓库+违规+获取罚款信息
class Others:

    def get_list_warehouses(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/warehouse/get-all?"+params
        r = requests.post(url)
        result = r.text
        return result


#违规

    #违规计数
    def get_infractions_count(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'stage' in execute_command:
            stage = wish_common.is_null_field(execute_command['stage'])
            params = params + '&stage' + '=' + stage
        url = "https://merchant.wish.com/api/v2/count/infractions?"+params
        r = requests.post(url)
        result = r.text
        return result

    #获取需要商家注意的违规链接
    def fetch_infractions(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        if 'stage' in execute_command:
            stage = wish_common.is_null_field(execute_command['stage'])
            params = params + '&stage' + '=' + stage
        if 'since' in execute_command:
            since = wish_common.is_null_field(execute_command['since'])
            params = params + '&since' + '=' + since
        if 'upto' in execute_command:
            upto = wish_common.is_null_field(execute_command['upto'])
            params = params+'upto' + '=' + upto
        url = "https://merchant.wish.com/api/v2/get/infractions?"+params
        r = requests.post(url)
        result = r.text
        return result


    #获取罚款信息
    def get_fine(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id' + '=' + id
        url = "https://merchant.wish.com/api/v2/fine?"+params
        r = requests.post(url)
        result = r.text
        return result