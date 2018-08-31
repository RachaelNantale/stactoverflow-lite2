import re


def validate_user_input(email, password=None):
    """This function validates user input"""

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return {'message': 'Please input a valid email'}, 400
    if len(password) < 7:
        return {'message': 'This password is not strong enough '}, 400


def validate_question_input(title, description, tags):
    """ Function to validate data entered while creating a question """
    if len(title) < 5 or title == "":
        return {'message': 'Title is too short. Please add more clarity'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(title):
        return {'message': 'Please dont input symbols'}, 400

    if len(description) < 5 or description == "":
        return {'message': 'Description is too short.'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(description):
        return {'message': 'Please dont input symbols'}, 400

    if not tags or tags == "":
        return {'message': 'Please a correct tag'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(tags):
        return {'message': 'Please dont input symbols'}, 400


def validate_answer_input(answer):
    """ Function to validate data entered while creating an answer """
    if len(answer) < 5 or answer == "":
        return {'message': 'Please use a valid answer input '}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(answer):
        return {'message': 'Please dont input symbols'}, 400
