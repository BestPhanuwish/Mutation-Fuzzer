"""
My built-in class to generate fuzzing according to the type of input
"""

from mutated_str import generate_random_mutated_str
from ast_helper import NodeVisiter

from typing import List
import ast
import random

class FunctionHolder:
    def __init__(self, func, value):
        self.func = func
        self.value = value

    def execute(self):
        return self.func(self.value)

# return key for split
def is_format_input(inputs: List[str]) -> str:
    key_for_split = [" ", ",", ":", "-", "/"]
    key = None
    var_num = 0

    # check what kind of split they use (in case they use other than space)
    for delimiter in key_for_split:
        if delimiter == " ":
            if len(inputs[0].split()) > 1:
                var_num = len(inputs[0].split(delimiter))
                key = delimiter
                break
        if len(inputs[0].split(delimiter)) > 1:
            var_num = len(inputs[0].split(delimiter))
            key = delimiter
            break
    
    # check if every input had the same amount sub input
    for input in inputs:
        if key == " ":
            if len(input.split()) != var_num:
                return
        else:
            if len(input.split(key)) != var_num:
                return
    
    return key

def generate_random_int(min_max: tuple) -> str:
    # small chance to generate num with space
    if random.randint(0,50) == 1:
        return (str(random.randint(min_max[0], min_max[1]))+" ") * 3
    return str(random.randint(min_max[0], min_max[1]))

def generate_random_boolean(any: None) -> str:
    return str(random.choice([True, False]))

def generate_random_float():
    # make it so it had a chance to generate 0
    if random.randint(1,20) == 1:
        return 0
    return random.uniform(-1e10, 1e10)

class InputGenerator():
    
    def __init__(self) -> None:
        self.mutators: List[List[FunctionHolder]] = []
        self.input_contain_int: List[int] = [0] * 10 # max with 10 for now
        self.input_contain_bool: List[int] = [0] * 10
        self.input_contain_str: List[int] = [0] * 10
        self.key_format = None
        self.list_input = []
        pass
    
    def input_analyser(self, inputs: List[str]):
        
        # check if it's formatted input
        self.key_format = is_format_input(inputs)
        if self.key_format != None:
            
            row_input = [[] for _ in range(len(inputs[0].split(self.key_format)))]

            # Split each input line and append values to the corresponding sub_input
            for line in inputs:
                values = line.split(self.key_format)
                for i, value in enumerate(values):
                    row_input[i].append(value)

            # create mutation function for their own sub input
            for i, inputs in enumerate(row_input):
                
                self.mutators.append([])
                all_int = []
                
                for input in inputs:
                    if input.lstrip('-+').isdigit():
                        self.input_contain_int[i] += 1
                        all_int.append(int(input))
                    elif input == "True" or input == "False":
                        self.input_contain_bool[i] += 1
                    else:
                        self.input_contain_str[i] += 1
                        
                # if the input had int number, add int input generate within the range
                for _ in range(self.input_contain_int[i]):
                    self.mutators[i].append(FunctionHolder(
                        generate_random_int,
                        (int((min(all_int)-1)/2), max(all_int)*2)
                    ))
                for _ in range(self.input_contain_bool[i]):
                    self.mutators[i].append(FunctionHolder(
                        generate_random_boolean,
                        None
                    ))
                for _ in range(self.input_contain_str[i]):
                    self.mutators[i].append(FunctionHolder(
                        generate_random_mutated_str,
                        inputs
                    ))
            
        else:

            self.mutators.append([])
            # use for int checking
            all_int = []
            
            for input in inputs:
                if input.lstrip('-+').isdigit():
                    self.input_contain_int[0] += 1
                    all_int.append(int(input))
                elif input == "True" or input == "False":
                    self.input_contain_bool[0] += 1
                else:
                    self.input_contain_str[0] += 1
                    
            # if the input had int number, add int input generate within the range
            for _ in range(self.input_contain_int[0]):
                self.mutators[0].append(FunctionHolder(
                    generate_random_int,
                    (min(all_int)-1, max(all_int))
                ))
            for _ in range(self.input_contain_bool[0]):
                self.mutators[0].append(FunctionHolder(
                    generate_random_boolean,
                    None
                ))
            for _ in range(self.input_contain_str[0]):
                self.mutators[0].append(FunctionHolder(
                    generate_random_mutated_str,
                    inputs
                ))
                
    def list_input_analyse(self, code_str: str):
        v = ast.parse(code_str)
        visitor = NodeVisiter()
        visitor.visit(v)
        self.list_input = visitor.list_items
    
    def generate_input(self):
        if self.key_format == None:
            choices = self.list_input.copy()
            choices.append(random.choice(self.mutators[0]).execute())
            return random.choice(choices)
        else:
            retval = ""
            for i, mut_list in enumerate(self.mutators):
                if self.input_contain_str[i] > 0:
                    choices = self.list_input.copy()
                    choices.append(random.choice(mut_list).execute())
                    retval += random.choice(choices) + self.key_format
                else:
                    retval += random.choice(mut_list).execute() + self.key_format
            retval = retval[:-1]
            return retval

# Example usage

"""
generator = InputGenerator()
inputs = [line.strip() for line in open("example.in").readlines()]
generator.input_analyser(inputs)
for i in range(10):
    print(generator.generate_input())
"""