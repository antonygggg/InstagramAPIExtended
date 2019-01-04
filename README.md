### Description

Instagram API extension methods for useful actions

this version uses [Instagram-API-python](https://github.com/LevPasha/Instagram-API-python)

Python Instagram API as his base, and all of
InstagramAPI methods can be accessed from InstagramAPIExtended


### Installation Instructions

1. Download this repo

    `git clone https://github.com/antonygggg/InstagramAPIExtended.git`


2. Navigate to the directory

    `cd  directory InstagramAPIExtended-master`


3. Install the dependencies

    `pip install -r requirements.txt`


4. Modify [example.py](example.py) with your own username and password


5. Run the [example.py](example.py) script (**use text editor to edit the script and type in valid Instagram username/password**)


### Using API :


##### Create and login :
```
myInstagram = InstagramAPIExtended('username', 'password')
print(myInstagram.get_status())
```

##### Call api method :
```
my_followers = myInstagram.get_all_my_followers()
for follower in my_followers:
    print(follower)
 ```

##### Access InstagramAPI methods :
```
myInstagram.InstagramAPI.getPopularFeed()
feed = myInstagram.InstagramAPI.LastJson
print(feed)
```

##### Logout :
```
myInstagram.InstagramAPI.logout()
```



### Extended API methods :

```
get_all_my_followers(count=None)
get_all_my_following(count=None)
get_all_my_likes(count=None)
get_all_my_posts(count=None)
get_all_user_followers(username, count=None)
get_all_user_following(username, count=None)
get_all_user_posts(username, count=None)
get_my_stories()
get_my_top_followed_users(count=10)
get_status()
get_story(username_id)
get_story_viewers(story_pk)
get_user_by_username(username)
get_user_info_by_usernameId(username)
has_pending_users()
search_query(query)
w_unfollow_user_by_username(username)
w_unfollow_users_from_list(wait_time_seconds=5)
w_unlike_all_my_posts()
```
