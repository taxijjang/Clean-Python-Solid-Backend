db = {
    'user': 'root',
    'password': 'schwisestudy',
    'host': 'wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"

JWT_SECRET_KEY = 'SOME_SUPER_SECRET_KEY'
JWT_EXP_DELTA_SECONDS = 7 * 24 * 60 * 60

test_db = {
    'user': 'root',
    'password': 'schwisestudy',
    'host': 'wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'test_db'
}

test_config = {
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@" \
              f"{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8",
    'JWT_SECRET_KEY': 'SOME_SUPER_SECRET_KEY',
    'JWT_EXP_DELTA_SECONDS': 7 * 24 * 60 * 60
}
