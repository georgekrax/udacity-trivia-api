import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'george2016','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    @TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['categories'], list)
        self.assertIsInstance(data['total_questions'], int)
    
    def test_404_get_questions_fail(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertIsInstance(data['categories'], list)

    def test_405_delete_category_fail(self):
        res = self.client().delete(f'/categories') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")
        self.assertEqual(data['error'], 405)

    def test_delete_question(self):
        question_id = 22
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], question_id)

    def test_405_delete_question_fail(self):
        res = self.client().delete(f'/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not allowed")

    def test_create_question(self):
        sample_question = {
            "question": "Which company is the owner of GitHub and npm?",
            "answer": "Microsoft",
            "category": 1,
            "difficulty": 4
        }
        res = self.client().post('/questions', data=json.dumps(sample_question), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
    
    def test_400_create_question_fail(self):
        res = self.client().post('/questions', data=json.dumps({}), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad request")

    def test_search_questions(self):
        request = {'searchTerm': 'PALACE'}
        res = self.client().post('/search', data=json.dumps(request), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(data['search_term'], request.get('searchTerm'))
        self.assertIsInstance(data['total_questions_for_search_term'], int)
    
    def test_405_search_questions_fail(self):
        search_term = 'PALACE'
        res = self.client().get('/search?q={search_term}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not allowed")
    
    def test_get_questions_by_category(self):
        category_id = 3
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions_for_category'], int)
        self.assertEqual(data['current_category'], category_id)
        for q in data['questions']:
            self.assertEqual(q['category'], category_id)

    def test_400_get_question_by_category_fail(self):
        category_id = 0
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad request")

    def test_play_quiz(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client().post('/quizzes', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'],
                             request_data['previous_questions'])

    def test_400_play_quiz(self):
        res = self.client().post('/quizzes', data=json.dumps({}), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()