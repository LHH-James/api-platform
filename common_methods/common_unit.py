#coding=utf-8
import sys
sys.path.append('../')
import time
from urllib.parse import quote
import hmac
import base64
import hashlib
import xmltodict
import json
import pymysql as mydatabase
from common_methods import db
import datetime

def make_access_param(execute_command):
    #添加请求中包含的asin
    params = []
    if 'access_key' in execute_command:
        if execute_command['access_key']!='':
            params += ['AWSAccessKeyId='+quote(execute_command['access_key'])]
    if 'mws_token' in execute_command:
        if execute_command['mws_token'] != '':
            params += ['MWSAuthToken=' + quote(execute_command['mws_token'])]
    if 'seller_id' in execute_command:
        if execute_command['seller_id'] != '':
            params += ['SellerId=' + quote(execute_command['seller_id'])]
    if 'market_place_id' in execute_command:
        if execute_command['market_place_id'] != '':
            params += ['MarketplaceId=' + quote(execute_command['market_place_id'])]
    return params

def database_connection():
    try:
        conn = mydatabase.connect(host=db.host, port=db.port, user=db.user, passwd=db.passwd, db=db.db, charset=db.charset)
    except:
        conn = mydatabase.connect(host=db.host, port=db.port, user=db.user, passwd=db.passwd, db=db.db,
                                  charset=db.charset)
    cursor = conn.cursor()
    return cursor,conn

def xmltojson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = json.dumps(xmlparse,indent=1)
    return jsonstr
    #把返回的xml格式处理成json

def get_md5(string):
    md5 = hashlib.md5(string).digest()
    # print(md5)
    md5 = base64.b64encode(md5).decode('ascii')
    # print(md5)
    return md5
    # 计算md5校验
    # 这里python作为一个弱类型语言的坑就出现了
    # 竟然传入值需要解码成ascii

def get_time_stamp():
    time_stamp = time.localtime()
    month = str(time_stamp[1])
    date = str(time_stamp[2])
    if len(month) == 1:
        month = '0'+ month
    if len(date) == 1:
        date = '0'+ date
    if len(str(int(time_stamp[3])-8)) == 2:
        time_stamp = str(time_stamp[0])+'-'+month+'-'+date+'T'+str(int(time_stamp[3])-8)+':'+str(int(time_stamp[4]))+':'+'00'+'.'+'00'
    else:
        time_stamp = str(time_stamp[0])+'-'+month+'-'+date+'T'+'0'+str(int(time_stamp[3])-8)+':'+str(int(time_stamp[4]))+':'+'00'+'.'+'00'

    stmp = time_stamp+'Z'
    return quote(stmp)

    # 计算格林尼治的时间戳
    # 毕竟是0度经线，


#获取店铺表所有新增的店铺的店铺id
def get_store(status):
    cursor, conn = database_connection()
    sid_list = []
    cursor.execute('SELECT id FROM store where status= %s',status)
    for i in cursor.fetchall():
        sid_list.append(i[0])
    return sid_list

def get_skuList(store_id):
    cursor, conn = database_connection()
    cursor.execute("select sku from syn_fba_stocks where store_id='%s'" % (store_id))
    sellerSku_list = []
    for sku in cursor.fetchall():
        sellerSku_list.append(sku[0])
    return sellerSku_list


def get_amazon_keys(store_id):
    cursor,conn = database_connection()
    cursor.execute('SELECT aws_access_key_id,secret_key,seller_id,mws_token,marketplace FROM store WHERE id = %s',store_id)
    store_info = cursor.fetchall()[0]
    # print(store_info)
    user_access = ['aws_access_key_id','secret_key','seller_id','mws_token']
    user_access_dict = {}
    for i in user_access:
        user_access_dict[i] = store_info[user_access.index(i)]
    # print(store_info[4])
    cursor.execute('SELECT dict_value FROM dictionary WHERE id = %s',store_info[4])
    market_place = str(cursor.fetchall()[0][0])
    user_access_dict['market_place'] = market_place
    return user_access_dict
    # 根据传入的store_id去获取对应的亚马逊登录凭证

