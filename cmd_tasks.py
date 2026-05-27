import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, GREEN, YELLOW
from utils import parse_date_string


def cmd_tasks(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    page_size = args.limit if args.limit else 50
    tasks = requests.get(
        f"https://thisdlstu.schoolis.cn/api/LearningTask/GetList?semesterId={semester_id}&pageIndex=1&pageSize={page_size}",
        headers=headers, cookies=cookies
    ).json()["data"]["list"]

    if args.pending:
        tasks = [t for t in tasks if not t["finishState"]]

    unfinished = [t for t in tasks if not t["finishState"]]
    finished = [t for t in tasks if t["finishState"]]

    print(f"\n📋 {BLUE}Learning Tasks{RESET} ({current_semester['name']})")
    print(f"{'─' * 40}")

    if unfinished:
        print(f"\n{YELLOW}⏳ Not handed in:{RESET}")
        for t in unfinished:
            print(f"  • {t['name']}")
            if t.get('subjectName'):
                print(f"    Subject: {t['subjectName']} ({t.get('subjectCode', '')})")
            if t.get('typeName'):
                print(f"    Type: {t['typeName']}")
            if t.get('endTime'):
                end = parse_date_string(t['endTime'])
                if end:
                    print(f"    Deadline: {end.strftime('%Y-%m-%d %H:%M')}")
            print()

    if finished and not args.pending:
        print(f"{GREEN}✅ Handed in:{RESET}")
        for t in finished:
            score_str = ""
            if t.get('score') is not None and t.get('totalScore'):
                score_str = f" ({t['score']}/{t['totalScore']})"
            print(f"  • {t['name']}{score_str}")
            if t.get('subjectName'):
                print(f"    Subject: {t['subjectName']}")
            print()

    print(f"Total: {len(tasks)} | {GREEN}Done: {len(finished)}{RESET} | {YELLOW}Pending: {len(unfinished)}{RESET}")
