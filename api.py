import json
import requests
import re
import random
import botSql



botQQ=123456789 #bot的QQ 例:123456789 不用带引号
repeatState=False #复读功能默认为关
admin=botSql.adminAccount() #获取数据库中bot的管理员账号

def botReply(data):
    url='http://localhost:5700/' #5700与go-cqhttp的默认端口相同
    botTrueReply=botSql.trueReply(data['raw_message'])
    if botTrueReply:
        news={'message_type':'group','group_id':data['group_id'],'message':f'{botTrueReply}'}
    else:
        news=''
    i =random.randint(0,300)

    #自带的简单几个对话，可按样式自行添加
    if data['message_type']=="group":
        u='send_msg'
        userID=data['user_id']

        if re.search(r'你(.*)好',data['raw_message']):
            news={'message_type':'group','group_id':data['group_id'],'message':f'[CQ:at,qq={userID}]你谁啊你[CQ:face,id={i}]'}

        elif re.search('涩图',data['raw_message']):
            setu(data)

        elif re.match('/teach (.*) (.*)',data['raw_message']):
            raw_msg=str(data['raw_message'])
            pos0=raw_msg.find(' ')
            pos1=raw_msg.find(' ',pos0+1)
            botListen=data['raw_message'][pos0+1:pos1]
            botReply=data['raw_message'][pos1+1:]
            nowReply=botSql.teachReply(botListen,botReply)
            news={'message_type':'group','group_id':data['group_id'],'message':f'{nowReply}'}

        elif re.match('/delete ',data['raw_message']):
            botListen=data['raw_message'][8:]
            nowReply=botSql.deleteReply(botListen)
            news={'message_type':'group','group_id':data['group_id'],'message':f'{nowReply}'}

        elif data['raw_message']=='/list':
            if data['sender']['user_id'] in admin:
                nowReply=botSql.listReply()
                news={'message_type':'group','group_id':data['group_id'],'message':f'{nowReply}'}
            else:
                news={'message_type':'group','group_id':data['group_id'],'message':f'你无权查看'}
        
        
        elif data['raw_message']=='/help':
            nowReply='1.随机歌曲：\n@我并输入听歌随机推送歌曲\n2.随机图片：\n@我并输入色图随机推送二次元图片\n3.语音功能：\n形如：@暖心爸爸 说话 我是你爹\n4.学习对话：\n形如：/teach xl 神！\n5.删除对话：\n形如：/delete xl\n6.复读机：\nadmin可用@我输入re开启 输入!re关闭'
            news={'message_type':'group','group_id':data['group_id'],'message':f'{nowReply}'}

        requests.post(url=url+u,json=news)

#功能触发
def botSkill(data):
    url='http://localhost:5700/send_msg'
    news=''
    global repeatState

    if data['raw_message']==f'[CQ:at,qq={botQQ}] re':
        news={'message_type':'group','group_id':data['group_id'],'message':'done'}
        repeatState=True

    elif data['raw_message']==f'[CQ:at,qq={botQQ}] !re':
        news={'message_type':'group','group_id':data['group_id'],'message':'done'}
        repeatState=False

    elif data['raw_message']==f'[CQ:at,qq={botQQ}] 听歌':
        news={'message_type':'group','group_id':data['group_id'],'message':'哥来咯'}
        music(data)
    elif data['raw_message'][:24]==f'[CQ:at,qq={botQQ}] 说话 ':
        voiceReply(data)
    elif data['raw_message']==f'[CQ:at,qq={botQQ}] 色图':
        setu(data)
    if news!='':
        requests.post(url=url,json=news)


#复读
def repeat(data):
    url='http://localhost:5700/send_msg'
    if repeatState:
        news={'message_type':'group','group_id':data['group_id'],'message':data['raw_message']}
        requests.post(url=url,json=news)


#色图
def setu(data):

    menu = requests.get('https://api.lolicon.app/setu/v2')
    menu1=json.loads(menu.text)
    menu2=menu1['data'][0]['urls']['original']
    menu3=menu1['data'][0]['tags']
    msg = [f'[CQ:image,file={menu2}]',f'{menu3}']
    #以请求图片的人的群转发消息来发送
    group_msg = []
    for item in msg:
        each_msg = {
            "type": "node",
            "data": {
                "name": data['sender']['nickname'],
                "uin": data['sender']['user_id'],
                "content": item
            }
        }
        group_msg.append(each_msg)
    news = {
        'group_id':data['group_id'], # '消息发送的QQ群号'
        'messages':group_msg
    }
    url = "http://127.0.0.1:5700/send_group_forward_msg"
    rev3 = requests.post(url,json=news)

#听歌
def music(data):
    url='http://localhost:5700/send_msg'
    menu=requests.get('https://api.uomg.com/api/rand.music?format=json')
    menu1=json.loads(menu.text)
    menu2=menu1['data']['url']
    num=menu2.find('=')
    menu3=menu2[(num+1):]
    news={'message_type':'group','group_id':data['group_id'],'message':f'[CQ:music,type=163,id={menu3}]'}
    requests.post(url=url,json=news)

#语音
def voiceReply(data):
    url='http://localhost:5700/send_msg'
    mess=data['raw_message'][24:]
    news={'message_type':'group','group_id':data['group_id'],'message':f'[CQ:tts,text={mess}]'}
    requests.post(url=url,json=news)

