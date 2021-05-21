class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = '9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True
    SQLALCHEMY_ECHO = True





class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    SECRET_KEY='9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
