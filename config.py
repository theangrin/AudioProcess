class BaseConfig(object):
    """所有配置类的基类"""
    SECRET_KEY = "LOVE"
    DEBUG = True
    TESTING = False
    VISIT_TIME = 0  # 网站访问次数
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin@localhost/yujie_audio"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库的修改


class ProductionConfig(BaseConfig):
    """生产环境下的配置类"""
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """开发模式下的配置类"""
    DEBUG = True
    TESTING = True