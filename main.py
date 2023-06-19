import requests

cookie = '' # Your .ROBLOSECURITY cookie
robloxId = 123456789 # Your Roblox Id

session = requests.Session()
session.cookies['.ROBLOSECURITY'] = cookie

response = session.post('https://friends.roblox.com/v1/users/1/unfollow')
session.headers['x-csrf-token'] = response.headers['x-csrf-token']

def unfollow_user(user_id):
    return session.post(f'https://friends.roblox.com/v1/users/{user_id}/unfollow')

while True:
    count_response = requests.get(f'https://friends.roblox.com/v1/users/{robloxId}/followings/count')
    count = count_response.json()['count']
    
    if count == 0:
        break
    
    following_response = requests.get(f'https://friends.roblox.com/v1/users/{robloxId}/followings?limit=100&sortOrder=Asc', headers=session.headers, cookies=session.cookies)
    following = following_response.json()['data']
    
    for user in following:
        userId = user['id']
        username_response = requests.get(f'https://friends.roblox.com/v1/metadata?targetUserId={userId}')
        username = username_response.json()['userName']
        
        print(f'Unfollowed: {username}')
        unfollow_user(userId)
    
    nextpagecursor = following_response.json()['nextPageCursor']
    following_response = requests.get(f'https://friends.roblox.com/v1/users/{robloxId}/followings?limit=100&sortOrder=Asc&cursor={nextpagecursor}', headers=session.headers, cookies=session.cookies)
    
