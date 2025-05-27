import logging

ENV_TEST = "test"
ENV_PROD = "prod"

current_env = ENV_PROD


class BaseEnv:
    red_host = "127.0.0.1"
    red_port = 6379
    red_pass = ''
    red_pool = 10
    red_db = 1


class EnvTest(BaseEnv):
    db_name = 'urchin_article'
    flask_app = {
        "host": "0.0.0.0",
        "debug": True,
        "port": 3321
    }
    db_host = '127.0.0.1'
    db_port = 3306
    db_user = 'sqljohn'
    db_password = '123'
    log_level = logging.DEBUG


class EnvProd(BaseEnv):
    db_name = 'railway'
    flask_app = {
        "host": "0.0.0.0",
        "debug": False,
        "port": 3321
    }
    db_host = 'gondola.proxy.rlwy.net'
    db_port = 37109
    db_user = 'root'
    db_password = 'hEKMpRbVgZXrxSllGxORlauPzJXRawOD'
    log_level = logging.INFO


config_dict = {
    ENV_TEST: EnvTest,
    ENV_PROD: EnvProd
}

config = config_dict[current_env]
