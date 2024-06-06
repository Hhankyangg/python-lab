import argparse
from fetcher import fetch_all
import json
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work_dir", type=str, default='..', help='The working directory of the project. Default is ..')
    parser.add_argument("--name", type=str, default='all_problems', help='The name of the file to save the fetched problems info. Default is all_problems')
    args = parser.parse_args()
    return args


def main(args):
    response_content = fetch_all()
    print(f'All {len(response_content)} problems fetched.')
    
    json_path = os.path.join(args.work_dir, f'{args.name}.json')
    with open(json_path, 'w') as f:
        f.write(json.dumps(response_content))
        print(f'All {len(response_content)} problems info saved into json_path file.')
        
        
if __name__ == '__main__':
    args = parse_args()
    main(args)
    