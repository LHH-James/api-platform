#coding=utf-8
import sys
sys.path.append('../')
import requests
from wish import wish_common





# 商品促销接口
class Product_boost:
    def __init__(self):
        pass

    def get_campaign(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/get?" + params
        r = requests.post(url)
        result = r.text
        return result

    def get_multiple_campagins(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            if start:
                params = params + '&start=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            if limit:
                params = params + '&limit=' + limit
        if 'start_time' in execute_command:
            start_time = wish_common.is_null_field(execute_command['start_time'])
            if start_time:
                params = params + '&start_time=' + start_time
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/multi-get?" + params
        r = requests.post(url)
        result = r.text
        return result


    def list_low_budget_campaigns(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            if start:
                params = params + '&start=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            if limit:
                params = params + '&limit=' + limit
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/list-low-budget?" + params
        r = requests.post(url)
        result = r.text
        return result

    def create_campaign(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'max_budget' in execute_command:
            max_budget = wish_common.is_null_field(execute_command['max_budget'])
            params = params + '&max_budget=' + max_budget
        if 'auto_renew' in execute_command:
            auto_renew = wish_common.is_null_field(execute_command['auto_renew'])
            params = params + '&auto_renew=' + auto_renew
        if 'campaign_name' in execute_command:
            campaign_name = wish_common.is_null_field(execute_command['campaign_name'])
            params = params + '&campaign_name=' + campaign_name
        if 'start_date' in execute_command:
            start_date = wish_common.is_null_field(execute_command['start_date'])
            params = params + '&start_date=' + start_date
        if 'end_date' in execute_command:
            end_date = wish_common.is_null_field(execute_command['end_date'])
            params = params + '&end_date=' + end_date
        if 'products' in execute_command:
            products = wish_common.is_null_field(execute_command['products'])
            params = params + '&products=' + products
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/create?" + params
        r = requests.post(url)
        result = r.text
        return result

    def update_campagin(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        if 'max_budget' in execute_command:
            max_budget = wish_common.is_null_field(execute_command['max_budget'])
            params = params + '&max_budget=' + max_budget
        if 'auto_renew' in execute_command:
            auto_renew = wish_common.is_null_field(execute_command['auto_renew'])
            params = params + '&auto_renew=' + auto_renew
        if 'campaign_name' in execute_command:
            campaign_name = wish_common.is_null_field(execute_command['campaign_name'])
            params = params + '&campaign_name=' + campaign_name
        if 'start_date' in execute_command:
            start_date = wish_common.is_null_field(execute_command['start_date'])
            params = params + '&start_date=' + start_date
        if 'end_date' in execute_command:
            end_date = wish_common.is_null_field(execute_command['end_date'])
            params = params + '&end_date=' + end_date
        if 'products' in execute_command:
            products = wish_common.is_null_field(execute_command['products'])
            params = params + '&products=' + products
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/update?" + params
        r = requests.post(url)
        result = r.text
        return result

    def update_running_campagin(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        if 'max_budget' in execute_command:
            max_budget = wish_common.is_null_field(execute_command['max_budget'])
            params = params + '&max_budget=' + max_budget
        if 'auto_renew' in execute_command:
            auto_renew = wish_common.is_null_field(execute_command['auto_renew'])
            params = params + '&auto_renew=' + auto_renew
        if 'end_date' in execute_command:
            end_date = wish_common.is_null_field(execute_command['end_date'])
            params = params + '&end_date=' + end_date
        if 'products' in execute_command:
            products = wish_common.is_null_field(execute_command['products'])
            params = params + '&products=' + products
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/update-running?" + params
        r = requests.post(url)
        result = r.text
        return result

    def add_budget_campagin(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        if 'amount' in execute_command:
            amount = wish_common.is_null_field(execute_command['amount'])
            params = params + '&amount=' + amount
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/add-budget?" + params
        r = requests.post(url)
        result = r.text
        return result


    def stop_campagin(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/stop?" + params
        r = requests.post(url)
        result = r.text
        return result

    def cancel_campagin(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/cancel?" + params
        r = requests.post(url)
        result = r.text
        return result

    def get_campagin_performance(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/get-performance?" + params
        r = requests.post(url)
        result = r.text
        return result


    def get_campagin_product_stats(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'id' in execute_command:
            id = wish_common.is_null_field(execute_command['id'])
            params = params + '&id=' + id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/get-product-stats?" + params
        r = requests.post(url)
        result = r.text
        return result


    def get_campagin_daily_stats(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'campaign_id' in execute_command:
            campaign_id = wish_common.is_null_field(execute_command['campaign_id'])
            params = params + '&campaign_id=' + campaign_id
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&product_id=' + product_id
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/get-product-daily-stats?" + params
        r = requests.post(url)
        result = r.text
        return result

    def get_keywords(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'keywords' in execute_command:
            keywords = wish_common.is_null_field(execute_command['keywords'])
            params = params + '&keywords=' + keywords
        url = "https://merchant.wish.com/api/v2/product-boost/keyword/multi-get?" + params
        r = requests.post(url)
        result = r.text
        return result


    def search_keywords(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'keyword' in execute_command:
            keyword = wish_common.is_null_field(execute_command['keyword'])
            params = params + '&keyword=' + keyword
        if 'exclude_keywords' in execute_command:
            exclude_keywords = wish_common.is_null_field(execute_command['exclude_keywords'])
            if exclude_keywords:
                params = params + '&exclude_keywords=' + exclude_keywords
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            if limit:
                params = params + '&limit=' + limit
        url = "https://merchant.wish.com/api/v2/product-boost/keyword/search?" + params
        r = requests.post(url)
        result = r.text
        return result


    def get_campagin_budget(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/product-boost/budget?" + params
        r = requests.post(url)
        result = r.text
        return result

    def vaildate_campagin_bids(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'campaign_id' in execute_command:
            campaign_id = wish_common.is_null_field(execute_command['campaign_id'])
            if campaign_id:
                params = params + '&campaign_id=' + campaign_id
        if 'campaign_start_time' in execute_command:
            campaign_start_time = wish_common.is_null_field(execute_command['campaign_start_time'])
            params = params + '&campaign_start_time=' + campaign_start_time
        if 'campaign_end_time' in execute_command:
            campaign_end_time = wish_common.is_null_field(execute_command['campaign_end_time'])
            params = params + '&campaign_end_time=' + campaign_end_time
        if 'bids' in execute_command:
            bids = wish_common.is_null_field(execute_command['bids'])
            params = params + '&bids=' + bids
        url = "https://merchant.wish.com/api/v2/product-boost/campaign/validate-bids?" + params
        r = requests.post(url)
        result = r.text
        return result






