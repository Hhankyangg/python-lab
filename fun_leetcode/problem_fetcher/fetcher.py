import urllib3
import json

# https://juejin.cn/post/7028127116516392990

# GraphQL query to fetch LeetCode problems
# {
#     "query": "
#         query problemsetQuestionList(
#             $categorySlug: String, 
#             $limit: Int, 
#             $skip: Int, 
#             $filters: QuestionListFilterInput
#         ) {
#             problemsetQuestionList: questionList(
#                 categorySlug: $categorySlug
#                 limit: $limit
#                 skip: $skip
#                 filters: $filters
#             ) {
#                 total: totalNum
#                 questions: data {
#                     acRate
#                     difficulty
#                     freqBar
#                     frontendQuestionId: questionFrontendId
#                     isFavor
#                     paidOnly: isPaidOnly
#                     status
#                     title
#                     titleSlug
#                     topicTags {
#                         name
#                         id
#                         slug
#                     }
#                     hasSolution
#                     hasVideoSolution
#                 }
#             }
#         }
#     ",
#     "variables": {
#         "categorySlug": "",
#         "skip": 0,
#         "limit": 50,
#         "filters": {}
#     },
#     "operationName": "problemsetQuestionList"
# }

def _fetch_problems(skip:int = 0, limit: int = 1):
    """A function to fetch problems info from LeetCode

    Args:
        skip (int, optional): The beginning problem to start fetching. Defaults to 0, means start from the first problem.
        limit (int, optional): Max fetching number. Defaults to 1, means only fetch one problem.

    Raises:
        RuntimeError: Fail to fetch problems! May be 404 error.

    Returns:
        response_content: A dictionary contains the fetched problems info based on the graphql query.
    """
    http = urllib3.PoolManager()


    data = {
        'query': 'query problemsetQuestionList($categorySlug:String,$limit:Int,$skip:Int,$filters:QuestionListFilterInput){problemsetQuestionList:questionList(categorySlug:$categorySlug limit:$limit skip:$skip filters:$filters){total:totalNum questions:data{acRate difficulty freqBar frontendQuestionId:questionFrontendId isFavor paidOnly:isPaidOnly status title titleSlug topicTags{name id slug}hasSolution hasVideoSolution}}}',
        'variables': {
            'categorySlug': '',
            'skip': skip,
            'limit': limit,
            'filters': {},
        },
    }
    encoded_data = json.dumps(data).encode('utf-8')
    r = http.request(
        'POST',
        'https://leetcode.com/graphql/',
        body=encoded_data,
        headers={
            'Content-Type': 'application/json',
        },
    )
    if r.status != 200:
        raise RuntimeError('Fail to fetch problems! status: %d, data: %s' % (r.status, r.data))
    response_content = json.loads(r.data)
    return response_content


def fetch_problem_info_from(num: int):
    """A function to fetch a specific problem info from LeetCode

    Args:
        num (int): The problem number to fetch. Must be a positive integer.

    Returns:
        info (dict): Info dict of the problem.
    """
    if num <= 0:
        raise ValueError('Invalid problem number! Must be a positive integer.')
    info = _fetch_problems(skip = num - 1)['data']['problemsetQuestionList']['questions'][0]
    return info


def fetch_problem_info_list(start: int, end: int):
    """A function to fetch a list of problems info from LeetCode based on [start, end]

    Args:
        start (int): The start problem number to fetch. Must be a positive integer.
        end (int): The end problem number to fetch. Must be a positive integer, and must be greater or equal than start.

    Returns:
        info_list(List[dict]): A list of problems info from start to end (both inclusive).
    """
    if start <= 0 or end <= 0:
        raise ValueError('Invalid problem number! Must be a positive integer.')
    if start > end:
        raise ValueError('Invalid range! Start number must be less than end number.')
    
    info_list = _fetch_problems(skip = start - 1, limit = end - start + 1)['data']['problemsetQuestionList']['questions']
    return info_list


def fetch_all():
    """A function to fetch all problems info from LeetCode

    Returns:
        info_list(List[dict]): A list of all problems info.
    """
    response_temp = _fetch_problems()
    total_count = response_temp['data']['problemsetQuestionList']['total']
    info_list = _fetch_problems(limit=total_count)['data']['problemsetQuestionList']['questions']
    return info_list


def return_problem_link(num: int, locale: str = 'cn'):
    """A function to return the problem link of a specific problem num

    Args:
        num (int): Problem number to fetch. Must be a positive integer.
        locale (str, optional): en or cn. Defaults to 'cn'.

    Returns:
        url: The problem url of the specific problem num.
    """
    if num <= 0:
        raise ValueError('Invalid problem number! Must be a positive integer.')
    if locale not in ['cn', 'en']:
        raise ValueError('Invalid locale! Must be "cn" or "en".')
    postfix = 'cn' if locale == 'cn' else 'com'
    
    problem_name_slug = fetch_problem_info_from(num)['titleSlug']
    url = f'https://leetcode.{postfix}/problems/{problem_name_slug}/'
    return url


# Example dict:
# {
# 'acRate':         52.759501704051125,
# 'difficulty':     'Easy',
# 'freqBar':        None,
# 'frontendQuestionId': '1',
# 'isFavor':        False,
# 'paidOnly':       False,
# 'status':         None,
# 'title':          'Two Sum',
# 'titleSlug':      'two-sum',
# 'topicTags':      [{'name': 'Array', 'id': 'VG9waWNUYWdOb2RlOjU=', 'slug': 'array'},
#                    {'name': 'Hash Table', 'id': 'VG9waWNUYWdOb2RlOjY=', 'slug': 'hash-table'}],
# 'hasSolution':    True,
# 'hasVideoSolution': True
# }

