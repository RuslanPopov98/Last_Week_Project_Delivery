import os

# Для указания пути к файлу БД воспользумся путем до текущего модуля# - Текущая папка
current_path = os.path.dirname(os.path.realpath(__file__))
# - Путь к файлу БД в данной папке
# db_path = "sqlite:///" + current_path + "\\test2.db"
# db_path = "sqlite:///" + current_path + "\\delivery.db"
# db_path = 'postgresql://postgres:1234@localhost:5432/delivery_info'
db_path = 'postgres://acqknfmfyczwzq:a91bd3bf9ff6555b006bb50bc696a310e63c9eb88bec05b9520d40bb4fad4025@ec2-3-215-137-131.compute-1.amazonaws.com:5432/daumv0qem7scks'


class Config:
    DEBUG = False
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# postgres://acqknfmfyczwzq:a91bd3bf9ff6555b006bb50bc696a310e63c9eb88bec05b9520d40bb4fad4025@ec2-3-215-137-131.compute-1.amazonaws.com:5432/daumv0qem7scks