import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, GREEN


def cmd_gpa(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    gpa = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetGpa?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    print(f"\n🎓 {BLUE}GPA{RESET}")
    print(f"{'─' * 20}")
    print(f"  Semester : {current_semester['name']}")
    print(f"  GPA      : {GREEN}{gpa}{RESET}")
