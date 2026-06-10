import time
import requests

from constants import headers, errors
from credentials import md5_upper, load_credentials, prompt_and_save, delete_credentials

WRONG_CREDENTIALS_STATES = (1010076, 1010082)

def password_hash(password_md5: str, timestamp: int):
    return md5_upper(password_md5 + str(timestamp))

def sign_in() -> str | None:
    saved = load_credentials()
    if not saved:
        saved = prompt_and_save()
    user_name, password_md5 = saved

    timestamp = int(time.time())
    hashed_password = password_hash(password_md5, timestamp)
    try:
        session_id = requests.get(
            "https://thisdlstu.schoolis.cn/api/MemberShip/GetStudentCaptchaForLogin",
            headers=headers
        ).cookies.get('SessionId')
    except ValueError:
        print("Failed to get session id")
        return None

    print("Got session id successfully!")
    print("Trying to login!")

    login_res = requests.post(
        "https://thisdlstu.schoolis.cn/api/MemberShip/Login?captcha=",
        headers=headers,
        cookies={
            "SessionId": session_id,
        },
        json={
            "name": user_name,
            "password": hashed_password,
            "timestamp": timestamp
        }
    )

    try:
        res = login_res.json()
        state = res['state']
        if state == 0 and res.get('data'):
            print("Login successfully!")
            return session_id
        print(res.get('msgCN') or errors.get(state) or f"Login failed (state {state})")
        if state in WRONG_CREDENTIALS_STATES:
            delete_credentials()
            print("Saved credentials cleared. You will be asked to enter them again next time.")
        return None
    except (ValueError, KeyError):
        print('Unknown error')
        return None


if __name__ == '__main__':
    print(sign_in())