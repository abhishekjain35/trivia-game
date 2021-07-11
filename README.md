# Trivia app

## Description:

Trivia is application where you can play with friends and family. It can be used to increase your knowledge towards different categories like science, sports, history etc. Anyone can add questions according to categories etc...

## Getting Started:

### Prerequisites:

1. Developer should have python3 installed on the local machine along with pip3.
2. NodeJs should also be preinstalled on the computer along with npm.
3. Postgresql database should be installed already along with psql.
4. Flask should be preinstalled.

### Installation - Backend:

1. Enable virtual environment on local machine - 
  * Go to backend folder by `cd backend`
  * run `python3 -m venv env`
  * run `source env/bin/activate`

2. Install dependencies with `pip3`
  * run `pip3 install -r requirements.txt`

3. Setup database (postgres):
  * run `createdb trivia`
  * then `psql trivia < trivia.psql`

4. Run the server
  * From backend folder run `export FLASK_ENV=development` to set environment to development.
  * run `export FLASK_APP=flaskr` to set App.
  * finally run `flask run --reload` to start local server.

### Installation - Frontend:

Install the dependencies with `npm install`, and then start the server by `npm start`

## Tests:

Tests are only implemented in backend. To setup tests follow these steps -

* run `dropdb trivia_test` to clear the db.
* run `createdb trivia_test` to create a fresh db.
* run from backend `psql trivia_test < trivia.psql` to seed database.
* finally run the tests by `python test_flaskr.py`

> NOTE: Repeat above steps everytime you run tests. Else two of the testcase will fail including `test_get_paginated_questions` and `test_delete_ques_by_id`. Because the delete testcase removes a question if you run it next time without seeding database it will fail.

# API reference

## Getting Started

### Base URL

Currently, this app is not hosted anywhere. So, it can only run in local server. The base URL for local server is `http://localhost:5000/`. It is also set as proxy in frontend.

### API keys

Currently, there is no authentication implemented for the API, so there is no API key required.

## Error

Errors are handled well and they are sent as JSON objects. Example of an Error response -
```python
    {
      "error": 404, 
      "message": "resource not found", 
      "success": false
    }
```

Every error response includes `"success": false`, error code in `error` key and message in `message` key.

Other error response includes -

* 400: "bad request"
* 405: "method not allowed"
* 422: "unprocessable"

## Request Endpoints

## Resource: Category

### GET `/categories`

* Fetches all the categories from database and returns a dictionary with key being id and value being category name

* Request arguments: None

* Returns: An JSON object with single key, categories: contains id(key):category(value) pairs.

* Response Example - (`curl 'http://localhost:5000/categories'`)
```python
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

### GET `/categories/<id>/questions`

* Fetches all questions from given category id and return a JSON object with three key:value pairs, `questions`, `total_questions`, `current_category`.

* Request arguments: `id` which is the category id.

* Returns: An JSON object with - `questions`: list of dictionaries consisting of questions, `total_questions`: Number of questions available for given category, `current_category`: Name of category

* Response Example - (`curl 'http://localhost:5000/categories/1/questions'`)
```python
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "total_questions": 3
}
```

## Resource: Questions

### GET `/questions` or `/questions?page=1`

* Fetches and returns paginated list of questions based on the page argument provided in the request URL. 

* Request arguments: None

* Returns: An JSON object with - `questions`: paginated list of questions, `total_questions`: Number of all questions, `categories`: all categories available.

* Response Example - (`curl 'http://localhost:5000/questions'`)

```python
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "total_questions": 19
}
```

### DELETE `/questions/<id>`

* Delete a question by id provided in request argument.

* Request argument: `id` The id of the question.

* Returns: An JSON object with key `success` and value `true`

* Response Example - (`curl -X DELETE 'http://localhost:5000/questions/26'`):

```python
{
  "success": true
}
```

### POST `/questions`

* Used to post a new question. It takes JSON object in request body with following properties - `question`, `answer`, `difficulty`, `category`: category id.

* Request Arguments: None

* Returns: An JSON object with key `success` and value `true`.

* Response Example - (`curl -X POST -H "Content-Type: application/json" -d '{"question": "a test question", "answer": "test", "difficulty": 3, "category": 2}' 'http://localhost:5000/questions'`)

```python
{
  "success": true
}
```

### POST `/questions/search`

* Searches in database according to `searchTerm` provided in request body. Returns all questions the matches.

* Request Arguments: None

* Returns: A JSON object with - `questions`: based on searchTerm, `total_questions`: length of all questions based on searchTerm.

* Response Example - (`curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' 'http://localhost:5000/questions/search'`)

```python
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 2
  "current_category": "", 
}
```

### POST `/quizzes`

* fetches a random question based on `quiz_category` and `previous_questions`, means the resulting question has not previously asked.

* Request Arguments: None

* Returns: An JSON object with - `question` key with value a dictionary of that question details

* Response Example - (`curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": 1, "type": "Science"}, "previous_questions": []}' 'http://localhost:5000/quizzes'`)

```python
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }
}
```

## Deployment

Currently, this project is not deployed anywhere. It is still in development phase.

## Authors

Abhishek Jain (developing and writing test for API), Udacity(Initial Setup in frontend and backend)