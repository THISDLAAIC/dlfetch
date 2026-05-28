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
  dlfetch gpa -d           Show GPA with detailed breakdown per subject
  dlfetch gpa list         List all subjects with their IDs
  dlfetch gpa -s 189741    Show detail for Honors Pre-Calculus
  dlfetch gpa -s 189741 131604
                           Show detail for multiple subjects
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

    p_gpa = sub.add_parser("gpa", help="Show current semester GPA")
    p_gpa.add_argument("-d", "--detail", action="store_true", help="Show detailed breakdown per subject")
    p_gpa.add_argument("-s", "--subject", type=int, nargs="+", dest="subject_ids", metavar="ID",
                       help="Show detail for specific subject ID(s) (use 'gpa list' to see IDs)")
    p_gpa.add_argument("subcmd", nargs="?", choices=["list"], help="List available subjects with IDs")

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
