
class FlaskConfig:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/supply_chain"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = '123456'