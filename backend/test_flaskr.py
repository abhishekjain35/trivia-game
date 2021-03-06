import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
unittest.TestLoader.sortTestMethodsUsing = None

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.question = {
            "question": "test question",
            "answer": "test answer",
            "difficulty": 5,
            "category": 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    # using POST instead of GET
    def test_get_all_categories_error(self):
        result = self.client().post('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 405)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "method not allowed")

    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["questions"])

        # since test_delete_ques_by_id runs first, it will delete 1 question
        self.assertEqual(data["total_questions"], 18)
        self.assertEqual(len(data["categories"]), 6)

    def test_get_paginated_questions_error(self):
        result = self.client().get('/questions?page=1000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_ques_by_id(self):
        result = self.client().delete('/questions/23')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_ques_by_id_error(self):
        result = self.client().delete('/questions/100')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_post_question(self):
        result = self.client().post('/questions', json=self.question)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])

    def test_post_question_error(self):
        result = self.client().post('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

    def test_search_questions(self):
        result = self.client().post('/questions/search', json={"searchTerm": "title"})
        print(result)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(data["questions"]), 2)

    def test_search_questions_error(self):
        result = self.client().post('/questions/search', json={"searchTerm": "something that can't be found"})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_questions_by_category(self):
        result = self.client().get('/categories/1/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["total_questions"], 3)
        self.assertTrue(data["questions"])

    def test_questions_by_category_error(self):
        result = self.client().get('/categories/100/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_quizzes(self):
        result = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": 1}})
        data = json.loads(result.data)
        question = data["question"]

        self.assertEqual(result.status_code, 200)
        self.assertTrue(question["question"])
        self.assertTrue(question["id"])
        self.assertTrue(question["difficulty"])

    def test_quizzes_error(self):
        result = self.client().post('/quizzes')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()