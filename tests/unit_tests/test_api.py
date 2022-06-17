import os
import conftest
import api
from fastapi.testclient import TestClient
import unittest


os.environ["API_KEY_TEST"] = conftest._API_KEY_TEST
auth_headers = {"x-api-key": conftest._API_KEY_TEST}

client = TestClient(api.app)


class TestRoot(unittest.TestCase):
    def test_api_root(self):
        response = client.get("/", headers=auth_headers)
        assert response.status_code == 200
