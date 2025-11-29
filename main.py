#! python3
# -*- coding: utf-8 -*-
import ast
import datetime
import os
from sys import exit

import requests

from SignIn import sign_in
from constants import logo
from utils import parse_date_string, get_info_lines

# 🎟️ Cookie 加载
cookie_path = os.path.expanduser("~/.dlfetch_cookies")
cookies = []
print("Loading cookies...")

if os.path.exists(cookie_path):
    try:
        with open(cookie_path) as cookie_file:
            cookies = ast.literal_eval(cookie_file.read())
    except SyntaxError:
        cookies = []
    if type(cookies) != list:
        open(cookie_path, "w").close()
        cookies = []

if not cookies:
    print("Cookies are empty! Trying to sign in...")
    cookies = sign_in(cookie_path)

cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://thisdlstu.schoolis.cn/",
}

# 🏫 获取学期
semesters = requests.get(
    "https://thisdlstu.schoolis.cn/api/School/GetSchoolSemesters",
    headers=headers,
    cookies=cookies_dict
).json().get("data")

if not semesters:
    print("Identification information is expired!")
    open(cookie_path, "w").close()
    print("Please run the script again.")
    exit(1)

current_semester = next(s for s in semesters if s["isNow"])
current_semester_id = current_semester["id"]

tasks = requests.get(
        f"https://thisdlstu.schoolis.cn/api/LearningTask/GetList?semesterId={current_semester_id}&pageIndex=1&pageSize=12",
        headers=headers,
        cookies=cookies_dict
    ).json()["data"]["list"]
unfinished = [t for t in tasks if not t["finishState"]]

# 🎓 获取 GPA
realtime_GPA = requests.get(
    f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetGpa?semesterId={current_semester_id}",
    headers=headers,
    cookies=cookies_dict
).json()["data"]

# 📅 获取课程表
schedule = requests.post(
    "https://rs.api.thisdlit.com/high_school",
    headers=headers,
    cookies=cookies_dict,
    json={
        "beginTime": str(datetime.date.today()),
        "endTime": str(datetime.date.today()),
    }
).json()["data"]


future_lessons = sorted(
    [l for l in schedule if parse_date_string(l["beginTime"]) >= datetime.datetime.now(tz=parse_date_string(l["beginTime"]).tzinfo)],
    key=lambda l: parse_date_string(l["beginTime"])
)
next_lesson = future_lessons[0] if future_lessons else None

info_lines = get_info_lines(current_semester, unfinished, next_lesson, realtime_GPA, current_semester_id)

# 🧩 Neofetch 风格输出
max_lines = max(len(logo), len(info_lines))
for i in range(max_lines):
    left = logo[i] if i < len(logo) else " " * 9
    right = info_lines[i] if i < len(info_lines) else ""
    print(f"{left:<10}  {right}")
