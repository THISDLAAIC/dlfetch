#! python3
# -*- coding: utf-8 -*-
import argparse

from cmd_info import cmd_info
from cmd_tasks import cmd_tasks
from cmd_schedule import cmd_schedule
from cmd_gpa import cmd_gpa

EPILOG = """\
examples:
  dlfetch                  Default neofetch-style overview
  dlfetch tasks            Show all recent tasks with scores
  dlfetch tasks -p         Show only unfinished tasks
  dlfetch tasks -l 20      Fetch the last 20 tasks
  dlfetch schedule         Show today's schedule
  dlfetch schedule -t      Show tomorrow's schedule
  dlfetch schedule -w      Show this week as a timetable
  dlfetch schedule -d 2026-06-01
                           Show schedule for a specific date
  dlfetch gpa              Show current semester GPA
"""


def main():
    parser = argparse.ArgumentParser(
        prog="dlfetch",
        description="🐱 A neofetch-style CLI for THISDL students",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", metavar="")

    sub.add_parser("info", help="Neofetch-style semester overview (default)")

    p_tasks = sub.add_parser("tasks", help="List learning tasks with scores and deadlines")
    p_tasks.add_argument("-p", "--pending", action="store_true", help="Show only unfinished tasks")
    p_tasks.add_argument("-l", "--limit", type=int, metavar="N", help="Max number of tasks to fetch (default: 50)")

    p_sched = sub.add_parser("schedule", help="View daily or weekly class schedule")
    date_group = p_sched.add_mutually_exclusive_group()
    date_group.add_argument("-t", "--tomorrow", action="store_true", help="Show tomorrow's schedule")
    date_group.add_argument("-w", "--week", action="store_true", help="Show this week as a timetable grid")
    date_group.add_argument("-d", "--date", type=str, metavar="YYYY-MM-DD", help="Show schedule for a specific date")

    sub.add_parser("gpa", help="Show current semester GPA")

    args = parser.parse_args()

    commands = {
        "info": cmd_info,
        "tasks": cmd_tasks,
        "schedule": cmd_schedule,
        "gpa": cmd_gpa,
    }

    if args.command:
        commands[args.command](args)
    else:
        cmd_info(args)


if __name__ == "__main__":
    main()
