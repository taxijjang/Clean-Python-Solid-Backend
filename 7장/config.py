db = {
    'user': 'root',
    'password': 'schwisestudy',
    'host': 'wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"


JWT_SECRET_KEY = "ABCDEF"