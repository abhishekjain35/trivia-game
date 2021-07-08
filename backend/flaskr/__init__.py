import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from sqlalchemy.sql.expression import null, true

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
  CORS(app, resources={r"/*" : {"origins": '*'}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response

  @app.route('/categories')
  def get_all_categories():
    all_categories = Category.query.all()
    formatted_categories = format_categories(all_categories)
    if len(formatted_categories) == 0:
      abort(404)
    return jsonify({
      "categories": formatted_categories,
      "success": True
    })

  @app.route('/questions')
  def get_paginated_questions():
      all_questions = Question.query.order_by(Question.id).all()
      formatted_questions = paginate_selection(request, all_questions)
      if len(formatted_questions) == 0:
        abort(404)

      categories = [c.format() for c in Category.query.all()]
      formatted_categories = {}
      for single_category in categories:
        formatted_categories[single_category['id']] = single_category['type']

      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(all_questions),
        'categories': formatted_categories,
        'current_category': ""
      })

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_ques_by_id(id):
    ques = Question.query.filter(Question.id==id).one_or_none()
    if ques is None:
      abort(404)
    ques.delete()
    return jsonify({
      "success": True
    })

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
      abort(400)

  @app.route("/questions/search", methods=['POST'])
  def search_questions():
    try:
      search_query = request.get_json()['searchTerm']
      questions_by_search = Question.query.filter(Question.question.ilike(f'%{search_query}%')).all()
      formatted_result = paginate_selection(request, questions_by_search)
      if len(formatted_result) == 0:
        abort(404)
      return jsonify({
        "questions": formatted_result,
        "total_questions": len(questions_by_search),
        "current_category": "",
        "success": True
      })

    # handles 404 and 422 separately
    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)
      else:
        abort(400)

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category_id(id):
    ques = Question.query.filter(Question.category==id).order_by(Question.id).all()
    formatted_ques = paginate_selection(request, ques)
    
    if len(formatted_ques) == 0:
      abort(404)

    return jsonify({
      "questions": formatted_ques,
      "total_questions": len(ques),
      "current_category": Category.query.get(id).format()["type"],
      "success": True
    })

  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    try:
      body = request.get_json()
      previous_questions_id_list = body["previous_questions"]
      quiz_category = body["quiz_category"]
      ques = {}

      if quiz_category['type'] == 'all':
        ques["all_ques"] = Question.query.all()
      else:
        category_id = quiz_category["id"]
        ques["all_ques"] = Question.query.filter(Question.category==category_id).all()
        
      all_ques = ques["all_ques"]

      if len(all_ques) == 0:
        abort(404)

      formatted_ques = [q.format() for q in all_ques]
      random.shuffle(formatted_ques)

      unique_question = False
      for q in formatted_ques:
        if q['id'] not in previous_questions_id_list:
          unique_question = q
      
      return jsonify({
        "question": unique_question,
        "success": True
      })

    except Exception as e:
      if isinstance(e, HTTPException):
        abort(e.code)
      else:
        abort(400)

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
  
  @app.errorhandler(405)
  def handler_bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  
  return app

    