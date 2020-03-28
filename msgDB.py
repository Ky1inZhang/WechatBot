import sqlite3
import time
import json
import urllib.request

# https://github.com/Ky1inZhang/WechatBot     api文档
#底层通信
def initDB():
      global conn
      conn = sqlite3.connect('exchange.db',check_same_thread=False)
      print ("Opened database successfully")
      
def endDB():
      conn.close()

def sendMsg(token,cmd,id1,id2,id3):
      conn.execute('INSERT INTO WX_COMMAND (TOKEN,CMD_TYPE,ID_1,ID_2,ID_3)\
                   VALUES ("%s", "%s", "%s", "%s","%s")'%(token,cmd,id1,id2,id3))
      conn.commit()
      print ("Records created successfully")

def recMsg():
      result=conn.execute('select * from wx_event limit 0,1')
      return (list(result))

def delMsg():
      conn.execute("delete from wx_event where ID1 in(select ID1 from wx_event limit 1)")
      conn.commit()

def send_wxPicture(wxid,picPath):
      sendMsg('0','wx_picture',wxid,picPath,"null")

#以下函数进行了一次封装
def send_wxMsg(wxid,text):
      sendMsg('0','wx_send',wxid,text,"null")

def listen_wxMsg():
      time.sleep(0.1)
      res=recMsg()
      if len(res)!=0:
            #print(recMsg()[0])
            return res[0]
      else:
            return "False"



# 图灵请求回复
def getMsg(msg):
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    text_input = msg

    req = {
        "perception":
        {
            "inputText":
            {
                "text": text_input
            },
        },
        "userInfo": 
        {
            "apiKey": "17abd15ba99e460a8b8cc2d433e97df9",
            "userId": "OnlyUseAlphabet"
        }
    }
    # print(req)
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    # print(req)

    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    # print(response_str)
    response_dic = json.loads(response_str)
    # print(response_dic)

    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    # print('Turing的回答：')
    # print('code：' + str(intent_code))
    # print('text：' + results_text)
    print(results_text)
    return results_text



if __name__=="__main__":
      initDB()#初始化
      # for i in range(1000):
      #       delMsg()#清空数据库
      while True: #死循环
            res=listen_wxMsg()#监听一次是否有新消息（本质是查询一次数据库是否有记录）
            if res==False:#无新消息产生则开始下一轮监听
                  continue
            if res[0]=="wxid_c5du2oo2mwhi12":#res[3]存着别人发来的消息
                  print(res[0] )
                  response = getMsg(res[3])
                  send_wxMsg(res[0],response)#res[0]是发送消息的人的id
            if res[3]=="picture":
                  print(res[0])
                  send_wxPicture(res[0],"C:\\1.jpg")#发送图片的函数，必须传入本地图片路径，不能是链接
            delMsg()#处理完该消息后把消息从数据库删除
