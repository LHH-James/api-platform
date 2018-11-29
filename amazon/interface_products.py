import sys
sys.path.append('../')
import requests
import json
from urllib.parse import quote
from common_methods import common_unit
from test_file import test_interface


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Products/2011-10-01'
api_version = ['Version=2011-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y




class interface_products:
    def __init__(self):
        pass


    def GetMatchingProduct(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            # result = common_unit.read_xmlfile('test_file/get_product.xml')
            if 'asin' in execute_command:
                if execute_command['asin']!='':
                    asin_list = execute_command['asin'].split(',')
                    result = common_unit.xmltojson(str(test_product_list_8))
                    result = test_interface.test_GetMatchingProduct(asin_list,result)

        else:
            params = ['Action=GetMatchingProduct']+api_version+['Timestamp='+common_unit.get_time_stamp()]
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

            url = connect_url(params,signature)
            r = requests.post(url,headers=headers)
            print(r.text)
            result = common_unit.xmltojson(r.text)
            # result = save_result_into_db(result,execute_command)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    def ListMatchingProducts(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            result = common_unit.read_xmlfile('test_file/product_list.xml')
        else:
            params = ['Action=ListMatchingProducts']+api_version+['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)

            if 'query' in execute_command:
                if execute_command['query']!='':
                    params.append('Query='+ quote(execute_command['query']))

            if 'query_context' in execute_command:
                if execute_command['query_context']!='':
                    params.append('QueryContextId='+ quote(execute_command['query_context']))

            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
            signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
            url = connect_url(params,signature)
            # print(url)
            r = requests.post(url,headers=headers)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    #根据 ASIN、GCID、SellerSKU、UPC、EAN、ISBN 和 JAN，返回商品及其属性列表
    #Id 值最多5个
    def GetMatchingProductForId(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            result = common_unit.read_xmlfile('test_file/get_product_for_id.xml')
        else:
            params = ['Action=GetMatchingProductForId'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)

            if 'id_type' in execute_command:
                if execute_command['id_type'] != '':
                    params.append('IdType=' + quote(execute_command['id_type']))

            if 'id' in execute_command:
                if execute_command['id']!='':
                    id_list = execute_command['id'].split(',')
                    id_param_list = []
                    for i in id_list:
                        id_param_list.append('IdList.Id.'+str(id_list.index(i)+1)+'='+i)
                    params+=id_param_list

            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n' + host_name +  '\n' + port_point + '\n' + params
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))
            url = connect_url(params, signature)
            r = requests.post(url, headers=headers)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result






    #根据卖的sku取得商品价格
    #sku是多个值  sku：'S123,S124,S125'
    def GetMyPriceForSKU(execute_command):
        params = ['Action=GetMyPriceForSKU'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典

        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                #计算sku列表
                for i in sku_list:
                    sku_param_list.append('SellerSKUList.SellerSKU.'+str(sku_list.index(i)+1)+'='+i)
                params+=sku_param_list

        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('%2B',"%20")
        params = params.replace(' ',"%20")
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

    # 根据asin取得商品价格
    #  asin的值是多个  asin：'B071JJ3BJ3,B071JJ3BJ7,B071JJ3BJ8'
    def GetMyPriceForASIN(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            # result = common_unit.read_xmlfile('test_file/get_price_for_asin.xml')
            if 'asin' in execute_command:
                if execute_command['asin'] != '':
                    asin_list = execute_command['asin'].split(',')
                    result = common_unit.xmltojson(test_product_price_8)
                    result = test_interface.test_GetMyPriceForASIN(asin_list, result)

        else:
            params = ['Action=GetMyPriceForASIN'] + api_version + ['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)   # 获取包含认证参数的字典
            if 'asin' in execute_command:
                if execute_command['asin']!='':
                    asin_list = execute_command['asin'].split(',')
                    asin_param_list = []
                    for i in asin_list:
                        asin_param_list.append('ASINList.ASIN.' + str(asin_list.index(i) + 1) + '=' + i)  # 计算asin列表
                    params+=asin_param_list
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            params = params.replace('%2B', "%20")
            params = params.replace(' ', "%20")
            sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
            signature = quote(str(common_unit.cal_signature(sig_string, execute_command['secret_key'])))  # 计算字符串的加密签名
            signature = signature.replace('/', '%2F')
            url = connect_url(params, signature)  # 拼接请求字符串
            r = requests.post(url, headers=headers)   # 发起请求
            # print(r.text)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result


    #根据sku取得商品类别
    #sku值是单个
    def GetProductCategoriesForSKU(execute_command):
        params = ['Action=GetProductCategoriesForSKU'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)  # 获取包含认证参数的字典
        if 'sku' in execute_command:
            if execute_command['sku']!='':
                params.append('SellerSKU=' + quote(execute_command['sku']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('%2B',"%20")
        # params = params.replace('+', "%2B")
        params = params.replace(' ', "%20")
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

    #根据asin取得商品的类别
    #asin的值是单个
    def GetProductCategoriesForASIN(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            result = common_unit.read_xmlfile('test_file/get_product_categories_for_asin.xml')
            # if 'asin' in execute_command:
            #     if execute_command['asin'] != '':
                    # asin = execute_command['asin']
                    # result = common_unit.xmltojson(test_product_categories_8)
                    # result = test_interface.test_GetProductCategoriesForASIN(asin, result)
        else:
            params = ['Action=GetProductCategoriesForASIN'] + api_version+ ['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command) # 获取包含认证参数的字典
            if 'asin' in execute_command:
                if execute_command['asin']!='':
                    params.append('ASIN=' + quote(execute_command['asin']))
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
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

    #返回产品API部分的操作状态
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


    def GetCompetitivePricingForSKU(execute_command):
        params = ['Action=GetCompetitivePricingForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        # 获取包含认证参数的字典
        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('SellerSKUList.SellerSKU.'+str(sku_list.index(i)+1)+'='+i)
                params+=sku_param_list
        params = params + default_params
        params = sorted(params)
        params = '&'.join(params)
        params = params.replace('%2B', "%20")
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




    def GetCompetitivePricingForASIN(execute_command):
        params = ['Action=GetCompetitivePricingForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        # 获取包含认证参数的字典
        if 'asin' in execute_command:
            if execute_command['asin'] != '':
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
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result





    def GetLowestOfferListingsForSKU(execute_command):
        params = ['Action=GetLowestOfferListingsForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params += ['ExcludeMe=false']
        if 'sku' in execute_command:
            if execute_command['sku']!='':
                sku_list = execute_command['sku'].split(',')
                sku_param_list = []
                for i in sku_list:
                    sku_param_list.append('SellerSKUList.SellerSKU.'+str(sku_list.index(i)+1)+'='+i)
                params+=sku_param_list
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


    def GetLowestOfferListingsForASIN(execute_command):
        params = ['Action=GetLowestOfferListingsForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        params += ['ExcludeMe=false']
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
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        result = common_unit.xmltojson(r.text)
        error_result = common_unit.catch_exception(result)  # 异常处理
        if error_result != '':
            result = error_result
        return result


test_product_list_8 = '''
<GetMatchingProductResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
  <GetMatchingProductResult ASIN="B072XGX5LM" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B072XGX5LM</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Kitchen</ns2:Binding>
          <ns2:IsAutographed>false</ns2:IsAutographed>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">0.5511811018</ns2:Height>
            <ns2:Length Units="inches">16.5354330540</ns2:Length>
            <ns2:Width Units="inches">11.8110236100</ns2:Width>
            <ns2:Weight Units="pounds">0.440924524</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PartNumber>001</ns2:PartNumber>
          <ns2:ProductGroup>Apparel</ns2:ProductGroup>
          <ns2:ProductTypeName>HOME</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/51pttN4BzVL._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>VIGBAGNIA Garment Bag Packing Envelope Folder Shirts Sleeves Wrinkled Free Travel Packing Organizers for Luggage(Black)</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>fashion_display_on_website</ProductCategoryId>
          <Rank>1737632</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B0731127ND" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B0731127ND</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Kitchen</ns2:Binding>
          <ns2:IsAdultProduct>false</ns2:IsAdultProduct>
          <ns2:IsAutographed>false</ns2:IsAutographed>
          <ns2:Model>huij-a</ns2:Model>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">1.9685039350</ns2:Height>
            <ns2:Length Units="inches">10.6299212490</ns2:Length>
            <ns2:Width Units="inches">5.9055118050</ns2:Width>
            <ns2:Weight Units="pounds">0.2645547144</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PartNumber>huuj-12a</ns2:PartNumber>
          <ns2:ProductGroup>Beauty</ns2:ProductGroup>
          <ns2:ProductTypeName>BEAUTY</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/41tY-R4xM1L._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>VIGBAGNIA Travel Toiletry Bag Travel Gym Grooming Shaving Bag Personal Shave Dopp Kit Travel Bottles Organizer Bag Waterproof Lining For Men(Black)</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>beauty_display_on_website</ProductCategoryId>
          <Rank>502055</Rank>
        </SalesRank>
        <SalesRank>
          <ProductCategoryId>387321011</ProductCategoryId>
          <Rank>2540</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B073B3J2TQ" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B073B3J2TQ</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:IsAutographed>false</ns2:IsAutographed>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">0.8661417314</ns2:Height>
            <ns2:Length Units="inches">16.2992125818</ns2:Length>
            <ns2:Width Units="inches">12.0472440822</ns2:Width>
            <ns2:Weight Units="pounds">0.9259415004</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PartNumber>001</ns2:PartNumber>
          <ns2:ProductGroup>Apparel</ns2:ProductGroup>
          <ns2:ProductTypeName>LUGGAGE</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/51-S8STToeL._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>VIGBAGNIA Garment Bag Packing Envelope Folder Shirts Sleeves Wrinkled Free Travel Packing Organizers(1 Black+1 Light Blue)</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>fashion_display_on_website</ProductCategoryId>
          <Rank>2794945</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B071S12DPC" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B071S12DPC</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Apparel</ns2:Binding>
          <ns2:IsAdultProduct>false</ns2:IsAdultProduct>
          <ns2:Model>10481758</ns2:Model>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">1.4960629906</ns2:Height>
            <ns2:Length Units="inches">9.9999999898</ns2:Length>
            <ns2:Width Units="inches">6.1023621985</ns2:Width>
            <ns2:Weight Units="pounds">0.39021820374</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PartNumber>10481758</ns2:PartNumber>
          <ns2:ProductGroup>Luggage</ns2:ProductGroup>
          <ns2:ProductTypeName>LUGGAGE</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/51ume9FAz%2BL._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>Multiple Passport Wallet Travel Document Organizer Travel Wallet with Hand Strap â¦</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>fashion_display_on_website</ProductCategoryId>
          <Rank>4183629</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B072ZZHWN2" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B072ZZHWN2</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Kitchen</ns2:Binding>
          <ns2:ItemDimensions>
            <ns2:Weight Units="pounds">0.22</ns2:Weight>
          </ns2:ItemDimensions>
          <ns2:IsAdultProduct>false</ns2:IsAdultProduct>
          <ns2:IsAutographed>false</ns2:IsAutographed>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">0.9448818888</ns2:Height>
            <ns2:Length Units="inches">9.7637795176</ns2:Length>
            <ns2:Width Units="inches">8.2677165270</ns2:Width>
            <ns2:Weight Units="pounds">0.220462262</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PackageQuantity>1</ns2:PackageQuantity>
          <ns2:PartNumber>001</ns2:PartNumber>
          <ns2:ProductGroup>Apparel</ns2:ProductGroup>
          <ns2:ProductTypeName>BEAUTY</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/516yI0Z3PWL._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>VIGBAGNIA Hanging Toiletry Bag Women Travel Cosmetic Makeup Bag Waterproof Organizer Travel Accessories Foldable Sturdy Hook for Business Leisure Travel</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>fashion_display_on_website</ProductCategoryId>
          <Rank>1714388</Rank>
        </SalesRank>
        <SalesRank>
          <ProductCategoryId>387321011</ProductCategoryId>
          <Rank>2723</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B07312SBJ9" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
        <Identifiers>
            <MarketplaceASIN>
                <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                <ASIN>B07312SBJ9</ASIN></MarketplaceASIN>
            </Identifiers>
            <AttributeSets><ns2:ItemAttributes xml:lang="en-US"><ns2:Binding>Electronics</ns2:Binding><ns2:PackageDimensions><ns2:Height Units="inches">1.2598425184</ns2:Height><ns2:Length Units="inches">9.2913385732</ns2:Length><ns2:Width Units="inches">5.9842519624</ns2:Width><ns2:Weight Units="pounds">0.2645547144</ns2:Weight></ns2:PackageDimensions><ns2:PackageQuantity>1</ns2:PackageQuantity><ns2:PartNumber>001</ns2:PartNumber><ns2:ProductGroup>CE</ns2:ProductGroup><ns2:ProductTypeName>OFFICE_ELECTRONICS</ns2:ProductTypeName><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/5142R6OOTeL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">75</ns2:Width></ns2:SmallImage><ns2:Title>VIGBAGNIA Triple Layer Travel Cord Organizer Electronics Accessories Case USB Drive Shuttle Travel Gear Carry Bag for Phone Charger and Cable</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>290458</ProductCategoryId><Rank>564</Rank></SalesRank></SalesRankings></Product>
  </GetMatchingProductResult> 
  <GetMatchingProductResult ASIN="B072ZVTG5M" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B072ZVTG5M</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Kitchen</ns2:Binding>
          <ns2:Brand>COSY</ns2:Brand>
          <ns2:ItemDimensions>
            <ns2:Weight Units="pounds">0.22</ns2:Weight>
          </ns2:ItemDimensions>
          <ns2:IsAdultProduct>false</ns2:IsAdultProduct>
          <ns2:IsAutographed>false</ns2:IsAutographed>
          <ns2:Label>Cosy Store</ns2:Label>
          <ns2:Manufacturer>Cosy Store</ns2:Manufacturer>
          <ns2:ManufacturerMinimumAge Units="months">48.00</ns2:ManufacturerMinimumAge>
          <ns2:Model>004</ns2:Model>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">1.4960629906</ns2:Height>
            <ns2:Length Units="inches">10.7086614064</ns2:Length>
            <ns2:Width Units="inches">5.5118110180</ns2:Width>
            <ns2:Weight Units="pounds">0.220462262</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PartNumber>066</ns2:PartNumber>
          <ns2:ProductGroup>Beauty</ns2:ProductGroup>
          <ns2:ProductTypeName>BEAUTY</ns2:ProductTypeName>
          <ns2:Publisher>Cosy Store</ns2:Publisher>
          <ns2:Size>113PCS/ABCDEF26</ns2:Size>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/41tY-R4xM1L._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Studio>Cosy Store</ns2:Studio>
          <ns2:Title>Unicorn Party Supplies Set Birthday Decorations</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>beauty_display_on_website</ProductCategoryId>
          <Rank>523120</Rank>
        </SalesRank>
        <SalesRank>
          <ProductCategoryId>13861652011</ProductCategoryId>
          <Rank>8695</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <GetMatchingProductResult ASIN="B07313N12G" status="Success">
    <Product xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
      <Identifiers>
        <MarketplaceASIN>
          <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
          <ASIN>B07313N12G</ASIN>
        </MarketplaceASIN>
      </Identifiers>
      <AttributeSets>
        <ns2:ItemAttributes xml:lang="en-US">
          <ns2:Binding>Electronics</ns2:Binding>
          <ns2:Brand>VIGBAGNIA</ns2:Brand>
          <ns2:PackageDimensions>
            <ns2:Height Units="inches">1.3385826758</ns2:Height>
            <ns2:Length Units="inches">9.4488188880</ns2:Length>
            <ns2:Width Units="inches">5.8267716476</ns2:Width>
            <ns2:Weight Units="pounds">0.2645547144</ns2:Weight>
          </ns2:PackageDimensions>
          <ns2:PackageQuantity>1</ns2:PackageQuantity>
          <ns2:PartNumber>001</ns2:PartNumber>
          <ns2:ProductGroup>CE</ns2:ProductGroup>
          <ns2:ProductTypeName>OFFICE_ELECTRONICS</ns2:ProductTypeName>
          <ns2:SmallImage>
            <ns2:URL>http://ecx.images-amazon.com/images/I/5142R6OOTeL._SL75_.jpg</ns2:URL>
            <ns2:Height Units="pixels">75</ns2:Height>
            <ns2:Width Units="pixels">75</ns2:Width>
          </ns2:SmallImage>
          <ns2:Title>VIGBAGNIA Triple Layer Travel Cord Organizer Electronics Accessories Case USB Drive Shuttle Travel Gear Carry Bag for Phone Charger and Cable</ns2:Title>
        </ns2:ItemAttributes>
      </AttributeSets>
      <Relationships/>
      <SalesRankings>
        <SalesRank>
          <ProductCategoryId>290458</ProductCategoryId>
          <Rank>553</Rank>
        </SalesRank>
      </SalesRankings>
    </Product>
  </GetMatchingProductResult>
  <ResponseMetadata>
    <RequestId>e2590ab2-559e-4468-9a2a-77fd010c84f7</RequestId>
  </ResponseMetadata>
</GetMatchingProductResponse>
'''




test_product_price_8='''<?xml version="1.0"?>
    <GetMyPriceForASINResponse  xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <GetMyPriceForASINResult ASIN="B072XGX5LM" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B072XGX5LM</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>303.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>300.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>300.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUA</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B0731127ND" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B0731127ND</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>203.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>200.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>200.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUB</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B073B3J2TQ" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B073B3J2TQ</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>103.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>100.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>100.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUC</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B071S12DPC" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B071S12DPC</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>73.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>70.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>70.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUD</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B072ZZHWN2" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B072ZZHWN2</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>33.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>30.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>30.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUE</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B07312SBJ9" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B07312SBJ9</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>53.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>50.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>50.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUF</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B072ZVTG5M" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B072ZVTG5M</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>83.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>80.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>80.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUG</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <GetMyPriceForASINResult ASIN="B07313N12G" status="Success">
            <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                     xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Identifiers>
                    <MarketplaceASIN>
                        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                        <ASIN>B07313N12G</ASIN>
                    </MarketplaceASIN>
                </Identifiers>
                <Offers>
                    <Offer>
                        <BuyingPrice>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>93.99</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>90.00</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>3.99</Amount>
                            </Shipping>
                        </BuyingPrice>
                        <RegularPrice>
                            <CurrencyCode>USD</CurrencyCode>
                            <Amount>90.00</Amount>
                        </RegularPrice>
                        <FulfillmentChannel>MERCHANT</FulfillmentChannel>
                        <ItemCondition>Used</ItemCondition>
                        <ItemSubCondition>Acceptable</ItemSubCondition>
                        <SellerSKU>SampleSKUH</SellerSKU>
                    </Offer>
                </Offers>
            </Product>
        </GetMyPriceForASINResult>
        <ResponseMetadata>
            <RequestId>a3381684-87bd-416e-9b95-EXAMPLE9c236</RequestId>
        </ResponseMetadata>
    </GetMyPriceForASINResponse>'''


test_product_categories_8 = '''<?xml version="1.0"?>
<GetProductCategoriesForASINResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
  <GetProductCategoriesForASINResult>
    <Self>
      <ProductCategoryId>3421054011</ProductCategoryId>
      <ProductCategoryName>Shoelaces</ProductCategoryName>
      <Parent>
        <ProductCategoryId>9616100011</ProductCategoryId>
        <ProductCategoryName>Shoe Care &amp; Accessories</ProductCategoryName>
        <Parent>
          <ProductCategoryId>7586146011</ProductCategoryId>
          <ProductCategoryName>Shoe, Jewelry &amp; Watch Accessories</ProductCategoryName>
          <Parent>
            <ProductCategoryId>7141124011</ProductCategoryId>
            <ProductCategoryName>Departments</ProductCategoryName>
            <Parent>
              <ProductCategoryId>7141123011</ProductCategoryId>
              <ProductCategoryName>Clothing, Shoes &amp; Jewelry</ProductCategoryName>
            </Parent>
          </Parent>
        </Parent>
      </Parent>
    </Self>
  </GetProductCategoriesForASINResult>
  <ResponseMetadata>
    <RequestId>51ac759a-5fef-4389-9fc5-d86d3ee73dde</RequestId>
  </ResponseMetadata>
</GetProductCategoriesForASINResponse>'''