"""
Write your program here.
"""
import sys, os, ast, io, trace, inspect

from input_generator import InputGenerator

# customisation constant
IS_GENERATE_REPORT = False # whether you want the output on terminal
HIGHEST_THRESHOLD = 95 # how much the coverage percentage, you want the program to stop generate
TIME_LIMIT = 100 # how many times the generate should be done (the more, the longer and more precise)

# getting input from argument
python_program = sys.argv[1]
input_file = sys.argv[2]


"""
Coverage class had been inspired and modified from tutorial 6
edstem.org. (n.d.). Ed Discussion. [online] 
Available at: https://edstem.org/au/courses/15196/lessons/51460/slides/349548 
[Accessed 6 May 2024].
"""
class Coverage:
    """
    A simple coverage analysis tool that hooks into the Python trace framework
    to record which lines of code are executed during the runtime of a script.
    """
    def __init__(self, python_program) -> None:
        """
        Initialises the Coverage instance with an empty trace list.
        """
        self.trace = []
        self.python_program = python_program

    def traceit(self, frame, event, arg):
        """
        Trace function called by sys.settrace for each event.
        """
        if self.orig_trace is not None:
            self.orig_trace(frame, event, arg)
        if event == "line":
            fi = inspect.getframeinfo(frame)
            name, num = fi.function, fi.lineno
            # when I inspect this property from frame execute from different file it return <string>
            # so, it will only append trace from other file that execute via exec()
            if inspect.getfile(frame) == "<string>":
                name = "<module>" # group all of that line in file in one name
                self.trace.append((name, num))
        return self.traceit

    def __enter__(self):
        """
        Sets the trace function to this instance's traceit method.
        """
        self.orig_trace = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """
        Restores the original trace function upon exiting the context.
        """
        sys.settrace(self.orig_trace)

    def coverage(self):
        """
        Returns a set of tuples representing the covered lines.
        """
        return set(self.trace)

    def __repr__(self) -> str:
        """ Provides a visual representation of the covered lines in the source code. """
        txt = ""
        for f_name in set(f_name for (f_name, line_number) in self.coverage()):
            # Handle the <module> case by reading file
            if f_name == "<module>":
                try:
                    src = open(self.python_program).readlines() # src is all the code from other file instead
                    start_ln = 1
                    for lineno in range(start_ln, start_ln + len(src)):
                        ind = ""
                        if (f_name, lineno) in self.trace:
                            ind = "| "
                        else:
                            ind = "  "
                        fmt = "%s%2d %s" % (ind, lineno, src[lineno - start_ln].rstrip())
                        txt += fmt + "\n"
                except Exception as exc:
                    print(exc)
            else:
                try:
                    fun = eval(f_name)  # Convert to code object
                except Exception as exc:
                    continue
                src, start_ln = inspect.getsourcelines(fun)
                for lineno in range(start_ln, start_ln + len(src)):
                    ind = ""
                    if (f_name, lineno) in self.trace:
                        ind = "| "
                    else:
                        ind = "  "
                    fmt = "%s%2d %s" % (ind, lineno, src[lineno - start_ln].rstrip())
                    txt += fmt + "\n"

        return txt
    
    def get_coverage_percent(self) -> str:
        total_statement = 0
        statement_cov = 0
        
        src = open(self.python_program).readlines() # src is all the code from other file instead
        start_ln = 1
        found_multi_comment = False
        for lineno in range(start_ln, start_ln + len(src)):
            
            # ignore multi comment
            code_str = src[lineno - start_ln].rstrip()
            if '"""' in code_str:
                found_multi_comment = not found_multi_comment
                continue
            if found_multi_comment:
                continue
            
            # if it got traced, that mean it's sure to be statement
            if ("<module>", lineno) in self.trace:
                statement_cov += 1
                total_statement += 1
                continue
            
            # otherwise evaluate the code string
            if self.is_statement(code_str):
                total_statement += 1
            
        return (statement_cov/total_statement) * 100

    def is_statement(self, code_str: str) -> bool:
        if code_str == "":
            return False
        if "else:" in code_str:
            return False
        if "#" in code_str:
            return False
        return True
    
    def clear_coverage(self):
        self.trace = []

ret_inputs = [line.strip() for line in open(input_file).readlines()]
old_inputs = ret_inputs
old_cov_percent = 0

# run the test on old input
sys.stdout = open(os.devnull, 'w')
with Coverage(python_program) as cov:
    # Iterate over inputs
    for input_data in old_inputs:     
        try:
            sys.stdin = io.StringIO(input_data)
            exec(open(python_program).read())
        except Exception as e:
            continue
old_cov_percent = cov.get_coverage_percent()
cov.clear_coverage()
sys.stdout = sys.__stdout__

best_cov_percent = 0

generator = InputGenerator()
generator.input_analyser(ret_inputs)
generator.list_input_analyse(open(python_program).read())

# test for n times
for _ in range(TIME_LIMIT):
    # generate new inputs from fuzzer
    new_inputs = []
    for _ in range(len(ret_inputs)):
        new_inputs.append(generator.generate_input())
    #print(new_inputs)
    
    # run the test
    sys.stdout = open(os.devnull, 'w')
    with Coverage(python_program) as cov:
        # Iterate over inputs
        for input_data in new_inputs:     
            try:
                sys.stdin = io.StringIO(input_data)
                exec(open(python_program).read())
            except Exception as e:
                continue
    sys.stdout = sys.__stdout__

    # select result input if it achieve better coverage
    if cov.get_coverage_percent() > best_cov_percent:
        best_cov_percent = cov.get_coverage_percent()
        ret_inputs = new_inputs
    cov.clear_coverage()
    
    if best_cov_percent > HIGHEST_THRESHOLD:
        break

# custom this if you want to see how much your new generated input cover your Python program
if IS_GENERATE_REPORT:
    print("The old inputs are: " + str(old_inputs))
    print('had coverage: ' + str(old_cov_percent) + "%")
    print()
    print("The new inputs are: " + str(ret_inputs))
    print('had the new coverage: ' + str(best_cov_percent) + "%")

with open(input_file, 'w') as f:
    for item in ret_inputs:
        f.write("%s\n" % item)