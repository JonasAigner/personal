"""Generate question for mathetest"""
import random

def solver(question):
    s = ""
    for i in question:
        if i.__class__.__name__ == "str":
            s += i
        elif i.__class__.__name__ == "int":
            s += str(i)
    result = int(eval(s))
    results = []
    # ~ if result.__class__.__name__ == "float":
        # ~ result = result.round()
    results.append(result)
    for x in range(3):
        a = random.randint(1,50)*random.choice((-1,1))+result
        results.append(a)
    #print(results) 
    return results

def generate_question(difficulty=1):
    question = []
    numbers = 0
    if difficulty == 1:
        lower_limit = 0
        upper_limit = 10
        operators = ["+","-"]
        max_numbers = 3
        brackets = False
        divi = False
        negativ = False
    elif difficulty == 2:
        lower_limit = 0
        upper_limit = 10
        operators = ["+","-","*"]
        max_numbers = 4
        brackets = False
        divi = False
        negativ = False
    elif difficulty == 3:
        lower_limit = -20
        upper_limit = 20
        operators = ["+","-","*"]
        max_numbers = 5
        brackets = False
        divi = False
        negativ = True
    elif difficulty == 4:
        lower_limit = -20
        upper_limit = +20
        operators = ["+","-","*"]
        max_numbers = 10
        brackets = True
        divi = False
        negativ = True
    
    null = True
    while True:
        if not null:
            zahl1 = random.randint(1, upper_limit) * random.choice((-1,1))
            null = True
        else:
            zahl1 = random.randint(lower_limit, upper_limit)
        
        question.append(zahl1)
        numbers += 1
        
        if numbers > 1 and numbers < max_numbers:
            if random.random() < 0.3:
                break
        elif numbers >= max_numbers:
            break
        op = random.choice(operators)
        if op == "*" and divi:
            if random.random() < 0.35:
                op = "/"
                null = False
        question.append(op)
    #  ---------------------
    if brackets:
        newquestion = []
        first = True
        bracked_placed = False
        for x in question:
            if first:
                first = False
                if random.random() < 0.1:
                    newquestion.append("(")
                    bracked_placed = True
                    newquestion.append(x)
                else:
                    newquestion.append(x)
            else:
                if bracked_placed and x.__class__.__name__ == "int":
                    newquestion.append(x)
                    if random.random() < 0.4:
                        newquestion.append(")")
                        bracked_placed = False
                elif bracked_placed == False and x.__class__.__name__ == "str":
                    newquestion.append(x)
                    if random.random() < 0.3:
                        newquestion.append("(")
                        bracked_placed = True
                else:
                    newquestion.append(x)
                
        if bracked_placed:
            newquestion.append(")")
        question = newquestion
    if int(solver(question)[0]) < 0 and negativ == False:
        generate_question(difficulty)
    else:           
        return question
    

        
if __name__ == "__main__":  
    solver(generate_question())

