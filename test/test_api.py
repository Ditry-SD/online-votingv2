import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from backend.database import SessionLocal
from backend import models
from fastapi.testclient import TestClient

client = TestClient(app)


class TestVotingAPI(unittest.TestCase):

    def setUp(self):
        """Сброс голосов и регистрация тестовых пользователей перед каждым тестом"""
        db = SessionLocal()
        db.query(models.Vote).delete()
        db.query(models.Candidate).update({"votes": 0})
        db.commit()
        db.close()
        
        client.post("/api/register", data={"username": "testuser1", "password": "test123"})
        client.post("/api/register", data={"username": "testuser2", "password": "test123"})

    def login(self, username, password):
        return client.post("/api/login", data={"username": username, "password": password})

    def test_home_page(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_candidates(self):
        response = client.get("/api/candidates")
        self.assertEqual(response.status_code, 200)

    def test_vote_without_login(self):
        """Проверка отказа в голосовании без авторизации"""
        client.get("/api/logout")  # Выходим из предыдущей сессии
        response = client.post("/api/vote/1")
        self.assertIn(response.status_code, [401, 400])

    def test_vote_for_candidate(self):
        self.login("testuser1", "test123")
        response = client.post("/api/vote/1")
        self.assertEqual(response.status_code, 200)

    def test_duplicate_vote(self):
        self.login("testuser2", "test123")
        client.post("/api/vote/2")
        response = client.post("/api/vote/3")
        self.assertEqual(response.status_code, 400)

    def test_vote_invalid_candidate(self):
        self.login("testuser1", "test123")
        response = client.post("/api/vote/999")
        self.assertEqual(response.status_code, 404)

    def test_results_page(self):
        response = client.get("/results")
        self.assertEqual(response.status_code, 200)

    def test_swagger_docs(self):
        response = client.get("/docs")
        self.assertEqual(response.status_code, 200)

    def test_openapi_json(self):
        response = client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)

    def test_has_voted(self):
        self.login("testuser1", "test123")
        client.post("/api/vote/1")
        response = client.get("/api/has-voted")
        self.assertTrue(response.json()["voted"])


if __name__ == "__main__":
    unittest.main()