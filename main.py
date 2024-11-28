import random, math
from typing import List

def attentive_agent_draw(urn_probability, guesses: List[str]):
    draw = random.random()
    if draw < urn_probability:
        if guesses.count("w") > guesses.count("b") + 1:
            guesses.append("w")
        else:
            guesses.append("b")
    else:
        if guesses.count("b") > guesses.count("w") + 1:
            guesses.append("b")
        else :
            guesses.append("w")

def inattentive_agent_draw(urn_probability, guesses: List[str]):
    draw = random.random()
    if draw < urn_probability:
        guesses.append("b")
    else:
        guesses.append("w")

def cascade_example(inattentivness_index = 0, draws=100, b_urn=0.66, w_urn=0.34):
    coin_toss = random.random()

    #probability of drawing a black ball from the urn
    if coin_toss < 0.5:
        urn_probability = b_urn
    else:
        urn_probability = w_urn

    guesses = []

    for i in range(draws):
        if inattentivness_index == 0:
            attentive_agent_draw(urn_probability, guesses)
        elif i % inattentivness_index == 0:
            inattentive_agent_draw(urn_probability, guesses)
        else: 
            attentive_agent_draw(urn_probability, guesses)

    if inattentivness_index == 0:
        probing_range = math.ceil(draws/10*2)
    else:
        probing_range = math.ceil(inattentivness_index*2)

    last_guess_sequence = guesses[-probing_range:]
    b_count = last_guess_sequence.count("b")
    w_count = last_guess_sequence.count("w")

    total_b_count = guesses.count("b")
    total_w_count = guesses.count("w")
    
    if b_count >= w_count and total_b_count > w_count:
        if urn_probability == b_urn:
            return 2
        else:
            return 1
        
    elif w_count >= b_count and total_w_count > b_count:
        if urn_probability == w_urn:
            return 2
        else:
            return 1
        
    elif w_count > 2 and total_b_count > total_w_count:
        return 0
        
    elif b_count > 2 and total_w_count > total_b_count:
        return 0

    return 0

def main():
    runs = 1000
    stats = { "correct_cascades": 0, "incorrect_cascades": 0 , "no_cascades": 0}
    intattentive_index = 0
    for _ in range(runs):
        result = cascade_example(inattentivness_index=intattentive_index)
        
        if result == 2:
            stats["correct_cascades"] += 1
        elif result == 1:
            stats["incorrect_cascades"] += 1
        elif result == 0:
            stats["no_cascades"] += 1

    print(stats)

main()