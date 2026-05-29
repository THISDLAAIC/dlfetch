# DLFetch
> A neofetch-style CLI tool to fetch data from the xiaobao system of THISDL.
---
## Demonstration
[![asciicast](https://asciinema.org/a/b8ycNjzS3Zm2MIii.svg)](https://asciinema.org/a/b8ycNjzS3Zm2MIii)
---
## Installation
### 1. Install dlfetch
You can install it with a command `zsh <(curl -fsSL https://raw.githubusercontent.com/huangdihd/dlfetch/master/install.sh)`
### 2. Enjoy it!
Use command `dlfetch` to fetch your data anywhere!
## Uninstallation
You can uninstall it with a command `zsh <(curl -fsSL https://raw.githubusercontent.com/huangdihd/dlfetch/master/uninstall.sh)`
---
## Usage
```
dlfetch                  Neofetch-style semester overview (default)
```
### List
```
dlfetch list             List all subjects with their codes and IDs
```
### Tasks
```
dlfetch tasks            Show all recent tasks with scores
dlfetch tasks 2273775    Show detail for a specific task by ID
dlfetch tasks -p         Show only unfinished tasks
dlfetch tasks -s EN203   Filter tasks by subject code
dlfetch tasks -l 20      Fetch the last 20 tasks
```
### Submit
```
dlfetch submit 2259391 -f homework.pdf
                         Upload and submit a task
dlfetch submit 2259391 -f file1.pdf file2.pdf -m "done"
                         Upload multiple files with a remark
```
### Schedule
```
dlfetch schedule         Show today's schedule
dlfetch schedule -t      Show tomorrow's schedule
dlfetch schedule -w      Show this week as a timetable grid
dlfetch schedule -d 2026-06-01
                         Show schedule for a specific date
```
### GPA
```
dlfetch gpa              Show current semester GPA overview
dlfetch gpa -d           Show GPA with detailed breakdown per subject
dlfetch gpa -s MAE01     Show detail for a subject by code
dlfetch gpa -s MAE01 SCE24
                         Show detail for multiple subjects by code
dlfetch gpa -i 189741    Show detail for a subject by ID
```
---
**If you like this project, please give me a star!**
