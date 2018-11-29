import json
import datetime
from common_methods import common_unit
import random
import time

time_tamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
nowdate_time = time.strftime("%Y-%m-%d",time.localtime())

inbountShipment_status = ['WORKING','SHIPPED','IN_TRANSIT','DELIVERED','CHECKED_IN','RECEIVING','CLOSED','CANCELLED','DELETED']
seller_sku = ['SampleSKUA','SampleSKUB','SampleSKUC','SampleSKUD','SampleSKUE','SampleSKUF','SampleSKUG','SampleSKUH']
seller_asin = ['B072XGX5LM','B0731127ND','B073B3J2TQ','B071S12DPC','B072ZZHWN2','B07312SBJ9','B072ZVTG5M','B07313N12G']
dict_asin = {'B072XGX5LM':0,'B0731127ND':1,'B073B3J2TQ':2,'B071S12DPC':3,'B072ZZHWN2':4,'B07312SBJ9':5,'B072ZVTG5M':6,'B07313N12G':7}

rad_tamp = [random.randrange(0,4),random.randrange(4,8)]


#生成随机数
def random_letter():
    #建立空字符串
    ll = ""
    # 循环6次，从0到5
    for i in range(6):
        #生成一个数字随机数
        rad2 = random.randrange(0,6)
        #这个随机数为2或者4时，生成一个1到9的随机数放到字符串中，否则在65到91中随机生成一个数并转换成大写字母，然后加入到字符串中
        if rad2 == 2 or rad2 == 4:
            ll = ll + str(random.randrange(0,10))
        else:
            rad1 = chr(random.randrange(65,91))
            ll = ll + rad1
    return ll


#===========================入库==============================#
#对传入的时间格式的转化
def conver_date_time(str_time):
    st = str_time.replace('+', ' ')
    timeStruct = time.strptime(st, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeStruct))
    localTime = time.localtime(timeStamp)
    str_date = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    return str_date


#ListInboundShipments  ========>   入口
#查询某个时间段的数据   入库单表
def select_inboundlist_between_time(start_time,end_time,result):
    cursor, conn = common_unit.database_connection()
    start_time = conver_date_time(start_time)
    end_time = conver_date_time(end_time)
    rs = cursor.execute("SELECT * FROM test_inboundlist where time Between '%s' AND '%s'"%(start_time,end_time))
    if rs!=0:
        result = json.loads(result)
        members = result['ListInboundShipmentsResponse']['ListInboundShipmentsResult']['ShipmentData']['member']
        members.clear()
        for i in cursor.fetchall():
            dict_m = {}
            # id = i[0]
            shipment_id = i[1]
            shipment_name = i[2]
            # print(id,shipment_id,shipment_name)
            dict_m['ShipFromAddress'] = {"PostalCode": "V5V 1A1","Name": "jsowprni Devo CA20","CountryCode": "CA","StateOrProvinceCode": "BC","AddressLine1": "Address Line 1","City": "Vancouver"}
            dict_m['ShipmentId'] = 'DF-FBA' + str(shipment_id)
            dict_m['ShipmentName'] = 'DF-' + str(shipment_name) + '-SHIPNAME'
            dict_m['ShipmentStatus'] = 'WORKING'
            dict_m['LabelPrepType'] = "NO_LABEL"
            dict_m['DestinationFulfillmentCenterId'] ="YYZ1"
            members.append(dict_m)
        rr = result
    else:
        rr = inboundShipments(start_time,result)
    cursor.close()
    conn.close()
    return rr

