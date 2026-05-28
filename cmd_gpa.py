import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, GREEN, YELLOW, CYAN


def get_grade(score, mapping):
    for cfg in mapping["scoreMappingConfigs"]:
        if cfg["minValue"] <= score <= cfg["maxValue"]:
            return cfg["displayName"], cfg["gpa"]
    return "F", 0.0


def print_evaluation(project, indent=2, mapping=None):
    name = project["evaluationProjectEName"] or project["evaluationProjectName"]
    proportion = project["proportion"]
    score = project["score"]
    grade = project["scoreLevel"]
    gpa = project["gpa"]
    is_null = project["scoreIsNull"]

    prefix = " " * indent

    if is_null:
        print(f"{prefix}{'·':<2} {name:<30} {'--':>6}  {'--':>5}  {'--':>4}  ({proportion:.0f}%)")
    else:
        if gpa >= 4.0:
            gpa_str = f"{GREEN}{gpa:.2f}{RESET}"
        elif gpa >= 3.0:
            gpa_str = f"{YELLOW}{gpa:.2f}{RESET}"
        else:
            gpa_str = f"{CYAN}{gpa:.2f}{RESET}"
        print(f"{prefix}{'·':<2} {name:<30} {score:>6.1f}  {grade:>5}  {gpa_str}  ({proportion:.0f}%)")

    for sub in project.get("evaluationProjectList", []):
        print_evaluation(sub, indent + 4, mapping)


def gpa_color(gpa):
    if gpa >= 4.0:
        return GREEN
    elif gpa >= 3.0:
        return YELLOW
    return CYAN


def print_subject_detail(s, mappings, semester_id, cookies):
    score = s["subjectScore"]
    mapping_id = s["scoreMappingId"]
    mapping = mappings.get(mapping_id)
    name = s["subjectEName"] or s["subjectName"]
    class_id = s["classId"]
    subject_id = s["subjectId"]

    if score is None or not mapping:
        print(f"\n  {BLUE}{name}{RESET}  No score data")
        return

    grade, gpa = get_grade(score, mapping)
    print(f"\n  {BLUE}{name}{RESET}  {score:.1f}  {grade}  {gpa_color(gpa)}{gpa:.2f}{RESET}")
    print(f"  {'─' * 56}")

    detail_resp = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetDynamicScoreDetail?classId={class_id}&subjectId={subject_id}&semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    for proj in detail_resp.get("evaluationProjectList", []):
        print_evaluation(proj, indent=4, mapping=mapping)


def cmd_gpa(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    if args.subcmd == "list":
        subjects = requests.get(
            f"https://thisdlstu.schoolis.cn/api/LearningTask/GetStuSubjectListForSelect?semesterId={semester_id}",
            headers=headers, cookies=cookies
        ).json()["data"]

        print(f"\n📚 {BLUE}Subjects{RESET} — {current_semester['name']}")
        print(f"{'─' * 60}")
        print(f"  {'ID':<8} {'Code':<8} {'Subject'}")
        print(f"  {'─' * 56}")
        for s in subjects:
            name = s["eName"] or s["name"]
            print(f"  {CYAN}{s['id']:<8}{RESET} {s['subjectCode']:<8} {name}")
        print(f"\n  Use: dlfetch gpa -s <CODE>  to view subject details")
        return

    resp = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetStuSemesterDynamicScore?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    subjects_data = resp["studentSemesterDynamicScoreBasicDtos"]
    mappings = {m["scoresMappingId"]: m for m in resp["scoreMappingList"]}

    overall_gpa = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetGpa?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    if args.subject_codes:
        subject_list = requests.get(
            f"https://thisdlstu.schoolis.cn/api/LearningTask/GetStuSubjectListForSelect?semesterId={semester_id}",
            headers=headers, cookies=cookies
        ).json()["data"]
        code_to_id = {s["subjectCode"].upper(): s["id"] for s in subject_list}

        target_codes = {c.upper() for c in args.subject_codes}
        found = set()
        for s in subjects_data:
            subject_id = s["subjectId"]
            matched_code = next((c for c, sid in code_to_id.items() if sid == subject_id), None)
            if matched_code and matched_code in target_codes:
                print_subject_detail(s, mappings, semester_id, cookies)
                found.add(matched_code)
        for missing in target_codes - found:
            print(f"\n  Subject code {CYAN}{missing}{RESET} not found in current semester")
        return

    sorted_subjects = sorted(subjects_data, key=lambda x: x["subjectName"])

    if args.detail:
        for s in sorted_subjects:
            print_subject_detail(s, mappings, semester_id, cookies)

        print(f"\n  {'═' * 56}")
        print(f"  {'Overall GPA:':<42} {GREEN}{overall_gpa}{RESET}")
    else:
        print(f"\n🎓 {BLUE}GPA{RESET} — {current_semester['name']}")
        print(f"{'─' * 58}")
        print(f"  {'Subject':<28} {'Score':>6}  {'Grade':>5}  {'GPA':>4}")
        print(f"  {'─' * 50}")

        for s in sorted_subjects:
            score = s["subjectScore"]
            mapping_id = s["scoreMappingId"]
            mapping = mappings.get(mapping_id)
            name = s["subjectEName"] or s["subjectName"]

            if score is None or not mapping:
                continue

            grade, gpa = get_grade(score, mapping)
            print(f"  {name:<28} {score:>6.1f}  {grade:>5}  {gpa_color(gpa)}{gpa:.2f}")

        print(f"  {'─' * 50}")
        print(f"  {'Overall':<28} {'':>6}  {'':>5}  {GREEN}{overall_gpa}{RESET}")
