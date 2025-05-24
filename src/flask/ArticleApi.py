import base64
import json
import os
import datetime

from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify

from Utils import Tools, Constants, DbUtil

articleBp = Blueprint("art", __name__)

UE_CONFIG = {
    "imageActionName": "uploadimage",
    "imageFieldName": "upfile",
    "imageMaxSize": 2048000,
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "imageCompressEnable": True,
    "imageInsertAlign": "none",
    "imageUrlPrefix": "",
}

ErspUser = [
    {
        "status": "200",
        "desc": "Register Success"
    },
    {
        "status": "art-1",
        "desc": "Operation need to login first."
    },
]


@articleBp.route("/new/<aid>")
@articleBp.route("/new/", defaults={"aid": ""})
@articleBp.route("/new", defaults={"aid": ""})
def new_art(aid):
    if 'usr' not in session:
        return redirect(url_for('home.home', login=True))
    else:
        randis = os.listdir("../resource/pic/randcover")
        randfs = []

        for fn in randis:
            randfs.append("/" + fn)

        conn = DbUtil.prepare()
        cursor = conn.cursor()
        cursor.execute(
            "select * from db_artype order by ayid;")
        artypes = cursor.fetchall()

        cursor.execute(
            "select * from db_artcat where acid not in (1,2,3) and opt not like 'col%' order by acid;")
        cats = cursor.fetchall()

        cursor.execute(
            "select * from db_artag;")
        tags = cursor.fetchall()

        cursor.execute(
            "select aid,title,content,coalesce(update_time,create_time) as time from db_article where uid=%(uid)s and status=2;",
            {"uid": session['usr']['uid']})
        drafts = cursor.fetchall()

        drafted = ""
        if aid:
            cursor.execute(
                "select aid,title,content from db_article where aid=%(aid)s and status=2 and uid=%(uid)s;",
                {"aid": aid, "uid": session['usr']['uid']})
            drafted = cursor.fetchone()
            print(drafted)

        DbUtil.culminate(conn)
        return render_template("newArt.html", artypes=artypes, cats=cats, tags=tags, randfs=randfs, drafts=drafts,
                               drafted=drafted)


@articleBp.route("/content/<aid>")
def art_content(aid):
    conn = DbUtil.prepare()
    cursor = conn.cursor()

    # article main content
    sqlart = """
    SELECT a.aid,a.title,a.content,a.uid,a.num_fav,a.num_like,a.acid,a.ayid,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                    FROM db_article a
                    LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                    where a.aid={}
                    GROUP BY a.aid
                    LIMIT 1;
    """.format(aid)
    cursor.execute(sqlart)
    arts = cursor.fetchall()
    if arts == ():
        return redirect(url_for('route_404'))

    # article author uid
    uid = arts[0]['uid']

    # view num +1
    cursor.execute("update db_article set num_view=num_view+1 where aid=%(aid)s;", {"aid": aid})

    # author information
    sql_author = """
    select nickname,job,intro,img,num_art,num_focus,num_laf from db_user where uid=%(uid)s;
    """
    cursor.execute(sql_author, {"uid": uid})
    author = cursor.fetchone()

    # other article of this author
    sql_other = """
    SELECT a.aid,a.title,a.cover,a.num_view,DATE_FORMAT(a.create_time, '%%m.%%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                    FROM db_article a
                    LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                    where a.uid=%(uid)s and a.aid!=%(aid)s
                    GROUP BY a.aid
                    LIMIT 5;
    """
    cursor.execute(sql_other, {"uid": uid, "aid": aid})
    other = cursor.fetchall()

    # comments
    sql_comments = """
        select r.uid,r.rid,r.content,u.nickname,DATE_FORMAT(r.create_time, '%%m.%%d') AS date,(
            select JSON_ARRAYAGG(
                JSON_OBJECT(
                    'rid', rr.rid,
                    'uid', rr.uid,
                    'rtuid', rr.rtuid,
                    'rtname', uut.nickname,
                    'content', rr.content,
                    'nickname', uu.nickname,
                    'date', DATE_FORMAT(rr.create_time, '%%m.%%d')
                )
            )
            from db_reply rr
            join db_user uu on uu.uid=rr.uid
            join db_user uut on uut.uid=rr.rtuid
            where rr.rbid=r.rid
        ) as replies
        from db_reply r
        join db_user u on u.uid=r.uid
        where r.aid=%(aid)s and r.rbid is null;
        """
    cursor.execute(sql_comments, {"aid": aid})
    comments = cursor.fetchall()
    for row in comments:
        if row["replies"]:  # 确保 replies 不是 NULL
            row["replies"] = json.loads(row["replies"])

    like_status = False
    focus_status = False
    # logined
    if 'usr' in session:
        # article was liked or not
        sql_like = """
        select sum(case when status="+" then 1 else -1 end) as net from db_like where aid=%(aid)s and uid=%(uid)s;
        """
        cursor.execute(sql_like, {"uid": session['usr']['uid'], "aid": aid})
        likerst = cursor.fetchone()
        if likerst['net'] is None:
            like_status = False
        elif likerst['net'] > 0:
            like_status = True

        # author was focused or not
        sql_focus = """
                    select sum(case when status="+" then 1 else -1 end) as net from db_focus where tuid=%(tuid)s and uid=%(uid)s;
                    """
        cursor.execute(sql_focus, {"uid": session['usr']['uid'], "tuid": uid})
        focusrst = cursor.fetchone()
        if focusrst['net'] is None:
            focus_status = False
        elif focusrst['net'] > 0:
            focus_status = True

    DbUtil.culminate(conn)

    return render_template("artContent.html", title=arts[0]['title'], art=arts[0], author=author, other=other,
                           like_status=like_status, focus_status=focus_status, comments=comments)


