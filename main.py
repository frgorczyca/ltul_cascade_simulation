"""
This module simulates a cascade phenomenon using attentive and inattentive agents drawing balls from an urn.
Functions:
    attentive_agent_draw(urn_probability, guesses: List[str]) -> None:
        Simulates a draw by an attentive agent and updates the guesses list based on the urn probability and previous guesses.
    inattentive_agent_draw(urn_probability, guesses: List[str]) -> None:
        Simulates a draw by an inattentive agent and updates the guesses list based solely on the urn probability.
    cascade_example(inattentivness_index=0, draws=100, b_urn=0.66, w_urn=0.34) -> int:
        Simulates a cascade example with a given inattentiveness index and number of draws, returning the type of cascade observed.
    cascade_example_insert_range(start_range=0, end_range=0, draws=100, b_urn=0.66, w_urn=0.34) -> int:
        Simulates a cascade example with inattentive agents within a specified range of draws, returning the type of cascade observed.
    run_simulation(times: int, runs: int, method, *arguments) -> List[dict]:
        Runs the specified cascade simulation method multiple times and collects statistics on the outcomes.
    save_results(filename: str, stats_set: List[dict]) -> None:
        Saves the simulation results to a CSV file.
    plot_results(results: List[List[dict]], x_axis: List) -> None:
        Plots the results of the cascade simulations, showing the average counts of correct, incorrect, and no cascades.
"""

import random, math
import matplotlib.pyplot as plt
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
        else:
            guesses.append("w")


def inattentive_agent_draw(urn_probability, guesses: List[str]):
    draw = random.random()
    if draw < urn_probability:
        guesses.append("b")
    else:
        guesses.append("w")


def cascade_example(
    inattentivness_index: int = 0,
    draws: int = 100,
    b_urn: float = 0.66,
    w_urn: float = 0.34,
):
    coin_toss = random.random()

    # probability of drawing a black ball from the urn
    if coin_toss < 0.5:
        urn_probability = b_urn
    else:
        urn_probability = w_urn

    guesses = []

    for i in range(draws):
        if inattentivness_index > 0 and i % inattentivness_index == 0:
            inattentive_agent_draw(urn_probability, guesses)
        else:
            attentive_agent_draw(urn_probability, guesses)

    if inattentivness_index == 0:
        probing_range = math.ceil(draws / 10 * 2)
    else:
        probing_range = math.ceil(inattentivness_index * 2)

    last_guess_sequence = guesses[-probing_range:]
    b_count = last_guess_sequence.count("b")
    w_count = last_guess_sequence.count("w")

    total_b_count = guesses.count("b")
    total_w_count = guesses.count("w")

    # probe range and the end and check if there is trend of one color increasing despite overall count
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


def cascade_example_insert_range(
    start_range: int = 0,
    end_range: int = 0,
    draws: int = 100,
    b_urn: int = 0.66,
    w_urn: int = 0.34,
):
    coin_toss = random.random()

    # probability of drawing a black ball from the urn
    if coin_toss < 0.5:
        urn_probability = b_urn
    else:
        urn_probability = w_urn

    guesses = []

    for i in range(draws):
        if i > start_range and i < end_range:
            inattentive_agent_draw(urn_probability, guesses)
        else:
            attentive_agent_draw(urn_probability, guesses)

    total_b_count = guesses.count("b")
    total_w_count = guesses.count("w")

    if total_b_count > total_w_count + 1:
        if urn_probability == b_urn:
            return 2
        else:
            return 1

    elif total_w_count > total_b_count + 1:
        if urn_probability == w_urn:
            return 2
        else:
            return 1

    return 0

def run_simulation(times: int, runs: int, method, *arguments):
    stats_set = []
    for i in range(times): #run the simulation multiple times
        stats = {"correct_cascades": 0, "incorrect_cascades": 0, "no_cascades": 0}
        for _ in range(runs):
            result = method(*arguments) #one experiment run

            if result == 2:
                stats["correct_cascades"] += 1
            elif result == 1:
                stats["incorrect_cascades"] += 1
            elif result == 0:
                stats["no_cascades"] += 1
        stats_set.append(stats)

    return stats_set


def save_results(filename: str, stats_set: List[dict]):
    with open(f"results/{filename}.csv", "w") as file:
        file.write("correct_cascades,incorrect_cascades,no_cascades\n")
        for stat in stats_set:
            file.write(
                f"{stat['correct_cascades']},{stat['incorrect_cascades']},{stat['no_cascades']}\n"
            )


def plot_results(results: List[dict], x_axis: List, title : str):
    averages_correct = []
    averages_incorrect = []
    averages_no = []

    for result in results:
        correct_cascades = [stat["correct_cascades"] for stat in result]
        incorrect_cascades = [stat["incorrect_cascades"] for stat in result]
        no_cascades = [stat["no_cascades"] for stat in result]

        averages_correct.append(sum(correct_cascades) / len(correct_cascades))
        averages_incorrect.append(sum(incorrect_cascades) / len(incorrect_cascades))
        averages_no.append(sum(no_cascades) / len(no_cascades))

    x = range(len(averages_correct))

    plt.bar(x, averages_correct, label="Correct Cascades")
    plt.bar(x, averages_incorrect, bottom=averages_correct, label="Incorrect Cascades")
    plt.bar(
        x,
        averages_no,
        bottom=[i + j for i, j in zip(averages_correct, averages_incorrect)],
        label="Broken Cascade or hasn't occurred",
    )

    plt.xlabel("Inattentive Index")
    plt.ylabel("Count")
    plt.title(title)
    plt.legend(loc="lower right")
    plt.xticks(x, x_axis)
    plt.yticks(range(0, 101, 10))
    plt.show()


def main():
    runs = 100

    # test various cyclic inattentive indexes
    inattentive_results = []
    for inattentive_index in [0, 1, 2, 5, 10, 12, 20]:
        result = run_simulation(100, runs, cascade_example, inattentive_index)
        inattentive_results.append(result)

    plot_results(inattentive_results, [0, 1, 2, 5, 10, 12, 20], "Cascade Simulation results for various inattentive indexes")

    # test various ranges of inattentiveness
    ranges_results = []
    for ranges in [
        (0, 10),
        (0, 20),
        (0, 50),
        (0, 90),
        (10, 30),
        (20, 30),
        (10, 50),
        (30, 70),
        (50, 90),
    ]:
        result = run_simulation(
            100, runs, cascade_example_insert_range, ranges[0], ranges[1]
        )
        ranges_results.append(result)

    plot_results(
        ranges_results,
        [
            (0, 10),
            (0, 20),
            (0, 50),
            (0, 90),
            (10, 30),
            (20, 30),
            (10, 50),
            (30, 70),
            (50, 90),
        ],
        "Cascade Simulation results for ranges of inattentiveness",
    )


main()
