import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from sqlalchemy.sql.expression import null

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_selection(request, selection):
  current = request.args.get('page', 1, type=int)
  initial_index =  (current - 1) * QUESTIONS_PER_PAGE
  final_index = initial_index + QUESTIONS_PER_PAGE

  result = [item.format() for item in selection]
  formatted_result = result[initial_index:final_index]

  return formatted_result

def format_categories(categories):
  result = [item.format() for item in categories]
  formatted_categories = {}
  for single_category in result:
    formatted_categories[single_category['id']] = single_category['type']

  return formatted_categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*" : {"origins": '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_all_categories():
    all_categories = Category.query.all()
    if len(all_categories) == 0:
      abort(404)
    formatted_categories = format_categories(all_categories)
    return jsonify({
      "categories": formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_paginated_questions():
    try:
      all_questions = Question.query.order_by(Question.id).all()
      if len(all_questions) == 0:
        abort(404)
      formatted_questions = paginate_selection(request, all_questions)

      categories = [c.format() for c in Category.query.all()]
      formatted_categories = {}
      for single_category in categories:
        formatted_categories[single_category['id']] = single_category['type']

      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(all_questions),
        'categories': formatted_categories,
        'current_category': {}
      })
    
    # handles 404 and 422 separately
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)
      else:
        abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions", methods=['POST'])
  def post_question():
    try:
      jsonObj = request.get_json()
      question = jsonObj["question"]
      answer = jsonObj["answer"]
      difficulty = jsonObj["difficulty"]
      category = jsonObj["category"]

      new_ques = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      new_ques.insert()
      return jsonify({
        "success": True
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route("/questions/search", methods=['POST'])
  def search_questions():
    try:
      search_query = request.get_json()['searchTerm']
      questions_by_search = Question.query.filter(Question.question.ilike(f'%{search_query}%')).all()
      if len(questions_by_search) == 0:
        abort(404)
      formatted_result = paginate_selection(request, questions_by_search)
      return jsonify({
        "questions": formatted_result,
        "total_questions": len(questions_by_search),
        "current_category": ""
      })

    # handles 404 and 422 separately
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)
      else:
        abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category_id(id):
    try:
      ques = Question.query.filter(Question.category==id).order_by(Question.id).all()
      if len(ques) == 0:
        abort(404)
      
      formatted_ques = paginate_selection(request, ques)

      return jsonify({
        "questions": formatted_ques,
        "total_questions": len(ques),
        "current_category": Category.query.get(id).format()["type"]
      })

    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)
      else:
        abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def handler_not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def handler_unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def handler_bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

    