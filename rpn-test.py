import math

stack = []


operations = {"+" : (lambda x,y : x + y),
            "-" : (lambda x,y : x - y),
            "*" : (lambda x,y : x * y),
            "/" : (lambda x,y : x / y),
            "**" : (lambda x,y : x ** y),
            "%" : (lambda x,y : x % y)
            }


inp = ""

while True:
    
    inp = input()
    
    if inp in operations.keys() and len(stack) >= 2 :
        
        op2 = stack.pop()
        op1 = stack.pop()
        
        res = operations[inp](op1,op2)
        
        stack.append(res)
        
        print(res)


    else:
        
        try:
            stack.append(float(inp))    
        except:
            print("unknown op")
		