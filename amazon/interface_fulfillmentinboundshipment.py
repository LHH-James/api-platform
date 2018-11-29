import sys

import time

sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit
import xmltodict
import json
from test_file import test_interface


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentInboundShipment/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


def xmljson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = json.dumps(xmlparse, indent=1)
    return jsonstr

class interface_fulfillmentinboundshipment:
    def __init__(self):
        pass



    def GetInboundGuidanceForSKU(execute_command):
        params = ['Action=GetInboundGuidanceForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'sku' in execute_command:
            if execute_command['sku'] != '':
                seller_sku_list = execute_command['sku'].split(',')
                seller_sku_param_list = []
                for i in seller_sku_list:
                    seller_sku_param_list.append('SellerSKUList.Id.'+str(seller_sku_list.index(i)+1)+'='+i)
                params+=seller_sku_param_list
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('/', '%2F')
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def GetInboundGuidanceForASIN(execute_command):
        params = ['Action=GetInboundGuidanceForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'asin' in execute_command:
            if execute_command['asin']!='':
                asin_list = execute_command['asin'].split(',')
                asin_param_list = []
                for i in asin_list:
                    asin_param_list.append('ASINList.ASIN.'+str(asin_list.index(i)+1)+'='+i)
                params+=asin_param_list

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def CreateInboundShipmentPlan(execute_command):
        params = ['Action=CreateInboundShipmentPlan']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'address_name' in execute_command:
            if execute_command['address_name']!='':
                params += ['ShipFromAddress.Name='+execute_command['address_name']]
        if 'address_line1' in execute_command:
            if execute_command['address_line1']!='':
                params += ['ShipFromAddress.AddressLine1='+execute_command['address_line1']]
        if 'address_line2' in execute_command:
            if execute_command['address_line2']!='':
                params += ['ShipFromAddress.AddressLine2='+execute_command['address_line2']]
        if 'address_city' in execute_command:
            if execute_command['address_city']!='':
                params += ['ShipFromAddress.City='+execute_command['address_city']]
        if 'district_or_country' in execute_command:
            if execute_command['district_or_country']!='':
                params += ['ShipFromAddress.DistrictOrCounty='+execute_command['district_or_country']]
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province']!='':
                params += ['ShipFromAddress.StateOrProvinceCode='+execute_command['state_or_province']]
        if 'post_code' in execute_command:
            if execute_command['post_code']!='':
                params += ['ShipFromAddress.PostalCode=' + execute_command['post_code']]
        if 'country_code' in execute_command:
            if execute_command['country_code']!='':
                params += ['ShipFromAddress.CountryCode='+execute_command['country_code']]
        if 'label_preference' in execute_command:
            if execute_command['label_preference']!='':
                params += ['LabelPrepPreference='+execute_command['label_preference']]
        if 'sku' in execute_command:
            if execute_command['sku'] != '':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('InboundShipmentPlanRequestItems.member.' + str(sku_list.index(i) + 1) + '.SellerSKU=' + i)
                params+=sku_param_list

        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('InboundShipmentPlanRequestItems.member.' + str(quantity_list.index(q) + 1) + '.Quantity=' + q)
                params+=quantity_param_list

        params += default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+','%2B')
        params = params.replace('%2B', "%20")
        params = params.replace(' ', "%20")
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # print(sig_string)
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        # print(url)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    #创建入境货物
    def CreateInboundShipment(execute_command):
        params = ['Action=CreateInboundShipment'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(execute_command)
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id']!='':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        if 'shipment_name' in execute_command:
            if execute_command['shipment_name']!='':
                params += ['InboundShipmentHeader.ShipmentName=' + execute_command['shipment_name']]

        if 'address_name' in execute_command:
            if execute_command['address_name']!='':
                params += ['InboundShipmentHeader.ShipFromAddress.Name=' + execute_command['address_name']]
        if 'address_line1' in execute_command:
            if execute_command['address_line1'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.AddressLine1=' + execute_command['address_line1']]
        if 'address_line2' in execute_command:
            if execute_command['address_line2']!='':
                params += ['InboundShipmentHeader.ShipFromAddress.AddressLine2=' + execute_command['address_line2']]
        if 'address_city' in execute_command:
            if execute_command['address_city'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.City=' + execute_command['address_city']]
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.StateOrProvinceCode=' + execute_command['state_or_province']]
        if 'post_code' in execute_command:
            if execute_command['post_code'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.PostalCode=' + execute_command['post_code']]
        if 'country_code' in execute_command:
            if execute_command['country_code'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.CountryCode=' + execute_command['country_code']]
        if 'fulfillment__center_id' in execute_command:
            if execute_command['fulfillment__center_id'] != '':
                # params += ['InboundShipmentHeader.DestinationFulfillmentCenterId=MDT2']
                params += ['InboundShipmentHeader.DestinationFulfillmentCenterId='+execute_command['fulfillment__center_id']]
        if 'shipment_status' in execute_command:
            if execute_command['shipment_status'] != '':
                params += ['InboundShipmentHeader.ShipmentStatus='+execute_command['shipment_status']]
        if 'label_preference' in execute_command:
            if execute_command['label_preference'] != '':
                # params += ['InboundShipmentHeader.LabelPrepPreference=SELLER_LABEL']
                params += ['InboundShipmentHeader.LabelPrepPreference='+execute_command['label_preference']]
        if 'content_source' in execute_command:
            if execute_command['content_source'] != '':
                # params += ['InboundShipmentHeader.IntendedBoxContentsSource=FEED']
                params += ['InboundShipmentHeader.IntendedBoxContentsSource='+execute_command['content_source']]

        if 'fulfillment_network_sku' in execute_command:
            if execute_command['fulfillment_network_sku'] != '':
                params += ['InboundShipmentItems.FulfillmentNetworkSKU=' + execute_command['fulfillment_network_sku']]

        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('InboundShipmentItems.member.'+str(sku_list.index(i)+1)+'.SellerSKU='+i)
                params+=sku_param_list
        # params += ['InboundShipmentItems.member.1.SellerSKU=' + execute_command['sku']]
        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('InboundShipmentItems.member.' + str(quantity_list.index(q) + 1) + '.QuantityShipped=' + q)
                params += quantity_param_list
        # params += ['InboundShipmentItems.member.1.QuantityShipped=' + execute_command['quantity']]
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




    def UpdateInboundShipment(execute_command):
        params = ['Action=UpdateInboundShipment'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(execute_command)
        params += ['ShipmentId=' + execute_command['shipment_id']]

        if 'shipment_name' in execute_command:
            if execute_command['shipment_name']!='':
                params += ['InboundShipmentHeader.ShipmentName=' + execute_command['shipment_name']]

        if 'address_name' in execute_command:
            if execute_command['address_name']!='':
                params += ['InboundShipmentHeader.ShipFromAddress.Name=' + execute_command['address_name']]
        if 'address_line1' in execute_command:
            if execute_command['address_line1'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.AddressLine1=' + execute_command['address_line1']]
        if 'address_line2' in execute_command:
            if execute_command['address_line2']!='':
                params += ['InboundShipmentHeader.ShipFromAddress.AddressLine2=' + execute_command['address_line2']]
        if 'address_city' in execute_command:
            if execute_command['address_city'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.City=' + execute_command['address_city']]
        if 'state_or_province' in execute_command:
            if execute_command['state_or_province'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.StateOrProvinceCode=' + execute_command['state_or_province']]
        if 'post_code' in execute_command:
            if execute_command['post_code'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.PostalCode=' + execute_command['post_code']]
        if 'country_code' in execute_command:
            if execute_command['country_code'] != '':
                params += ['InboundShipmentHeader.ShipFromAddress.CountryCode=' + execute_command['country_code']]
        if 'fulfillment__center_id' in execute_command:
            if execute_command['fulfillment__center_id'] != '':
                # params += ['InboundShipmentHeader.DestinationFulfillmentCenterId=MDT2']
                params += ['InboundShipmentHeader.DestinationFulfillmentCenterId='+execute_command['fulfillment__center_id']]
        if 'shipment_status' in execute_command:
            if execute_command['shipment_status'] != '':
                params += ['InboundShipmentHeader.ShipmentStatus='+execute_command['shipment_status']]
        if 'label_preference' in execute_command:
            if execute_command['label_preference'] != '':
                # params += ['InboundShipmentHeader.LabelPrepPreference=SELLER_LABEL']
                params += ['InboundShipmentHeader.LabelPrepPreference='+execute_command['label_preference']]
        if 'content_source' in execute_command:
            if execute_command['content_source'] != '':
                # params += ['InboundShipmentHeader.IntendedBoxContentsSource=FEED']
                params += ['InboundShipmentHeader.IntendedBoxContentsSource='+execute_command['content_source']]

        if 'fulfillment_network_sku' in execute_command:
            if execute_command['fulfillment_network_sku'] != '':
                params += ['InboundShipmentItems.FulfillmentNetworkSKU=' + execute_command['fulfillment_network_sku']]

        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('InboundShipmentItems.member.'+str(sku_list.index(i)+1)+'.SellerSKU='+i)
                params+=sku_param_list
        # params += ['InboundShipmentItems.member.1.SellerSKU=' + execute_command['sku']]
        if 'quantity' in execute_command:
            if execute_command['quantity'] != '':
                quantity_list = execute_command['quantity'].split(',')
                quantity_param_list = []
                for q in quantity_list:
                    quantity_param_list.append('InboundShipmentItems.member.' + str(quantity_list.index(q) + 1) + '.QuantityShipped=' + q)
                params += quantity_param_list
        # params += ['InboundShipmentItems.member.1.QuantityShipped=' + execute_command['quantity']]

        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('+', '%2B')
        params = params.replace('%2B', "%20")
        params = params.replace(' ', "%20")
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



    def GetPreorderInfo(execute_command):
        params = ['Action=GetPreorderInfo']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(execute_command)
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id']!='':
                params += ['ShipmentId='+execute_command['shipment_id']]   # 添加货运单编号
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def ConfirmPreorder(execute_command):
        params = ['Action=ConfirmPreorder']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id']!='':
                params += ['ShipmentId='+execute_command['shipment_id']]   # 添加运单编号

        if 'need_by_date' in execute_command:
            if execute_command['need_by_date']!='':
                # params += ['NeedByDate='+common_unit.timestamp_to_datetime(execute_command['need_by_time'])]
                params += ['NeedByDate='+(execute_command['need_by_date'])]

        params += default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # print(sig_string)
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        url = connect_url(params,signature)
        # print(url)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetPrepInstructionsForSKU(execute_command):
        params = ['Action=GetPrepInstructionsForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'sku' in execute_command:
            if execute_command['sku'] != '':
                seller_sku_list = execute_command['sku'].split(',')
                seller_sku_param_list = []
                for i in seller_sku_list:
                    seller_sku_param_list.append('SellerSKUList.Id.'+str(seller_sku_list.index(i)+1)+'='+i)
                params+=seller_sku_param_list
        if 'ship_to_country_code' in execute_command:
            if execute_command['ship_to_country_code'] !='':
                params+=['ShipToCountryCode=' + quote(execute_command['ship_to_country_code'])]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetPrepInstructionsForASIN(execute_command):
        params = ['Action=GetPrepInstructionsForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)

        if 'asin' in execute_command:
            if execute_command['asin']!='':
                asin_list = execute_command['asin'].split(',')
                asin_param_list = []
                for i in asin_list:
                    asin_param_list.append('ASINList.ASIN.'+str(asin_list.index(i)+1)+'='+i)
                params+=asin_param_list

        if 'ship_to_country_code' in execute_command:
            if execute_command['ship_to_country_code'] !='':
                params += ['ShipToCountryCode=' + quote(execute_command['ship_to_country_code'])]
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    #向亚马逊发送关于入境货物的运输信息
    def PutTransportContent(execute_command):
        params = ['Action=PutTransportContent'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id']!='':
                params += ['ShipmentId=' + execute_command['shipment_id']]

        if 'is_partner' in execute_command:
            if execute_command['is_partner'] != '':
                params += ['IsPartnered=' + execute_command['is_partner']]

        if 'shipment_type' in execute_command:
            if execute_command['shipment_type'] != '':
                params += ['ShipmentType=' + execute_command['shipment_type']]

        params = sorted(params)
        params = '&'.join(params)
        params = params + default_params
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    def EstimateTransportRequest(execute_command):
        params = ['Action=EstimateTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetTransportContent(execute_command):
        params = ['Action=GetTransportContent']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def ConfirmTransportRequest(execute_command):
        params = ['Action=ConfirmTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def VoidTransportRequest(execute_command):
        params = ['Action=VoidTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetPackageLabels(execute_command):
        params = ['Action=GetPackageLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        if 'page_type' in execute_command:
            if execute_command['page_type'] != '':
                params += ['PageType='+execute_command['page_type']]
                # params += ['PageType=PackageLabel_Plain_Paper']
        if 'number_of_page' in execute_command:
            if execute_command['page_type'] != '':
                params += ['NumberOfPackages='+execute_command['number_of_page']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result
        
    def GetUniquePackageLabels(execute_command):
        params = ['Action=GetUniquePackageLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(execute_command)
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        if 'page_type' in execute_command:
            if execute_command['page_type'] != '':
                params += ['PageType=' + execute_command['page_type']]
        if 'carton' in execute_command:
            if execute_command['carton'] != '':
                carton_list = execute_command['carton'].split(',')
                carton_param_list = []
                for i in carton_list:
                    carton_param_list.append('PackageLabelsToPrint.member.' + str(carton_list.index(i) + 1) + '=' + i)
                params += carton_param_list
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetPalletLabels(execute_command):
        params = ['Action=GetPalletLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        if 'page_type' in execute_command:
            if execute_command['page_type'] != '':
                params += ['PageType=' + execute_command['page_type']]
        params += ['NumberOfPallets=4']
        if 'number_pallet' in execute_command:
            if execute_command['number_pallet'] != '':
                params += ['NumberOfPallets=' + execute_command['number_pallet']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        return common_unit.xmltojson(r.text)

    def GetBillOfLading(execute_command):
        params = ['Action=GetBillOfLading']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params = params + default_params
        if 'shipment_id' in execute_command:
            if execute_command['shipment_id'] != '':
                params += ['ShipmentId=' + execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def ListInboundShipments(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            # result = common_unit.read_xmlfile('test_file/listinboundshipments.xml')
            if ('last_updated_before' in execute_command) and ('last_updated_after' in execute_command):
                start_time = execute_command['last_updated_after']
                end_time = execute_command['last_updated_before']
                result = xmljson(inboundStr)
                result = test_interface.select_inboundlist_between_time(start_time,end_time,result)
        else:
            params = ['Action=ListInboundShipments'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            params = params + default_params
            if 'shipment_status' in execute_command:
                if execute_command['shipment_status'] != '':
                    status_list = execute_command['shipment_status'].split(',')
                    status_param_list = []
                    for i in status_list:
                        status_param_list.append('ShipmentStatusList.member.' + str(status_list.index(i) + 1) + '=' + i)
                    params += status_param_list
            if 'last_updated_before' in execute_command:
                if execute_command['last_updated_before']!='':
                    end_time = common_unit.conver_time(execute_command['last_updated_before'])
                    params += ['LastUpdatedAfter=' + quote(end_time)]
            if 'last_updated_after' in execute_command:
                if execute_command['last_updated_after'] != '':
                    start_time = common_unit.conver_time(execute_command['last_updated_after'])
                    params += ['LastUpdatedBefore=' + quote(start_time)]

            if 'shipmentid_list' in execute_command:
                if execute_command['shipmentid_list'] != '':
                    shipid_list = execute_command['shipmentid_list'].split(',')
                    shipid_param_list = []
                    for i in shipid_list:
                        shipid_param_list.append('ShipmentIdList.member.' + str(shipid_list.index(i) + 1) + '=' + i)
                    params += shipid_param_list
            # 添加时间区间或者运单id，二者只能存在一样
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            # print(r.text)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    def ListInboundShipmentsByNextToken(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            result = common_unit.read_xmlfile('test_file/listinboundshipmentsbyNexttoken.xml')
        else:
            params = ['Action=ListInboundShipmentsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'next_token' in execute_command:
                if execute_command['next_token'] != '':
                    params.append('NextToken=' + (quote(execute_command['next_token'])))  # 取上一个接口 NextToken的返回值
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



    def ListInboundShipmentItems(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            # result = common_unit.read_xmlfile('test_file/listinboundshipmentItems.xml')
            if 'shipment_id' in execute_command:
                if execute_command['shipment_id']!='':
                    shipment_id = execute_command['shipment_id']
                    result = xmljson(inboundStr_item)
                    result = test_interface.select_inboundlistItem_between_time(shipment_id,result)
        else: 
            params = ['Action=ListInboundShipmentItems']+api_version+['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            params = params + default_params
            if 'shipment_id' in execute_command:
                if execute_command['shipment_id']!='':
                    params += ['ShipmentId='+execute_command['shipment_id']]
            if 'last_updated_before' in execute_command:
                if execute_command['last_updated_before']!='':
                    end_time = common_unit.conver_time(execute_command['last_updated_before'])
                    params += ['LastUpdatedAfter=' + end_time]
            if 'last_updated_after' in execute_command:
                if execute_command['last_updated_after'] != '':
                    start_time = common_unit.conver_time(execute_command['last_updated_after'])
                    params += ['LastUpdatedBefore=' + start_time]
            # 添加时间区间或者运单id，二者只能存在一样
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
            signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
            url = connect_url(params,signature)
            r = requests.post(url,headers=headers)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    def ListInboundShipmentItemsByNextToken(execute_command):
        if common_unit.test_access_param(execute_command) == 0:
            result = common_unit.read_xmlfile('test_file/listinboundshipmentItemsbyNexttoken.xml')
        else:
            params = ['Action=ListInboundShipmentItemsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'next_token' in execute_command:
                if execute_command['next_token'] != '':
                    params.append('NextToken=' + (quote(execute_command['next_token'])))  # 取上一个接口 NextToken的返回值
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
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result




inboundStr = '''<?xml version="1.0"?>
<ListInboundShipmentsResponse
    xmlns="http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/">
    <ListInboundShipmentsResult>
        <ShipmentData>
            <member>
                <ShipFromAddress>
                    <PostalCode>V5V 1A1</PostalCode>
                    <Name>jsowprni Devo CA20</Name>
                    <CountryCode>CA</CountryCode>
                    <StateOrProvinceCode>BC</StateOrProvinceCode>
                    <AddressLine1>Address Line 1</AddressLine1>
                    <City>Vancouver</City>
                </ShipFromAddress>
                <ShipmentId>FBAN4QNH</ShipmentId>
                <ShipmentName>FBA (8/27/12 1:55 PM)</ShipmentName>
                <ShipmentStatus>WORKING</ShipmentStatus>
                <LabelPrepType>NO_LABEL</LabelPrepType>
                <DestinationFulfillmentCenterId>YYZ1</DestinationFulfillmentCenterId>
            </member>
            <member>
                <ShipFromAddress>
                    <PostalCode>V5V 1A1</PostalCode>
                    <Name>Janani Arvind FBA QA</Name>
                    <CountryCode>CA</CountryCode>
                    <StateOrProvinceCode>BC</StateOrProvinceCode>
                    <AddressLine1>Address 1</AddressLine1>
                    <City>Vancouver</City>
                </ShipFromAddress>
                <ShipmentId>FBA1123</ShipmentId>
                <ShipmentName>Test MWS CA Shipment 1</ShipmentName>
                <ShipmentStatus>WORKING</ShipmentStatus>
                <LabelPrepType>NO_LABEL</LabelPrepType>
                <DestinationFulfillmentCenterId>RIC2</DestinationFulfillmentCenterId>
                <BoxContentsSource>NONE</BoxContentsSource>
                <EstimatedBoxContentsFee>
                    <TotalUnits>10</TotalUnits>
                    <FeePerUnit>
                        <CurrencyCode>USD</CurrencyCode>
                        <Value>0.10</Value>
                    </FeePerUnit>
                    <TotalFee>
                        <CurrencyCode>USD</CurrencyCode>
                        <Value>10.0</Value>
                    </TotalFee>
                </EstimatedBoxContentsFee>
            </member>
        </ShipmentData>
    </ListInboundShipmentsResult>
</ListInboundShipmentsResponse>'''



inboundStr_item = '''<?xml version="1.0"?>
<ListInboundShipmentItemsResponse xmlns="http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/">
    <ListInboundShipmentItemsResult>
        <ItemData>
            <member>
                <ShipmentId>SSF85DGIZZ3OF1</ShipmentId>
                <SellerSKU>SampleSKU1</SellerSKU>
                <QuantityShipped>3</QuantityShipped>
                <QuantityInCase>0</QuantityInCase>
                <QuantityReceived>0</QuantityReceived>
                <FulfillmentNetworkSKU>B000FADVPQ</FulfillmentNetworkSKU>
            </member>
            <member>
                <ShipmentId>SSF85DGIZZ3OF1</ShipmentId>
                <SellerSKU>SampleSKU2</SellerSKU>
                <QuantityShipped>10</QuantityShipped>
                <QuantityInCase>0</QuantityInCase>
                <QuantityReceived>0</QuantityReceived>
                <FulfillmentNetworkSKU>B0011VECH4</FulfillmentNetworkSKU>
            </member>
        </ItemData>
    </ListInboundShipmentItemsResult>
    <ResponseMetadata>
        <RequestId>ffce8932-8e69-11df-8af1-5bf2881764d8</RequestId>
    </ResponseMetadata>
</ListInboundShipmentItemsResponse>
'''











