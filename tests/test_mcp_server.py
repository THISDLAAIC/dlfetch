import unittest
from unittest.mock import patch

import mcp_server


class McpServerToolTests(unittest.TestCase):
    @patch("mcp_server._run_dlfetch", return_value="tasks")
    def test_get_tasks_builds_cli_arguments(self, run_dlfetch):
        result = mcp_server.get_tasks(
            task_id=42,
            pending_only=True,
            subject_code="EN203",
            limit=10,
        )

        self.assertEqual(result, "tasks")
        run_dlfetch.assert_called_once_with(
            ["tasks", "42", "--pending", "--subject", "EN203", "--limit", "10"]
        )

    @patch("mcp_server._run_dlfetch", return_value="schedule")
    def test_get_schedule_builds_date_argument(self, run_dlfetch):
        result = mcp_server.get_schedule(date="2026-06-01")

        self.assertEqual(result, "schedule")
        run_dlfetch.assert_called_once_with(["schedule", "--date", "2026-06-01"])

    def test_get_schedule_rejects_conflicting_ranges(self):
        with self.assertRaisesRegex(ValueError, "Only one"):
            mcp_server.get_schedule(date="2026-06-01", week=True)

    def test_submit_requires_content(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            mcp_server.submit_task(task_id=42)


if __name__ == "__main__":
    unittest.main()
