import mysql.connector

cnx=None

# def filter_input(max_length=100):
#     while True:
#         input_string = input("请输入字符串：")

#         # 过滤中文字符
#         input_string = re.sub(r'[\u4e00-\u9fa5]', '', input_string)

#         # 过滤特殊字符和十六进制代码
#         input_string = re.sub(r'[^\w\s]', '', input_string)
#         input_string = re.sub(r'\\x..', '', input_string)

#         # 防止SQL注入
#         input_string = pymysql.escape_string(input_string)

#         # 限制长度
#         if len(input_string) > max_length:
#             print("输入的字符串超过了最大长度，请重新输入。")
#             continue

#         return input_string
    
def connect_db():
    # 连接数据库
    global cnx
    try:
        cnx = mysql.connector.connect(user='root', password='oj.jzxx.net',host='127.0.0.1',database='screenshot')
        print("数据库连接成功")
    except mysql.connector.Error as err:
        print("数据库连接失败: {}".format(err))

def init_db():
    global cnx
    try:
        cursor = cnx.cursor()
        cursor.execute("CREATE TABLE if not exists Users (account CHAR(100) PRIMARY KEY, password CHAR(100))") # 创建表
        cursor.execute("CREATE TABLE if not exists IP (account CHAR(100), ip CHAR(100),port INT)") # 创建表
        cursor.close()
    except mysql.connector.Error as err:
        print("创建失败: {}".format(err))

def login(account,password):
    global cnx
    try:
        cursor = cnx.cursor()
        query = ("SELECT * FROM Users WHERE account = %s AND password = %s")
        cursor.execute(query, (account,password))
        if cursor.fetchone():
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("查询失败: {}".format(err))

def register(account:str,password:str):
    global cnx
    try:
        cursor = cnx.cursor()
        cursor.execute("CREATE TABLE if not exists Users (account CHAR(100) PRIMARY KEY, password CHAR(100))") # 创建表
        # 创建插入SQL语句
        add_data = ("INSERT INTO Users "
                "(account, password) "
                "VALUES (%s, %s)")
        # 插入新数据
        cursor.execute(add_data,(account,password))
        # 提交到数据库
        cnx.commit()
        cursor.close()
        print("插入成功")
        return True
    except mysql.connector.Error as err:
        print("插入失败: {}".format(err))
        return False

def add_IP(account:str,ip:str,port:int):
    global cnx
    try:
        cursor = cnx.cursor()
        # 创建插入SQL语句
        add_data = ("INSERT INTO IP "
                "(account, ip,port) "
                "VALUES (%s, %s,%s)")
        # 插入新数据
        cursor.execute(add_data,(account,ip,port))
        # 提交到数据库
        cnx.commit()
        cursor.close()
        print("插入成功")
    except mysql.connector.Error as err:
        print("插入失败: {}".format(err))

def get_IP(account:str):
    global cnx
    try:
        cursor = cnx.cursor()
        query = ("SELECT IP,PORT FROM IP WHERE account = %s ORDER BY ip ASC, port ASC")
        cursor.execute(query, (account,))
        result=[]
        for (ip,port) in cursor:
            print(f"account: {account}, ip: {ip},port: {port}")
            result.append((ip,port))
        cursor.close
        return result
    except mysql.connector.Error as err:
        print("查询失败: {}".format(err))

def close_db(cnx):
    cnx.close()

if __name__ == "__main__":
    connect_db()
    add_IP('','127.0.0.1',9999)
    close_db(cnx)