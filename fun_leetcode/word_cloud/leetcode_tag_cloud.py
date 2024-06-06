import argparse
from collections import defaultdict
import json
from typing import List
import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work_dir", type=str, default='../..', help='The working directory of the project. Default is ..')
    parser.add_argument("--data_name", type=str, default='all_problem.json', help='The data json file name. Default is all_problem.json')
    parser.add_argument("--save_path", type=str, default='tag_freq.png', help='The path to save the tag frequency wordcloud. Default is tag_freq.png')
    args = parser.parse_args()
    return args


def get_data_from(path: str) -> List[dict]:
    with open(path, 'r') as f:
        data = json.load(f)
    
    return data


def get_freq_dict(data: List[dict]) -> dict:
    tag_freq = defaultdict(int)

    for ques in data:
        for tag in ques['topicTags']:
            tag_freq[tag['name']] += 1
            
    total_sum = sum(tag_freq.values())
    tag_freq = {k: v/total_sum for k, v in tag_freq.items()}
    
    return tag_freq


def generate_wordcloud_save(tag_freq: dict, save_path: str):
    wordcloud = WordCloud(width=1600, height=1200, background_color ='white')

    wordcloud.generate_from_frequencies(tag_freq)

    plt.figure(figsize=(8, 6), dpi=500)
    plt.title('Tag Frequency on LeetCode')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(save_path)
    print(f'Tag frequency wordcloud saved as {save_path}')


def main(args):
    data_path = os.path.join(args.work_dir, args.data_name)
    save_path = os.path.join(args.work_dir, args.save_path)
    data = get_data_from(data_path)
    tag_freq = get_freq_dict(data)
    generate_wordcloud_save(tag_freq, save_path)
    return tag_freq


if __name__ == '__main__':
    args = parse_args()
    main(args)
