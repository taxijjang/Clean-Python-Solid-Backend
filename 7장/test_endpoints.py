import pytest
import bcrypt
import json
import config

from app import create_app
from sqlalchemy import create_engine, text

database = create_engine(config.test_config['DB_URL'], encoding='UTF-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api


def setup_function():
    ## Create a test user
    hashed_password = bcrypt.hashpw(
        b"xordbs224!",
        bcrypt.gensalt()
    )

    new_users = [
        {
            'id': 1,
            'name': '김택윤',
            'email': 'gw9122@naver.com',
            'profile': 'test_profile',
            'hashed_password': hashed_password
        },
        {
            'id': 2,
            'name': '이은지',
            'email': 'gw224@daum.net',
            'profile': 'test_profile',
            'hashed_password': hashed_password
        }
    ]
    database.execute(text("""
        INSERT INTO users(
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """), new_users)

    ## USER 2의 트윗 미리 생성
    database.execute(text("""
        INSERT INTO tweets(
            user_id,
            tweet
        ) VALUES (
            2,
            "Hello World"
        )
    """))


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


# def test_tweet(api):
#     ## 테스트 사용자 생성
#     new_user = {
#         'email': 'gw9122@naver.com',
#         'password': 'xordbs224!',
#         'name': '김택윤',
#         'profile': 'test_profile',
#     }
#
#     resp = api.post(
#         '/sign-up',
#         data=json.dumps(new_user),
#         content_type='application/json'
#     )
#
#     assert resp.status_code == 200
#
#     ## GET the id of the new user
#     resp_json = json.loads(resp.data.decode('utf-8'))
#     new_user_id = resp_json['id']
#
#     ## 로그인
#     resp = api.post(
#         '/login',
#         data = json.dumps({
#             'email' : 'gw9122@naver.com',
#             'password' : 'xordbs224!'
#                            }),
#         contest_type = 'application/json'
#     )
#
#     resp_json = json.loads(resp.data.decode('utf-8'))
#     access_token = resp_json['access_token']
#
#     ## tweet
#     resp = api.post()


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


# def test_sign_up(api):
#     resp = api.post(
#         '/sign-up',
#         data=json.dumps(
#             {
#                 'email': 'gw224@daum.com',
#                 'password': 'xordbs224!',
#                 'name': '김택윤2',
#                 'profile': 'test_profile',
#             }
#         ),
#         content_type='application/json',
#     )
#
#     assert resp.status_code == 200


def test_login(api):
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'gw9122@naver.com',
                         'password': 'xordbs224!'}),
        content_type='application/json',
    )
    assert b"access_token" in resp.data


def test_unauthorized(api):
    # access token이 없이는 401 응답을 리턴하는지 확인
    resp = api.post(
        '/tweet',
        data=json.dumps(
            {
                'tweet': "Hello World",
            }),
        content_type='application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/follow',
        data=json.dumps(
            {
                'follow': 2
            }),
        content_type='application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/unfollow',
        data=json.dumps(
            {
                'unfollow': 2
            }),
        content_type='application/json'
    )
    assert resp.status_code == 401


def test_tweet(api):
    ## 로그인
    resp = api.post(
        '/login',
        data=json.dumps(
            {
                'email': 'gw9122@naver.com',
                'password': 'xordbs224!'
            }),
        content_type="application/json"
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## tweet
    resp = api.post(
        '/tweet',
        data=json.dumps(
            {
                'tweet': "Hello World",
            }),
        content_type='application/json',
        headers={
            'Authorization': access_token
        }
    )
    assert resp.status_code == 200

    ## tweet 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200

    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 1,
                'tweet': 'Hello World'
            }
        ]
    }


def test_follow(api):
    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps(
            {
                'email': 'gw9122@naver.com',
                'password': 'xordbs224!'
            }),
        content_type="application/json"
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    assert b'access_token' in resp.data

    # follow
    resp = api.post(
        '/follow',
        data=json.dumps(
            {
                'follow': 2
            }),
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200
