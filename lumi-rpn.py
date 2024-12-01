import customtkinter as ctk 
from ast import literal_eval
from sympy import divisors
import math
import sympy.ntheory
import scipy.special

def create_ui():
    # Set the appearance mode and theme
    ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
    ctk.set_default_color_theme("green")  # Options: "blue", "dark-blue", "green"

    # Initialize main window
    #progress_window = ctk.CTk()
    root = ctk.CTk()
    #progress_window.title("Lumi RPN Launcher")
    root.title("Lumi RPN")
    
    # Fix the window size and make it non-resizable
    window_width = 400
    window_height = 560
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    
    #progress_window.geometry(f"{400}x{50}")
    #progress_window.resizable(False, False)
    #progress_window.mainloop()

    # Create a textbox with 'Courier New' font
    textbox_width = 380  # Width in pixels
    textbox_height = 200 # Height in pixels
    textbox = ctk.CTkTextbox(root, 
                        width=textbox_width, 
                        height=textbox_height, font=("Cascadia Mono", 16))
                        
    textbox.tag_config("highlight", background="black", foreground="white")
    
    textbox.pack(pady=10, padx=1)  # Add 1px padding to the sides
    
    # insert startup text
    #with open("startup.txt", "r") as file:
    #    startup = file.read
    
    VERSION = "1.12"
    startup = r'''
    __                _                
   / /  __ _____ __  (_) ________  ___ 
  / /  / // / _ `_ \/ / / __/ __ \/ _ \
 / /__/ // / // // / / / / / /_/ / // /
/_____\_,_/_//_//_/_/ /_/ / .___/_//_/
   nov'24 ver $$$$$$$$$$$/_/   (c) ajgl'''
    textbox.insert("1.0", startup.replace("$$$$$$$$$$$",VERSION + (11-len(VERSION))* " "))  # Insert new text
    textbox.configure(state="disabled")

    # Create a frame for the button grid
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=1, padx=1)
    
    # lower frame, settings, text TODO
    text_label = ctk.CTkLabel(root, text = "Lumi RPN '24 ver $$$".replace("$$$",VERSION),
    font=("Cascadia Mono", 16, "italic"))
    text_label.pack(pady=1, padx=1)
    
    #textbox.tag_add("highlight", "3.1","3.10")  # Highlight one character
    
    stack = [""]
    unit_stack = [[0,0,0,0,0,0,0]] # s m kg A K mol cd
    
    def unit_mul(x,y):
        return [x_ + y_ for x_,y_ in zip(x,y)]
    def unit_div(x,y):
        return [x_ - y_ for x_,y_ in zip(x,y)]
    
    unit_operations = {"+" : (lambda x,y : x),
                       "-" : (lambda x,y : x),
                       "*" : (lambda x,y : unit_mul(x,y)),
                       "/" : (lambda x,y : unit_div(x,y)),
                       "mod" : (lambda x,y : unit_div(x,y)),
                       "(-)" : (lambda x : x),
                       "con" : (lambda x : x),
                       "abs" : (lambda x : x),
    }
    
    units = {"s" : [1,0,0,0,0,0,0],
            "m"  : [0,1,0,0,0,0,0],
            "kg" : [0,0,1,0,0,0,0],
            "A"  : [0,0,0,1,0,0,0],
            "K"  : [0,0,0,0,1,0,0],
            "mol": [0,0,0,0,0,1,0],
            "cd" : [0,0,0,0,0,0,1],
            "V"  : [-3,2,1,-1,0,0,0],
            "J"  : [-2,2,1,0,0,0,0]
    }
    
    operations = {"+" : (lambda x,y : x + y),
            "-" : (lambda x,y : x - y),
            "*" : (lambda x,y : x * y),
            "/" : (lambda x,y : x / y),
            "^" : (lambda x,y : x ** y),
            "^n" : (lambda x,y : x ** y),
            "mod" : (lambda x,y : x % y),
            "n√" : (lambda x,y : x ** (1/y)),
            "bnm" : (lambda x,y : math.comb(x,y)),
            "gcd" : (lambda x,y : math.gcd(x,y)),
            "lcm" : (lambda x,y : math.lcm(x,y)),
            }
            
    functions = {
            "(*)" : (lambda x : x.real - 1j*x.imag ),
            "sin" : (lambda x : math.sin(x)),
            "cos" : (lambda x : math.cos(x)),
            "tan" : (lambda x : math.tan(x)),
            "exp" : (lambda x : math.exp(x)),
            "10^": (lambda x : 10**x),
            "ln" : (lambda x : math.log(x)), 
            "log" : (lambda x : math.log(x)/math.log(10)), 
            "sqr": (lambda x : math.sqrt(x)),
            "cbr": (lambda x : x**(1/3)),
            "^2" : (lambda x : x**2),
            "^3" : (lambda x : x**3),
            "^-1": (lambda x : 1/x),
            "asn" : (lambda x : math.asin(x)),
            "acs" : (lambda x : math.acos(x)),
            "atn" : (lambda x : math.atan(x)),
            "!"   :  (lambda x : math.factorial(x)),
            "abs" : (lambda x : abs(x)),
            "(-)" : (lambda x : -x),
            "snh" : (lambda x : math.sinh(x)),
            "csh" : (lambda x : math.cosh(x)),
            "tnh" : (lambda x : math.tanh(x)),
            "ash" : (lambda x : math.asinh(x)),
            "ach" : (lambda x : math.acosh(x)),
            "ath" : (lambda x : math.atanh(x)),
            "ζ": (lambda x : scipy.special.zeta(x)),
            "Γ" : (lambda x : math.gamma(x))
            }
            
                                                   # s m kg A K mol cd
    constants = {"π" : {"value" : math.pi, "unit" : [0,0,0,0,0,0,0]},
                 "e" : {"value" : math.e, "unit" : [0,0,0,0,0,0,0]},
                 "u" : {"value" : 1.66053906892e-27, "unit" : [0,0,1,0,0,0,0]},
                 "qₑ": {"value" : 1.602176634e-19, "unit" : [1,0,0,1,0,0,0]},
                 "mₑ": {"value" : 9.1093837e-31, "unit" : [0,0,1,0,0,0,0]},
                 "ε₀": {"value" : 8.8541878188e-12, "unit" : [4,-3,-1,2,0,0,0]},
                 "μ₀": {"value" : 1.25663706127e-6 , "unit" : [-2,1,1,-2,0,0,0]},
                 "c" : {"value" : 299792458, "unit" : [-1,1,0,0,0,0,0]},
                 "h" : {"value" : 6.62607015e-34, "unit" : [-1,2,1,0,0,0,0]},
                 "ħ" : {"value" : 1.054571817e-34, "unit" : [-1,2,1,0,0,0,0]},
                 "G" : {"value" : 6.67430e-11, "unit" : [-2,3,-1,0,0,0,0]},
                 "k" : {"value" : 1.380649e-23, "unit" : [-2,2,1,0,1,0,0]},
                 "Nₐ": {"value" : 6.02214076e23, "unit" : [0,0,0,0,0,-1,0]},
                 "σ" : {"value" : 5.670374419e-8, "unit" : [-3,0,1,0,-4,0,0]},
                 "g" : {"value" : 9.80665, "unit" : [-2,1,0,0,0,0,0]}
                }
            
    button_labels = [["sqr","n√","abs","mod","gcd","lcm","!","bnm","fct"], 
                ["^2","^3","^n","(-)","(*)","sin","cos","tan","exp"], 
                ["i","π","e","ζ","Γ","snh","csh","tnh","ln"], 
                ["u","qₑ","ε₀","c","h","G","σ","k","Nₐ"], 
                ["s","m","kg","A","K","mol","cd","V","J"]]
    
    under_button_labels = {"ln" : "log",
                        "s" : "Hz",
                        "sin" : "asn",
                        "cos" : "acs",
                        "tan" : "atn",
                        "snh" : "ash",
                        "csh" : "ach",
                        "tnh" : "ath",
                        "qₑ" : "mₑ",
                        "ε₀" : "μ₀",
                        "h" : "ħ",
                        "exp" : "10^",
                        "fct" : "div",
                        "G" : "g",
                        "^n": "^-1"
                        }
    
    def onButtonPress(inp,stack):
        
        def func_handler(inp,event,stack):
            
            button_num = event.num
            
            # replace function with secondary function if poss
            if button_num == 3: 
                inp = under_button_labels.get(inp,inp) 
                        
            #print("pressed",button_num)
            err = False
            if inp in functions.keys():
                
                try:
                    op = stack.pop(); op_unit = unit_stack.pop()
                    if op == "":
                        op = "0"
                    

                    res = functions[inp](literal_eval(op))
                    
                    stack.append(str(res)) 
                    
                    if inp in unit_operations.keys():
                        res = unit_operations[inp](op_unit)
                        unit_stack.append(res)
                    elif inp == "^2":
                        res = [2*exponent for exponent in op_unit]
                        unit_stack.append(res)
                    elif inp == "^3":
                        res = [3*exponent for exponent in op_unit]
                        unit_stack.append(res)
                    elif inp == "sqr":
                        res = [exponent//2 for exponent in op_unit]
                        unit_stack.append(res)
                    elif inp == "cbr":
                        res = [exponent//3 for exponent in op_unit]
                        unit_stack.append(res)
                    else:
                        unit_stack.append([0,0,0,0,0,0,0])
                        
                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op); unit_stack.append(op_unit)
                    err = e
                except:
                    stack.append(op); unit_stack.append(op_unit)
                    err = "error"
                    
            
            elif inp in operations.keys() and len(stack) >= 2 :
                
                try:
                    op2 = stack.pop(); op_unit2 = unit_stack.pop()
                    op1 = stack.pop(); op_unit1 = unit_stack.pop()
                    
                    if op2 == "":
                        op2 = "0"
                    
                    if op1 == "":
                        op1 = "0"
                        
                    res = operations[inp](literal_eval(op2),literal_eval(op1))
                    
                    stack.append(str(res));
                    
                    if inp in unit_operations.keys():
                        res = unit_operations[inp](op_unit2,op_unit1)
                        unit_stack.append(res)
                    elif inp == "n√":
                        res = [exponent//int(literal_eval(op1)) for exponent in op_unit2]
                        unit_stack.append(res)
                    elif inp == "^n":
                        res = [int(literal_eval(op1))*exponent for exponent in op_unit2]
                        unit_stack.append(res)
                    else:
                        unit_stack.append([0,0,0,0,0,0,0])
                        
                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op1); unit_stack.append(op_unit1)
                    stack.append(op2); unit_stack.append(op_unit2)
                    err = e
                except:
                    stack.append(op1); unit_stack.append(op_unit1)
                    stack.append(op2); unit_stack.append(op_unit2)
                    err = "error"
                    
            elif inp in constants.keys():
                
                if stack[-1] == "":
                    stack[-1] = str(constants[inp]["value"]); unit_stack[-1] = constants[inp]["unit"]
                else:
                    stack.append(str(constants[inp]["value"])); unit_stack.append(constants[inp]["unit"])
            
            elif inp == "(.)":
                stack[-1] += "."
                
            elif inp == "fct":
                try:
                    op = stack.pop(); op_unit = unit_stack.pop()
                    dict = sympy.ntheory.factorint(literal_eval(op))
                    
                    for index,prime in enumerate(dict.keys()):
                        for i in range(dict[prime]):
                            stack.append(str(prime))
                            if index == len(dict.keys()) -1: 
                                unit_stack.append(op_unit)
                            else:
                                unit_stack.append([0,0,0,0,0,0,0])
                                
                    if len(dict.keys()) == 1 and dict[prime] == 1 and literal_eval(op) > 1:
                        err = f"{op} is prime"
                    
                    if not dict:
                        stack.append(op); unit_stack.append(op_unit)

                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op); unit_stack.append(op_unit)
                    err = e
                except:
                    stack.append(op); unit_stack.append(op_unit)
                    err = "error"
            elif inp == "div":

                try:
                    op = stack.pop(); op_unit = unit_stack.pop()
                    divs = divisors(literal_eval(op)) 
                    
                    for index, num in enumerate(divs):
                        
                        stack.append(str(num))
                        if index == len(divs)-1:
                            unit_stack.append(op_unit)
                        else:
                            unit_stack.append([0,0,0,0,0,0,0])
                            
                    if not divs:
                        stack.append(op); unit_stack.append(op_unit)

                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op); unit_stack.append(op_unit)
                    err = e
                except:
                    stack.append(op); unit_stack.append(op_unit)
                    err = "error"
                    
            elif inp == "i":
                stack[-1] += "j"
                
            elif inp in units.keys():
                
                if button_num == 1:
                    unit_stack[-1] = unit_mul(unit_stack[-1],units[inp])
                elif button_num == 3:
                    unit_stack[-1] = unit_div(unit_stack[-1],units[inp])
                    
            print_stack(stack,err)
            
            
        return lambda event: func_handler(inp,event,stack)
        
    # Add buttons in a 3x9 grid
    for i in range(5):
        for j in range(9):
            ctext = button_labels[i][j]
            ctext2 = under_button_labels.get(ctext, "") #under_button_labels[i][j]
                
            btn = ctk.CTkButton(button_frame, text=ctext + "\n" + ctext2)
            #command=onButtonPress(ctext,stack)) # Button height in pixels
            
            btn.bind("<Button-1>", onButtonPress(ctext,stack))
            btn.bind("<Button-2>", onButtonPress(ctext,stack)) # no general support atm
            btn.bind("<Button-3>", onButtonPress(ctext,stack)) # inverse units
            
            btn.grid(row=i, column=j, padx=1, pady=1)
            btn.configure(font = ("Cascadia Mono", 14), width=40, height=60,border_spacing=0)
            #if ctext not in ["(.)","fct","i"] + list(constants.keys()) + list(functions.keys()) + list(operations.keys()):
            #    btn.configure(state = "disabled")
            if i == 3:
                btn.configure(fg_color = "green")
                btn.configure(font = ("Cascadia Mono", 14, "italic"))
                
            if i == 4:
                btn.configure(fg_color = "blue")
    
    
    def print_stack(stack,err,print_shell=False):
            
        textbox.configure(font=("Cascadia Mono", 18))
        if print_shell : print(stack)
        
        textbox.configure(state="normal")  # Temporarily make it editable
        textbox.delete("1.0", ctk.END)  # Clear existing text
        
        print_string = ""
        
        for i,(num,unit) in reversed(list(enumerate(zip(stack,unit_stack)))):
            # unit formatting "s","m","kg","A","K","mol","cd" -> "A","K","cd","mol","kg","m","s"
            unit_string = ""
            for index in (2,3,4,6,5,1,0):
                exponent  = unit[index]
                base_unit = ("s","m","kg","A","K","mol","cd")[index]
                
                if exponent == 1:
                    unit_string += f".{base_unit}"
                elif exponent == -1 and unit_string != "":
                    unit_string += f"/{base_unit}"
                elif exponent == -1 and unit_string == "":
                    unit_string += f"1/{base_unit}"
                elif exponent < -1 and unit_string != "":
                    unit_string += f"/{base_unit}^{-exponent}"
                elif exponent < -1 and unit_string == "":
                    unit_string += f"1/{base_unit}^{-exponent}"
                elif exponent not in (0,1):
                    unit_string += f".{base_unit}^{exponent}"
                    
            if unit_string and unit_string[0] == ".": unit_string = unit_string[1:]
            
            print_string += f"[{i+1}] >> " + str(num).replace("j","i") + " " + unit_string + "\n"
            
        textbox.insert("1.0", print_string )  # Insert new text
        if print_shell : print(err)
        if err: textbox.insert("8.0", err )  # Insert new text
          
        textbox.configure(state="disabled")  # Lock it again
        
            
    def onKeyPress(event,stack):
        
        err = False
        inp = event.char
        
        if inp in operations.keys() and stack[-1] != "" and stack[-1][-1] != "e" and len(stack) >= 2 :
            
            try:
                op2 = stack.pop(); op_unit2 = unit_stack.pop()
                op1 = stack.pop(); op_unit1 = unit_stack.pop()
                
                if op2 == "":
                    op2 = "0"
                
                if op1 == "":
                    op1 = "0"
                    
                res = operations[inp](literal_eval(op2),literal_eval(op1))
                
                stack.append(str(res))
                
                if inp in unit_operations.keys():
                    res = unit_operations[inp](op_unit2,op_unit1)
                    unit_stack.append(res)
                else:
                    unit_stack.append([0,0,0,0,0,0,0])
                    
            except (ValueError,TypeError,OverflowError) as e:
                stack.append(op1); unit_stack.append(op_unit1)
                stack.append(op2); unit_stack.append(op_unit2)
                err = e
            except:
                stack.append(op1); unit_stack.append(op_unit1)
                stack.append(op2); unit_stack.append(op_unit2)
                err = "error"
            
        elif inp in ("0","1","2","3","4","5","6","7","8","9","e"):
            
            stack[-1] += inp
            
        elif inp in ("i","j"):
            
            stack[-1] += "j"
        
        elif inp in ("+","-"): # only after j or e ?
            
            stack[-1] += inp
            
        elif inp in (",","."):
            
            stack[-1] += "."
        elif event.keysym == "BackSpace":  # delete last char
            if len(stack[-1]) > 0:
                stack[-1] = stack[-1][:-1]
            elif len(stack) > 1:
                stack.pop() ; unit_stack.pop()
                
        elif event.keysym == "Delete":  # Delete input
            if len(stack[-1]) > 0 or unit_stack[-1] != [0,0,0,0,0,0,0]:
                stack[-1] = "" ; unit_stack[-1] = [0,0,0,0,0,0,0]
            elif len(stack) > 1:
                stack.pop(); unit_stack.pop()
            
        elif event.keysym == "Escape":  # Delete stack
            stack[:] = [""] ; unit_stack[:] = [[0,0,0,0,0,0,0]]
            
        elif event.keysym == "Return":
            try:
                #stack[-1] = str(literal_eval(stack[-1]))
                
                if stack[-1] != "": 
                    stack[-1] = str(literal_eval(stack[-1]))
                    stack.append("")
                    unit_stack.append([0,0,0,0,0,0,0])
            except:

                err = f"literal '{stack[-1]}' cannot be evaluated"
                

            
        print_stack(stack,err)
            
        
    root.bind('<KeyPress>',  lambda event: onKeyPress(event,stack))
    
    # Start the main loop
    
    root.mainloop()
    


if __name__ == "__main__":
    create_ui()
