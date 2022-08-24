import botSql
from flask import Flask, request
import api

app = Flask(__name__)
admin=botSql.adminAccount()
botQQ=123456789 #bot的QQ 不用带引号

'''监听端口，获取QQ信息'''
@app.route('/', methods=["POST"])

def post_data():
	data=request.get_json()
	if 'message_type' in data:
		if  f'[CQ:at,qq={botQQ}]' in data['raw_message'] and data['sender']['user_id'] in admin:
			repeatState=api.botSkill(data)
			print(repeatState)
		else:
			api.botReply(data)
		if f'[CQ:at,qq={botQQ}]' not in data['raw_message'] and 'group_id' in data:
			api.repeat(data)
		
	return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)# 此处的 host和 port对应 go-cqhttp yml文件的设置

