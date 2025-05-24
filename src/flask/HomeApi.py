import json

from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify

from Utils.RedisDb import redis_connect

from Utils import DbUtil

homeBp = Blueprint("home", __name__)

red_client = redis_connect()


def get_art_sql(opt, page):
    offset = page * 10
    if opt == "reco":
        art_sql = """
                SELECT a.aid,a.title,a.cover,a.num_view,c.cat_name,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_artcat c ON a.acid = c.acid
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                where a.status=1
                GROUP BY a.aid
                """
    elif opt == "latest":
        art_sql = """
                SELECT a.aid,a.title,a.cover,a.num_view,c.cat_name,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_artcat c ON a.acid = c.acid
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                where a.status=1
                GROUP BY a.aid
                order by a.create_time desc
                """
    elif opt == "focus":
        art_sql = f"""
                SELECT a.aid,a.title,a.cover,a.num_view,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                join(SELECT f.tuid FROM db_focus f
                    JOIN (
                            SELECT tuid, MAX(fcid) AS latest_fcid
                            FROM db_focus
                            WHERE uid = '{session['usr']['uid']}'
                            GROUP BY tuid
                    ) latest ON f.fcid = latest.latest_fcid
                    WHERE f.status = '+'
                ) as sq on sq.tuid=a.uid
                where a.status=1
                GROUP BY a.aid
                """

    elif opt.startswith("col"):
        art_sql = f"""
                SELECT a.aid,a.title,a.cover,a.num_view,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                join(select c.uid from db_artcat c where c.opt="{opt}") as sq on sq.uid=a.uid
                where a.status=1
                GROUP BY a.aid
                """
    elif opt == "search":
        art_sql = """
                SELECT a.aid,a.title,a.cover,a.num_view,c.cat_name,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_artcat c ON a.acid = c.acid
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                where a.title like '%{}%' and a.status=1
                GROUP BY a.aid
                """.format(request.args.get("word"))
    else:
        art_sql = f"""
                SELECT a.aid,a.title,a.cover,a.num_view,c.cat_name,u.nickname,DATE_FORMAT(a.create_time, '%m.%d') AS date,GROUP_CONCAT(t.tag_name ORDER BY t.atid ASC SEPARATOR ',') AS tags
                FROM db_article a
                JOIN db_artcat c ON a.acid = c.acid
                JOIN db_user u ON u.uid = a.uid
                LEFT JOIN db_artag t ON FIND_IN_SET(t.atid, a.atids) > 0
                where c.opt='{opt}' and a.status=1
                GROUP BY a.aid
                """
    art_sql += "LIMIT 10 OFFSET {};".format(offset)
    return art_sql


@homeBp.route("/", defaults={"opt": "reco"})
@homeBp.route("/<opt>")
def home(opt):
    # home
    conn = DbUtil.prepare()

    cursor = conn.cursor()
    if red_client.exists("artcats"):
        artcats = json.loads(red_client.get("artcats"))
    else:
        cursor.execute(
            "select * from db_artcat order by acid;")
        artcats = cursor.fetchall()
        red_client.set("artcats", json.dumps(artcats))

    if opt == "focus" and 'usr' not in session:
        return redirect(url_for('home.home'))

    art_sql = get_art_sql(opt, 0)

    cursor.execute(art_sql)
    articles = cursor.fetchall()

    reco_twins = None
    author = None

    if opt == 'reco':
        if red_client.exists("reco_twins_l"):
            reco_twins = [red_client.hgetall("reco_twins_l"), red_client.hgetall("reco_twins_r")]
        else:
            twin_sql = """
                select u.nickname, u.intro,sq.opt from db_user u join(select c.uid,c.opt from db_artcat c where c.uid is not NULL limit 2) as sq on u.uid=sq.uid;
                """
            cursor.execute(twin_sql)
            reco_twins = cursor.fetchall()
            red_client.hset("reco_twins_l", mapping=reco_twins[0])
            red_client.hset("reco_twins_r", mapping=reco_twins[1])

    if opt.startswith("col"):
        cursor.execute(
            'select u.nickname,u.motto from db_user u join(select c.uid from db_artcat c where c.opt="{}") as sq on sq.uid=u.uid;'.format(
                opt))
        author = cursor.fetchone()

    DbUtil.culminate(conn)
    # return render_template("home.html", artcats=artcats, opt)
    return render_template("home.html", title="Urchin Article - Home", artcats=artcats, opti=opt, articles=articles,
                           reco_twins=reco_twins,
                           author=author)


@homeBp.route('/load_more_articles')
def load_more_articles():
    page = request.args.get("page", 1, type=int)
    opt = request.args.get("opt", "reco")
    art_sql = get_art_sql(opt, page)

    conn = DbUtil.prepare()
    cursor = conn.cursor()
    cursor.execute(art_sql)
    articles = cursor.fetchall()
    return jsonify({"articles": articles})
