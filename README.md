# Fuzzing with mutated input

## Description

Mutation Fuzzer is a program written in Python designed to read in the example input and test it against other Python program to generate a better input test suite that can cover more statement in that Python program by repeatly automatically generate new input by combining the pre knowledge input and structure of Python code to test it multiple times against that Python program. Then pick the best input test suite and write back to the input file.

## About

Mutation Fuzzer program is dedicated for educational purpose only. Since this is only a part for university project at USYD - SOFT3202 Software Construction and Design 2 given by the task:
> In this part of the assignment, you will develop a fuzzer designed to automate the generation and mutation of test inputs to maximize the coverage of a test suite. The primary goal is to expand the test coverage by identifying and adding inputs that expose new paths or states in the software under test. - USYD

Only student at USYD can see the [scaffold](https://edstem.org/au/courses/15196/lessons/51934/slides/353593)

There's a different between statement and branch coverage that's the output of this program. That is statement coverage is the percentage of executable statements in the software that are executed by all the test cases in the test suite. Where branch coverage is the percentage of every path for each condition that had been covered through (for example if and while statement had at least 2 branch).

## Goals and Knowledge outcome

During the development of Mutation Fuzzer program I had gain an understanding of
- Automation in testing using fuzzer
- Using Fuzzer for input mutation and generate better test suite that cover more statement
- White-box testing using ast, trace, and inspect for internal code testing

## How to use the program

1. Clone this directory into your local computer
2. Make sure that your terminal is in the correct directory. Then you can run the program using command below
```
python mutation_fuzzer.py <python_program> <input_file>
```
*Note: If you doesn't have your Python and input file you can try run it against the example files that's also include in this directory:
```
python mutation_fuzzer.py example.py example.in
```
*Note 2: If you use your input file. Be sure to back up your input file as well since this program will make change to your input file

3. Your input file will be changed. If you use an example input file ```example.in```. Originally like this:
```
Monday
Tuesday
Holiday
Monday
```
It will change randomly to something new. If you run it again, you will see that it will change as well.

4. Now you can have fun and try with different other Python program and test suite.

## Note for developer
This program also allow some bit of customisation that you can manipulate it in ```mutation_fuzzer.py```
- ```IS_GENERATE_REPORT = False```
This program doesn't show output to the terminal. But if you want to, you can turn it on.
- ```HIGHEST_THRESHOLD = 95```
The program will stop generating new input when it reach certain threshold of coverage. The default value if 95. But if you want it to cover all your program then you change it to 100. (The value should be between 0-100)
- ```TIME_LIMIT = 100```
This is the number of time the program had generate new input. The default value is 100 that means it generate for 100 times max. The more this number, the more the input will be generate, that mean you might have a chance to get the perfect input if you had high number of time limit, but please consider the trade of which will take more time for the program to run before it got terminated.

## Contributor

USYD: https://www.sydney.edu.au/

## Credit

Programmer: Phanuwish Chamnivigaiwech (Best)