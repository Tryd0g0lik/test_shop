"""variables it save data from the env"""

import os

import dotenv

dotenv.load_dotenv()
TEST_HOST = os.getenv("TEST_HOST", "yandex.ru")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
TEST_LOGIN = os.getenv("TEST_LOGIN", "")
