import logging

ENV_TEST = "test"
ENV_PROD = "prod"

current_env = ENV_TEST


class BaseEnv:
    db_name = 'urchin_article'


class EnvTest(BaseEnv):
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
    flask_app = {
        "host": "0.0.0.0",
        "debug": True,
        "port": 3321
    }
    db_host = '127.0.0.1'
    db_port = 3302
    db_user = 'sqljohn'
    db_password = '123'
    log_level = logging.INFO


config_dict = {
    ENV_TEST: EnvTest,
    ENV_PROD: EnvProd
}

config = config_dict[current_env]
