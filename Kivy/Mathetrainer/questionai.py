import random

def generate_question(max_num=100):
    question = []
    lower_limit = 0
    upper_limit = 10
    operators = ["+","-","*","/"]
    numbers = 0
    max_numbers = max_num
    while True:
        #print(question,"::", solver(question))
        term = []
        zahl1 = random.randint(lower_limit, upper_limit)
        zahl2 = random.randint(lower_limit, upper_limit)
        op = random.choice(operators)
        #print("I want ", op)
        if question == []:
            if op == "/":
                term = [zahl1*zahl2, op, zahl1]
                if zahl1 == 0:
                    continue
            question.extend(term)
            numbers += 2
        else:
            old_question = question[:]
            intpositions = []
            for x,i in enumerate(question):
                if i.__class__.__name__ == "int":
                    intpositions.append(x)
            pos = random.choice(intpositions)
            result = question[pos]
            #print("I want to replace ", result)
            left = old_question[:pos]
            right = old_question[pos+1:]
            #-----------------------
            if op == "+":
                term.append(zahl1)
                zahl2 = zahl1 - result
                if zahl2 < 0:
                    term.append("-")
                else:
                    term.append("-")
                term.append(zahl2)
            # ------------------
            elif op == "-":
                term.append(zahl1)
                zahl2 = zahl1 - result
                if zahl2 < 0:
                    term.append("+")
                    term.append(zahl2*(-1))
                else:
                    term.append("-")
                    term.append(zahl2)
            # ------------------------
            elif op == "*":
                # finde ggt von result
                if result == 0:
                    continue
                ggt = []
                ggt.append(result)
                for z in range(result-1, 0, -1):
                    if result % z == 0:
                        ggt.append(z)
                zahl1 = random.choice(ggt)
                zahl2 = int(result / zahl1)
                term.append(zahl1)
                term.append("*")
                term.append(zahl2)
            # --------------------=
            elif op == "/":
                if result == 0:
                    continue
                zahl1 = random.randint(1, upper_limit)
                zahl2 = result * zahl1
                term.append(zahl2)
                term.append(op)
                term.append(zahl1)
            # =----=----=----=----=
            middle = ["(", term[0], term[1], term[2], ")"]
            question = left
            question.extend(middle)
            question.extend(right)
            numbers += 1
            if random.random() < 0.25 or max_numbers <= numbers:
                break
    #print(question)
    return question

def solver(question):
    s = ""
    for i in question:
        if i.__class__.__name__ == "str":
            s += i
        elif i.__class__.__name__ == "int":
            s += str(i)
    try:
        result = int(eval(s))
    except:
        print("Bad Result")
        return None
    results = []
    results.append(result)
    for x in range(3):
       a = random.randint(1,50)*random.choice((-1,1))+result
       results.append(a) 
    return results
            
if __name__ == "__main__":
    print(solver(generate_question()))
