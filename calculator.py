import customtkinter as ctk 
import ast
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
    window_height = 500
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
                        height=textbox_height, font=("Consolas", 16))
                        
    textbox.tag_config("highlight", background="black", foreground="white")
    
    textbox.pack(pady=10, padx=1)  # Add 1px padding to the sides
    
    # insert startup text
    #with open("startup.txt", "r") as file:
    #    startup = file.read
        
    startup = r'''
    __                _                
   / /  __ _____ __  (_) ________  ___ 
  / /  / // / _ `_ \/ / / __/ __ \/ _ \
 / /__/ // / // // / / / / / /_/ / // /
/_____\_,_/_//_//_/_/ /_/ / .___/_//_/
 oct 2024 ver 1.0        /_/   (c) ajgl  
    '''
    textbox.insert("1.0", startup)  # Insert new text
    textbox.configure(state="disabled")


    # Create a frame for the button grid
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=1, padx=1)
    
    
    #textbox.tag_add("highlight", "3.1","3.10")  # Highlight one character
    
    stack = [""]
    
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
            "con" : (lambda x : x.real - 1j*x.imag ),
            "sin" : (lambda x : math.sin(x)),
            "cos" : (lambda x : math.cos(x)),
            "tan" : (lambda x : math.tan(x)),
            "exp" : (lambda x : math.exp(x)),
            "ln" : (lambda x : math.log(x)), 
            "sqr": (lambda x : math.sqrt(x)),
            "cbr": (lambda x : x**(1/3)),
            "^2" : (lambda x : x**2),
            "^3" : (lambda x : x**3),
            "asn" : (lambda x : math.asin(x)),
            "acs" : (lambda x : math.acos(x)),
            "atn" : (lambda x : math.atan(x)),
            "!"   :  (lambda x : math.factorial(x)),
            "abs" : (lambda x : abs(x)),
            "(-)" : (lambda x : -x),
            "sinh" : (lambda x : math.sinh(x)),
            "cosh" : (lambda x : math.cosh(x)),
            "tanh" : (lambda x : math.tanh(x)),
            "asnh" : (lambda x : math.asinh(x)),
            "acsh" : (lambda x : math.acosh(x)),
            "atnh" : (lambda x : math.atanh(x)),
            "ζ": (lambda x : scipy.special.zeta(x)),
            "Γ" : (lambda x : math.gamma(x))
            }
            
    constants = {"π" : math.pi,
                 "e" : math.e,
                 "u" : 1.66053906892e-27,
                 "qₑ" : 1.602176634e-19,
                 "ε₀" : 8.8541878188e-12,
                 "μ₀" : 1.25663706127e-6,
                 "c" : 299792458,
                 "ℎ" : 6.62607015e-34,
                 "G" : 6.67430e-11,
                 "k" : 1.380649e-23,
                 "Nₐ": 6.02214076e23
                }
            
    button_labels = [["sqr","n√","abs","mod","gcd","lcm","!","bnm","fct"], 
                ["^2","^3","^n","(-)","con","sin","cos","tan","exp"], 
                ["i","π","e","ζ","Γ","asn","acs","atn","ln"], 
                ["u","qₑ","ε₀","μ₀","c","ℎ","G","k","Nₐ"], 
                ]
        
    
    def onButtonPress(inp,stack):
        
        def func_handler(stack):
            #print("pressed",inp)
            err = False
            if inp in functions.keys():
                
                try:
                    op = stack.pop()
                    if op == "":
                        op = "0"
                        
                    res = functions[inp](ast.literal_eval(op))
                    
                    stack.append(str(res))
                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op)
                    err = e
                except:
                    stack.append(op)
                    err = "error"
                    
            
            elif inp in operations.keys() and len(stack) >= 2 :
                
                try:
                    op2 = stack.pop()
                    op1 = stack.pop()
                    
                    if op2 == "":
                        op2 = "0"
                    
                    if op1 == "":
                        op1 = "0"
                        
                    res = operations[inp](ast.literal_eval(op2),ast.literal_eval(op1))
                    
                    stack.append(str(res))
                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op1)
                    stack.append(op2)
                    err = e
                except:
                    stack.append(op1)
                    stack.append(op2)
                    err = "error"
                    
            elif inp in constants.keys():
                
                if stack[-1] == "":
                    stack[-1] = str(constants[inp])
                else:
                    stack.append(str(constants[inp]))
            
            elif inp == "(.)":
                stack[-1] += "."
                
            elif inp == "fct":
                try:
                    op = stack.pop()
                    dict = sympy.ntheory.factorint(ast.literal_eval(op))
                    
                    for prime in dict.keys():
                        for i in range(dict[prime]):
                            stack.append(str(prime))
                except (ValueError,TypeError,OverflowError) as e:
                    stack.append(op)
                    err = e
                except:
                    stack.append(op)
                    err = "error"
                    
            elif inp == "i":
                stack[-1] += "j"
                    
            print_stack(stack,err)
            
            
        return lambda : func_handler(stack)
        
    # Add buttons in a 3x9 grid
    for i in range(4):
        for j in range(9):
            ctext = button_labels[i][j]
                
            btn = ctk.CTkButton(button_frame, text=ctext,
            command=onButtonPress(ctext,stack)) # Button height in pixels
            
            btn.grid(row=i, column=j, padx=1, pady=1)
            btn.configure(font = ("Consolas", 14), width=40, height=60,border_spacing=0)
            if ctext not in ["(.)","fct","i"] + list(constants.keys()) + list(functions.keys()) + list(operations.keys()):
                btn.configure(state = "disabled")
            if i == 3:
                btn.configure(fg_color = "green")
    
    
    def print_stack(stack,err,print_shell=False):
            
        textbox.configure(font=("Consolas", 20))
        if print_shell : print(stack)
        
        textbox.configure(state="normal")  # Temporarily make it editable
        textbox.delete("1.0", ctk.END)  # Clear existing text
        
        print_string = ""
        
        for i,num in reversed(list(enumerate(stack))):
            print_string += f"[{i+1}] >> " + str(num).replace("j","i") + "\n"
            
        textbox.insert("1.0", print_string )  # Insert new text
        print(err)
        if err: textbox.insert("8.0", err )  # Insert new text
          
        textbox.configure(state="disabled")  # Lock it again
        
            
    def onKeyPress(event,stack):
        
        err = False
        inp = event.char
        
        if inp in operations.keys() and stack[-1] != "" and stack[-1][-1] != "e" and len(stack) >= 2 :
            
            try:
                op2 = stack.pop()
                op1 = stack.pop()
                
                if op2 == "":
                    op2 = "0"
                
                if op1 == "":
                    op1 = "0"
                    
                res = operations[inp](ast.literal_eval(op2),ast.literal_eval(op1))
                
                stack.append(str(res))
            except (ValueError,TypeError,OverflowError) as e:
                stack.append(op1)
                stack.append(op2)
                err = e
            except:
                stack.append(op1)
                stack.append(op2)
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
                stack.pop()
                
        elif event.keysym == "Delete":  # Delete input
            if len(stack[-1]) > 0:
                stack[-1] = ""
            elif len(stack) > 1:
                stack.pop()
            
        elif event.keysym == "Escape":  # Delete stack
            stack[:] = [""]
            
        elif event.keysym == "Return":
            try:
                stack[-1] = str(ast.literal_eval(stack[-1]))
                
                if stack[-1] != "": stack.append("")
            except:
                err = f"literal '{stack[-1]}' cannot be evaluated"
                

            
        print_stack(stack,err)
            
        
    root.bind('<KeyPress>',  lambda event: onKeyPress(event,stack))
    
    # Start the main loop
    
    root.mainloop()
    


if __name__ == "__main__":
    create_ui()
