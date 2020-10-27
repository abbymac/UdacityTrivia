import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from random import randint
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.delete_new_question = {
            'question': 'Is this a test?',
            'answer': 'Yes, it is',
            'category': 2,
            'difficulty': 1
        }

        self.create_new_question = {
            'question': 'Testing to create?',
            'answer': 'Yes we are.',
            'category': 3,
            'difficulty': 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #--------------------------------------------------------------------------------------------
    # TEST ENDPOINTS
    #--------------------------------------------------------------------------------------------
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) #check status is OK
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)  #check pagination returns back 10 q
        self.assertTrue(data['questions']) #check questions are returned
        self.assertTrue(len(data['categories']))  # check categories are included

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))  # check categories are included

    def test_get_cateogry_questions(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], 3)

  
    def test_get_search_results(self): 
        #Using searchTerm = autobiography should only yield 1 result.
        res = self.client().post('/questions/search', json={'searchTerm': 'autobiography'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'][0]['id'], 5)
        self.assertEqual(data['success'], True)


    def test_create_question(self):
        res = self.client().post('/questions', json=self.create_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question created successfully')

    def test_delete_question(self):
        question = Question(
            question=self.delete_new_question['question'],
            answer=self.delete_new_question['answer'],
            category=self.delete_new_question['category'],
            difficulty=self.delete_new_question['difficulty'],
        )
        question.insert()
        question.update()
        
        get_new_question = Question.query.filter(Question.question == self.delete_new_question['question']).all()
        id_new = str(get_new_question[0].id)

        res = self.client().delete('/questions/'+id_new)
        data = json.loads(res.data)

        did_delete = Question.query.filter(Question.id == id_new).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id_new)
        self.assertEqual(did_delete, None)

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [0,3], 
            'quiz_category': {'type': 'science', 'id': 3}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
   
    #----------------------------------------------------------------------------------------
    # TEST ERRORS 
    #----------------------------------------------------------------------------------------

    def test_422_create_question_error(self):
        #ommit difficulty field
        res = self.client().post('/questions', json={
            'question': 'Is this a test?',
            'answer': 'Yes, it is',
            'category': 'Science',
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422) #Check that we get back an Internal Server error
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')
        self.assertEqual(data['error'], 422)

    def test_404_sent_requesting_beyond_valid_page(self): 
        #send request for questions with an out of range page
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)


    def test_404_cateogry_questions(self):
        #send request for questions from an invalid category
        res = self.client().get('/categories/30/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_no_data_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()