import logging
import os
import Utils.Logger

from flask import Flask, render_template
from HomeApi import homeBp
from ArticleApi import articleBp
from UserApi import usrBp
from Filters import filBp
from Utils.Env import config
from Utils.Logger import init_log


def getapp():
    init_log()
    ap = Flask(__name__, template_folder="../template", static_url_path="/", static_folder="../resource")
    return ap


app = getapp()
app.register_blueprint(homeBp)
app.register_blueprint(articleBp)
app.register_blueprint(usrBp)
app.register_blueprint(filBp)

app.config['SECRET_KEY'] = "b'\x96!_\xea\x8e\xaa\xa3n\x94\xc0?\xa5\t\x83^\xeew\xb9X\x08\t#\xdb?'"
# app.config['SECRET_KEY'] = os.urandom(24)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  # 禁止 JavaScript 访问
    SESSION_COOKIE_SECURE=True,  # 仅 HTTPS 传输
    SESSION_COOKIE_SAMESITE='Lax'  # 防止 CSRF 攻击
)


@app.errorhandler(404)
def uni_404(error):
    return render_template("404.html")


@app.route("/404")
def route_404():
    return render_template("404.html")


@app.route("/test")
def test():
    return "test ok"


if __name__ == '__main__':
    app.run(**config.flask_app)
    # app.run(host="0.0.0.0", debug=True, port=3321)
