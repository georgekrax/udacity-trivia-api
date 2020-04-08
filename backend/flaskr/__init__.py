import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  ~ @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  ~ @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [q.format() for q in selection]
    current_questions = questions[start:end]
    return current_questions

  '''
  ~ @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = {}
    for c in Category.query.all():
        categories[c.id] = c.type
    return jsonify({
      "success": True,
      "categories": categories,
      "total_categories": len(categories)
    })

  '''
  ~ @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.

  ~ @TODO:
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.all()
    categories_dict = {}

    for c in categories:
      categories_dict[c.id] = c.type

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": current_questions,
      "categories": categories_dict,
      "total_questions": len(selection),
    })

  '''
  ~ @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  ~ @TODO:
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    if not isinstance(question_id, int):
      abort(400)
    try:
      question = Question.query.get(question_id)
    
      if not question:
        abort(404)

      question.delete()

      return jsonify({
        "success": True,
        "id": question_id,
      })
    except:
      abort(500)

  '''
  ~ @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  ~ @TODO:
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    if not (question and answer and category and difficulty):
      abort(400)

    try:
      question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      question.insert()

      return jsonify({
        "success": True,
        "question": question.format()
      })
    except:
      abort(500)

  '''
  ~ @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  ~ @TODO:
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_for_question():
    search_term = request.get_json().get('searchTerm')
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    formatted_questions = [q.format() for q in questions]

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "search_term": search_term,
      "total_questions": len(formatted_questions)
    })  

  '''
  ~ @TODO: 
  Create a GET endpoint to get questions based on category. 

  ~ @TODO:
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    if not category_id or category_id == 0:
      abort(400)

    questions_by_category = Question.query.filter(Question.category == category_id)
    formatted_questions = [q.format() for q in questions_by_category]

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "current_category": category_id
    })


  '''
  ~ @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  ~ @TODO:
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():
    previous_questions = request.get_json().get('previous_questions')
    quiz_category = request.get_json().get('quiz_category')

    if not (previous_questions or quiz_category):
      abort(400)

    category_id = int(quiz_category['id'])
    
    if category_id == 0:
      questions = Question.query.filter(~Question.id.in_(previous_questions)).order_by(Question.id)
    else:
      questions = Question.query.filter(Question.category == category_id, 
      ~Question.id.in_(previous_questions)
      ).order_by(Question.id)
    
    question = questions.order_by(func.random()).first()

    if not question:
      return jsonify({})

    return jsonify({
      "success": True,
      "question": question.format()
    })

  '''
  ~ @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
    }), 405
    
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable entity"
    }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error"
    }), 500
  
  return app

    