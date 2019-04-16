import json
import requests
import re

INITIAL = 'https://9gag.com/v1/group-posts/group/default/type/hot'
NEXT_CURSOR_IDS = 3
POST_COUNT = 40

def parse_next_cursor(cursor):
    result = re.match(r'after=(([a-zA-Z0-9]+[(%2C)]?)+)', cursor)
    if result:
        code = result.group(1)
        if code:
            ids = re.split('%2C', code)
            return ids

    return None

def get_next_ids(params):
    response = requests.get(INITIAL, params=params)
    response_json = response.json()
    try:
        posts = response_json["data"]["posts"]
        next_cursor = response_json["data"]["nextCursor"]
        print(next_cursor)
        next_cursor_ids = parse_next_cursor(next_cursor)

        if len(next_cursor_ids) != NEXT_CURSOR_IDS:
            print("Length is different from default " + NEXT_CURSOR_IDS)
        
        found_posts = list(filter(lambda post, ids=next_cursor_ids: post['id'] in ids, posts))

        if len(found_posts) != len(next_cursor_ids):
            print("Not all posts found")

        return next_cursor_ids
    except:
        print('Count not parse')
        return None


params = {'c': POST_COUNT}

while True:
    next_ids = get_next_ids(params)
    if next_ids is None:
        break
    print(next_ids)
    params = {'after': ','.join(next_ids), 'c': POST_COUNT}

print('Finished')    
