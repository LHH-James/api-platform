#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common




class Order:
    def __init__(self):
        pass

    def retrieve_order(execute_command):
        params = 'access_token'+'='+execute_command['access_token']
        if 'order_id' in execute_command:
            order_id = wish_common.is_null_field(execute_command['order_id'])
            params = params+'&id'+'='+order_id
        if 'show_original_shipping_detail' in execute_command:
            show_shipping_detail = wish_common.is_null_field(execute_command['show_original_shipping_detail'])
            params = params + '&show_original_shipping_detail' + '=' + show_shipping_detail
        url = "https://merchant.wish.com/api/v2/order?"+params
        r = requests.post(url)
        result = r.text
        return result

#检索最近更改订单
    def recently_changed_orders(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params+'&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params+'&limit' + '=' + limit
        if 'since' in execute_command:
            since = wish_common.is_null_field(execute_command['since'])
            params = params+'&since' + '=' + since
        if 'upto' in execute_command:
            upto = wish_common.is_null_field(execute_command['upto'])
            params = params+'&upto' + '=' + upto
        if 'wish_express_only' in execute_command:
            wish_express_only = wish_common.is_null_field(execute_command['wish_express_only'])
            params = params+'&wish_express_only' + '=' + wish_express_only
        if 'show_original_shipping_detail' in execute_command:
            show_original_shipping_detail = wish_common.is_null_field(execute_command['show_original_shipping_detail'])
            params = params+'&show_original_shipping_detail' + '=' + show_original_shipping_detail
        url = "https://merchant.wish.com/api/v2/order/multi-get?"+params
        r = requests.get(url)
        result = r.text
        return result


#检索未履行订单
    def retrieve_unfulfilled_orders(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        if 'since' in execute_command:
            since = wish_common.is_null_field(execute_command['since'])
            params = params + '&since' + '=' + since
        if 'wish_express_only' in execute_command:
            wish_express_only = wish_common.is_null_field(execute_command['wish_express_only'])
            params = params + '&wish_express_only' + '=' + wish_express_only
        url = "https://merchant.wish.com/api/v2/order/get-fulfill?"+params
        r = requests.get(url)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#履行订单
    def fulfill_orders(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'order_id' in execute_command:
            order_id = wish_common.is_null_field(execute_command['order_id'])
            params = params + '&id' + '=' + order_id
        if 'tracking_provider' in execute_command:
            tracking_provider = wish_common.is_null_field(execute_command['tracking_provider'])
            params = params + '&tracking_provider' + '=' + tracking_provider
        if 'tracking_number' in execute_command:
            tracking_number = wish_common.is_null_field(execute_command['tracking_number'])
            params = params + '&tracking_number' + '=' + tracking_number
        if 'origin_country_code' in execute_command:
            origin_country_code = wish_common.is_null_field(execute_command['origin_country_code'])
            params = params + '&origin_country_code' + '=' + origin_country_code
        if 'ship_note' in execute_command:
            ship_note = wish_common.is_null_field(execute_command['ship_note'])
            params = params + '&ship_note' + '=' + ship_note
        url = "https://merchant.wish.com/api/v2/order/fulfill-one?"+params
        r = requests.post(url)
        result = r.text
        return result


#退款/取消订单
    def refund_order(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'order_id' in execute_command:
            order_id = wish_common.is_null_field(execute_command['order_id'])
            params = params + '&id' + '=' + order_id
        if 'reason_code' in execute_command:
            reason_code = wish_common.is_null_field(execute_command['reason_code'])
            params = params + '&reason_code' + '=' + reason_code
        if 'reason_note' in execute_command:
            reason_note = wish_common.is_null_field(execute_command['reason_note'])
            params = params + '&reason_note' + '=' + reason_note
        url = "https://merchant.wish.com/api/v2/order/refund?" +params
        r = requests.post(url)
        result = r.text
        return result


#修改发运订单的跟踪   更新订单的跟踪信息
    def modify_track_ship_order(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'order_id' in execute_command:
            order_id = wish_common.is_null_field(execute_command['order_id'])
            params = params + '&id' + '=' + order_id
        if 'tracking_provider' in execute_command:
            tracking_provider = wish_common.is_null_field(execute_command['tracking_provider'])
            params = params + '&tracking_provider' + '=' + tracking_provider
        if 'tracking_number' in execute_command:
            tracking_number = wish_common.is_null_field(execute_command['tracking_number'])
            params = params + '&tracking_number' + '=' + tracking_number
        if 'origin_country_code' in execute_command:
            origin_country_code = wish_common.is_null_field(execute_command['origin_country_code'])
            params = params + '&origin_country_code' + '=' + origin_country_code
        if 'ship_note' in execute_command:
            ship_note = wish_common.is_null_field(execute_command['ship_note'])
            params = params + '&ship_note' + '=' + ship_note
        url = "https://merchant.wish.com/api/v2/order/modify-tracking?"+params
        r = requests.post(url)
        result = r.text
        return result


#在装运前修改订单的发货地址
    def modify_address_order(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'order_id' in execute_command:
            order_id = wish_common.is_null_field(execute_command['order_id'])
            params = params + '&id' + '=' + order_id
        if 'street_address1' in execute_command:
            street_address1 = wish_common.is_null_field(execute_command['street_address1'])
            params = params + '&street_address1' + '=' + street_address1
        if 'street_address2' in execute_command:
            street_address2 = wish_common.is_null_field(execute_command['street_address2'])
            params = params + '&street_address2' + '=' + street_address2
        if 'city' in execute_command:
            city = wish_common.is_null_field(execute_command['city'])
            params = params + '&city' + '=' + city
        if 'state' in execute_command:
            state = wish_common.is_null_field(execute_command['state'])
            params = params + '&state' + '=' + state
        if 'zipcode' in execute_command:
            zipcode = wish_common.is_null_field(execute_command['zipcode'])
            params = params + '&zipcode' + '=' + zipcode
        if 'phone_number' in execute_command:
            phone_number = wish_common.is_null_field(execute_command['phone_number'])
            params = params + '&phone_number' + '=' + phone_number
        url = "https://merchant.wish.com/api/v2/order/change-shipping?"+params
        r = requests.post(url)
        result = r.text
        return result


#启动批量订单下载
    def batch_order_download(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'end' in execute_command:
            end = wish_common.is_null_field(execute_command['end'])
            params = params + '&end' + '=' + end
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        if 'sort' in execute_command:
            sort = wish_common.is_null_field(execute_command['sort'])
            params = params + '&sort' + '=' + sort
        url = "https://merchant.wish.com/api/v2/order/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result


#获取批量订单下载的状态
    def batch_order_download_status(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/order/get-download-job-status?"+params
        r = requests.post(url)
        result = r.text
        return result


#取消批量订购下载
    def batch_order_download_cancel(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/order/cancel-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result



#获取需要确认交付的国家
    def get_countries_confirmed_delivery(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/order/get-confirmed-delivery-countries?"+params
        r = requests.post(url)
        result = r.text
        return result


#获得国家确认的送货船
    def get_shipping_for_country(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'country_code' in execute_command:
            country_code = wish_common.is_null_field(execute_command['country_code'])
            params = params + '&country_code' + '=' + country_code
        url = "https://merchant.wish.com/api/v2/order/get-confirmed-delivery-shipping-carriers-for-country?"+params
        r = requests.post(url)
        result = r.text
        return result







