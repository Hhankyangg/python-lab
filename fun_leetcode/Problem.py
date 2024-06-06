

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

class Problem:
    
    def __init__(self, info: dict):
        self.title = info['title']
        self.ac_rate = float(info['acRate'])
        self.difficulty = info['difficulty']
        self.id = int(info['frontendQuestionId'])
        self.tags = [tag['name'] for tag in info['topicTags']]
         