@articleBp.route('/ueditor/controller', methods=['GET', 'POST'])
def upload_image():
    action = request.args.get('action')
    # return UEditorplus configuration
    if request.method == 'GET' and action == "config":
        return jsonify(UE_CONFIG)

    # receive images
    if request.method == 'POST' and action == "uploadimage":
        file = request.files['upfile']
        # milisecond that drops last 3 digit
        fmtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        filename = f"{fmtime}-{file.filename}"
        file.save(f"../resource/pic/uploads/{filename}")  # save in server
        return jsonify({
            "state": "SUCCESS",
            "url": f"/pic/uploads/{filename}",
            "title": file.filename,
            "original": file.filename
        })
    return jsonify({"state": "ERROR", "message": "Invalid request"}), 400


@articleBp.route('/publish', methods=['POST'])
def publish():
    return add_article("1")
    # return Tools.gen200rsp("Publish success.")


@articleBp.route('/draft', methods=['POST'])
def draft():
    return add_article("2")


def add_article(status):
    print(f"json = {request.get_json()}")
    title = request.get_json()["title"]
    content = request.get_json()["content"]
    if status == "1":
        aid = ""
        cover = request.get_json()["cover"]
        acid = request.get_json()["acid"]
        ayid = request.get_json()["ayid"]
        atids = request.get_json()["atids"]
    else:
        aid = request.get_json()["aid"]
        cover = "0"
        acid = "0"
        ayid = "0"
        atids = "0"

    def query(conn):
        cursor = conn.cursor()
        if aid:
            cursor.execute(
                "update db_article set title=%(title)s,content=%(content)s where aid=%(aid)s;",
                {"title": title, "content": content, "aid": aid})
        else:
            cursor.execute(
                "insert into db_article(title,content,cover,uid,acid,ayid,atids,status) values(%(title)s,%(content)s,%(cover)s,%(uid)s,%(acid)s,%(ayid)s,%(atids)s,%(status)s);",
                {"title": title, "content": content, "cover": cover, "uid": session['usr']['uid'], "acid": acid,
                 "ayid": ayid,
                 "atids": atids, "status": status})
        fetch = cursor.fetchall()
        if not fetch:
            if status == "1":
                cursor.execute("update db_user set num_art=num_art+1 where uid=%(uid)s", {"uid": session['usr']['uid']})
                return Tools.gen200rsp("Article publish success.")
            else:
                return Tools.gen200rsp("Draft saved.")
        else:
            return Constants.rsp_se

    return DbUtil.execute(query)


@articleBp.route('/like')
def like():
    if not session['usr']:
        return ErspUser[1]

    aid = request.args.get("aid")
    status = request.args.get("status")
    if status != "-":
        status = "+"

    def query(conn):
        cursor = conn.cursor()
        cursor.execute(
            "insert into db_like(uid,aid,status) values(%(uid)s,%(aid)s,%(status)s);",
            {"uid": session['usr']['uid'], "aid": aid, "status": status})
        fetch = cursor.fetchall()
        if not fetch:
            cursor.execute(
                "update db_user u set u.num_laf=u.num_laf{}1 where u.uid = (select a.uid from db_article a where a.aid=%(aid)s);".format(
                    status),
                {"aid": aid})
            cursor.execute("update db_article set num_like=num_like{}1 where aid=%(aid)s".format(status),
                           {"aid": aid})
            return Tools.gen200rsp("Article liked.")
        else:
            return Constants.rsp_se

    return DbUtil.execute(query)


@articleBp.route("/submitComment", methods=["POST"])
def submit_comment():
    js = request.get_json()
    aid = js['aid']
    content = js['content']
    rbid = js['rbid']
    rtuid = js['rtuid']

    def query(conn):
        cursor = conn.cursor()
        cursor.execute(
            "insert into db_reply(uid,aid,content,rbid,rtuid) values (%(uid)s,%(aid)s,%(content)s,%(rbid)s,%(rtuid)s);",
            {"content": content, "uid": session['usr']['uid'], "aid": aid, "rbid": rbid, "rtuid": rtuid})
        fetch = cursor.fetchall()
        if not fetch:
            return Tools.gen200rsp("Comment publish success.")
        else:
            return Constants.rsp_se

    return DbUtil.execute(query)


@articleBp.route("/delDraft", methods=["POST"])
def del_draft():
    js = request.get_json()
    aid = js['aid']

    def query(conn):
        cursor = conn.cursor()
        cursor.execute(
            "update db_article set status=0 where aid=%(aid)s and uid=%(uid)s;",
            {"aid": aid, "uid": session['usr']['uid']})
        fetch = cursor.fetchall()
        if not fetch:
            return Tools.gen200rsp("Draft deleted.")
        else:
            return Constants.rsp_se

    return DbUtil.execute(query)
