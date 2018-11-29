#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common

#常见问题的解决
class Faq:

    def __init__(self):
        pass


#更新产品价格
    def update_price(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        if 'new_price' in execute_command:
            new_price = wish_common.is_null_field(execute_command['new_price'])
            params = params + '&price' + '=' + new_price
        url = "https://merchant.wish.com/api/v2/variant/update?"+params
        r = requests.post(url)
        result = r.text
        return result

#更新产品库存
    def update_inventory(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        if 'inventory' in execute_command:
            inventory = wish_common.is_null_field(execute_command['inventory'])
            params = params + '&inventory' + '=' + inventory
        url = "https://merchant.wish.com/api/v2/variant/update-inventory?"+params
        r = requests.post(url)
        result = r.text
        return result

#启用/禁用产品
    def enable_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        url = "https://merchant.wish.com/api/v2/product/enable?"+params
        r = requests.post(url)
        result = r.text
        return result


    def get_all_products(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/product/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result

    def get_product_by_job_id(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/product/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result

    def get_all_orders(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/order/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result

    def get_order_by_job_id(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/order/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result
