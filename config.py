class BaseConfig(object):
    """所有配置类的基类"""

    SECRET_KEY = "LOVE"
    DEBUG = True
    TESTING = False
    VISIT_TIME = 0  # 网站访问次数
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://yujie:yujie@localhost/yujie_audio"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库的修改


class ProductionConfig(BaseConfig):
    """生产环境下的配置类"""

    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """开发模式下的配置类"""

    DEBUG = True
    TESTING = True


class AlgorithmConfig:
    """算法配置类"""

    PYANNOTE_TOKEN = "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"
    ERNIE_API_TYPE = "aistudio"
    ERNIE_ACCESS_TOKEN = "5c42c7c4f6571c7c97bbda75f3d20b17b7b4f5ea"


class PluginConfig:
    """插件配置类"""

    FRONTEND_URL = "http://127.0.0.1:4523"
