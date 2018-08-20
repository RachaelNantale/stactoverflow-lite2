# stackoverflow-lite2
[![Build Status](https://travis-ci.org/RachaelNantale/stactoverflow-lite2.svg?branch=master)](https://travis-ci.org/RachaelNantale/stactoverflow-lite2)


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

## Requirements
> pip install -r requirements.txt

## The API Endpoints

| End Point  | Description |
| ------------- | ------------- |
| GET /api/v1/questions | Fetch all the questions |
| GET /api/v1/questions/<int:qtnid>/ |  Fetch a single question |
| POST /api/v1/questions |Create a question|
| POST /api/v1/questions/<int:iqtnd>/answers|Post An answer to a question |
