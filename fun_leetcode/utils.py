from matplotlib import pyplot as plt
import numpy as np
import json

from fun_leetcode.Problem import Problem


def build_problem_list(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        
    problem_list = [None]

    for p in data:
        problem_list.append(Problem(p))

    return problem_list


def top_bottom_tags(problem_list, top_scale=10, save_path='top_bottom_tags.png'):
    
    if problem_list[0] is None:
        problem_list = problem_list[1:]
    
    tag_counts = set(tag for problem in problem_list for tag in problem.tags)
    tag_ac_rates = {tag: [] for tag in tag_counts}
    for problem in problem_list:
        for tag in problem.tags:
            tag_ac_rates[tag].append(problem.ac_rate)

    average_ac_rates = {tag: sum(rates)/len(rates) for tag, rates in tag_ac_rates.items()}

    tags, ac_rates = zip(*sorted(average_ac_rates.items(), key=lambda item: item[1]))
    top_tags = tags[:top_scale]
    bottom_tags = tags[-top_scale:]
    top_rates = ac_rates[:top_scale]
    bottom_rates = ac_rates[-top_scale:]

    combined_tags = list(top_tags) + ['...'] + list(bottom_tags)
    combined_rates = list(top_rates) + [0] + list(bottom_rates)
    colors = plt.cm.viridis(np.linspace(0, 1, len(combined_tags)))

    plt.figure(figsize=(16, 8), dpi=500)
    plt.barh(combined_tags, combined_rates, color=colors)
    plt.xlabel('Average Acceptance Rate')
    plt.title('Top 10 & Last 10 Tags with Highest Average Acceptance Rates')
    plt.savefig(save_path)
    
    
