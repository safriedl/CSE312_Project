import random


# pandas
def generate_question():
    operation_types = ["+", "-", "*"]
    question_types = ["# & #"]
    question = random.choice(question_types)
    for i in question:
        if i == "#":
            question = question.replace(i, str(random.randint(1, 10)), 1)
        if i == "&":
            question = question.replace(i, str(random.choice(operation_types)), 1)
    ans = eval(question)
    return question, round(ans, 4)

