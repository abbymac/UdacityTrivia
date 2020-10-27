# Udacity Trivia API Backend

## Getting Started

### Installing Dependencies

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

# API Reference

## Getting Started

- Base URL: Currently this app can only be run locally. The backend is hosted at `http://127.0.0.1:5000/`
- Authentication: There is not currently any authentication in this application.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
	"success": False,
    "error": 400,
    "message": "Bad request"
}

```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable entity
- 500: Internal Server Error

## Endpoints

### GET '/categories'

- Fetches all categories
- Request Arguments: None
- Returns: An object with two keys: 'categories', that contains an object, and 'success'
- Sample returned object:

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

```

### GET '/questions'

- Fetches 10 questions and all categories
- Request Arguments: Optional- 'page='. Page argument is multiplied by 10 (the number of questions_per_page). Default value is page=1.
- Returns: An object with the keys: 'categories', 'current_category', 'questions', 'totalQuestions', 'success'
- Sample returned object:

```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
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
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
    "success": true,
    "total_questions": 19
}
```

### DELETE '/questions/<question_id>'

- Given a question_id, delete the question where id=question_id
- Request Argument: 'question_id'. Where ID is an integer
- Returns: an object with keys: 'deleted', 'message', 'success'
- Sample returned object:

```
{
    "deleted": "34",
    "message": "deleted",
    "success": true
}
```

### POST '/questions'

- Create new question
- Request Argument: none
- Requires: a question object

Sample returned object:

```
	{
    	'success': True,
        'message': 'Question created successfully'
    }
```

### POST '/questions/search'

- Given some 'searchTerm', return all questions that contain search term in their 'question' attribute.
- Request Argument: none.
- Returns: An object with keys: "questions", and "success".

Sample returned object with searchTerm="who":

```
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
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    ],
    "success": true
}

```

### GET '/categories/<category_id>/questions

- Fetches questions by category
- Request Arguments: category_id. Where ID is an integer.
- Returns: an object with the keys: "current_category", "questions", "success"
  - current_category
    - an integer corresponding to the ID of the category
    - questions
      - an array of question objects
    - success
      - a boolean value dependent on if the action was completed successfully

Sample object returned with category_id=2

```
{
    "current_category": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true
}

```

### POST '/quizzes'

- Fetches a question in a particular category that has NOT been displayed yet.
- Request arguments: 'previous_questions', 'quiz_category'
- Returns: an object with the keys: "question" and "success"
  - question
    - object that follows the 'question' format
  - success
    - a boolean value dependent on if the action was completed successfully

Sample response:

```
{
	'question': {
    	'id': 20,
        'question': 'What is the heaviest organ in the human body?',
        'answer': 'The Liver',
        'category': 1,
        'difficulty': 4
     },
     'success': True
}

```
