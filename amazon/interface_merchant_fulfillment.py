import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/MerchantFulfillment/2015-06-01'
api_version = ['Version=2015-06-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


class interface_merchant_fulfillment:

    def __init__(self):
        pass

    #返回航运服务报价列表
    def GetEligibleShippingServices(execute_command):
        params = ['Action=GetEligibleShippingServices'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(user_access_dict, execute_command)
        params += ['ShipmentRequestDetails.AmazonOrderId=' + execute_command['order_id']]
        params += ['ShipmentRequestDetails.MustArriveByDate=' + execute_command['must_arrive_date']+'T00:00:00']
        params += ['ShipmentRequestDetails.PackageDimensions.Length=' + execute_command['length']]
        params += ['ShipmentRequestDetails.PackageDimensions.Width=' + execute_command['width']]
        params += ['ShipmentRequestDetails.PackageDimensions.Height=' + execute_command['height']]

        params += ['ShipmentRequestDetails.PackageDimensions.Unit=' + execute_command['dimension_unit']]
        params += ['ShipmentRequestDetails.Weight.Value=' + execute_command['weight_value']]
        params += ['ShipmentRequestDetails.Weight.Unit=' + execute_command['weight_unit']]
        params += ['ShipmentRequestDetails.ShipDate='+execute_command['ship_date']]

        params += ['ShipmentRequestDetails.ShipFromAddress.Name='+ execute_command['address_name']]
        params += ['ShipmentRequestDetails.ShipFromAddress.AddressLine1='+ execute_command['address_line1']]
        params += ['ShipmentRequestDetails.ShipFromAddress.City='+ execute_command['address_city']]
        params += ['ShipmentRequestDetails.ShipFromAddress.StateOrProvinceCode=' + execute_command['state_or_province']]

        params += ['ShipmentRequestDetails.ShipFromAddress.PostalCode=' + execute_command['post_code']]
        params += ['ShipmentRequestDetails.ShipFromAddress.CountryCode=' + execute_command['country_code']]
        params += ['ShipmentRequestDetails.ShipFromAddress.Email=' + execute_command['email']]
        params += ['ShipmentRequestDetails.ShipFromAddress.Phone=' + execute_command['phone']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeliveryExperience=' + execute_command['d_experience']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.CurrencyCode=' + execute_command['currency_code']]

        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.Amount=' + execute_command['amount']]
        params += ['ShipmentRequestDetails.ItemList.Item.1.OrderItemId=' + execute_command['order_item_id']]
        params += ['ShipmentRequestDetails.ItemList.Item.1.Quantity=' + execute_command['quantity']]

        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result




    def CreateShipment(execute_command):
        params = ['Action=CreateShipment'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)
        params = params + default_params
        params += ['HazmatType=' + execute_command['hazmat_type']]
        params += ['ShipmentId=' + execute_command['shipment_id']]
        params += ['ShippingServiceId=' + execute_command['shipment_id']]
        params += ['ShipmentRequestDetails.AmazonOrderId=' + execute_command['order_id']]
        params += ['ShipmentRequestDetails.LabelCustomization.CustomTextForLabel=' + execute_command['custom_label']]
        params += ['ShipmentRequestDetails.LabelCustomization.StandardIdForLabel=' + execute_command['stand_label']]
        params += ['ShipmentRequestDetails.MustArriveByDate=' + execute_command['must_arrive_date']]
        params += ['ShipmentRequestDetails.PackageDimensions.Length=' + execute_command['length']]
        params += ['ShipmentRequestDetails.PackageDimensions.Width=' + execute_command['width']]
        params += ['ShipmentRequestDetails.PackageDimensions.Height=' + execute_command['height']]
        params += ['ShipmentRequestDetails.PackageDimensions.Unit=' + execute_command['unit']]
        params += ['ShipmentRequestDetails.Weight.Value=' + execute_command['weight_value']]
        params += ['ShipmentRequestDetails.Weight.Unit=' + execute_command['weight_unit']]
        params += ['ShipmentRequestDetails.ShipDate=' + execute_command['ship_date']]
        params += ['ShipmentRequestDetails.ShipFromAddress.Name=' + execute_command['address_name']]
        params += ['ShipmentRequestDetails.ShipFromAddress.AddressLine1=' + execute_command['address_line']]
        params += ['ShipmentRequestDetails.ShipFromAddress.City=' + execute_command['address_city']]
        params += ['ShipmentRequestDetails.ShipFromAddress.StateOrProvinceCode=' + execute_command['state_or_province']]
        params += ['ShipmentRequestDetails.ShipFromAddress.PostalCode=' + execute_command['post_code']]
        params += ['ShipmentRequestDetails.ShipFromAddress.CountryCode=' + execute_command['country_code']]
        params += ['ShipmentRequestDetails.ShipFromAddress.Email=' + execute_command['email']]
        params += ['ShipmentRequestDetails.ShipFromAddress.Phone=' + execute_command['phone']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeliveryExperience=' + execute_command['experience']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.CarrierWillPickUp=' + execute_command['pick_up']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.CurrencyCode=' + execute_command['currency_code']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.Amount=' + execute_command['amount']]
        params += ['ShipmentRequestDetails.ShippingServiceOptions.LabelFormat=' + execute_command['label_format']]
        params += ['ShipmentRequestDetails.ItemList.Item.1.OrderItemId=' + execute_command['order_item_id']]
        params += ['ShipmentRequestDetails.ItemList.Item.1.Quantity=' + execute_command['quantity']]

        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



    def GetShipment(execute_command):
        params = ['Action=GetShipment']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params
        params += ['ShipmentId='+execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def CancelShipment(execute_command):
        params = ['Action=CancelShipment']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params
        params += ['ShipmentId='+execute_command['shipment_id']]
        params = sorted(params)
        params = '&'.join(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result

    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  
        params = params + default_params
        params = sorted(params)  
        params = '&'.join(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
        url = connect_url(params, signature)
        r = requests.post(url, headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result