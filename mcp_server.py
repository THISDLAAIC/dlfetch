import os
import re
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SERVER_NAME = "dlfetch"
PROJECT_ROOT = Path(__file__).resolve().parent
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

mcp = FastMCP(SERVER_NAME)


def _run_dlfetch(arguments: list[str], timeout: int = 120) -> str:
    environment = os.environ.copy()
    environment["DLFETCH_NONINTERACTIVE"] = "1"

    completed = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py"), *arguments],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = ANSI_ESCAPE.sub("", completed.stdout).strip()
    if completed.returncode == 0:
        return output

    error = ANSI_ESCAPE.sub("", completed.stderr).strip()
    detail = output or error or f"dlfetch exited with status {completed.returncode}"
    raise RuntimeError(detail)


@mcp.tool()
def get_overview() -> str:
    """Get the current semester overview, pending task count, GPA, and next class."""
    return _run_dlfetch(["info"])


@mcp.tool()
def get_tasks(
    task_id: int | None = None,
    pending_only: bool = False,
    subject_code: str | None = None,
    limit: int | None = None,
) -> str:
    """List learning tasks or get one task's details.

    Args:
        task_id: A task ID to inspect. Omit it to list tasks.
        pending_only: Return only unfinished tasks.
        subject_code: Filter by a subject code such as EN203.
        limit: Maximum number of tasks to fetch.
    """
    if limit is not None and limit <= 0:
        raise ValueError("limit must be greater than zero")

    arguments = ["tasks"]
    if task_id is not None:
        arguments.append(str(task_id))
    if pending_only:
        arguments.append("--pending")
    if subject_code:
        arguments.extend(["--subject", subject_code])
    if limit is not None:
        arguments.extend(["--limit", str(limit)])
    return _run_dlfetch(arguments)


@mcp.tool()
def get_schedule(date: str | None = None, tomorrow: bool = False, week: bool = False) -> str:
    """Get the class schedule.

    Args:
        date: A specific date in YYYY-MM-DD format.
        tomorrow: Get tomorrow's schedule.
        week: Get the current week's timetable.

    Only one of date, tomorrow, and week may be supplied.
    """
    choices = sum((date is not None, tomorrow, week))
    if choices > 1:
        raise ValueError("Only one of date, tomorrow, and week may be supplied")

    arguments = ["schedule"]
    if date:
        arguments.extend(["--date", date])
    elif tomorrow:
        arguments.append("--tomorrow")
    elif week:
        arguments.append("--week")
    return _run_dlfetch(arguments)


@mcp.tool()
def get_gpa(
    semester: str | None = None,
    detail: bool = False,
    subject_codes: list[str] | None = None,
    subject_ids: list[int] | None = None,
) -> str:
    """Get GPA information for a semester or selected subjects.

    Args:
        semester: Semester name, a unique part of its name, or "list".
        detail: Include each subject's grading breakdown.
        subject_codes: Subject codes to inspect.
        subject_ids: Subject IDs to inspect.
    """
    if subject_codes and subject_ids:
        raise ValueError("Use subject_codes or subject_ids, not both")

    arguments = ["gpa"]
    if semester:
        arguments.extend(["--semester", semester])
    if detail:
        arguments.append("--detail")
    if subject_codes:
        arguments.extend(["--subject", *subject_codes])
    if subject_ids:
        arguments.extend(["--id", *(str(subject_id) for subject_id in subject_ids)])
    return _run_dlfetch(arguments)


@mcp.tool()
def list_subjects() -> str:
    """List subjects in the current semester, including their codes and IDs."""
    return _run_dlfetch(["list"])


@mcp.tool()
def submit_task(task_id: int, file_paths: list[str] | None = None, remark: str | None = None) -> str:
    """Submit files and/or a remark for a learning task.

    This changes the task submission on THISDL. Call it only after the user has
    explicitly confirmed the task ID, file paths, and remark.

    Args:
        task_id: The learning task ID to submit.
        file_paths: Local files to upload and attach.
        remark: A comment to include with the submission.
    """
    if not file_paths and not remark:
        raise ValueError("At least one file path or a remark is required")

    if file_paths:
        missing_paths = [file_path for file_path in file_paths if not Path(file_path).is_file()]
        if missing_paths:
            raise ValueError(f"Files do not exist or are not regular files: {', '.join(missing_paths)}")

    arguments = ["submit", str(task_id)]
    if file_paths:
        arguments.extend(["--file", *file_paths])
    if remark:
        arguments.extend(["--remark", remark])
    return _run_dlfetch(arguments, timeout=300)


def run_stdio_server() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_stdio_server()
