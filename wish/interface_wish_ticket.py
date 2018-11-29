#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common

class Ticket:

    def __init__(self):
        pass



    #ticket_id : 票证对象中的ID
    #检索票据
    def retrieve_ticket(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'ticket_id' in execute_command:
            ticket_id = wish_common.is_null_field(execute_command['ticket_id'])
            params = params + '&id' + '=' + ticket_id
        url = "https://merchant.wish.com/api/v2/ticket?"+params
        r = requests.post(url)
        result = r.text
        return result


    #列出所有等待你处理的票剧
    def retrieve_all_ticket_waiting(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        url = "https://merchant.wish.com/api/v2/ticket/get-action-required?"+params
        r = requests.post(url)
        result = r.text
        return result

    #票据回复
    def replay_to_ticket(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'ticket_id' in execute_command:
            ticket_id = wish_common.is_null_field(execute_command['ticket_id'])
            params = params + '&id' + '=' + ticket_id
        if 'reply' in execute_command:
            reply = wish_common.is_null_field(execute_command['reply'])
            params = params + '&reply' + '=' + reply
        url = "https://merchant.wish.com/api/v2/ticket/reply?"+params
        r = requests.post(url)
        result = r.text
        return result


    def close_ticket(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'ticket_id' in execute_command:
            ticket_id = wish_common.is_null_field(execute_command['ticket_id'])
            params = params + '&id' + '=' + ticket_id
        url = "https://merchant.wish.com/api/v2/ticket/close?"+params
        r = requests.post(url)
        result = r.text
        return result


    def appeal_to_wish_support(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'ticket_id' in execute_command:
            ticket_id = wish_common.is_null_field(execute_command['ticket_id'])
            params = params + '&id' + '=' + ticket_id
        url = "https://merchant.wish.com/api/v2/ticket/appeal-to-wish-support?"+params
        r = requests.post(url)
        result = r.text
        return result


    def reopen_ticket(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'ticket_id' in execute_command:
            ticket_id = wish_common.is_null_field(execute_command['ticket_id'])
            params = params + '&id' + '=' + ticket_id
        if 'reply' in execute_command:
            reply = wish_common.is_null_field(execute_command['reply'])
            params = params + '&reply' + '=' + reply
        url = "https://merchant.wish.com/api/v2/ticket/re-open?"+params
        r = requests.post(url)
        result = r.text
        return result