#时间格式的转换  时间转换为时间数组
def time_to_timeArray(give_time):
    time_stamp = time.strptime(give_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = quote(str(time_stamp[0]) + '-' + str(time_stamp[1]) + '-' + str(time_stamp[2]) + 'T' + str(
        int(time_stamp[3]) - 8) + ':' + str(time_stamp[4]) + ':' + str(time_stamp[5]) + '.' + str(time_stamp[6]))
    stmp = time_stamp[:-2] + 'Z'
    return stmp
    # 计算格林尼治标准时间戳

def anti_sql_inject_attack(sql_keywords_raw):
    # 过滤关键词拦截sql注入攻击
    sql_inject_warning = 0
    sql_keywords = sql_keywords_raw.lower()
    for word in db.reject_word_list:
        if word in sql_keywords:
            sql_inject_warning = 1
            break
    if sql_inject_warning == 0:
        return sql_keywords_raw

    else:
        cursor,conn = database_connection()
        cursor.execute('INSERT INTO warning_of_sql_inject_attack_method(unix_time_stamp_of_attack_happend,comment) values(%s,%s)',(time.time(),'拦截成功一次攻击'))
        conn.commit()
    # 如果不存在攻击，则返回原始语句，如果存在sql攻击，将该次攻击写入数据库并保存，返回空值


def cal_signature(string,secret_key):
    message = bytes(string.encode('utf-8'))
    secret = bytes(secret_key.encode('utf-8'))
    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    signature = signature.decode('utf-8')
    return signature
    #计算签名，必须解码成utf-8的格式

def timestamp_to_datetime(timestamp):
    return (timestamp.split('T')[0])
    # 把时间戳格式化为YYYY-MM-DD格式
    # 其实这个时间戳还不是unix时间戳
    # 其实这个时间戳是亚马逊风格的时间戳，叫亚马逊标准基础时间戳，简称Amazon SB timestamp

def real_print(a):
    for i in a:
        sys.stdout.write(str(i))
    sys.stdout.write('\n')

def get_sql_time_stamp():
    time_stamp = time.localtime()
    time_struct = []
    for i in time_stamp[:6]:
        time_struct.append(str(i))

    for i in time_struct:
        if len(i) == 1:
            time_struct[time_struct.index(i)] = '0'+i

    result = '-'.join(time_struct[:3])+' '+':'.join(time_struct[3:])

    return result

def get_time_stamp_now():
    time_struct = []
    time_stamp = time.localtime()
    for i in time_stamp[:6]:
        time_struct.append(str(i))
    # print(time_struct)
    for i in time_struct[1:]:
        if len(i) == 1:
            time_struct[time_struct.index(i)] = '0'+i

    return '-'.join(time_struct)

def write_log(log_content):
    open("log.log","a").write(get_time_stamp_now()+"\n"+log_content+"\n\n")


# country_code = {
#     'usa':'US',
#     'canada':'CA',
#     'mexico':'MX'
# }
# # 国际通用国家编码

market_place_dict = {
    'US':'ATVPDKIKX0DER',
    'CA':'A2EUQ1WTGCTBG2',
}
# 亚马逊给的国家编码

headers = {
            "Host":"mws.amazonservices.com",
            "x-amazon-user-agent": "AmazonJavascriptScratchpad/1.0 (Language=Javascript)",
            "Content-Type": "text/xml",
            "User_Agent":"Data_Force"
            }
        #公用请求头

default_params = [
            'SignatureMethod=HmacSHA256',
            'SignatureVersion=2'
        ]
        #公用请求参数

# if debug:
#     get_product_info('test')

#2018-08-21


#捕获错误的  异常代码  异常信息
def catch_exception(request_result):
    error=''
    if 'ErrorResponse' in request_result:
        if 'Error' in request_result:
            result = json.loads(request_result)
            error = result['ErrorResponse']['Error']
            # error_code = result['ErrorResponse']['Error']['Code']
            # error_message = result['ErrorResponse']['Error']['Message']
    return error


#将csv格式的转成json
def read_file(f):
    # 获取输入数据
    f_lines = f.splitlines()
    lines = [line.strip() for line in f_lines]
    # 获取键值
    keys = lines[0].split('\t')
    line_num = 1
    total_lines = len(lines)
    parsed_datas = {}
    while line_num < total_lines:
        values = lines[line_num].split("\t")
        # parsed_datas.append(dict(zip(keys, values)))
        parsed_datas[line_num]=(dict(zip(keys, values)))
        line_num = line_num + 1
    json_str = json.dumps(parsed_datas, ensure_ascii=False, indent=4)
    return json_str



#对传入的时间格式的转化
def conver_time(str_time):
    st = str_time.replace('+', ' ')
    # 将其转换为时间数组
    timeStruct = time.strptime(st, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    timeStamp = int(time.mktime(timeStruct))
    localTime = time.localtime(timeStamp)
    str_date = time.strftime("%Y-%m-%d", localTime)
    str_time = time.strftime("%H:%M:%S", localTime)
    iso_datetime = str_date+'T'+str_time
    return iso_datetime



#对传入的时间格式的转化
def conver_date_time(str_time):
    st = str_time.replace('+', ' ')
    timeStruct = time.strptime(st, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeStruct))
    localTime = time.localtime(timeStamp)
    str_date = time.strftime("%Y-%m-%d", localTime)
    return str_date,timeStamp

#=====测试=======
def test_access_param(execute_command):
    if 'seller_id' in execute_command:
        if execute_command['seller_id'] != '':
            seller_id = execute_command['seller_id']
            flag = seller_id.find('XMDF')
    return flag

def read_xmlfile(file_name):
    request_content = open(file_name,'r').read()
    result = xmltojson(request_content)
    return result


report_content = {
    "1": {
        "quantity": "10",
        "price": "4.99",
        "sku": "SampleSKUA",
        "asin": "B072XGX5LM"
    },
    "2": {
        "quantity": "11",
        "price": "4.99",
        "sku": "SampleSKUB",
        "asin": "B0731127ND"
    },
    "3": {
        "price": "9.99",
        "sku": "SampleSKUC",
        "asin": "B073B3J2TQ"
    },
    "4": {
        "quantity": "10",
        "price": "4.99",
        "sku": "SampleSKUD",
        "asin": "B071S12DPC"
    },
    "5": {
        "price": "9.99",
        "sku": "SampleSKUE",
        "asin": "B072ZZHWN2"
    },
    "6": {
        "quantity": "10",
        "price": "5.99",
        "sku": "SampleSKUF",
        "asin": "B07312SBJ9"
    },
    "7": {
        "quantity": "12",
        "price": "5.09",
        "sku": "SampleSKUG",
        "asin": "B072ZVTG5M"
    },
    "8": {
        "quantity": "13",
        "price": "5.99",
        "sku": "SampleSKUH",
        "asin": "B07313N12G"
    }
}
# def make_access_param(user_access_dict,execute_command):
#     #添加请求中包含的asin
#     params = [
#     'AWSAccessKeyId='+quote(user_access_dict['aws_access_key_id']),
#     'MWSAuthToken='+quote(user_access_dict['mws_token']),
#     'SellerId='+quote(user_access_dict['seller_id']),
#     'MarketplaceId='+quote(market_place_dict[user_access_dict['market_place']])
#     ]
#     return params