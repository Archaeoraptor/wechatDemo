
from flask import Flask, request, Response, render_template
from common.util import validate_wx_public,parseXML,createXML,createMenu,sendMsg
from validate.form import WxpublicForm
app = Flask(__name__)
#创建menu自定义菜单
createMenu()
sendMsg()

@app.route('/',methods=['GET','POST'])
def validate():
    if request.method == 'GET':
        data = request.args.to_dict()
        form = WxpublicForm(**data)
        if form.validate():
            result = validate_wx_public(form)
            if result[0]:
                return result[1]
        else:
            ValueError
    else:
        str = request.get_data()
        parseXML(str)
        xml = "<xml>" \
              "<ToUserName><![CDATA[oIPLH1P31seTfvqU2Gvr852DHS_Q]]></ToUserName>" \
              "<FromUserName><![CDATA[gh_9715d2592755]]></FromUserName>" \
              "<CreateTime>12345678</CreateTime>" \
              "<MsgType><![CDATA[text]]></MsgType>" \
              "<Content><![CDATA[我是胖胡]]></Content>" \
              "</xml>"
        return Response(xml, mimetype='text/xml')


@app.route('/list/',methods=["GET","POST"])
def getList():
    return render_template("html/list.html")


if __name__ == '__main__':
    app.run()
