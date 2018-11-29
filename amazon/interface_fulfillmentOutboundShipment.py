import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit
from test_file import test_interface

headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentOutboundShipment/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


#配送出库
class interface_fulfillmentOutboundShipment:

    def __init__(self):
        pass
    #根据您指定的送货条件返回配送订单预览列表
    #参数  Address   Items
    def GetFulfillmentPreview(execute_command):
        params = ['Action=GetFulfillmentPreview'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'address_name' in execute_command:
            if execute_command['address_name'] != '':
                params.append('Address.Name=' + execute_command['address_name'])
        if 'address_line1' in execute_command:
            if execute_command['address_line1'] != '':
                params.append('Address.Line1=' + execute_command['address_line1'])

        if 'address_line2' in execute_command:
            if execute_command['address_line2'] != '':
                params.append('Address.Line2=' + execute_command['address_line2'])
        if 'address_line3' in execute_command:
            if execute_command['address_line3'] != '':
                params.append('Address.Line3=' + execute_command['address_line3'])
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province'] != '':
                params.append('Address.StateOrProvinceCode=' + execute_command['state_or_province'])
        if 'post_code' in execute_command:
            if execute_command['post_code'] != '':
                params.append('Address.PostalCode=' + execute_command['post_code'])
        if 'country_code' in execute_command:
            if execute_command['country_code'] != '':
                params.append('Address.CountryCode=' + execute_command['country_code'])
        if 'address_city' in execute_command:
            if execute_command['address_city'] != '':
                params.append('Address.City=' + execute_command['address_city'])

        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('Items.member.' + str(quantity_list.index(q) + 1) + '.Quantity=' + q)
                params += quantity_param_list

        if 'order_item_id' in execute_command:
            if execute_command['order_item_id']!='':
                order_item_list = execute_command['order_item_id'].split(',')
                order_param_list = []
                for i in order_item_list:
                    order_param_list.append('Items.member.'+str(order_item_list.index(i)+1)+'.SellerFulfillmentOrderItemId='+i)
                params+=order_param_list

        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('Items.member.'+str(sku_list.index(i)+1)+'.SellerSKU='+i)
                params+=sku_param_list

        if 'ship_speed_category' in execute_command:
            if execute_command['ship_speed_category']!='':
                categry_list = execute_command['ship_speed_category'].split(',')
                category_param_list = []
                for i in categry_list:
                    category_param_list.append('ShippingSpeedCategories.'+str(categry_list.index(i)+1)+'='+i)
                params+=category_param_list

        if 'fulfillment_preview' in execute_command:
            if execute_command['fulfillment_preview'] != '':
                params.append('IncludeCODFulfillmentPreview=' + execute_command['fulfillment_preview'])

        if 'delivery_windows' in execute_command:
            if execute_command['delivery_windows'] != '':
                params.append('IncludeDeliveryWindows=' + execute_command['delivery_windows'])

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('%2B', "%20")
        params = params.replace(' ', "%20")
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    #要求亚马逊将来自亚马逊实现网络中卖方库存的项目运送到目的地地址
    #DisplayableOrderDateTime
    def CreateFulfillmentOrder(execute_command):
        params = ['Action=CreateFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'fulfillment_order_id' in execute_command:
            if execute_command['fulfillment_order_id']!='':
                params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))
        if 'fulfillment_action' in execute_command:
            if execute_command['fulfillment_action'] != '':
                params.append('FulfillmentAction='+quote(execute_command['fulfillment_action']))
        if 'display_order_id' in execute_command:
            if execute_command['display_order_id']!='':
                params.append('DisplayableOrderId=' + quote(execute_command['display_order_id']))
        if 'display_order_datetime' in execute_command:
            if execute_command['display_order_datetime']!='':
                order_datetime = execute_command['display_order_datetime']
                order_datetime = common_unit.conver_time(order_datetime)
                params.append('DisplayableOrderDateTime=' + quote(order_datetime))
        if 'display_order_comment' in execute_command:
            if execute_command['display_order_comment']!='':
                params.append('DisplayableOrderComment=' + quote(execute_command['display_order_comment']))
        if 'ship_speed_category' in execute_command:
            if execute_command['ship_speed_category']!='':
                params.append('ShippingSpeedCategory=' + quote(execute_command['ship_speed_category']))
        if 'address_name' in execute_command:
            if execute_command['address_name'] != '':
                params.append('DestinationAddress.Name=' + quote(execute_command['address_name']))
        if 'address_line1' in execute_command:
            if execute_command['address_line1'] != '':
                params.append('DestinationAddress.Line1=' + quote(execute_command['address_line1']))
        if 'address_line2' in execute_command:
            if execute_command['address_line2'] != '':
                params.append('DestinationAddress.Line2=' + quote(execute_command['address_line2']))
        if 'address_line3' in execute_command:
            if execute_command['address_line3'] != '':
                params.append('DestinationAddress.Line2=' + quote(execute_command['address_line3']))
        if 'district_or_country' in execute_command:
            if execute_command['district_or_country'] != '':
                params.append('DestinationAddress.DistrictOrCounty=' + quote(execute_command['district_or_country']))
        if 'address_city' in execute_command:
            if execute_command['address_city'] != '':
                params.append('DestinationAddress.City=' + execute_command['address_city'])
        if 'country_code' in execute_command:
            if execute_command['country_code'] != '':
                params.append('DestinationAddress.CountryCode=' + quote(execute_command['country_code']))
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province'] != '':
                params.append('DestinationAddress.StateOrProvinceCode=' + quote(execute_command['state_province_code']))
        if 'post_code' in execute_command:
            if execute_command['post_code'] != '':
                params.append('DestinationAddress.PostalCode=' + quote(execute_command['post_code']))
        if 'phone_number' in execute_command:
            if execute_command['phone_number'] != '':
                params.append('DestinationAddress.PhoneNumber=' + quote(execute_command['phone_number']))
        if 'fulfillment_policy' in execute_command:
            if execute_command['fulfillment_policy'] != '':
                params.append('FulfillmentPolicy='+ quote(execute_command['fulfillment_policy']))

        if 'notific_email_list' in execute_command:
            if execute_command['notific_email_list'] != '':
                email_list = execute_command['notific_email_list'].split(',')
                email_param_list = []
                for q in email_list:
                    email_param_list.append('NotificationEmailList.member.' + str(email_list.index(q) + 1) + '=' + q)
                params += email_param_list

        if 'iscod_required' in execute_command:
            if execute_command['iscod_required'] != '':
                params.append('CODSettings.IsCODRequired='+ quote(execute_command['iscod_required']))

        if 'codcharge_currency_code' in execute_command:
            if execute_command['codcharge_currency_code'] != '':
                params.append('CODSettings.CODCharge.CurrencyCode='+ quote(execute_command['codcharge_currency_code']))

        if 'codcharge_currency_value' in execute_command:
            if execute_command['codcharge_currency_value'] != '':
                params.append('CODSettings.CODCharge.Value='+ quote(execute_command['codcharge_currency_value']))

        if 'codcharge_tax_currency_code' in execute_command:
            if execute_command['codcharge_tax_currency_code'] != '':
                params.append('CODSettings.CODChargeTax.CurrencyCode='+ quote(execute_command['codcharge_tax_currency_code']))

        if 'codcharge_tax_currency_value' in execute_command:
            if execute_command['codcharge_tax_currency_value'] != '':
                params.append('CODSettings.CODChargeTax.Value='+ quote(execute_command['codcharge_tax_currency_value']))

        if 'ship_charge_currency_code' in execute_command:
            if execute_command['ship_charge_currency_code'] != '':
                params.append('CODSettings.ShippingCharge.CurrencyCode=' + quote(execute_command['ship_charge_currency_code']))

        if 'ship_charge_currency_value' in execute_command:
            if execute_command['ship_charge_currency_value'] != '':
                params.append('CODSettings.ShippingCharge.Value=' + quote(execute_command['ship_charge_currency_value']))

        if 'ship_charge_tax_currency_code' in execute_command:
            if execute_command['ship_charge_currency_code'] != '':
                params.append('CODSettings.ShippingChargeTax.CurrencyCode=' + quote(execute_command['ship_charge_tax_currency_code']))

        if 'ship_charge_tax_currency_value' in execute_command:
            if execute_command['ship_charge_tax_currency_value'] != '':
                params.append('CODSettings.ShippingChargeTax.Value=' + quote(execute_command['ship_charge_tax_currency_value']))

        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('Items.member.'+str(sku_list.index(i)+1)+'.SellerSKU='+i)
                params+=sku_param_list

        if 'order_item_id' in execute_command:
            if execute_command['order_item_id'] != '':
                sku_list = execute_command['order_item_id'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('Items.member.' + str(sku_list.index(i) + 1) + '.SellerFulfillmentOrderItemId=' + i)
                params += sku_param_list

        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('Items.member.' + str(quantity_list.index(q) + 1) + '.Quantity=' + q)
                params += quantity_param_list
        # params.append('Items.member.1.SellerSKU=' + quote(execute_command['sku']))
        # params.append('Items.member.1.SellerFulfillmentOrderItemId=' + quote(execute_command['order_item_id']))
        # params.append('Items.member.1.Quantity=' + quote(execute_command['quantity']))
        # params.append('Items.member.1.GiftMessage=' + quote(execute_command['gift_message']))
        # params.append('Items.member.1.DisplayableComment=' + quote(execute_command['dispaly_comment']))
        # params.append('Items.member.1.FulfillmentNetworkSKU=' + quote(execute_command['network_sku']))
        # params.append('Items.member.1.PerUnitDeclaredValue.CurrencyCode=' + quote(execute_command['puv_currency_code']))
        # params.append('Items.member.1.PerUnitDeclaredValue.Value=' + quote(execute_command['puv_value']))
        # params.append('Items.member.1.PerUnitPrice.CurrencyCode=' + quote(execute_command['pup_currency_code']))
        # params.append('Items.member.1.PerUnitPrice.Value=' + quote(execute_command['pup_value']))
        # params.append('Items.member.1.PerUnitTax.CurrencyCode=' + quote(execute_command['put_currency_code']))
        # params.append('Items.member.1.PerUnitTax.Value=' + quote(execute_command['put_value']))


        if 'start_time' in execute_command:
            st = execute_command['start_time']
            st = common_unit.conver_time(st)
            params.append('DeliveryWindow.StartDateTime=' + quote(st))

        if 'end_time' in execute_command:
            et = execute_command['end_time']
            et = common_unit.conver_time(et)
            params.append('DeliveryWindow.EndDateTime=' + quote(et))

        # params = params.replace('+', '%2B')
        # params = params.replace('/', '%2F')
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)

        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        # print(sig_string)
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        # print(url)
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



    #更新和/或请求订单完成订单的发货
    #请求参数   SellerFulfillmentOrderId  必须
    def UpdateFulfillmentOrder(execute_command):
        params = ['Action=UpdateFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)

        if 'fulfillment_order_id' in execute_command:
            if execute_command['fulfillment_order_id']!='':
                params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))
        if 'fulfillment_action' in execute_command:
            if execute_command['fulfillment_action'] != '':
                params.append('FulfillmentAction='+quote(execute_command['fulfillment_action']))
        if 'display_order_id' in execute_command:
            if execute_command['display_order_id']!='':
                params.append('DisplayableOrderId=' + quote(execute_command['display_order_id']))
        if 'display_order_datetime' in execute_command:
            if execute_command['display_order_datetime']!='':
                order_datetime = execute_command['display_order_datetime']
                order_datetime = common_unit.conver_time(order_datetime)
                params.append('DisplayableOrderDateTime=' + quote(order_datetime))
        if 'display_order_comment' in execute_command:
            if execute_command['display_order_comment']!='':
                params.append('DisplayableOrderComment=' + quote(execute_command['display_order_comment']))
        if 'ship_speed_category' in execute_command:
            if execute_command['ship_speed_category']!='':
                params.append('ShippingSpeedCategory=' + quote(execute_command['ship_speed_category']))
        if 'address_name' in execute_command:
            if execute_command['address_name'] != '':
                params.append('DestinationAddress.Name=' + quote(execute_command['address_name']))
        if 'address_line1' in execute_command:
            if execute_command['address_line1'] != '':
                params.append('DestinationAddress.Line1=' + quote(execute_command['address_line1']))
        if 'address_line2' in execute_command:
            if execute_command['address_line2'] != '':
                params.append('DestinationAddress.Line2=' + quote(execute_command['address_line2']))
        if 'address_line3' in execute_command:
            if execute_command['address_line3'] != '':
                params.append('DestinationAddress.Line2=' + quote(execute_command['address_line3']))
        if 'district_or_country' in execute_command:
            if execute_command['district_or_country'] != '':
                params.append('DestinationAddress.DistrictOrCounty=' + quote(execute_command['district_or_country']))
        if 'address_city' in execute_command:
            if execute_command['address_city'] != '':
                params.append('DestinationAddress.City=' + execute_command['address_city'])
        if 'country_code' in execute_command:
            if execute_command['country_code'] != '':
                params.append('DestinationAddress.CountryCode=' + quote(execute_command['country_code']))
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province'] != '':
                params.append('DestinationAddress.StateOrProvinceCode=' + quote(execute_command['state_province_code']))
        if 'post_code' in execute_command:
            if execute_command['post_code'] != '':
                params.append('DestinationAddress.PostalCode=' + quote(execute_command['post_code']))
        if 'phone_number' in execute_command:
            if execute_command['phone_number'] != '':
                params.append('DestinationAddress.PhoneNumber=' + quote(execute_command['phone_number']))
        if 'fulfillment_policy' in execute_command:
            if execute_command['fulfillment_policy'] != '':
                params.append('FulfillmentPolicy='+ quote(execute_command['fulfillment_policy']))
        if 'notific_email_list' in execute_command:
            if execute_command['notific_email_list'] != '':
                email_list = execute_command['notific_email_list'].split(',')
                email_param_list = []
                for q in email_list:
                    email_param_list.append('NotificationEmailList.member.' + str(email_list.index(q) + 1) + '=' + q)
                params += email_param_list
        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('Items.member.'+str(sku_list.index(i)+1)+'='+i)
                params+=sku_param_list

        if 'order_item_id' in execute_command:
            if execute_command['order_item_id'] != '':
                sku_list = execute_command['order_item_id'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('Items.member.' + str(sku_list.index(i) + 1) + '=' + i)
                params += sku_param_list

        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('Items.member.' + str(quantity_list.index(q) + 1) + '=' + q)
                params += quantity_param_list
        # params.append('Items.member.1.SellerSKU=' + quote(execute_command['sku']))
        # params.append('Items.member.1.SellerFulfillmentOrderItemId=' + quote(execute_command['order_item_id']))
        # params.append('Items.member.1.Quantity=' + quote(execute_command['quantity']))
        # params.append('Items.member.1.GiftMessage=' + quote(execute_command['gift_message']))
        # params.append('Items.member.1.DisplayableComment=' + quote(execute_command['dispaly_comment']))
        # params.append('Items.member.1.FulfillmentNetworkSKU=' + quote(execute_command['network_sku']))
        # params.append('Items.member.1.PerUnitDeclaredValue.CurrencyCode=' + quote(execute_command['puv_currency_code']))
        # params.append('Items.member.1.PerUnitDeclaredValue.Value=' + quote(execute_command['puv_value']))
        # params.append('Items.member.1.PerUnitPrice.CurrencyCode=' + quote(execute_command['pup_currency_code']))
        # params.append('Items.member.1.PerUnitPrice.Value=' + quote(execute_command['pup_value']))
        # params.append('Items.member.1.PerUnitTax.CurrencyCode=' + quote(execute_command['put_currency_code']))
        # params.append('Items.member.1.PerUnitTax.Value=' + quote(execute_command['put_value']))

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        print(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        signature = signature.replace('+', '%2B').replace('/', '%2F')
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)
        if error_result != '':
            result = error_result
        return result



    #返回在指定日期（或以后）完成的履行订单清单
    #参数  QueryStartDateTime
    def ListAllFulfillmentOrders(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            # result = common_unit.xmltojson(listAllfulfillmentOrder)
            # result = common_unit.read_xmlfile('test_file/listAllfulfillmentorder.xml')

            if 'start_time' in execute_command:
                if execute_command['start_time']!='':
                    start_time = execute_command['start_time']
                    start_date,time_stamp = common_unit.conver_date_time(start_time)
                    # print(start_time,time_stamp)
                    result = common_unit.xmltojson(listAllfulfillmentOrder)
                    result = test_interface.listAllfulfillmentOrders_between_time(start_date,result)

        else:
            params = ['Action=ListAllFulfillmentOrders'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            if 'start_time' in execute_command:
                if execute_command['start_time']!='':
                    st = execute_command['start_time']
                    st = common_unit.conver_time(st)
                    params.append('QueryStartDateTime=' + quote(st))
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            print(r.text)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result



    # 使用NextToken参数返回履行订单的下一页
    # 给进来参数[next_token]
    def ListAllFulfillmentOrdersByNextToken(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            result = common_unit.read_xmlfile('test_file/listAllfulfillmentorderbynextToken.xml')
            # result = common_unit.xmljson(listAllfulfillmentOrders)
            # result = test_interface.select_inboundlist_between_time(result)
        else:
            r = ''
            if 'next_token' in execute_command:
                if execute_command['next_token']!='':
                    ntoken = execute_command['next_token']
                    params = 'Action=ListAllFulfillmentOrdersByNextToken&NextToken=' + ntoken
                    url = 'https://' + host_name + port_point + '?' + params
                    r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    # 根据指定的SellerFulfillmentOrderId返回执行订单
    # 参数  order_id
    def GetFulfillmentOrder(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            # result = common_unit.read_xmlfile('test_file/getfulfillmentorder.xml')
            if 'fulfillment_order_id' in execute_command:
                if execute_command['fulfillment_order_id']!='':
                    fulfillment_order_id = execute_command['fulfillment_order_id']
                    result = common_unit.xmltojson(getfulfillmentOrder)
                    result = test_interface.getFulfillmentOrder(fulfillment_order_id,result)
        else:
            params = ['Action=GetFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            if 'fulfillment_order_id' in execute_command:
                if execute_command['fulfillment_order_id']!='':
                    params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            print(r.text)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)
            if error_result != '':
                result = error_result
        return result


    #返回多渠道配送订单的出货中包裹的配送跟踪信息
    #参数  PackageNumber  件号
    def GetPackageTrackingDetails(execute_command):
        params = ['Action=GetPackageTrackingDetails'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'package_number' in execute_command:
            if execute_command['package_number']!='':
                params.append('PackageNumber=' + quote(execute_command['package_number']))

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)
        if error_result != '':
            result = error_result
        return result


    #要求亚马逊停止尝试完成现有的配送订单
    def CancelFulfillmentOrder(execute_command):
        params = ['Action=CancelFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'fulfillment_order_id' in execute_command:
            if execute_command['fulfillment_order_id']!='':
                params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))

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

    # 返回给定 seller SKU的退货原因代码 描述 列表
    # 参数  order_id 可以为空   seller_sku 必须   Language 也是可以为空  格式如：fr_FR
    def ListReturnReasonCodes(execute_command):
        params = ['Action=ListReturnReasonCodes'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'fulfillment_order_id' in execute_command:
            if execute_command['fulfillment_order_id']!='':
                params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))
        if 'sku' in execute_command:
            if execute_command['sku']!='':
                params.append('SellerSKU=' + quote(execute_command['sku']))
        if 'language' in execute_command:
            if execute_command['language']!='':
                params.append('Language=' + quote(execute_command['language']))
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

    #创建一个 配送列表的返回
    def CreateFulfillmentReturn(execute_command):
        params = ['Action=CreateFulfillmentReturn'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)

        if 'fulfillment_order_id' in execute_command:
            if execute_command['fulfillment_order_id']!='':
                params.append('SellerFulfillmentOrderId=' + quote(execute_command['fulfillment_order_id']))

        if 'return_item_id' in execute_command:
            if execute_command['return_item_id']!='':
                return_item_list = execute_command['return_item_id'].split(',')
                return_param_list = []
                for i in return_item_list:
                    return_param_list.append('Items.member.'+str(return_item_list.index(i)+1)+'.SellerReturnItemId='+i)
                params+=return_param_list

        if 'order_item_id' in execute_command:
            if execute_command['order_item_id']!='':
                order_item_list = execute_command['order_item_id'].split(',')
                order_param_list = []
                for i in order_item_list:
                    order_param_list.append('Items.member.'+str(order_item_list.index(i)+1)+'.SellerFulfillmentOrderItemId='+i)
                params+=order_param_list

        if 'shipment_id' in execute_command:
            if execute_command['shipment_id']!='':
                ship_id_list = execute_command['shipment_id'].split(',')
                ship_param_list = []
                for i in ship_id_list:
                    ship_param_list.append('Items.member.'+str(ship_id_list.index(i)+1)+'.AmazonShipmentId='+i)
                params+=ship_param_list

        if 'reason_code' in execute_command:
            if execute_command['reason_code']!='':
                reason_code_list = execute_command['reason_code'].split(',')
                reason_code_param_list = []
                for i in reason_code_list:
                    reason_code_param_list.append('Items.member.'+str(reason_code_list.index(i)+1)+'.ReturnReasonCode='+i)
                params+=reason_code_param_list

        if 'comment' in execute_command:
            if execute_command['comment']!='':
                comment_list = execute_command['comment'].split(',')
                comment_param_list = []
                for i in comment_list:
                    comment_param_list.append('Items.member.'+str(comment_list.index(i)+1)+'.ReturnComment='+i)
                params+=comment_param_list

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)
        if error_result != '':
            result = error_result
        return result


    # 返回  配送出库 这块API的操作状态
    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)
        if error_result != '':
            result = error_result
        return result



listAllfulfillmentOrder = '''<ListAllFulfillmentOrdersResponse xmlns="http://mws.amazonaws.com/FulfillmentOutboundShipment/2010-10-01/">
  <ListAllFulfillmentOrdersResult>
    <FulfillmentOrders>
      <member>
        <SellerFulfillmentOrderId>CONSUMER-20180411-193056</SellerFulfillmentOrderId>
        <DestinationAddress>
          <PhoneNumber>7047951585</PhoneNumber>
          <City>CONCORD</City>
          <CountryCode>US</CountryCode>
          <PostalCode>28025-1273</PostalCode>
          <Name>Kathy Irminger</Name>
          <StateOrProvinceCode>NC</StateOrProvinceCode>
          <Line3/>
          <DistrictOrCounty/>
          <Line2/>
          <Line1>7015 ERINBROOK DR</Line1>
        </DestinationAddress>
        <DisplayableOrderDateTime>2018-04-11T07:00:00Z</DisplayableOrderDateTime>
        <ShippingSpeedCategory>Expedited</ShippingSpeedCategory>
        <FulfillmentMethod>Consumer</FulfillmentMethod>
        <FulfillmentOrderStatus>COMPLETE</FulfillmentOrderStatus>
        <StatusUpdatedDateTime>2018-04-12T09:12:54Z</StatusUpdatedDateTime>
        <FulfillmentPolicy>FillOrKill</FulfillmentPolicy>
        <ReceivedDateTime>2018-04-12T02:31:16Z</ReceivedDateTime>
        <DisplayableOrderId>CONSUMER-20180411-193056</DisplayableOrderId>
        <DisplayableOrderComment>感谢您的订购！</DisplayableOrderComment>
      </member>
      <member>
        <SellerFulfillmentOrderId>CONSUMER-20180410-023603</SellerFulfillmentOrderId>
        <DestinationAddress>
          <PhoneNumber>9567845826</PhoneNumber>
          <City>Victoria</City>
          <CountryCode>US</CountryCode>
          <PostalCode>77904</PostalCode>
          <Name>Jonathan Serna</Name>
          <StateOrProvinceCode>TX</StateOrProvinceCode>
          <Line3/>
          <DistrictOrCounty/>
          <Line2/>
          <Line1>209 Nantucket Ave. Apt I103</Line1>
        </DestinationAddress>
        <DisplayableOrderDateTime>2018-04-10T07:00:00Z</DisplayableOrderDateTime>
        <ShippingSpeedCategory>Standard</ShippingSpeedCategory>
        <FulfillmentMethod>Consumer</FulfillmentMethod>
        <FulfillmentOrderStatus>COMPLETE</FulfillmentOrderStatus>
        <StatusUpdatedDateTime>2018-04-12T09:39:20Z</StatusUpdatedDateTime>
        <FulfillmentPolicy>FillOrKill</FulfillmentPolicy>
        <ReceivedDateTime>2018-04-10T09:36:13Z</ReceivedDateTime>
        <DisplayableOrderId>CONSUMER-20180410-023603</DisplayableOrderId>
        <DisplayableOrderComment>感谢您的订购！</DisplayableOrderComment>
      </member>
      <member>
        <SellerFulfillmentOrderId>CONSUMER-20180411-193416</SellerFulfillmentOrderId>
        <DestinationAddress>
          <PhoneNumber>303-548-4101</PhoneNumber>
          <City>GREELEY</City>
          <CountryCode>US</CountryCode>
          <PostalCode>80634-4475</PostalCode>
          <Name>Sherry Nesmith</Name>
          <StateOrProvinceCode>CO</StateOrProvinceCode>
          <Line3/>
          <DistrictOrCounty/>
          <Line2/>
          <Line1>5401 W 6TH ST</Line1>
        </DestinationAddress>
        <DisplayableOrderDateTime>2018-04-11T07:00:00Z</DisplayableOrderDateTime>
        <ShippingSpeedCategory>Standard</ShippingSpeedCategory>
        <FulfillmentMethod>Consumer</FulfillmentMethod>
        <FulfillmentOrderStatus>COMPLETE</FulfillmentOrderStatus>
        <StatusUpdatedDateTime>2018-04-12T15:19:45Z</StatusUpdatedDateTime>
        <FulfillmentPolicy>FillOrKill</FulfillmentPolicy>
        <ReceivedDateTime>2018-04-12T02:34:26Z</ReceivedDateTime>
        <DisplayableOrderId>CONSUMER-20180411-193416</DisplayableOrderId>
        <DisplayableOrderComment>感谢您的订购！</DisplayableOrderComment>
      </member>
    </FulfillmentOrders>
  </ListAllFulfillmentOrdersResult>
  <ResponseMetadata>
    <RequestId>0213e1d5-397a-49a8-acd8-45f22fbee837</RequestId>
  </ResponseMetadata>
</ListAllFulfillmentOrdersResponse>'''


getfulfillmentOrder = '''<GetFulfillmentOrderResponse
      xmlns="http://mws.amazonaws.com/FulfillmentOutboundShipment/2010-10-01/">
      <GetFulfillmentOrderResult>
        <FulfillmentOrderItem>
          <member>
            <SellerSKU>SKU100</SellerSKU>
            <GiftMessage>giftwrap_message</GiftMessage>
            <SellerFulfillmentOrderItemId>merchant_order_item_id_2</SellerFulfillmentOrderItemId>
            <EstimatedShipDateTime>2018-09-03T07:07:53Z</EstimatedShipDateTime>
            <DisplayableComment>Example comment</DisplayableComment>
            <UnfulfillableQuantity>0</UnfulfillableQuantity>
            <CancelledQuantity>0</CancelledQuantity>
            <Quantity>1</Quantity>
            <EstimatedArrivalDateTime>2018-09-05T08:07:53Z</EstimatedArrivalDateTime>
            <PerUnitPrice>
              <CurrencyCode>JPY</CurrencyCode>
              <Value>2500</Value>
            </PerUnitPrice>
            <PerUnitTax>
              <CurrencyCode>JPY</CurrencyCode>
              <Value>5000</Value>
            </PerUnitTax>
          </member>
        </FulfillmentOrderItem>
        <FulfillmentOrder>
          <ShippingSpeedCategory>ScheduledDelivery</ShippingSpeedCategory>
          <NotificationEmailList>
            <member>o8c2EXAMPLsfr7o@marketplace.amazon.com</member>
          </NotificationEmailList>
          <StatusUpdatedDateTime>2018-09-05T23:48:48Z</StatusUpdatedDateTime>
          <SellerFulfillmentOrderId>extern_id_1154539615776</SellerFulfillmentOrderId>
          <DestinationAddress>
            <PostalCode>153-0002</PostalCode>
            <Name>Amazon Taro</Name>
            <CountryCode>JP</CountryCode>
            <Line1>Meguro-ku Shimomeguro 12-34-56</Line1>
            <StateOrProvinceCode>Tokyo</StateOrProvinceCode>
            <Line2>XXX building 101</Line2>
          </DestinationAddress>
          <DisplayableOrderDateTime>2018-09-02T17:26:56Z </DisplayableOrderDateTime>
          <FulfillmentPolicy>FillOrKill</FulfillmentPolicy>
          <ReceivedDateTime>2018-09-02T17:26:56Z</ReceivedDateTime>
          <DisplayableOrderId>test_displayable_id</DisplayableOrderId>
          <DisplayableOrderComment>Sample comment</DisplayableOrderComment>
          <CODSettings>
            <IsCODRequired>true</IsCODRequired>
            <CODCharge>
              <Value>4000</Value>
              <CurrencyCode>JPY</CurrencyCode>
            </CODCharge>
            <CODChargeTax>
              <Value>300</Value>
              <CurrencyCode>JPY</CurrencyCode>
            </CODChargeTax>
            <ShippingCharge>
              <Value>1000</Value>
              <CurrencyCode>JPY</CurrencyCode>
            </ShippingCharge>
            <ShippingChargeTax>
              <Value>75</Value>
              <CurrencyCode>JPY</CurrencyCode>
            </ShippingChargeTax>
          </CODSettings>
          <FulfillmentOrderStatus>PROCESSING</FulfillmentOrderStatus>
          <FulfillmentAction>Ship</FulfillmentAction>
          <MarketplaceId>ATVPDKIKX0DER </MarketplaceId>
        </FulfillmentOrder>
        <FulfillmentShipment>
          <member>
            <FulfillmentShipmentStatus>PENDING</FulfillmentShipmentStatus>
            <FulfillmentShipmentItem>
              <member>
                <SellerSKU>SKU100</SellerSKU>
                <SellerFulfillmentOrderItemId>merchant_order_item_id_2</SellerFulfillmentOrderItemId>
                <Quantity>1</Quantity>
                <PackageNumber>0</PackageNumber>
              </member>
            </FulfillmentShipmentItem>
            <AmazonShipmentId>DnMDLWJWN</AmazonShipmentId>
            <ShippingDateTime>2018-09-03T07:00:00Z</ShippingDateTime>
            <FulfillmentCenterId>RNO1</FulfillmentCenterId>
            <EstimatedArrivalDateTime>2018-09-04T07:00:00Z
              </EstimatedArrivalDateTime>
          </member>
        </FulfillmentShipment>
      </GetFulfillmentOrderResult>
      <ResponseMetadata>
        <RequestId>5e5e5694-8e76-11df-929f-87c80302f8f6</RequestId>
      </ResponseMetadata>
    </GetFulfillmentOrderResponse>
'''