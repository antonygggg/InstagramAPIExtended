
'''

Instagram API extension methods for useful actions

this version uses https://github.com/LevPasha/Instagram-API-python

Python Instagram API as his base


this is a unofficial beta version
which is still in development
and comes as is

'''


class InstagramAPIExtended:
    from InstagramAPI import InstagramAPI
    import csv
    import time
    import json

    version = 'InstagramAPIExtended 0.0.7 beta https://i.instagram.com/api/v1/'

    def __init__(self, username, password, auto_login=True):
        self.__un = ''
        self.__pw = ''
        self.users_to_unfollow = self.__get_list('users_to_unfollow.txt')
        self.users_to_search = self.__get_list('list.txt')
        self.__api = None
        self.InstagramAPI = None

        # self.__get_api_methods_list()

        try:
            self.__api = InstagramAPI(self.__un, self.__pw)
            self.InstagramAPI = self.__api
            if not self.__api.isLoggedIn and auto_login:
                self.__api.login()
        except Exception as e:
            print(str(e))
            raise

    def __str__(self):
        o = {
            'un': self.__un,
            'pw': self.__pw,
            'api.isLoggedIn': self.__api.isLoggedIn
        }
        return json.dumps(o)

    def get_status(self):
        return str(self)

    def get_story_viewers(self, story_pk):
        pass

    def get_my_stories(self):
        # self.__api.
        return self.get_story(self.__api.username_id)

    def get_story(self, username_id):
        self.__run(self.__api.getStory, username_id)
        stories = self.__api.LastJson
        return stories

    def has_pending_users(self):
        self.__run(self.__api.getPendingFollowRequests)
        has_pending = self.__api.LastJson
        return has_pending

    def w_unfollow_user_by_username(self, username):
        pass

    def search_query(self, query):
        self.__run(self.__api.searchUsers, query)
        users = self.__api.LastJson
        return users

    def get_user_by_username(self, username):
        self.__run(self.__api.searchUsername, username)
        user = self.__api.LastJson
        return user

    def get_user_info_by_usernameId(self, username):
        self.__run(self.__api.getUsernameInfo, username)
        user_info = self.__api.LastJson
        return user_info

    def get_all_my_likes(self, count=None):
        more_like = True
        next_max_id = ''
        likes_count = 0
        items = []
        while more_like and (count is None or likes_count <= count):
            self.__run(self.__api.getLikedMedia, next_max_id)
            res = self.__api.LastJson
            more_like = res['more_available']
            if more_like:
                next_max_id = res['next_max_id']
            items.extend(res['items'])
            likes_count += len(res['items'])
        return items

    def get_all_my_posts(self, count=None):
        return self.get_all_user_posts(self.__api.username_id, count)

    def get_all_user_posts(self, username, count=None):
        more = True
        next_max_id = ''
        items_count = 0
        items = []
        while more and (count is None or items_count <= count):
            self.__run(self.__api.getUserFeed, {
                'usernameId': username, 'maxid': next_max_id})
            res = self.__api.LastJson
            more = res['more_available']
            if more:
                next_max_id = res['next_max_id']
            items.extend(res['items'])
            items_count += len(res['items'])
        return items

    def get_my_top_followed_users(self, count=10):
        wait_time = 2
        wait_round = 20
        users = self.get_all_my_followers()
        users_info = []
        for i, user in enumerate(users):
            if i % wait_round == 0:
                time.sleep(wait_time)
            self.__write_log(str(i + 1) + '/' + str(len(users)) +
                             ' \'' + user['username'] + '\'')
            temp_user = self.get_user_by_username(user['username'])
            if 'user' in temp_user:
                users_info.append(temp_user['user'])
        top_users = (users_info.sort(
            key=lambda u: u['follower_count'], reverse=True))[:count]
        return top_users

    def get_all_my_followers(self, count=None):
        return self.get_all_user_followers(self.__api.username_id, count)

    def get_all_user_followers(self, username, count=None):
        next_max_id = ''
        first_time = True
        items_count = 0
        items = []
        while (
            (first_time or next_max_id) and
            (count is None or items_count <= count)
        ):

            first_time = False
            self.__run(self.__api.getUserFollowers, {
                'usernameId': username, 'maxid': next_max_id})
            res = self.__api.LastJson
            if 'next_max_id' in res:
                next_max_id = res['next_max_id']
            else:
                next_max_id = ''
            items.extend(res['users'])
            items_count += len(res['users'])
        return items

    def get_all_my_following(self, count=None):
        return self.get_all_user_following(self.__api.username_id, count)

    def get_all_user_following(self, username, count=None):
        next_max_id = ''
        first_time = True
        items_count = 0
        items = []
        while (
            (first_time or next_max_id) and
            (count is None or items_count <= count)
        ):

            first_time = False
            self.__run(self.__api.getUserFollowings, {
                'usernameId': username, 'maxid': next_max_id})
            res = self.__api.LastJson
            if 'next_max_id' in res:
                next_max_id = res['next_max_id']
            else:
                next_max_id = ''
            items.extend(res['users'])
            items_count += len(res['users'])
        return items

    def w_unlike_all_my_posts(self):
        my_posts = self.get_all_my_posts()
        unliked_list = []
        for post in my_posts:
            if post and post['has_liked']:
                self.__api.unlike(post['id'])
                unliked_list.append(post)
        return unliked_list

    def w_unfollow_users_from_list(self, wait_time_seconds=5):
        user_to_unfollow = self.__get_list('users_to_unfollow.txt')
        unfollowed_users = []
        for i, username in enumerate(user_to_unfollow):
            user = self.get_user_by_username(username)
            if 'user' in user:
                user = user['user']
                if self.__run(self.__api.unfollow, user['pk']):
                    unfollowed_users.append(user)
                    self.__write_log(
                        str(i + 1) + '/' + str(len(user_to_unfollow)) +
                        ' \'' + user['username'] + '\' unfollowed')
        time.sleep(wait_time_seconds)
        self.__write_log(str(len(unfollowed_users)) + ' of ' +
                         str(len(user_to_unfollow)) + ' were unfollowed')
        return unfollowed_users

    def __print_result(self, res):
        if res is None:
            self.__write_log('res is None')
            return
        self.__write_log('length = ' + str(len(res)))
        for item in res:
            self.__write_log(item)

    def __run(self, function_run, parameters=None,
              wait_on_exception_seconds=10):
        try:
            res = False
            if parameters is None:
                res = function_run()
            elif type(parameters) is dict:
                res = function_run(**parameters)
            else:
                res = function_run(parameters)
            if not res:
                raise Exception('Error in running ' + str(function_run) +
                                ' with parameters ' + str(parameters))
            return res
        except Exception as e:
            print(self.__time_f() + ' - ' + str(e))
            if wait_on_exception_seconds > 0:
                print(self.__time_f() + ' - Waiting ' +
                      str(wait_on_exception_seconds) + ' seconds')
                time.sleep(wait_on_exception_seconds)

    def __time_f(self):
        return time.strftime('%H:%M:%S')

    def __get_function_display(self, func_name, func_args):
        call_args = ''
        if(func_args and len(func_args) > 1):
            func_args = [arg for arg in func_args if arg != 'self']
            for arg in func_args[0:-1]:
                if arg != 'self':
                    call_args = arg + ', '
            call_args = call_args + func_args[-1]
        return '{}({})'.format(func_name, call_args)

    def __get_api_methods_list(self):
        import re
        import inspect

        for d in dir(self):
            dm = getattr(self, d)
            if (inspect.ismethod(dm) and
                    re.match('^[a-zA-Z0-9][a-zA-Z0-9_]*$', d)):
                ms = inspect.signature(dm)
                print(d+str(ms))

    def __write_log(self, message):
        print(message)

    def __get_list(self, filename):
        from pathlib import Path

        dir_lists = 'lists'
        list_res = []

        script_location = Path(__file__).absolute().parent
        file_location = str(script_location) + '\\' + \
            dir_lists + '\\' + filename

        if file_location.endswith('csv'):
            try:
                with open(file_location) as csvfile:
                    readcsv = csv.reader(csvfile, delimiter=',')
                    for line in readcsv:
                        if line:
                            line = line.strip().replace(',', '')
                            if line:
                                list_res.append(line)
                return list_res
            except Exception as e:
                self.__write_log(str(e))
                return None
        else:
            try:
                with open(file_location) as fc:
                    for line in fc:
                        if line:
                            line = line.strip().replace(',', '')
                            if line:
                                list_res.append(line)
                return list_res
            except Exception as e:
                self.__write_log(str(e))
                return None


if __name__ == '__main__':
    myInstagram = InstagramAPIExtended('username', 'password')
    print(myInstagram.get_status())
    my_followers = myInstagram.get_all_my_followers()
    myInstagram.InstagramAPI.logout()
