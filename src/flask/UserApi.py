import base64
import copy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, render_template, request, session, Response, make_response, url_for
import re
from Utils import Constants, Tools, PrivateConfigurations, DbUtil, ImageCode

usrBp = Blueprint("usr", __name__)

ErspUser = [
    {
        "status": "200",
        "desc": "Register Success"
    },
    {
        "status": "usr-1",
        "desc": "Empty input for E-mail, password or verification code."
    },
    {
        "status": "usr-2",
        "desc": "Email format incorrect."
    }, {
        "status": "usr-3",
        "desc": "Password at least 8 digits, including numbers and characters."
    }, {
        "status": "usr-4",
        "desc": "Wrong verification code."
    }, {
        "status": "usr-5",
        "desc": "Email already registered."
    }, {
        "status": "usr-6",
        "desc": "Wrong email or password."
    }, {
        "status": "usr-7",
        "desc": "Nickname can't be empty."
    }, {
        "status": "usr-8",
        "desc": "Image not provided."
    }, {
        "status": "usr-9",
        "desc": "Operation need to login first."
    },
]


@usrBp.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['pass']
    verify_code = request.form['veri']

    if not email or not password or not verify_code:
        return ErspUser[1]
    elif not re.match(Constants.Reg_Email, email):
        return ErspUser[2]
    elif not re.match(Constants.Reg_Pass, password):
        return ErspUser[3]
    else:
        def query(conn):
            cursor = conn.cursor()
            cursor.execute("select vcid from db_vericode where email = %(email)s and code = %(code)s limit 1;",
                           {"email": email, "code": verify_code.upper()})
            if not cursor.fetchall():
                return ErspUser[4]
            else:
                cursor.execute("select uid from db_user where email = %(email)s limit 1;",
                               {"email": email, "code": verify_code.upper()})
                if cursor.fetchall():
                    return ErspUser[5]
                else:
                    cursor.execute("insert into db_user(email,pwd,nickname) values(%(email)s,%(pwd)s,%(email)s);",
                                   {"email": email, "pwd": Tools.md555(password)})
                    fetch = cursor.fetchall()
                    if not fetch:
                        cursor.execute(
                            "select uid,email,nickname,date_birth from db_user where email=%(email)s and pwd = %(pwd)s limit 1;",
                            {"email": email, "pwd": Tools.md555(password)})
                        frst = cursor.fetchall()
                        session['usr'] = frst[0]
                        session['isLogin'] = True

                        return Tools.gen200rsp("Register success.")
                    else:
                        return Constants.rsp_se

    return DbUtil.execute(query)


@usrBp.route("/emailVerify", methods=["POST"])
def email_verify():
    email = request.form['email']
    if not re.match(Constants.Reg_Email, email):
        return ErspUser[2]
    code = Tools.generate_verification_code()

    # content = render_template("vericode.html", vericode=code, email=email)
    #
    # msg = MIMEMultipart()
    # msg["Subject"] = "User Registration Verification Code"
    # msg["From"] = "Urchin"
    # msg["To"] = email
    # msg.attach(MIMEText(content, "html", "utf-8"))
    #
    # s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # s.login(PrivateConfigurations.mail, PrivateConfigurations.pas)
    # s.sendmail(PrivateConfigurations.mail, email, msg.as_string())
    # s.quit()

    def sql(conn):
        conn.cursor().execute("insert into db_vericode(email,code) values(%(email)s,%(code)s);",
                              {"email": email, "code": code})
        return Tools.gen200rsp("Verification code sent to mailbox.")

    return DbUtil.execute(sql)


