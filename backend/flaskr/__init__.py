import os
import sys

from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}
   

    return jsonify({
      'success': True, 
      'categories': formatted_categories
    })


  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    page = request.args.get('page', 1, type=int)
    
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.all()
    categories = Category.query.all()

    formatted_categories = {category.id: category.type for category in categories}
    formatted_questions = [question.format() for question in questions]

    current_questions = formatted_questions[start:end]

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True, 
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_categories,
      'current_category': None
    })
  
  
  
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = False
    try: 
      question = Question.query.get(question_id)
      question.delete()
    except:
      db.session.rollback()
      error = True
    finally: 
      db.session.close()
    if error: 
      abort(500)
    else: 
      return jsonify({
        'message': 'deleted',
        'success': True, 
        'deleted': question_id
      })


  @app.route('/questions', methods=['POST'])
  def create_question():  
    data = json.loads(request.data.decode('utf-8'))
   
    error = False

    new_question = data.get('question', None)
    new_answer = data.get('answer', None)
    new_category = data.get('category', None)
    new_difficulty = data.get('difficulty', None)

    try: 
      question = Question(
        question=new_question,
        answer=new_answer,
        category=new_category,
        difficulty=new_difficulty
      )
      question.insert()
      question.update()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info)
    finally: 
      db.session.close()
    if error: 
      abort(422)
      flash('An error occured. Question unsuccessfully created.')
    else: 
      return jsonify({
        'success': True,
        'message': 'Question created successfully'
      })

  @app.route('/questions/search', methods=['POST'])
  def get_search_results():
    term = request.get_json()['searchTerm']
    
    questions = Question.query.filter(Question.question.ilike('%' + term + '%')).all()
    formatted_questions = [question.format() for question in questions]

    return jsonify({
      'success': True,
      'questions': formatted_questions
    })

 
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in questions]

    if len(questions)==0:
      abort(404)

    return jsonify({
      'success': True, 
      'questions': formatted_questions,
      'current_category': category_id
    })
    

  @app.route('/quizzes', methods=['POST'])
  def get_quizz():
    data = request.get_json()
    if not data:
      abort(400)

    previous_questions = data['previous_questions']
    category_id = data['quiz_category']['id']

    if category_id == 0: 
      question = Question.query.filter(Question.id.notin_(previous_questions)).first()
    else: 
      question = Question.query.filter(Question.category==category_id, Question.id.notin_(previous_questions)).first()
    if question == None:
      return jsonify({'message': 'no more questions.'})
    else:
      formatted_question = question.format()
      return jsonify({
        'question': formatted_question,
        'success': True
      })

    

  @app.errorhandler(400)
  def bad_request(error): 
      return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def not_found(error): 
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unproccesable(error): 
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable entity"
        }), 422

  @app.errorhandler(500)
  def unproccesable(error): 
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500
  
  
  
  return app

