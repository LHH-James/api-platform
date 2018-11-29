#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common


class Notifications:

    def __init__(self):
        pass


    def fetch_notifications(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        url = "https://merchant.wish.com/api/v2/noti/fetch-unviewed?"+params
        r = requests.post(url)
        result = r.text
        return result


    def mark_as_viewed(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'noti_id' in execute_command:
            noti_id = wish_common.is_null_field(execute_command['noti_id'])
            params = params + '&noti_id' + '=' + noti_id
        url = "https://merchant.wish.com/api/v2/noti/mark-as-viewed?"+params
        r = requests.post(url)
        result = r.text
        return result


    def count_unview_notifications(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/noti/get-unviewed-count?"+params
        r = requests.post(url)
        result = r.text
        return result



    def fetch_announcements(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/fetch-bd-announcement?"+params
        r = requests.post(url)
        result = r.text
        return result


    def fetch_system_update_notifications(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/fetch-sys-updates-noti?" +params
        r = requests.post(url)
        result = r.text
        return result