@usrBp.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['pass']
    verify_code = request.form['veri']
    print("verify_code:" + verify_code)
    print("sescode:" + session['vcode'])

    if not email or not password or not verify_code:
        return ErspUser[1]
    elif not re.match(Constants.Reg_Email, email):
        return ErspUser[2]
    elif not re.match(Constants.Reg_Pass, password):
        return ErspUser[3]
    elif verify_code != session['vcode']:
        return ErspUser[4]
    else:

        def query(conn):
            cursor = conn.cursor()
            cursor.execute(
                "select uid,email,nickname,date_birth from db_user where email=%(email)s and pwd = %(pwd)s limit 1;",
                {"email": email, "pwd": Tools.md555(password), "code": verify_code.upper()})
            frst = cursor.fetchall()
            if not frst:
                return ErspUser[6]
            else:
                session['usr'] = frst[0]
                session['isLogin'] = True
                return Tools.gen200rsp("Login success, refreshing.")
    return DbUtil.execute(query)


@usrBp.route("/accountInfo")
def account_info():
    return render_template("accountInfo.html", title="Account Information")


@usrBp.route("/logout")
def logout():
    session.clear()
    response = make_response("Log out", 302)
    response.headers["Location"] = url_for("home.home")
    return response


@usrBp.route("/updateAccount", methods=["POST"])
def update_account():
    nick = request.form['nick']
    date = request.form['date']
    if not date or date == "****-**-**":
        date = None

    if not nick:
        return ErspUser[7]
    else:
        def sql(conn):
            cursor = conn.cursor()
            cursor.execute(
                'update db_user set nickname=%(nick)s, date_birth=%(date)s where uid=%(uid)s;',
                {"nick": nick, "date": date, "uid": session['usr']['uid']})
            rst = cursor.fetchall()
            if not rst:
                session['usr']['nickname'] = nick
                session['usr']['date_birth'] = date
                session.modified = True
                return Tools.gen200rsp("Update success.")
            else:
                return Constants.rsp_se

        return DbUtil.execute(sql)


@usrBp.route('/uploadImage', methods=['POST'])
def upload_image():
    data = request.get_json()
    # remove "data:image/png;base64,"
    base64_image = data.get('image').split(',')[1]
    if not base64_image:
        return ErspUser[8]
    try:
        def sql(conn):
            cursor = conn.cursor()
            cursor.execute(
                'update db_user set img=%(img)s where uid=%(uid)s;',
                {"img": base64_image, "uid": session['usr']['uid']})
            rst = cursor.fetchall()
            if not rst:
                return Tools.gen200rsp("Image updated.")
            else:
                return Constants.rsp_se

        return DbUtil.execute(sql)
    except Exception as e:
        return Constants.rsp_se, 500


@usrBp.route('/get_avatar', defaults={"tuid": ""})
@usrBp.route('/ge_avatar/<tuid>')
def get_avatar(tuid):
    if not tuid:
        tuid = session['usr']['uid']
    conn = DbUtil.prepare()
    cursor = conn.cursor()
    cursor.execute(
        "select img from db_user where uid = %(uid)s limit 1;",
        {"uid": tuid})
    frst = cursor.fetchall()
    DbUtil.culminate(conn)
    if not frst:
        return ErspUser[6]
    else:
        if frst[0]["img"] is None:
            image_binary = ""
        else:
            image_binary = base64.b64decode(frst[0]["img"])
        return Response(image_binary, mimetype='image/png')


@usrBp.route("/focusAuthor")
def focus_author():
    if not session['usr']:
        return ErspUser[9]

    tuid = request.args.get("tuid")
    status = request.args.get("status")
    if status != "-":
        status = "+"

    def query(conn):
        cursor = conn.cursor()
        cursor.execute(
            "insert into db_focus(uid,tuid,status) values(%(uid)s,%(tuid)s,%(status)s);",
            {"uid": session['usr']['uid'], "tuid": tuid, "status": status})
        fetch = cursor.fetchall()
        if not fetch:
            cursor.execute(
                "update db_user u set u.num_focus=u.num_focus{}1 where u.uid = %(tuid)s;".format(
                    status),
                {"tuid": tuid})
            return Tools.gen200rsp("Author focused.")
        else:
            return Constants.rsp_se

    return DbUtil.execute(query)


@usrBp.route("/vcode")
def vcode():
    code, byte_string = ImageCode.byte_code()
    rsp = make_response(byte_string)
    rsp.headers["Content-Type"] = "image/jpeg"
    session["vcode"] = code.lower()
    return rsp
