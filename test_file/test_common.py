import random
import pymysql
import datetime

# 查询
def select_sql(sql):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    resp = cursor.fetchall()
    db.commit()
    return resp

def get_order_id():
    order_id = 'DF-' + str(random.randint(100, 999)) + \
               '-' + str(random.randint(1000000, 9999999)) + \
               '-' + str(random.randint(1000000, 9999999))
    return order_id

def get_orderitem_id():
    item_id = random.randint(10000000000000, 99999999999999)
    return str(item_id)

# 获取订单id
def get_order_ids():
    sql = 'select order_id from test_orderlist'
    ids = select_sql(sql)
    ids = [id[0] for id in ids]
    return ids

# 获取订单
def get_order_list(dt):
    sql = 'select order_id, time from test_orderlist where date(time)>="%s"' % dt
    orders = select_sql(sql)
    return orders

# 获取订单通过id
def get_order_list_by_id(id):
    sql = 'select order_id, time from test_orderlist where order_id="%s"' % id
    order = select_sql(sql)
    return order

# 获取订单明细
def get_order_item(order_id):
    sql = 'select * from test_orderlist_item where order_id="%s"' % order_id
    order_item = select_sql(sql)
    return order_item

# 获取库存信息
def get_inventory():
    sql = 'select asin, sku, quantity from test_inventory'
    inventory = select_sql(sql)
    return inventory

# 添加订单
def add_order_list(id, dt):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    sql = 'INSERT INTO test_orderlist (order_id, time) VALUES ("%s", "%s")' % (id, dt)
    cursor.execute(sql)
    db.commit()

# 添加订单明细
def add_orderitem_list(item_id, order_id, asin, sku, title):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    sql = 'INSERT INTO test_orderlist_item (order_item_id, order_id, asin, seller_sku, title) ' \
          'VALUES ("%s", "%s", "%s", "%s", "%s")' % (item_id, order_id, asin, sku, title)
    cursor.execute(sql)
    db.commit()

# 更新商品库存
def update_inventory(num, sku):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    sql = 'UPDATE test_inventory SET quantity="%s" WHERE sku="%s"' %(num, sku)
    cursor.execute(sql)
    db.commit()

def update_order(order_id, order_time):
    order = {
        'AmazonOrderId': order_id,
        'SellerOrderId': order_id,
        'LatestShipDate': order_time,
        'PurchaseDate': order_time,
        'LastUpdateDate': order_time,
        'EarliestShipDate': order_time,
        'CreatedBefore': order_time
    }
    return order

# 通过订单id返回测试订单模板
def get_test_order(params, result):
    order_id = params.get('order_id', None)
    if order_id:
        order = get_order_list_by_id(order_id)
        if order:
            id = order[0][0]
            order_time = order[0][1].replace(' ', 'T') + 'Z'
            test_order = update_order(id, order_time)
            test_order.pop('CreatedBefore')
            result.get('GetOrderResponse') \
                  .get('GetOrderResult') \
                  .get('Orders') \
                  .get('Order') \
                  .update(test_order)
        else:
            orders = {
                'Orders': ''
            }
            result.get('GetOrderResponse') \
                  .get('GetOrderResult') \
                  .update(orders)

# 返回测试订单模板
def get_test_order_list(params, result):
    start_time = params.get('create_time', None)
    if start_time:
        order_list = get_order_list(start_time)
        if order_list:
            orders = []
            test_orders = result.get('ListOrdersResponse') \
                                .get('ListOrdersResult') \
                                .get('Orders') \
                                .get('Order')
            for order in order_list:
                order_id = order[0]
                order_time = order[1].replace(' ', 'T') + 'Z'
                test_order = update_order(order_id, order_time)
                test_orders.update(test_order)
                orders.append(test_orders)
            result.get('ListOrdersResponse') \
                  .get('ListOrdersResult') \
                  .update({'Orders': orders})
        else:
            # 添加订单
            order_id = get_order_id()
            order_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            orders = update_order(order_id, order_time)
            result.get('ListOrdersResponse') \
                  .get('ListOrdersResult') \
                  .get('Orders') \
                  .get('Order') \
                  .update(orders)
            add_order_list(order_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # 添加订单明细
            inventory = get_inventory()
            inventory = random.choice(inventory)
            asin = inventory[0]
            sku = inventory[1]
            title = sku + '_Title'
            item_id = get_orderitem_id()
            add_orderitem_list(item_id, order_id, asin, sku, title)
            # 更新商品库存
            num = inventory[2]
            num = int(num) - 1
            update_inventory(num, sku)


def update_orderitem(item_id, asin, sku, title):
    order_item = {
        'OrderItemId': item_id,
        'ASIN': asin,
        'SellerSKU': sku,
        'Title': title
    }
    return order_item

# 返回测试订单明细模板
def get_test_orderitem_list(params, result):
    order_id = params.get('order_id', None)
    if order_id:
        order_ids = get_order_ids()
        if order_id in order_ids:
            order_item = get_order_item(order_id)
            id = order_item[0][2]
            item_id = order_item[0][1]
            asin = order_item[0][3]
            sku = order_item[0][4]
            title = order_item[0][5]
            orderitem = update_orderitem(item_id, asin, sku, title)
            result.get('ListOrderItemsResponse') \
                  .get('ListOrderItemsResult') \
                  .get('OrderItems') \
                  .get('OrderItem') \
                  .update(orderitem)
            result.get('ListOrderItemsResponse') \
                  .get('ListOrderItemsResult') \
                  .update({
                'AmazonOrderId': id
            })
        else:
            order_items = {
                'OrderItems': ''
            }
            result.get('ListOrderItemsResponse') \
                .get('ListOrderItemsResult') \
                .update(order_items)
            result.get('ListOrderItemsResponse') \
                .get('ListOrderItemsResult') \
                .update({
                'AmazonOrderId': order_id
            })


