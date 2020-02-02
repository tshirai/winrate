#! /usr/bin/env python

"""
Calcurate best picking rate.
Shogi players are required more than 0.65 win rate in 30 matches best picking
to promote from free class to C2.
Then, how many people satisfy the condition, whose win rate is less than 0.65.

Usage:
python best_picking.py
# not implemented.
python best_picking.py --win-rate 0.4 --required-rate 0.65 --matches 30 --trial 200
"""

import math
import random


def show_conditions(win_rate, required_rate, required_win, matches, trial_num):
    print(f'''Conditions:
  Win Rate:      {win_rate}
  Required rate: {required_rate}
  Required wins: {required_win} / {matches}
  Trials:        {trial_num}
''')


def readable_match_results(results):
    # return map(lambda r: '*' if r else '.', results)
    return ''.join(map(lambda r: '*' if r else '.', results))


def show_result(idx, actual_win_rate, satisfied, recent_results):
    results = readable_match_results(recent_results)
    print(f'{str(idx).rjust(4)}: {str(actual_win_rate).ljust(4)} / {results} {"!" if satisfied else ""}')


def main():
    win_rate = 0.5
    # Free class to C2.
    #   more than 0.65 in 30 matches
    # required_rate = 0.65
    # matches = 30

    # Professional test for amateur.
    #   more than 0.65 in 15 matches (10 wins)
    required_rate = 0.65
    matches = 15

    required_win = math.ceil(matches * required_rate)
    trial_num = 2000

    show_conditions(win_rate, required_rate, required_win, matches, trial_num)

    random.seed(0)

    match_results = []
    recent_wins = 0
    satisfied_results = []
    idx = 1
    for i in range(trial_num):
        result = random.random() < win_rate
        match_results.append(result)
        recent_wins += 1 if result else 0
        actual_win_rate = math.floor(100 * recent_wins // idx) / 100
        satisfied = recent_wins >= required_win

        if len(match_results) >= matches and match_results[-matches]:
            recent_wins -= 1
        if satisfied:
            satisfied_results.append(idx)

        show_result(idx, actual_win_rate, satisfied, match_results[-matches:])

        idx += 1

        if satisfied:
            # reset
            match_results = []
            recent_wins = 0
            idx = 1

    print()
    show_conditions(win_rate, required_rate, required_win, matches, trial_num)

    print(f"""Results:
  {len(satisfied_results)} times:
  Number of matches to satisfy:
  {satisfied_results}

  Sorted:
  {sorted(satisfied_results)}
""")



main()
