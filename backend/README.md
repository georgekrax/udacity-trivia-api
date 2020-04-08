# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
or
```bash
pipenv install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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
To run the tests, within the `backend` directory, run:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation
### Introduction
The frontend of the application uses our own implemented API for all CRUD operations. You can do the same too with your own client (frontend). And the ebst part, you do not need to authenticated your app to use it!

### Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is currently hosted at the default port of your computer, `http://127.0.0.1:5000/`, or `http://localhost:5000/`, which is set as a proxy in the frontend configuration.
* Authentication: As mentioned above this version of the application does not require authentication or any API keys.

### Error Handling
Errors are return as JSON format in the following format:
```json
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

The API will return five (5) error types when a request fails:
* 400: Bad request
* 404: Not found
* 405: Method now allowed
* 422: Unprocessable entity
* 500: Internal server error

### Endpoints
#### GET "/questions"
* General:
    * Fetches the questions to be displayed. Orders the questions by their id, and filters them according to the current page number
    * Results are paginated in groups of ten (10), ten questions per page. By including a request argument you can choose which page number to display. Page number starts from 1, as its default number.
    * Returns a list of `questions`, a dictionary of `categories`, a `success` value, and the `total number of questions`.

* Sample: <br> `curl http://127.0.0.1:5000/questions`
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Athens",
            "category": 3,
            "difficulty": 3,
            "id": 24,
            "question": "Which is the capital city of Greece?"
        }
    ],
    "success": true,
    "total_questions": 17
}
```

#### POST "/questions"
* General:
    * Creates a new question and adds it to the database, using the submitted question name, an answer, a difficulty score and its category ID.
    * In order for the request to be successful in the request body a `question` statement, a `answer` statement, the `category` id, and the `difficulty` score should be provided.
    * Returns the newly created question object, as well and a success value of the request.

* Sample: <br> `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which company is the owner of GitHub and npm?", "answer":"Microsoft", "category": 1, "difficulty": 4}'`
```json
{
    "question": {
        "answer": "Microsoft",
        "category": 1,
        "difficulty": 4,
        "id": 26,
        "question": "Which company is the owner of GitHub and npm?"
    },
    "success": true
}
```

#### GET "/categories"
* General:
    * Fetches a dictionary of all of the available categories, in which he keys are the ids and the value is the corresponding type (string) of the category.
    * Returns a list of `categories`, a `success` value, and the `total number of categories`.

* Sample: <br> `curl http://127.0.0.1:5000/categories`
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```

#### DELETE "/questions/<int:question_id>"
* General:
    * Deletes a specific question from the database
    * A `question_id` that is an integer (int) should be provided, as a request parameter, in order for the request to be successful. Its value corresponds to the ID of one of the questions in the database system.
    * Returns the `id` of the deleted question and a success value.

* Sample: <br> `curl -X DELETE http://127.0.0.1:5000/questions/16`
```json
{
    "success": true,
    "id": 16
}
```

#### POST "/search"
* General:
    * Fetches all of the questions in the database sustem, based on the search term provided.
    * For a successful request, there should be provided the key `searchTerm`, converted into a `JavaScript Object Notation (JSON)` by the user, in the request body.
    * Returns a list of all the `questions` mathcing (ilike) the search term, a `success` value, the `search term` provided in the request body, and the `total number of questions` that were fetched in the search.

* Sample: <br> `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "GitHub"}'`
```json
{
    "questions": [
        {
            "answer": "Microsoft",
            "category": 1,
            "difficulty": 4,
            "id": 26,
            "question": "Which company is the owner of GitHub and npm?"
        }
    ],
    "search_term": "GitHub",
    "success": true,
    "total_questions": 1
}
```

#### GET "/categories/<int:category_id>/questions"
* General:
    * Fetches all the questions for the requested category.
    * The user ought to include the `category_id`, as a request parameters, which has to be an integer (int). Its value corresponds to ID of one of the category in the database.
    * Returns a list of `questions` for the requeste category, the type (string) of `current category`, a   `success` value, and the `total number of questions` for the requested category.

* Sample: <br> `curl http://127.0.0.1:5000/categories/6/questions`
```json
{
    "current_category": 6, 
    "questions": [
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
        }
    ],
    "success": true,
    "total_questions": 2
}
```

#### POST "/quizzes"
* General:
    * Fetches a unique question for the quiz of the selected category provided.
    * At the request body, the user should submit a list (array) of previously answered questions IDs `previous_questions` that are all integers (int). Also,  a dictionary {id, type} with the key `quiz_category`, which is the object of the category the user selects for the quiz, should be attached. All the data should be converted into a `JavaScript Object Notation (JSON)` format by the user itself, so that the request to be successful.
    * Returns a `question` object, which is the random question of the requested category chosen by the API, and a `success` value.

* Sample: <br> `curl http://127.0.0.1:5000//quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3, 4], "quiz_category": {"id": 1, "type": "Science"}}'`
```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the humna body?"
    },
    "success": true
}
```