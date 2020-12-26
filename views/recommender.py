from flask import Blueprint, request, jsonify, render_template
from recommender.run import getRecommendedList
from models.User import User

recommender = Blueprint('recommender', __name__)


def init_blue(app):
    app.register_blueprint(blueprint=recommender)


@recommender.route('/generate', methods=["POST"])
def generate():
    """
    接收用户参数，返回文章信息
    :return:
    """
    mode = request.json.get("mode")  # mode=1表示仅返回推荐列表，mode=0表示返回推荐列表+分类列表（肺部肿瘤、肝部。。）
    username = request.json.get("username")
    user_id = 0  # 需要连接数据库查询用户ID，此处方便调试，设置为0
    article_id_list = getRecommendedList(user_id, num=50)
    # TODO 数据库查询，返回文章详情列表，python进行数据库查询尽量需要使用try，except
    article_list = []
    """
    data示例：[{"title":"","from":"","url":"","article_id",""}]
    """
    return jsonify({
        'flag': 1,
        'data': article_list

    })
