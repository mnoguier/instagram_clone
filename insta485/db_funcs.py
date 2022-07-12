"""Functions that will grab data from our sql database (db)."""
import flask
import jinja2
import arrow


# Retrieval by username below.
def get_username_fullname_profile_pic(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the username and fullname from sql db.
    It will abort 404, if the user doesn't exist.
    it will return a dictionary {username:'...',fullname:'...'}
    """
    users = connection.execute(
        "SELECT username, fullname, filename AS profile_pic "
        "FROM users "
        "WHERE username == ?",
        (user_url_slug,)).fetchall()
    # the user does not exist in the db, so abort.
    # if len(users) == 0:
    #     flask.abort(404, 'No user exists')
    # change the key for filename to profile_pic
    return users


def get_profile_pic_email_fullname(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the username and fullname from sql db.
    It will abort 404, if the user doesn't exist.
    it will return a dictionary {username:'...',fullname:'...'}
    """
    users = connection.execute(
        "SELECT email, filename AS profile_pic, fullname "
        "FROM users "
        "WHERE username == ?",
        (user_url_slug,)).fetchall()
    # the user does not exist in the db, so abort.
    # if len(users) == 0:
    #     flask.abort(404, 'No user exists')
    # change the key for filename to profile_pic
    return users


def get_username(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the username and fullname from sql db.
    It will abort 404, if the user doesn't exist.
    it will return a dictionary {username:'...'}
    """
    users = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username == ? ",
        (user_url_slug,)).fetchall()
    # the user does not exist in the db, so abort.
    print("Users:", users)
    if len(users) == 0:
        flask.abort(404, 'No user exists')
    return users[0]


def grab_profile_pic(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    profile_pic = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username == ?",
        (user_url_slug,)).fetchall()
    return profile_pic[0]


def get_num_posts(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the number of posts the owner has.
    It will abort 404, if the user doesn't exist.
    it will return a dictionary {posts_by_user:int}
    """
    num_posts = connection.execute(
        "SELECT COUNT(owner) "
        "FROM posts "
        "WHERE owner == ?",
        (user_url_slug,)).fetchall()
    return {"posts_by_user": num_posts[0]['COUNT(owner)']}


def get_posts_postid(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    get all the posts and their ids from the sql db.
    it will return a dictionary {posts:[{filename:'..',postid:'..'}]}
    """
    pics_request = connection.execute(
        "SELECT filename, postid "
        "FROM posts "
        "WHERE owner == ?",
        (user_url_slug,)).fetchall()
    return {'posts': pics_request[:]}


def get_num_followers(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the num of followers for given user_url_slug
    it will return a dictionary {followers:<int>}
    """
    followers = connection.execute(
        "SELECT COUNT(username2)"
        "FROM following "
        "WHERE username2 == ?",
        (user_url_slug,)).fetchall()
    return {"followers": followers[0]['COUNT(username2)']}


def get_num_following(connection, user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets the num of following for given user_url_slug
    it will return a dictionary {following:<int>}
    """
    following = connection.execute(
        "SELECT COUNT(username1)"
        "FROM following "
        "WHERE username1 == ?",
        (user_url_slug,)).fetchall()
    return {"following": following[0]['COUNT(username1)']}


def get_logname_follow_user(connection, logname: str,
                            user_url_slug: str):
    """
    Pydocstyle summary satisfaction.

    gets if logname follows the user.
    it will return a dictionary {logname_follows_username:<bool>}
    """
    logname_follows_username = connection.execute(
        "SELECT COUNT(username1)"
        "FROM following "
        "WHERE username1 == ? and username2 == ?",
        (logname, user_url_slug, )).fetchall()
    if logname_follows_username[0]['COUNT(username1)']:
        return {"logname_follows_username": True}
    return {"logname_follows_username": False}


def has_user_liked_post(connection, logname: str, postid: int):
    """
    Pydocstyle summary satisfaction.

    gets if user has liked the post yet.
    it will return a dictionary {user_likes_post:<bool>}
    """
    user_likes_post = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner == ? and postid == ?",
        (logname, postid, )).fetchall()
    if len(user_likes_post) == 0:
        return {"user_likes_post": False}
    return {"user_likes_post": True}


def check_comments(connection, commentid: int):
    """
    Pydocstyle summary satisfaction.

    gets if user has liked the post yet.
    it will return a dictionary {user_likes_post:<bool>}
    """
    user_made_comment = connection.execute(
        "SELECT text "
        "FROM comments "
        "WHERE commentid == ? ",
        (commentid, )).fetchall()
    if len(user_made_comment) == 0:
        return {'user_made_comment': False}
    return {'user_made_comment': True}


def get_password(connection, username: str):
    """
    Pydocstyle summary satisfaction.

    retrieves a user's hashed password.
    """
    password = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username == ?",
        (username, )).fetchall()
    # user does not exist

    if len(password) == 0 or not password[0].get('password', False):
        flask.abort(403, 'User does not exist.')
    return password[0]['password']


# Retrieval by post id below.
def get_filename_owner_created(connection, postid: int):
    """
    Pydocstyle summary satisfaction.

    gets filename and owner when given a postid.
    it will return a dictionary {following:<int>}
    """
    filename_owner_created = connection.execute(
        "SELECT owner, filename, created "
        "FROM posts "
        "WHERE postid == ?",
        (postid,)).fetchall()
    # make the time user readable
    humanized_time = arrow.get(filename_owner_created[0]['created'])
    humanized_time = humanized_time.humanize()
    filename_owner_created[0]['created'] = humanized_time
    # also grabs profile picture
    profile_pic = connection.execute(
        "SELECT filename as ownerImgUrl "
        "FROM users "
        "WHERE username == ?",
        (filename_owner_created[0]['owner'],)).fetchall()
    # change the key for filename to profile_pic
    profile_pic[0]['profile_pic'] = profile_pic[0]['ownerImgUrl']
    profile_pic[0].pop('ownerImgUrl')
    filename_owner_created[0].update(profile_pic[0])
    return filename_owner_created[0]


def get_comments_owner_created_id(connection, postid: int):
    """
    Pydocstyle summary satisfaction.

    gets comments and owner when given a postid.
    it will return a dictionary {comments:<comment>}
    """
    comments = connection.execute(
        "SELECT owner, created, commentid, text "
        "FROM comments "
        "WHERE postid == ?",
        (postid, )).fetchall()
    # if there are no comments.
    if len(comments) == 0:
        return {}
    return {'comments': comments}


def get_likes(connection, postid: int):
    """
    Pydocstyle summary satisfaction.

    gets num of likes when given a postid.
    it will return a dictionary {following:<int>}
    """
    likes = connection.execute(
        "SELECT COUNT(likeid)"
        "FROM likes "
        "WHERE postid == ?",
        (postid,)).fetchall()
    # if there are no comments.
    if len(likes) == 0:
        return {'likes': 0}
    return {'likes': likes[0]['COUNT(likeid)']}


# access control below.
def requested_user_equal_logname(requested_user: str, logname: str) -> None:
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    if requested_user == logname:
        return
    flask.abort(403)


# Jinja2 below.
def render_template(json_dict: dict, template_name: str):
    """
    Pydocstyle summary satisfaction.

    renders a template and returns it.
    """
    template_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str('insta485/templates')),
                autoescape=jinja2.select_autoescape(['html', 'xml']),
            )
    # Grab the template from the template folder. Render it and return it.
    template = template_env.get_template(str(template_name))
    rendered_template = template.render(json_dict)
    return rendered_template
