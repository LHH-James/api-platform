import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from common_methods import common_unit
from test_file import test_interface


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Sellers/2011-07-01'
api_version = ['Version=2011-07-01']
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y

class interface_sellers:
    def __init__(self):
        pass

    def ListMarketplaceParticipations(execute_command):
        if common_unit.test_access_param(execute_command)==0:
            # result = common_unit.read_xmlfile('test_file/listmarketplace.xml')
            seller_id = execute_command['seller_id']
            result = common_unit.xmltojson(listMarketplace)
            result = test_interface.test_ListMarketplaceParticipations(seller_id,result)
        else:
            params = ['Action=ListMarketplaceParticipations']+api_version+['Timestamp='+common_unit.get_time_stamp()]
            # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
            params += common_unit.make_access_param(execute_command)
            params = params + default_params
            params = sorted(params)
            params = '&'.join(params)
            sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
            signature = quote(str(common_unit.cal_signature(sig_string,execute_command['secret_key'])))
            url = connect_url(params,signature)
            r = requests.post(url,headers=headers)
            print(r.text)
            result = common_unit.xmltojson(r.text)
            error_result = common_unit.catch_exception(result)  # 异常处理
            if error_result != '':
                result = error_result
        return result



    def ListMarketplaceParticipationsByNextToken(execute_command):
        params = ['Action=ListMarketplaceParticipationsByNextToken']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
        if 'next_token' in execute_command:
            if execute_command['next_token'] != '':
                params += ['NextToken=' + quote(execute_command['next_token'])]
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





    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        # user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(execute_command)
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


listMarketplace='''<ListMarketplaceParticipationsResponse xmlns="https://mws.amazonservices.com/Sellers/2011-07-01">
  <ListMarketplaceParticipationsResult>
    <ListParticipations>
      <Participation>
        <MarketplaceId>A1AM78C64UM0Y8</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>A1MQXOICRS2Z7M</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>A2EUQ1WTGCTBG2</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>A2ZV50J4W1RKNI</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>A3H6HPSLHAK3XG</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>AHRY1CZE9ZY4H</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
      <Participation>
        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
        <SellerId>A1TVK9W4UM80AB</SellerId>
        <HasSellerSuspendedListings>No</HasSellerSuspendedListings>
      </Participation>
    </ListParticipations>
    <ListMarketplaces>
      <Marketplace>
        <MarketplaceId>A1AM78C64UM0Y8</MarketplaceId>
        <DefaultCountryCode>MX</DefaultCountryCode>
        <DomainName>www.amazon.com.mx</DomainName>
        <Name>Amazon.com.mx</Name>
        <DefaultCurrencyCode>MXN</DefaultCurrencyCode>
        <DefaultLanguageCode>es_MX</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>A1MQXOICRS2Z7M</MarketplaceId>
        <DefaultCountryCode>CA</DefaultCountryCode>
        <DomainName>siprod.stores.amazon.ca</DomainName>
        <Name>SI CA Prod Marketplace</Name>
        <DefaultCurrencyCode>CAD</DefaultCurrencyCode>
        <DefaultLanguageCode>en_CA</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>A2EUQ1WTGCTBG2</MarketplaceId>
        <DefaultCountryCode>CA</DefaultCountryCode>
        <DomainName>www.amazon.ca</DomainName>
        <Name>Amazon.ca</Name>
        <DefaultCurrencyCode>CAD</DefaultCurrencyCode>
        <DefaultLanguageCode>en_CA</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>A2ZV50J4W1RKNI</MarketplaceId>
        <DefaultCountryCode>US</DefaultCountryCode>
        <DomainName>sim1.stores.amazon.com</DomainName>
        <Name>Non-Amazon</Name>
        <DefaultCurrencyCode>USD</DefaultCurrencyCode>
        <DefaultLanguageCode>en_US</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>A3H6HPSLHAK3XG</MarketplaceId>
        <DefaultCountryCode>MX</DefaultCountryCode>
        <DomainName>sidevo.stores.amazon.mx</DomainName>
        <Name>Non-Amazon</Name>
        <DefaultCurrencyCode>MXN</DefaultCurrencyCode>
        <DefaultLanguageCode>es_MX</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>AHRY1CZE9ZY4H</MarketplaceId>
        <DefaultCountryCode>US</DefaultCountryCode>
        <DomainName>invoicing-shadow-marketplace.amazon.com</DomainName>
        <Name>Amazon.com Invoicing Shadow Marketplace</Name>
        <DefaultCurrencyCode>USD</DefaultCurrencyCode>
        <DefaultLanguageCode>en_US</DefaultLanguageCode>
      </Marketplace>
      <Marketplace>
        <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
        <DefaultCountryCode>US</DefaultCountryCode>
        <DomainName>www.amazon.com</DomainName>
        <Name>Amazon.com</Name>
        <DefaultCurrencyCode>USD</DefaultCurrencyCode>
        <DefaultLanguageCode>en_US</DefaultLanguageCode>
      </Marketplace>
    </ListMarketplaces>
  </ListMarketplaceParticipationsResult>
  <NextToken>uJ7azT3papiaJqJYLDm0ZIfVkJJPpovRu+h4GHIH2f5UojdU4H46tsNI3HOI22PIxqXyQLkGMBs8VhF73Xgy+6O6y68JrC7CxD8gRjCqrLVSxhzXajqcovmDOU6fp6slInTAy+XKVmRZBY+oaVuyc4D8eV8v09jgkF1bGZ6P/ng6eU+70V3XHi+GfJJMLStaf2GLmUGyr9UGnxD0RJmrrxhFP8KzGB62m5xaobyXfHTK9kUavBVIe6I4GnWh00CCRxHAuPz7ThaaBUA8hbyHBroItFPqI70tYKJLRAbGuF7q0sjrJVSK8Z0FUIyM6yC5boHX0iN4j9bXUOznDVC2NfUJ1nExbwKxM48r5nOh7ZTzrxRr597AWze71jXZj4BqIYWiflP7yRrhBtgUjYSPlIL7x7hs8aiEXUM5IL/bq6ISyoYkkmy7z4+envNcHi415FBs1CFOdGJYKTGNikHXtM9mNOdUz8cZ</NextToken>
  <ResponseMetadata>
    <RequestId>e00146c4-89a2-4f19-a26f-e99518fa45cd</RequestId>
  </ResponseMetadata>
</ListMarketplaceParticipationsResponse>

'''