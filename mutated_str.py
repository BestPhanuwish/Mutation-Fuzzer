from typing import List
import random
import string

"""
This mutated string function had been developed and inspried by Lecture 7
Fuzzing and search based fuzzing: Mutation of Inputs
edstem.org. (n.d.). Ed Discussion. [online] 
Available at: https://edstem.org/au/courses/15196/lessons/51658/slides/351558
[Accessed 17 May 2024].
"""
def delete_random_character(s: str) -> str:
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]

def insert_random_character(s: str) -> str:
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]

def multiply_character(s):
    """Returns s with random multiple"""
    return s*random.randint(1,6)

def same_str_but_big(s):
    return s.upper()

def generate_random_string(min_length, max_length):
    length = random.randint(min_length, max_length)
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

mutators = [
    delete_random_character,
    insert_random_character,
    flip_random_character,
    multiply_character,
    same_str_but_big
]

def generate_random_mutated_str(inputs: List[str]) -> str:
    """Return s with a random mutation applied"""
    # very small chance to generate completely random string
    if random.randint(0,10) == 1:
        # count lenght
        all_len = []
        for input in inputs:
            all_len.append(len(input))
        return generate_random_string(min(all_len)-(random.randint(0,2)*10), max(all_len)+(random.randint(0,2)*10))
    else:
        mutator = random.choice(mutators)
        # print(mutator)
        return mutator(random.choice(inputs))