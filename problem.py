import random

question_set = {}


# pandas
def generate_question():
    operation_types = ["+", "-", "*", "/"]
    question_types = ["# & #"]
    question = random.choice(question_types)
    for i in question:
        if i == "#":
            question = question.replace(i, str(random.randint(1, 10)), 1)
        if i == "&":
            question = question.replace(i, str(random.choice(operation_types)), 1)
    ans = eval(question)
    question_set[question] = round(ans, 4)
    # added a return to get a question for the local problem, as a tuple of (question, answer)
    return (question, question_set[question])


def generator(num: int):
    for i in range(num):
        generate_question()


generator(10)
print(question_set)
