import json
import os
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from src.app import require_teacher


class TeacherAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_accepts_configured_teacher(self):
        os.environ["TEACHER_CREDENTIALS"] = json.dumps(
            {"coordinator": "correct-horse-battery"}
        )

        username = require_teacher(
            HTTPBasicCredentials(
                username="coordinator",
                password="correct-horse-battery",
            )
        )

        self.assertEqual(username, "coordinator")

    def test_rejects_missing_or_incorrect_credentials(self):
        os.environ["TEACHER_CREDENTIALS"] = json.dumps(
            {"coordinator": "correct-horse-battery"}
        )

        for credentials in (
            None,
            HTTPBasicCredentials(username="student", password="wrong"),
            HTTPBasicCredentials(username="coordinator", password="wrong"),
        ):
            with self.subTest(credentials=credentials):
                with self.assertRaises(HTTPException) as error:
                    require_teacher(credentials)
                self.assertEqual(error.exception.status_code, 401)

    def test_rejects_missing_or_invalid_configuration(self):
        for value in (None, "not-json", "[]", '{"coordinator": ""}'):
            with self.subTest(value=value):
                if value is not None:
                    os.environ["TEACHER_CREDENTIALS"] = value
                else:
                    os.environ.pop("TEACHER_CREDENTIALS", None)
                with self.assertRaises(HTTPException) as error:
                    require_teacher(
                        HTTPBasicCredentials(
                            username="coordinator",
                            password="correct-horse-battery",
                        )
                    )
                self.assertEqual(error.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()
