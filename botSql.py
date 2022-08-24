import pymysql

#请自行在数据库内创建两个表，一个名为admin(id INT64 , username CHAR64 , account CHAR64)用于记录管理员账号，
#另一个可自己命名，但是需要在下面的botTable变量中填入表名(listen CHAR64 , reply CHAR64)

def adminAccount():
    account=[]
    sql="select account from admin;"
    botcursor.execute(sql)
    res=botcursor.fetchall()
    for i in range(len(res)):
        account.append(res[i][0])
    return account

def teachReply(botListen,botReply):
    sql=f'select reply from {botTable} where listen=%s;'
    botcursor.execute(sql,botListen)
    res=botcursor.fetchall()
    if res:
            return '我早就知道了'
    else:
        sql=f'insert into {botTable} (listen,reply) values (%s,%s);'
        botcursor.execute(sql,(botListen,botReply))
        botdb.commit()
        return '你爹知道了'

def deleteReply(botListen):
    sql=f'select reply from {botTable} where listen=%s;'
    botcursor.execute(sql,botListen)
    res=botcursor.fetchall()
    if res:
        sql=f'delete from {botTable} where listen=%s;'
        botcursor.execute(sql,botListen)
        botdb.commit()
        return '我的记忆。。。消失了？'
    else:
        return '你想删掉什么！？'

def trueReply(botListen):
    sql=f'select reply from {botTable} where listen=%s;'
    botcursor.execute(sql,botListen)
    res=botcursor.fetchall()
    if res:
        return res[0][0]
    else:
        pass

def listReply():
    first=1
    sql=f'select * from {botTable};'
    botcursor.execute(sql)
    res=botcursor.fetchall()
    reStr=''
    for i in range(len(res)):
        if first:
            first=0
            pass
        else:
            reStr+='\n'
        reStr+=f'{i+1}.'
        reStr+=res[i][0]
        reStr+=' '
        reStr+=res[i][1]
    return reStr
    


botdb = pymysql.connect(host='localhost',#数据库地址
                       port=3306,#数据库端口
                       user='root',#数据库用户名
                       passwd='root',#数据库密码
                       database='bot',#数据库名
                       charset = 'utf8'
                       )

botcursor = botdb.cursor()#获取操作游标
botTable=''#数据库表名

