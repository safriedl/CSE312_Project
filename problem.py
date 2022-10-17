import random


class problem:

    
    questions={}


    def generate_basic():
        question_types=["+","-","*","/"]
        int_a=random.randint(1,1000)
        int_b=random.randint(1,1000)
        type=random.choice(question_types)
        question=str(int_a)+" "+str(type)+" "+str(int_b)
        ans=eval(question)
        problem.questions[question]=round(ans,4)
    




