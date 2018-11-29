import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit
from test_file import test_interface


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentInventory/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y





#了解库存的可用性
class interface_fulfillmentInventory:


    def __init__(self):
        pass

    #返回关于卖方库存的可用性信息下一页  使用nexttoken参数
    def ListInventorySupplyByNextToken(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            result = common_unit.read_xmlfile('test_file/inventory_list_next.xml')

        else:
            params = ['Action=ListInventorySupplyByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
            if 'next_token' in execute_command:
                if execute_command['next_token'] != '':
                    params += ['NextToken=' + execute_command['next_token']]

            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            params = params.replace('+', '%2B')
            params = params.replace('/', '%2F')
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
            url = connect_url(params, signature)  # 拼接请求字符串
            r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result



    #返回  实现库存API  的操作状态
    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


    # 返回关于卖方库存可用性的信息   非第一次做更新操作
    def ListInventorySupply(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            # result = common_unit.read_xmlfile('test_file/inventory_list.xml')
            result = common_unit.xmltojson(str(inventory))
            result = test_interface.select_inventory_list(result)
        else:
            params = ['Action=ListInventorySupply'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典

            if 'sku' in execute_command:
                if execute_command['sku'] != '':
                    sku_list = execute_command['sku'].split(',')
                    sku_params_list = []
                    for i in sku_list:
                        sku_params_list.append('SellerSkus.member.' + str(sku_list.index(i) + 1) + '=' + i)
                    params += sku_params_list

            if 'start_time' in execute_command:
                if execute_command['start_time'] != '':
                    st = execute_command['start_time']
                    s_time = common_unit.conver_time(st)
                    params.append('QueryStartDateTime=' + quote(s_time))

            if 'response_group' in execute_command:
                if execute_command['response_group'] != '':
                    params.append('ResponseGroup=' + quote(execute_command['response_group']))

            params = params + default_params
            params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
            params = '&'.join(params)  # 对请求身进行分割
            params = params.replace('+',"%2B")
            params = params.replace(' ',"%20")
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            signature = signature.replace('/', '%2F')
            # print(signature)
            # signature = signature.replace('=','%3D') # 计算字符串的加密签名
            url = connect_url(params, signature)  # 拼接请求字符串
            r = requests.post(url, headers=headers)  # 发起请求
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result



    # 同步库存产品列表的库存信息  第一次同步做插入操作
    def syn_inventory(execute_command):
        params = ['Action=ListInventorySupply'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        start_time = '1970-12-31T16:00:00'  # 设置一个久远的时间开始同步库存(第一次同步店铺商品列表的库存)
        start_time = start_time.replace(':', '%3A')
        params.append('QueryStartDateTime=' + start_time)

        params = params + default_params  #
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
        signature = signature.replace('/', '%2F')
        # signature = signature.replace('=','%3D') # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result



inventory='''<ListInventorySupplyResponse>
                <ListInventorySupplyResult>
                <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                <InventorySupplyList>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>300</TotalSupplyQuantity>
                    <FNSKU>B072XGX5LM</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B072XGX5LM</ASIN>
                    <SellerSKU>SampleSKUA</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>400</TotalSupplyQuantity>
                    <FNSKU>B0731127ND</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B0731127ND</ASIN>
                    <SellerSKU>SampleSKUB</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>350</TotalSupplyQuantity>
                    <FNSKU>B073B3J2TQ</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B073B3J2TQ</ASIN>
                    <SellerSKU>SampleSKUC</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>400</TotalSupplyQuantity>
                    <FNSKU>X001ETQ1RX</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B071S12DPC</ASIN>
                    <SellerSKU>SampleSKUD</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>500</TotalSupplyQuantity>
                    <FNSKU>B072ZZHWN2</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B072ZZHWN2</ASIN>
                    <SellerSKU>SampleSKUE</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>600</TotalSupplyQuantity>
                    <FNSKU>B07312SBJ9</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B07312SBJ9</ASIN>
                    <SellerSKU>SampleSKUF</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>700</TotalSupplyQuantity>
                    <FNSKU>B072ZVTG5M</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B072ZVTG5M</ASIN>
                    <SellerSKU>SampleSKUG</SellerSKU>
                  </member>
                  <member>
                    <Condition>NewItem</Condition>
                    <SupplyDetail/>
                    <TotalSupplyQuantity>900</TotalSupplyQuantity>
                    <FNSKU>B07313N12G</FNSKU>
                    <InStockSupplyQuantity>0</InStockSupplyQuantity>
                    <ASIN>B07313N12G</ASIN>
                    <SellerSKU>SampleSKUH</SellerSKU>
                  </member>
                </InventorySupplyList>
                </ListInventorySupplyResult>
                <ResponseMetadata>
                <RequestId>244800c9-df03-46c4-8809-760706af8ee2</RequestId>
                </ResponseMetadata>
            </ListInventorySupplyResponse>'''



