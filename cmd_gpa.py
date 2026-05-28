import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, GREEN, YELLOW, CYAN


def get_grade(score, mapping):
    for cfg in mapping["scoreMappingConfigs"]:
        if cfg["minValue"] <= score <= cfg["maxValue"]:
            return cfg["displayName"], cfg["gpa"]
    return "F", 0.0


def cmd_gpa(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    resp = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetStuSemesterDynamicScore?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    subjects = resp["studentSemesterDynamicScoreBasicDtos"]
    mappings = {m["scoresMappingId"]: m for m in resp["scoreMappingList"]}

    overall_gpa = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetGpa?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    print(f"\n🎓 {BLUE}GPA{RESET} — {current_semester['name']}")
    print(f"{'─' * 58}")
    print(f"  {'Subject':<28} {'Score':>6}  {'Grade':>5}  {'GPA':>4}")
    print(f"  {'─' * 50}")

    total_gpa = 0.0
    count = 0

    for s in sorted(subjects, key=lambda x: x["subjectName"]):
        score = s["subjectScore"]
        mapping_id = s["scoreMappingId"]
        mapping = mappings.get(mapping_id)
        name = s["subjectEName"] or s["subjectName"]

        if score is None or not mapping:
            continue

        grade, gpa = get_grade(score, mapping)
        total_gpa += gpa
        count += 1

        if gpa >= 4.0:
            gpa_str = f"{GREEN}{gpa:.2f}{RESET}"
        elif gpa >= 3.0:
            gpa_str = f"{YELLOW}{gpa:.2f}{RESET}"
        else:
            gpa_str = f"{CYAN}{gpa:.2f}{RESET}"

        print(f"  {name:<28} {score:>6.1f}  {grade:>5}  {gpa_str}")

    print(f"  {'─' * 50}")
    avg_gpa = total_gpa / count if count else 0
    print(f"  {'Overall':<28} {'':>6}  {'':>5}  {GREEN}{overall_gpa}{RESET}")
