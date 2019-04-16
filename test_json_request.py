import json
import requests
import re
import os

try:
    os.makedirs("./data")
except:
    print("")

INITIAL = 'https://9gag.com/v1/group-posts/group/default/type/hot'
NEXT_CURSOR_IDS = 3
POST_COUNT = 40
DUMP_COUNT = 100

def parse_next_cursor(cursor):
    result = re.match(r'after=(([a-zA-Z0-9]+[(%2C)]?)+)', cursor)
    if result:
        code = result.group(1)
        if code:
            ids = re.split('%2C', code)
            return ids

    return None

def get_next_data(p):
    response = requests.get(INITIAL, params=p)
    response_json = response.json()
    next_ids = parse_next_ids(response_json)
    next_posts = parse_posts(response_json)

    if next_ids is not None and next_posts is not None:
        return { 'ids': next_ids, 'posts': next_posts}

def parse_posts(response_json):
    try:
        return response_json['data']['posts']        
    except:
        print('Count not parse posts')
        return None

def parse_next_ids(response_json):
    try:
        posts = response_json['data']['posts']
        next_cursor = response_json['data']['nextCursor']
        next_cursor_ids = parse_next_cursor(next_cursor)

        if len(next_cursor_ids) != NEXT_CURSOR_IDS:
            print('Length is different from default ' + NEXT_CURSOR_IDS)
        
        found_posts = list(filter(lambda post, ids=next_cursor_ids: post['id'] in ids, posts))

        if len(found_posts) != len(next_cursor_ids):
            print('Not all posts found')

        return next_cursor_ids
    except:
        print('Count not parse ids')
        return None


params = {'c': POST_COUNT}
current_posts = []
current_iter = 0

while True:
    data = get_next_data(params)
    if data is None:
        break
    print(data['ids'])
    current_posts.extend(data['posts'])
    if len(current_posts) >= DUMP_COUNT:
        current_iter += 1
        print('Iter {}'.format(current_iter))
        
        filename = './data/' + '{:06d}'.format(current_iter) + '.json'
        with open(filename, 'w') as f:
            json.dump(current_posts, f, ensure_ascii=False, sort_keys=True, indent=4)
        current_posts = []

    params = {'after': ','.join(data['ids']), 'c': POST_COUNT}

print('Finished')    
