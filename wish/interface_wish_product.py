#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common
from common_methods import common_unit
params = ''


class Product:

    def __init__(self):
        pass


    #创建产品
    def create_product(execute_command):
        params = 'access_token'+'='+execute_command['access_token']
        if 'main_image' in execute_command:
            main_image = wish_common.is_null_field(execute_command['main_image'])
            params = params+'&main_image'+'='+main_image
        if 'name' in execute_command:
            name = wish_common.is_null_field(execute_command['name'])
            params = params + '&name' + '=' + name
        if 'description' in execute_command:
            description = wish_common.is_null_field(execute_command['description'])
            params = params + '&description' + '=' + description
        if 'tags' in execute_command:
            tags = wish_common.is_null_field(execute_command['tags'])
            params = params + '&tags' + '=' + tags
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        if 'inventory' in execute_command:
            inventory = wish_common.is_null_field(execute_command['inventory'])
            params = params + '&inventory' + '=' + inventory
        if 'price' in execute_command:
            price = wish_common.is_null_field(execute_command['price'])
            params = params + '&price' + '=' + price
        if 'shipping' in execute_command:
            shipping = wish_common.is_null_field(execute_command['shipping'])
            params = params + '&shipping' + '=' + shipping
        if 'extra_images' in execute_command:
            extra_images = wish_common.is_null_field(execute_command['extra_images'])
            params = params + '&extra_images' + '=' + extra_images
        if 'parent_sku' in execute_command:
            parent_sku = wish_common.is_null_field(execute_command['parent_sku'])
            params = params + '&parent_sku' + '=' + parent_sku
        url = "https://merchant.wish.com/api/v2/product/add?"+params
        r = requests.post(url)
        result = r.text
        return result

    #创建变种产品
    def create_variation_product(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        sku = quote(execute_command['sku'])
        inventory = quote(execute_command['inventory'])
        price = quote(execute_command['price'])
        shipping = quote(execute_command['shipping'])
        size = quote(execute_command['size'])
        parent_sku = quote(execute_command['parent_sku'])
        url = "https://merchant.wish.com/api/v2/variant/add?access_token=%s&sku=%s&inventory=%s&price=%s&shipping=%s&size=%s&parent_sku=%s" %(access_token,sku,inventory,price,shipping,size,parent_sku)
        r = requests.post(url)
        result = r.text
        return result



    #检索产品
    #produt_id 或者  parent_sku   两者取其一
    def retrieve_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'parent_sku' in execute_command:
            parent_sku = wish_common.is_null_field(execute_command['parent_sku'])
            params = params + '&parent_sku' + '=' + parent_sku
        url = "https://merchant.wish.com/api/v2/product?"+params
        r = requests.post(url)
        result = r.text
        return result


    #检索变种产品
    def retrieve_variation_product(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        sku = quote(execute_command['sku'])
        url = "https://merchant.wish.com/api/v2/variant?access_token=%s&id=%s"%(access_token,sku)
        r = requests.post(url)
        result = r.text
        return result


    #编辑产品
    #produt_id 或者  parent_sku   两者取其一
    def update_product(execute_command):
        # access_token = wish_common.get_wish_access(execute_command['store_id'])
        # product_id = quote(execute_command['product_id'])
        # name = quote(execute_command['name'])
        # description = quote(execute_command['description'])
        # tags = quote(execute_command['tags'])

        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'name' in execute_command:
            name = wish_common.is_null_field(execute_command['name'])
            params = params + '&name' + '=' + name
        if 'description' in execute_command:
            description = wish_common.is_null_field(execute_command['description'])
            params = params + '&description' + '=' + description
        if 'tags' in execute_command:
            tags = wish_common.is_null_field(execute_command['tags'])
            params = params + '&tags' + '=' + tags
        url = "https://merchant.wish.com/api/v2/product/update?"+params
        r = requests.post(url)
        result = r.text
        return result


    #编辑变种产品信息
    def update_variation_product(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        sku = quote(execute_command['sku'])
        inventory =  quote(execute_command['inventory'])
        price = quote(execute_command['price'])
        shipping = quote(execute_command['shipping'])
        url = "https://merchant.wish.com/api/v2/product/variant/update?access_token=%s&sku=%s&inventory=%s&price=%s&shipping=%s" %(access_token,sku,inventory,price,shipping)
        r = requests.post(url)
        result = r.text
        return result


    #编辑变种产品的sku
    def change_variation_product_sku(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        sku = quote(execute_command['sku'])
        new_sku = quote(execute_command['new_sku'])
        url = "https://merchant.wish.com/api/v2/variant/change-sku??access_token=%s&sku=%s&new_sku=%s"%(access_token,sku,new_sku)
        r = requests.post(url)
        result = r.text
        return result


    # 启用产品
    # produt_id 或者  parent_sku   两者取其一
    def enable_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        url = "https://merchant.wish.com/api/v2/product/enable?"+params
        r = requests.post(url)
        result = r.text
        return result


    # 启用变种产品
    def enable_variation_product(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
        url = "https://merchant.wish.com/api/v2/variant/enable?access_token=%s&sku=%s"%(access_token,sku)
        r = requests.post(url)
        result = r.text
        return result


    #禁用产品
    #produt_id 或者  parent_sku   两者取其一
    def disable_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        url = "https://merchant.wish.com/api/v2/product/disable?"+params
        r = requests.post(url)
        result = r.text
        return result


    # 禁用变种产品
    def disable_variation_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        url = "https://merchant.wish.com/api/v2/variant/disable?"+params
        r = requests.post(url)
        result = r.text
        return result


    #更新  变种
    def update_inventory(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        if 'inventory' in execute_command:
            inventory = wish_common.is_null_field(execute_command['inventory'])
            params = params + '&inventory' + '=' + inventory
        if 'warehouse_name' in execute_command:
            warehouse_name = wish_common.is_null_field(execute_command['warehouse_name'])
            params = params + '&warehouse_name' + '=' + warehouse_name
        url = "https://merchant.wish.com/api/v2/variant/update-inventory?"+params
        r = requests.post(url)
        result = r.text
        return result


    #获取所有变种产品
    #参数 start / limit      类型为integer
    def list_all_variation_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
            params = params + '&start' + '=' + start
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        if 'warehouse_name' in execute_command:
            warehouse_name = wish_common.is_null_field(execute_command['warehouse_name'])
            params = params + '&warehouse_name' + '=' + warehouse_name
        url = "https://merchant.wish.com/api/v2/variant/multi-get?"+params
        r = requests.post(url)
        result = r.text
        return result

    def bulk_update_variation_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'updates' in execute_command:
            updates = wish_common.is_null_field(execute_command['updates'])
            params = params + '&updates' + '=' + updates
        url = "https://merchant.wish.com/api/v2/variant/bulk-sku-update?format=json"+params
        r = requests.post(url)
        result = r.text
        return result

    def bulk_update_variation_job_status(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/variant/get-bulk-update-job-status?"+params
        r = requests.post(url)
        result = r.text
        return result


    def bulk_update_variation_job_success(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
        url = "https://merchant.wish.com/api/v2/variant/get-bulk-update-job-successes?job_id=%s&access_token=%s&start=%s&limit=%s"%(job_id,access_token,start,limit)
        r = requests.post(url)
        result = r.text
        return result

    def bulk_update_variation_job_errors(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/variant/get-bulk-update-job-failures?"+params
        r = requests.post(url)
        result = r.text
        return result



    #全部产品列表
    def list_all_product(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
        if 'start' in execute_command:
            start = wish_common.is_null_field(execute_command['start'])
        if 'since' in execute_command:
            since = wish_common.is_null_field(execute_command['since'])
        if 'upto' in execute_command:
            upto = wish_common.is_null_field(execute_command['upto'])
        if 'show_rejected' in execute_command:
            show_rejected = wish_common.is_null_field(execute_command['show_rejected'])
        if 'warehouse_name' in execute_command:
            warehouse_name = wish_common.is_null_field(execute_command['warehouse_name'])

        url = "https://merchant.wish.com/api/v2/product/multi-get?access_token=%s&limit=%s&start=%s"%(access_token,limit,start)
        r = requests.post(url)
        result = r.text
        return result


    #从产品中移除多余的图像
    #produt_id 或者  parent_sku   两者取其一
    def remove_extra_images(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'sku' in execute_command:
            sku = wish_common.is_null_field(execute_command['sku'])
            params = params + '&sku' + '=' + sku
        url = "https://merchant.wish.com/api/v2/product/remove-extra-images?"+params
        r = requests.post(url)
        result = r.text
        return result



    #编辑产品的运输价格
    def edit_ship_price(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
        if 'country' in execute_command:
            country = wish_common.is_null_field(execute_command['country'])
        if 'price' in execute_command:
            price = wish_common.is_null_field(execute_command['price'])
        if 'wish_express' in execute_command:
            wish_express = wish_common.is_null_field(execute_command['wish_express'])
        url = "https://merchant.wish.com/api/v2/product/update-shipping?access_token=%s&id=%s&country=%s&price=%s&wish_express=%s"%(access_token,product_id,country,price,wish_express)
        r = requests.post(url)
        result = r.text
        return result


    def edit_multiple_ship_price(execute_command):
        if 'access_token' in execute_command:
            access_token = wish_common.is_null_field(execute_command['access_token'])
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
        if 'CA' in execute_command:
            CA = quote(execute_command['CA'])
        if 'AU' in execute_command:
            AU = quote(execute_command['AU'])
        if 'use_product_shipping_countries' in execute_command:
            use_product_shipping_countries = quote(execute_command['use_product_shipping_countries'])
        if 'disabled_countries' in execute_command:
            disabled_countries = quote(execute_command['disabled_countries'])
        if 'wish_express_add_countries' in execute_command:
            wish_express_add_countries = quote(execute_command['wish_express_add_countries'])
        if 'wish_express_remove_countries' in execute_command:
            wish_express_remove_countries = quote(execute_command['wish_express_remove_countries'])
        if 'default_shipping_price' in execute_command:
            default_shipping_price = quote(execute_command['default_shipping_price'])
        if 'warehouse_name' in execute_command:
            warehouse_name = quote(execute_command['warehouse_name'])
        url = "https://merchant.wish.com/api/v2/product/update-multi-shipping?access_token=%s&id=%s&CA=%s&AU=%s&use_product_shipping_countries=%s&disabled_countries=%s&" \
              "wish_express_add_countries=%s&wish_express_remove_countries=%s&default_shipping_price=%s&warehouse_name=%s"%(access_token, product_id, CA, AU, use_product_shipping_countries, disabled_countries,wish_express_add_countries,wish_express_remove_countries,default_shipping_price,warehouse_name)
        r = requests.post(url)
        result = r.text
        return result


    #获取产品的航运价格
    #produt_id 或者  parent_sku   两者取其一
    def get_shipping_price(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        if 'country' in execute_command:
            country = wish_common.is_null_field(execute_command['country'])
            params = params + '&country' + '=' + country
        url = "https://merchant.wish.com/api/v2/product/get-shipping?"+params
        r = requests.post(url)
        result = r.text
        return result


    #获得产品的所有运费
    # produt_id 或者  parent_sku   两者取其一
    def get_all_shipping_price(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        url = "https://merchant.wish.com/api/v2/product/get-all-shipping?"+params
        r = requests.post(url)
        result = r.text
        return result


    #获得许多产品的运输价格
    #ids = 123456789009876543211234,111122223333444455556666
    def get_ship_price_many_product(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'product_id' in execute_command:
            product_id = wish_common.is_null_field(execute_command['product_id'])
            params = params + '&id' + '=' + product_id
        url = "https://merchant.wish.com/api/v2/product/get-products-shipping?"+params
        r = requests.post(url)
        result = r.text
        return result

    #获取商家航运设置
    def get_shipping_setting(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        url = "https://merchant.wish.com/api/v2/product/get-shipping-setting?"+params
        r = requests.post(url)
        result = r.text
        return result


    #启动批量产品下载
    #since = 2016-07-01
    def batch_product_download(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'since' in execute_command:
            since = wish_common.is_null_field(execute_command['since'])
            params = params + '&since' + '=' + since
        if 'limit' in execute_command:
            limit = wish_common.is_null_field(execute_command['limit'])
            params = params + '&limit' + '=' + limit
        if 'sort' in execute_command:
            sort = wish_common.is_null_field(execute_command['sort'])
            params = params + '&sort' + '=' + sort
        if 'show_rejected' in execute_command:
            show_rejected = wish_common.is_null_field(execute_command['show_rejected'])
            params = params + '&show_rejected' + '=' + show_rejected
        if 'warehouse_name' in execute_command:
            warehouse_name = wish_common.is_null_field(execute_command['warehouse_name'])
            params = params + '&warehouse_name' + '=' + warehouse_name
        url = "https://merchant.wish.com/api/v2/product/create-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result


    #获取批量产品下载的状态
    def batch_product_download_status(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/product/get-download-job-status?"+params
        r = requests.post(url)
        result = r.text
        return result

    #取消批量产品下载
    def cancel_batch_product_download(execute_command):
        params = 'access_token' + '=' + execute_command['access_token']
        if 'job_id' in execute_command:
            job_id = wish_common.is_null_field(execute_command['job_id'])
            params = params + '&job_id' + '=' + job_id
        url = "https://merchant.wish.com/api/v2/product/cancel-download-job?"+params
        r = requests.post(url)
        result = r.text
        return result