#插入入库单表
def insert_test_inboundlist(inbound_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_inboundlist(shipment_id,shipment_name,time) values(%s,%s,%s)',inbound_list)
    conn.commit()
    cursor.close()
    conn.close()
    return


#插入入库单明细
def insert_test_inboundlist_item(inbound_item_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_inboundlist_item(shipment_id,seller_sku,quantity_shiped,network_sku,time) values(%s,%s,%s,%s,%s)',inbound_item_list)
    conn.commit()
    cursor.close()
    conn.close()
    return


#随机生成入库单
def inboundShipments(start_time,result):
    result = json.loads(result)
    members = result['ListInboundShipmentsResponse']['ListInboundShipmentsResult']['ShipmentData']['member']
    for m in members:
        ll = random_letter()
        m['ShipmentId'] ='DF-FBA'+str(ll)
        m['ShipmentName'] = 'DF-'+str(ll)+'-SHIPNAME'
        now_time = start_time
        insert_test_inboundlist([m['ShipmentId'],m['ShipmentName'],now_time])
    rr = result
    return rr



#ListInboundShipmentItems  =========>  入口
#查询某个时间段的数据   入库单明细表
def select_inboundlistItem_between_time(shipmentId,result):
    cursor, conn = common_unit.database_connection()
    # rs = cursor.execute("SELECT * FROM test_inboundlist_item where time Between '2018-11-23 14:00:00' AND '2018-11-23 16:00:00'")
    rs = cursor.execute("SELECT * FROM test_inboundlist_item where shipment_id='%s'" % (shipmentId))
    if rs!=0:
        result = json.loads(result)
        members = result['ListInboundShipmentItemsResponse']['ListInboundShipmentItemsResult']['ItemData']['member']
        members.clear()
        for i in cursor.fetchall():
            dict_m = {}
            id = i[0]
            shipment_id = i[1]
            seller_sku = i[2]
            quantity_shiped = i[3]
            netword_sku = i[4]
            dict_m['ShipmentId'] = shipment_id
            dict_m['SellerSKU'] = seller_sku
            dict_m['QuantityShipped'] =quantity_shiped
            dict_m['QuantityInCase'] =0
            dict_m['QuantityReceived'] =0
            dict_m['FulfillmentNetworkSKU'] = netword_sku
            members.append(dict_m)
        rr = result
        # print(rr)
    else:
        rr = inboundShipmentsItems(shipmentId,result)
    cursor.close()
    conn.close()
    return rr


#获取入库
def select_inboundItem_by_shipmentId(shipmentId):
    cursor, conn = common_unit.database_connection()
    cursor.execute("SELECT time FROM test_inboundlist where shipment_id='%s'" % (shipmentId))
    # id = cursor.fetchone()[0]
    ship_time = cursor.fetchone()[0]
    ship_time = datetime.datetime.strftime(ship_time, "%Y-%m-%d")
    # print(type(ship_time))
    shipment_date = conver_date(str(ship_time))
    # print(shipment_date,nowdate_time)
    cursor.close()
    conn.close()
    if shipment_date==nowdate_time:
        return 0
    else:
        return 1


#随机生成入库单明细
def inboundShipmentsItems(shipmentId,result):
    i = 0
    result = json.loads(result)
    members = result['ListInboundShipmentItemsResponse']['ListInboundShipmentItemsResult']['ItemData']['member']
    for m in members:
        m['ShipmentId'] = str(shipmentId)
        m['SellerSKU'] = seller_sku[int(rad_tamp[i])]
        m['QuantityShipped'] = str(int(rad_tamp[i])+1)
        i = i + 1
        now_time = create_time
        item_list= [m['ShipmentId'], m['SellerSKU'],m['QuantityShipped'],m['FulfillmentNetworkSKU'],now_time]
        insert_test_inboundlist_item(item_list)
        isTrue = select_inboundItem_by_shipmentId(m['ShipmentId'])    #判断是不是今天的入库的，是今天入库的话，要更新库存信息
        if isTrue==0:
            update_test_inventory(m['QuantityShipped'],m['SellerSKU'])
    return result




#上面随机生成入库明细之后相应的更改库存
def update_test_inventory(new_add,sku):
    cursor, conn = common_unit.database_connection()
    cursor.execute("SELECT quantity FROM test_inventory where sku='%s'" % (sku))
    quant = cursor.fetchone()[0]
    total = int(new_add)+int(quant)
    cursor.execute("update test_inventory set quantity='%s',time='%s' where sku='%s'" % (total,create_time,sku))
    conn.commit()
    cursor.close()
    conn.close()

#===========================出库==============================#


#查询某个时间段的数据   出库单表
#  获取出库单列表 =======> 入口
#  ListAllFulfillmentOrders

def listAllfulfillmentOrders_between_time(start_date,result):
    cursor, conn = common_unit.database_connection()
    select_order_orderItem()     #对新生成的订单进行创建出库单
    rs = cursor.execute("SELECT * FROM test_outboundlist where status_time > '%s'" %(start_date))
    if rs!=0:
        result = json.loads(result)
        members = result['ListAllFulfillmentOrdersResponse']['ListAllFulfillmentOrdersResult']['FulfillmentOrders']['member']
        members.clear()
        for i in cursor.fetchall():
            dict_m = {}
            # id = i[0]
            dict_m['SellerFulfillmentOrderId'] = i[1]
            dict_m['DestinationAddress'] = {
                               "PhoneNumber": "7047951585",
                               "City": "CONCORD",
                               "CountryCode": "US",
                               "PostalCode": "28025-1273",
                               "Name": "Kathy Irminger",
                               "StateOrProvinceCode": "NC",
                               "Line3": 'null',
                               "DistrictOrCounty": 'null',
                               "Line2": 'null',
                               "Line1": "7015 ERINBROOK DR"
                              }
            dict_m['DestinationAddress']['Name'] =i[2]
            dict_m['DisplayableOrderDateTime'] =i[3]
            dict_m['FulfillmentOrderStatus'] =i[4]
            dict_m['StatusUpdatedDateTime'] =i[5]
            dict_m['ReceivedDateTime'] =i[7]
            dict_m['DisplayableOrderId'] =i[8]

            dict_m['ShippingSpeedCategory']='Expedited'
            dict_m['FulfillmentMethod']='Consumer'
            dict_m['FulfillmentPolicy']='FillOrKill'
            dict_m['DisplayableOrderComment']='感谢您的订购！'
            members.append(dict_m)
        rr = result
    else:
        rr = listAllfulfillment(start_date, result)
        # nowTime = int(time.time())
        # timeStruct = time.strptime(start_date, "%Y-%m-%d")
        # startDate_time = int(time.mktime(timeStruct))
        # # print(nowTime,startDate_time)
        # if nowTime - startDate_time > 604800:      #退7天    生成历史的出库单的话传入的时间的是 ： （当前时间 - 7天）
        #     rr = listAllfulfillment(start_date,result)
        # else:
        #     rr={}
    cursor.close()
    conn.close()
    return rr



#对传入的时间格式的转化
def conver_date(st):
    timeStruct = time.strptime(st, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeStruct))
    # timeStamp = timeStamp+86400
    localTime = time.localtime(timeStamp)
    str_date = time.strftime("%Y-%m-%d", localTime)
    return str_date


#插入出库单表
def insert_test_outboundlist(outbound_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_outboundlist(seller_order_id,name,display_order_time,order_status,status_update_time,status_time,receive_date_time,display_order_id,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',outbound_list)
    conn.commit()
    cursor.close()
    conn.close()
    return

#随机生成出库单    列表
# 当没有新订单的时候    随机生成出库单   出库单明细(指的是GetFulfillmentOrder接口的结果)
def listAllfulfillment(start_time,result):
    result = json.loads(result)
    members = result['ListAllFulfillmentOrdersResponse']['ListAllFulfillmentOrdersResult']['FulfillmentOrders']['member']
    for m in members:
        ll = random_letter()
        end  = conver_date(start_time)
        m['SellerFulfillmentOrderId'] ='DF-CONSUMER-'+str(ll)
        m['DestinationAddress']['Name'] = 'DF-'+str(ll)+'-NAME'
        m['DisplayableOrderDateTime'] =  end +'T01:00:00Z'
        m['FulfillmentOrderStatus'] ='COMPLETE'
        m['StatusUpdatedDateTime'] =  end+'T05:12:54Z'
        status_time = end+' 14:15:54'
        timeStruct = time.strptime(status_time, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeStruct))
        localTime = time.localtime(timeStamp)
        str_datetime= time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        m['ReceivedDateTime'] =  end +'T08:12:54Z'
        m['DisplayableOrderId'] ='DF-CONSUMER-'+str(ll)
        start_time = end
        now_time = create_time
        outbund_list = [m['SellerFulfillmentOrderId'],m['DestinationAddress']['Name'],m['DisplayableOrderDateTime'],
                        m['FulfillmentOrderStatus'],m['StatusUpdatedDateTime'],str_datetime,m['ReceivedDateTime'],
                        m['DisplayableOrderId'],now_time]
        # print(outbund_list)
        insert_test_outboundlist(outbund_list)
        ounbound_list_item = [m['SellerFulfillmentOrderId'], seller_sku[1], 1, m['DisplayableOrderDateTime'], seller_asin[1], create_time]
        insert_test_outboundlist_item(ounbound_list_item)
    return result


#==========根据出库单号获取配送的订单明细=================
#插入库存表
def insert_test_inventory(inventory_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_inventory(sku,asin,quantity,time) values(%s,%s,%s,%s)',inventory_list)
    conn.commit()
    cursor.close()
    conn.close()
    return




#根据订单列表创建出库单，创建完成之后把状态更新为1
def update_test_orderlist_status(order_id):
    cursor, conn = common_unit.database_connection()
    cursor.execute("update test_orderlist set status=1 where order_id='%s'" % (order_id))
    conn.commit()
    cursor.close()
    conn.close()

#插入出库单明细表
def insert_test_outboundlist_item(outbound_item_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_outboundlist_item(seller_order_id,sku,quantity,order_time,asin,time) values(%s,%s,%s,%s,%s,%s)',outbound_item_list)
    conn.commit()
    cursor.close()
    conn.close()
    return


#查询订单、订单明细
def select_order_orderItem():
    cursor, conn = common_unit.database_connection()
    rs = cursor.execute("SELECT order_id,time FROM test_orderlist where status=0")
    if rs!=0:
        for orderID in cursor.fetchall():
            ll = random_letter()
            order_id = orderID[0]
            order_time = orderID[1]
            seller_order_id = 'DF-CONSUMER-' + str(ll)
            name = 'DF-' + str(ll) + '-NAME'
            order_status = 'COMPLETE'
            outbound_list = [seller_order_id,name,order_time,order_status,order_time,create_time,order_time,order_id,create_time]
            insert_test_outboundlist(outbound_list)      #查询到新增的订单时(状态为0的订单数据)，创建出库单据
            update_test_orderlist_status(order_id)
            cursor.execute("SELECT order_item_id,order_id,asin,seller_sku FROM test_orderlist_item where order_id=%s"%(order_id))
            # for sku_quantity in cursor.fetchall():
            sku_quantity = cursor.fetchone()
            # order_item_id = sku_quantity[0]
            asin = sku_quantity[2]
            sku = sku_quantity[3]
            quantity = 1
            ounbound_list_item = [seller_order_id,sku,quantity,order_time,asin,create_time]
            insert_test_outboundlist_item(ounbound_list_item)
    cursor.close()
    conn.close()
    return



#返回出库单明细列表过去  ====》  给到php那边
# GetFulfillmentOrder接口 ---- 入口
# 通过sellerFulfillmentOrderId
def getFulfillmentOrder(sellerOrderID,result):
    # print(sellerOrderID)
    cursor, conn = common_unit.database_connection()
    rs = cursor.execute("SELECT seller_order_id,sku,quantity,order_time,asin FROM test_outboundlist_item where seller_order_id='%s'"%(sellerOrderID))
    if rs!=0:
        outbound_list_item = cursor.fetchone()
        result = json.loads(result)
        # print(result)
        FulfillmentOrderItem = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentOrderItem']['member']
        # print(FulfillmentOrderItem)
        FulfillmentOrderItem['SellerSKU'] = outbound_list_item[1]
        FulfillmentOrderItem['EstimatedShipDateTime'] = outbound_list_item[3]
        FulfillmentOrderItem['EstimatedArrivalDateTime'] = outbound_list_item[3]

        FulfillmentOrder = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentOrder']
        # print(FulfillmentOrder)
        FulfillmentOrder['SellerFulfillmentOrderId'] = outbound_list_item[0]
        FulfillmentOrder['StatusUpdatedDateTime'] = outbound_list_item[3]
        FulfillmentOrder['DisplayableOrderDateTime'] = outbound_list_item[3]
        FulfillmentOrder['ReceivedDateTime'] = outbound_list_item[3]
        FulfillmentOrder['DisplayableOrderId'] = outbound_list_item[0]

        FulfillmentShipment = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentShipment']['member']
        # print(FulfillmentShipment)
        FulfillmentShipment['FulfillmentShipmentItem']['member']['SellerSKU'] = outbound_list_item[1]
        FulfillmentShipment['FulfillmentShipmentItem']['member']['SellerFulfillmentOrderItemId'] = outbound_list_item[0]
        FulfillmentShipment['ShippingDateTime'] = outbound_list_item[3]
        FulfillmentShipment['EstimatedArrivalDateTime'] = outbound_list_item[3]
    cursor.close()
    conn.close()
    return result


# #getFulfillmentOrders    创建出库单明细
# def random_fulfillmentOrder(result):
#     result = json.loads(result)
#     FulfillmentOrderItem = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentOrderItem']['member']
#     FulfillmentOrderItem['SellerSKU'] =
#     FulfillmentOrderItem['EstimatedShipDateTime']=
#     FulfillmentOrderItem['EstimatedArrivalDateTime']=
#
#     FulfillmentOrder = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentOrder']
#     FulfillmentOrder['FulfillmentOrder']['SellerFulfillmentOrderId'] =
#     FulfillmentOrder['FulfillmentOrder']['DisplayableOrderDateTime'] =
#     FulfillmentOrder['FulfillmentOrder']['DisplayableOrderId'] =
#
#     FulfillmentShipment = result['GetFulfillmentOrderResponse']['GetFulfillmentOrderResult']['FulfillmentShipment']['member']
#     FulfillmentShipment['member']['SellerSKU']=
#     FulfillmentShipment['member']['SellerFulfillmentOrderItemId'] =
#
#
#     start_time = end
#     now_time = create_time
#     outbund_list = [m['SellerFulfillmentOrderId'],m['DestinationAddress']['Name'],m['DisplayableOrderDateTime'],
#                     m['FulfillmentOrderStatus'],m['StatusUpdatedDateTime'],str_datetime,m['ReceivedDateTime'],
#                     m['DisplayableOrderId'],now_time]
#     # print(outbund_list)
#     # insert_test_outboundlist(outbund_list)
#     return result


#=================库存======================#

#插入库存列表
def insert_test_inventory(inventory_list):
    cursor, conn = common_unit.database_connection()
    cursor.execute('INSERT INTO test_inventory(sku,asin,quantity,time) values(%s,%s,%s,%s)',inventory_list)
    conn.commit()
    cursor.close()
    conn.close()

#库存的接口==========>  入口
def select_inventory_list(result):
    mb = 0
    cursor, conn = common_unit.database_connection()
    result = json.loads(result)
    members = result['ListInventorySupplyResponse']['ListInventorySupplyResult']['InventorySupplyList']['member']
    rs = cursor.execute("SELECT sku,asin,quantity FROM test_inventory")
    if rs != 0:
        for inventory in cursor.fetchall():
            members[mb]['SellerSKU'] = inventory[0]
            members[mb]['ASIN'] = inventory[1]
            members[mb]['TotalSupplyQuantity'] = inventory[2]
            mb = mb + 1
        rr = result
    else:
        lr = list_inventory_supply(result)
        rr = lr
    cursor.close()
    conn.close()
    return rr


#同步库存
def list_inventory_supply(result):
    # result = json.loads(result)
    members = result['ListInventorySupplyResponse']['ListInventorySupplyResult']['InventorySupplyList']['member']
    for m in members:
        sku = m['SellerSKU']
        asin = m['ASIN']
        quantity = m['TotalSupplyQuantity']
        inventory_list = [sku,asin,quantity,create_time]
        insert_test_inventory(inventory_list)
    rr = result
    return rr



#=======授权获取市场列表=========#

# 获取市场列表  ======>   入口

def test_ListMarketplaceParticipations(SellerId,result):
    result = json.loads(result)
    members = result['ListMarketplaceParticipationsResponse']['ListMarketplaceParticipationsResult']['ListParticipations']['Participation']
    for m in members:
        m['SellerId'] = SellerId
    return result


#=======产品列表================#
# GetMatchingProduct  ======>  入口
#根据 asin（可以多个） 获取商品信息

def test_GetMatchingProduct(asin_list,result):
    a_value_list = []
    result = json.loads(result)
    products = result['GetMatchingProductResponse']['GetMatchingProductResult']
    del_asin = set(seller_asin) - set(asin_list)
    for a in del_asin:
        a_value = int(dict_asin[a])
        a_value_list.append(a_value)
    a_value_list.sort(reverse=True)
    for de in a_value_list:
        del(products[de])
    rr = result
    return rr

#GetMyPriceForASIN  ======>  入口
#根据 asin（可以多个） 获取商品价格

def test_GetMyPriceForASIN(asin_list,result):
    a_value_list = []
    result = json.loads(result)
    products_price = result['GetMyPriceForASINResponse']['GetMyPriceForASINResult']
    del_asin = set(seller_asin) - set(asin_list)
    for a in del_asin:
        a_value = int(dict_asin[a])
        a_value_list.append(a_value)
    a_value_list.sort(reverse=True)
    for de in a_value_list:
        del (products_price[de])
    rr = result
    # print(rr)
    return rr

#暂时没用
#GetMyPriceForASIN  ======>  入口
#根据 asin（可以多个） 获取商品分类信息
def test_GetProductCategoriesForASIN(asin_list,result):
    a_value_list = []
    result = json.loads(result)
    products_category = result['GetProductCategoriesForASINResponse']['GetProductCategoriesForASINResult']
    print(products_category)
    del_asin = set(seller_asin) - set(asin_list)
    for a in del_asin:
        a_value = int(dict_asin[a])
        a_value_list.append(a_value)
    a_value_list.sort(reverse=True)
    for de in a_value_list:
        del (products_category[de])
    rr = result
    return rr








