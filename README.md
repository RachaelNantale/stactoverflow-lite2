# stackoverflow-lite2
[![Build Status](https://travis-ci.org/RachaelNantale/stactoverflow-lite2.svg?branch=tests)](https://travis-ci.org/RachaelNantale/stactoverflow-lite2)


## Description
The website serves as a platform for users to ask and answer questions, to vote questions and answers up or down and edit questions and answers.


## Features

- Users can create an account and log in. 
-  Users can post questions. 
-  Users can delete the questions they post. 
-  Users can post answers. 
-  Users can view the answers to questions. 
-  Users can accept an answer out of all the answers to his/her question as the preferred
answer.  


## Main requirements include:
> 1. [git](https://git-scm.com/)
>2. [python](https://docs.python.org/) 
> 3. [pip](https://pypi.python.org/pypi/pip) 
> 4. [virtualenv](https://virtualenv.pypa.io/en/stable/) 

## Set u of the App
1. Clone the project

`git clone https://github.com/RachaelNantale/stactoverflow-lite2.git`

2. Navigate to the project directory

`cd stactocerflow-lite2`

3. Create a virtual environment using `virtualenv` and activate it.

`virtualenv env`
`source env/bin/activate`

4. Install packages using `pip install -r requirements.txt`

5. Run the app by running `run.py`

`python run.py`

## The API Endpoints

| End Point  | Description |
| ------------- | ------------- |
| GET /api/v1/questions | Fetch all the questions |
| GET /api/v1/questions/<int:Question_ID>/ |  Fetch a single question |
| POST /api/v1/questions |Create a question|
| POST /api/v1/questions/<int:Question_ID>/answers|Post An answer to a question |
