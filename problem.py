import random


class problem:

    
    question_set={}

    #pandas
    def generate_question():
        operation_types=["+" , "-" , "*" , "/", "**"]
        question_types=["(# & (# & #))",
                        "((# & #) & (# & #))",
                        "((# & (# & #)) & (# & #))"]
        question=random.choice(question_types)
        for i in question:
            if i =="#":
                question=question.replace(i,str(random.randint(1,10)),1)
            if i =="&":
                question=question.replace(i,str(random.choice(operation_types)),1)
        ans=eval(question)
        problem.question_set[question]=round(ans,4)
    def generator(num:int):
        for i in range(num):
            problem.generate_question()

problem.generator(10)
print(problem.question_set)
