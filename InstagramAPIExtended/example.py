from InstagramAPIExtended import InstagramAPIExtended


def main():
    # create and login
    myInstagram = InstagramAPIExtended('username', 'password')
    print(myInstagram.get_status())

    # call api method
    my_followers = []  # myInstagram.get_all_my_followers()
    for follower in my_followers:
        print(follower)

    # access InstagramAPI methods
    myInstagram.InstagramAPI.getPopularFeed()
    feed = myInstagram.InstagramAPI.LastJson
    print(feed)

    # logout
    myInstagram.InstagramAPI.logout()


if __name__ == '__main__':
    main()
