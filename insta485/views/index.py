"""
summary.

Insta485 index (main) view.
URLs include:
/
"""
from copy import deepcopy
import datetime
import pathlib
# from re import U
import uuid
import os
# from urllib.parse import urlencode
import flask
# import requests
# import arrow
import insta485
from insta485 import db_funcs
from insta485 import safety_checks
from insta485.config import UPLOAD_FOLDER


# ONTO COOKIE IN create()


@insta485.app.route("/", methods=['GET'])
def show_index():
    """
    Pydocstyle summary.

    Display / route.
    """
    # need to be logged in
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])

    user = flask.session['username']
    # Connect to database

    # Query database
    logname = user

    # Set the user in the dictionary
    context = {'logname': logname}
    # '''
    # cur = connection.execute(
    #     " SELECT posts.*, users.filename AS owner_img_url "
    #     " FROM posts "
    #     " INNER JOIN users ON posts.owner == users.username "
    #     " WHERE users.username IN ( SELECT username2 "
    #     " FROM following "
    #     " INNER JOIN users ON following.username1 == users.username "
    #     "WHERE users.username == ?) "
    #     " OR users.username = ? "
    #     " ORDER BY created DESC ",
    #     (logname, logname, )
    # )

    # usrposts = cur.fetchall()
    # pos = {"posts": usrposts}

    # for post in pos['posts']:
    #     post['created'] = arrow.get(post['created']).humanize()
    #     # print("Post:", post)
    #     cur = connection.execute(
    #         " SELECT comments.* "
    #         " FROM comments "
    #         " INNER JOIN posts ON comments.postid == posts.postid "
    #         " WHERE posts.postid = ? ",
    #         (post['postid'], )
    #     )
    #     comment = cur.fetchall()
    #     com = {"comments": comment}
    #     post.update(com)

    #     cur = connection.execute(
    #         " SELECT likes.owner, COUNT(likes.likeid) as lk "
    #         " FROM likes "
    #         " INNER JOIN posts ON likes.postid == posts.postid "
    #         " WHERE posts.postid = ? ",
    #         (post['postid'], )
    #     )
    #     like = cur.fetchall()
    #     user_likes_p = db_funcs.has_user_liked_post(
    #         connection, logname, post['postid'])
    #     likes = {"likes": like}
    #     post.update(likes)
    #     post.update(user_likes_p)
    # # Add database info to context
    # # print("p: ", pos)
    # # for post in pos['posts']:
    # #     for like in post['likes']:
    # #         print("POST: ", like['lk'])
    # context.update(pos)
    # # print("CONTEXT ")
    # # print(context)
    # # print('User: ', context['user'])
    # # Query databse for posts, likes, and comments related to username
    # # Edit html to diplay everything properly
    # '''
    insta485.model.close_db(False)
    print('THIS IS THE CONTEXT\n\n\n\n', context)
    return flask.render_template("index.html", context=context)
    # db_funcs.render_template(context, "index.html")


# Ethan's Functions are below
@insta485.app.route('/users/<user_url_slug>/', methods=["GET"])
def get_user(user_url_slug: str):
    """
    Pydocstyle summary.

    Gets the user information from the database. Once the function has the
    info, it will create a custom user.html and return it.
    """
    # need to be logged in
    logname = safety_checks.check_login_status(flask.session)

    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user exists
    db_funcs.get_username(connection, user_url_slug)
    # insta485.model.close_db(False)

    jinja_dict = {'logname': logname}

    # Connect to the DB.
    connection = insta485.model.get_db()
    # get username, fullname. This checks if the user exists, if not abort 404
    ufd = db_funcs.get_username_fullname_profile_pic(connection,
                                                     user_url_slug)
    jinja_dict.update(ufd[0])

    # grab pictures, postid from database
    pics_request = db_funcs.get_posts_postid(connection, user_url_slug)
    jinja_dict.update(pics_request)

    # grab num of posts
    num_posts_by_user = db_funcs.get_num_posts(connection, user_url_slug)
    jinja_dict.update(num_posts_by_user)

    # grab num of followers
    followers = db_funcs.get_num_followers(connection, user_url_slug)
    jinja_dict.update(followers)

    # grab num of following
    follow = db_funcs.get_num_following(connection, user_url_slug)
    jinja_dict.update(follow)

    # grab if logname_follows_username
    logname_following = db_funcs.get_logname_follow_user(connection, logname,
                                                         user_url_slug)
    jinja_dict.update(logname_following)
    # Close the DB connection with False error status.
    insta485.model.close_db(False)

    # Render a template using jinja2 and return it to the user.
    return db_funcs.render_template(jinja_dict, "user.html")


@insta485.app.route('/posts/<postid_url_slug>/', methods=["GET"])
def get_post_static(postid_url_slug: str):
    """
    Pydocstyle summary.

    Gets the user information from the database. Once the function has the
    info, it will create a custom user.html and return it.
    """
    postid = postid_url_slug
    # need to be logged in
    logname = safety_checks.check_login_status(flask.session)

    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    # insta485.model.close_db(False)
    # dictionary we will use to render jinja.
    jinja_dict = {'logname': logname, 'postid': postid}

    # Connect to the DB.
    connection = insta485.model.get_db()

    file = db_funcs.get_filename_owner_created(connection, postid)
    jinja_dict.update(file)

    comment_info = db_funcs.get_comments_owner_created_id(connection, postid)
    jinja_dict.update(comment_info)

    user_likes_p = db_funcs.has_user_liked_post(connection, logname, postid)
    jinja_dict.update(user_likes_p)

    like_info = db_funcs.get_likes(connection, postid)
    jinja_dict.update(like_info)

    # Close the DB connection with False error status.
    insta485.model.close_db(False)

    # Render a template using jinja2 and return it to the user.
    return db_funcs.render_template(jinja_dict, "post.html")


@insta485.app.route('/accounts/password/', methods=["GET"])
def get_accounts_password():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    insta485.model.close_db(False)

    # dictionary we will use to render jinja.
    jinja_dict = {'logname': logname}
    return db_funcs.render_template(jinja_dict, "password.html")


@insta485.app.route('/users/<user_url_slug>/following/', methods=["GET"])
def get_user_following(user_url_slug):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # check login status. If not logged in then redirect
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user exists
    db_funcs.get_username(connection, user_url_slug)
    # # check if the user exists
    # user = connection.execute(
    #     "SELECT username "
    #     "FROM users "
    #     "WHERE username == ?",
    #     (user_url_slug,)).fetchall()
    # if len(user) == 0:
    #     flask.abort(404, "User not found")
    # Connect to database
    jinja_dict = {'logname': logname, 'following': [], 'owner': user_url_slug}
    # get following
    follow = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (user_url_slug,)).fetchall()
    for pair in follow:
        filename = db_funcs.grab_profile_pic(connection, pair['username2'])
        pair['profile_pic'] = filename['filename']
        logname_f = db_funcs.get_logname_follow_user(connection,
                                                     logname,
                                                     pair['username2'])
        pair['logname_follows'] = logname_f['logname_follows_username']
        jinja_dict['following'].append(pair)

    # define our dictionary that we will pass into jinja renderer
    return db_funcs.render_template(jinja_dict, "following.html")


@insta485.app.route('/users/<user_url_slug>/followers/', methods=["GET"])
def get_user_followers(user_url_slug):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # check login status. If not logged in then redirect
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")

    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, user_url_slug)

    jinja_dict = {'logname': logname, 'following': [], 'owner': user_url_slug}
    # get following
    follow = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 == ?",
        (user_url_slug,)).fetchall()
    for pair in follow:
        filename = db_funcs.grab_profile_pic(connection, pair['username1'])
        logname_f = db_funcs.get_logname_follow_user(connection,
                                                     logname,
                                                     pair['username1'])
        pair['logname_follows'] = logname_f['logname_follows_username']
        pair['profile_pic'] = filename['filename']
        jinja_dict['following'].append(pair)

    # define our dictionary that we will pass into jinja renderer
    return db_funcs.render_template(jinja_dict, "followers.html")


@insta485.app.route('/likes/', methods=["POST"])
def post_likes():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])

    # now get all queries from the POST
    args = flask.request.args
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    vals = flask.request.form
    operation = vals['operation']
    postid = vals['postid']
    # dictionary we will use to render jinja.
    created = datetime.datetime.now()
    user_like = db_funcs.has_user_liked_post(connection, logname, postid)
    user_like = user_like['user_likes_post']
    if operation == "like" and user_like is False:
        connection.execute(
            "INSERT INTO likes (owner, postid, created) "
            "VALUES (?, ?, ?);",
                          (logname, postid, created, ))
    elif operation == 'unlike' and user_like:
        connection.execute(
            "DELETE FROM likes "
            "WHERE postid == ? and owner == ?;",
                          (postid, logname,))
    # probably was a malicious attempt
    else:
        flask.abort(409)
    # now redirect the user to their designated target.
    insta485.model.close_db(False)
    return flask.redirect(target, code=302)


@insta485.app.route('/following/', methods=["POST"])
def post_following():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])

    args = flask.request.args
    vals = flask.request.form
    operation = vals.get('operation')
    user = vals.get('username')

    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    user_follow = db_funcs.get_logname_follow_user(connection, logname, user)
    user_follow = user_follow["logname_follows_username"]
    if logname == user:
        flask.abort(403, 'Cannot unfollow yourself.')

    elif operation == 'follow' and not user_follow:
        print("username1: ", logname, "username2", user)
        connection.execute(" INSERT INTO following(username1, username2) "
                           " VALUES (?, ? ) ",
                           (logname, user,))
    elif operation == 'unfollow' and user_follow:
        connection.execute(
            "DELETE FROM following "
            "WHERE username1 == ? and username2 == ?;",
            (logname, user,))
    # probably was a malicious attempt
    elif (operation ==
          'unfollow' and not user_follow) or (operation
                                              == 'follow' and user_follow):
        flask.abort(409, 'Malicious Attempt. post_following().')
    # now redirect the user to their designated target.
    insta485.model.close_db(False)
    return flask.redirect(target, code=302)


# need to add login and redirect to url
def create(user_request: flask.request):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # connect to the database
    connection = insta485.model.get_db()
    # now get all queries from the POST
    # args = user_request.args
    # target = '/'
    # if len(args.getlist('target')) == 0:
    #     target = "/users/" + flask.session['username'] + "/"
    vals = user_request.form
    args = flask.request.args
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    hashed_password = safety_checks.hash_password(vals.get('password'),
                                                  'sha512', '', False)
    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    # if anything is empty abort 400
    if not(filename and vals.get('email', False) and
           vals.get('fullname', False) and
           vals.get('password', False) and vals.get('username', False)):
        print('line 440')
        flask.abort(400)

    # now check if the user is creating an account with username
    # that already exists
    username = db_funcs.get_username_fullname_profile_pic(connection,
                                                          vals.get('username')
                                                          )
    if username:
        flask.abort(409, 'Existing username')

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that the
    # name is compatible with the filesystem.
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.filename = uuid_basename
    fileobj.save(path)
    print("path:", path, "filename: ", fileobj.filename)
    # Upload user data and coehere to file upload and naming procedure
    connection.execute(
        "INSERT INTO users (username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?) ",
        (vals.get('username'), vals.get('fullname'), vals.get('email'),
         fileobj.filename, hashed_password))
    # Close the connection to the db.
    insta485.model.close_db(False)
    flask.session['username'] = vals.get('username')
    return target


def update_password(user_request: flask.request):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # make sure the user is logged in. If not abort(403)
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    args = user_request.args
    # see if target is given. If not redirect to '/'
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    vals = user_request.form
    user = flask.session['username']
    new_password1 = vals.get('new_password1', False)
    new_password2 = vals.get('new_password2', False)

    # if anything is empty, abort(400)
    if not (vals.get('password', False) and new_password1 and new_password2):
        print('line 521')
        flask.abort(400, "Empty Field")

    # make sure both new passwords match, if not abort(401)
    if new_password1 != new_password2:
        flask.abort(401)
    # get the hashed password, break it up into encryption scheme,salt,passwrd
    db_password = db_funcs.get_password(connection, user).split('$')

    # hashing algo used.
    algo = db_password[0].strip()
    # salt we used on the password
    salt = db_password[1].strip()
    # the current hashed password in the db
    current_db_password = db_password[2].strip()
    # hash the check password they gave us and compare to current one in db
    check_password = safety_checks.hash_password(vals.get('password'), algo,
                                                 salt, False)
    check_password = check_password.split('$')[2]
    if current_db_password != check_password:
        flask.abort(403)
    # they match so create a new password
    hashed_new = safety_checks.hash_password(new_password1, algo, '', True)

    # Now update the db with the new password and salt
    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username = ? ;",
        (hashed_new, user,))

    # now redirect the user to their designated target.
    insta485.model.close_db(False)
    return target


@insta485.app.route('/accounts/edit/', methods=['GET'])
def edit_account():
    """
    Pydocstyle summary.

    Login function
    """
    # make sure the user is logged in. If not abort(403)
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    pfp = db_funcs.get_profile_pic_email_fullname(connection,
                                                  flask.session['username'])
    insta485.model.close_db(False)
    context = {'logname': logname,
               'profile_pic': pfp}
    print("Context: ", context)
    return db_funcs.render_template(context, "edit.html")


@insta485.app.route('/accounts/delete/', methods=['GET'])
def delete_account():
    """
    Pydocstyle summary.

    Login function
    """
    print('In delete')
    # make sure the user is logged in. If not abort(403)
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    insta485.model.close_db(False)
    return db_funcs.render_template({'logname': logname}, "delete.html")
# End of Ethan's Functions
# Nick's Functions are below


@insta485.app.route('/accounts/login/', methods=['GET'])
def login():
    """
    Pydocstyle summary.

    Login function
    """
    logname = safety_checks.check_login_status(flask.session)
    if logname:
        return flask.redirect("/")
    return flask.render_template("login.html")


def post_login(user_request: flask.request):
    """
    Pydocstyle summary satisfaction.

    Login function handling POST request
    """
    print("DEBUG Login:", flask.request.form['username'])
    vals = user_request.form
    username = vals.get('username', False)
    password = vals.get('password', False)
    # if anything is empty, abort(400)
    if not username and not password:
        print('line 628')
        flask.abort(400, "No username")
    if not password:
        print('line 628')
        flask.abort(400, "No password")
    # Connect to database
    connection = insta485.model.get_db()
    # get the algo used, salt, and hashed password of user in db
    algo = db_funcs.get_password(connection, username).split('$')[0]
    salt = db_funcs.get_password(connection, username).split('$')[1]
    passwd = db_funcs.get_password(connection, username).split('$')[2]
    givenpwd = safety_checks.hash_password(password, algo, salt, False)
    # Close connection to db
    insta485.model.close_db(False)
    # Check if username (implicit check)
    # and password (explicit check) are valid
    if passwd == givenpwd.split('$')[2]:
        # GET url, set cookie and redirect to URL
        args = flask.request.args
        flask.session['username'] = username
        target = '/'
        if len(args.getlist('target')) != 0:
            target = args.getlist('target')[0]
        return target
    # Username and password authentication fails
    flask.abort(403)
    return "Junk"


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """
    Pydocstyle summary.

    Logout function
    """
    print("DEBUG Logout:", flask.session['username'])
    flask.session.clear()
    return flask.redirect("/accounts/login/")


@insta485.app.route("/accounts/create/", methods=['GET'])
def create_account():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    logname = safety_checks.check_login_status(flask.session)
    if logname:
        return flask.redirect("/accounts/edit/")
    return flask.render_template("create.html")


@insta485.app.route('/posts/', methods=['POST'])
def posts():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # Check if user is logged in. If not, send to login page
    # If not redirect to /accounts/login/
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    # Check if ?target is set
    # If not redirect to /users/<logname>/
    args = flask.request.args
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    else:
        target = "/users/" + flask.session['username'] + "/"
    # Get operation and and postid vals from POST response from content
    # Get URL and set it
    operation = flask.request.form['operation']
    # Create or delete posts
    if operation == "create":
        print("DEBUG post create:")
        # Check if file is empty.
        # If empty. abort 400
        file = flask.request.files['file']
        if file.filename == '':
            flask.abort(400, "No file uploaded")
        # Compute Filename and safe file to disk
        # Unpack flask object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        # Create Post. SQL to add post to posts table
        connection.execute(
            "INSERT INTO posts (filename, owner) "
            "VALUES (?, ?);",
            (uuid_basename, flask.session['username']))
        insta485.model.close_db(False)
        return flask.redirect(target, code=302)
    if operation == "delete":
        postid = flask.request.form['postid']
        print("DEBUG post delete: postid", postid)
        post_owner = connection.execute(
            " SELECT owner "
            " FROM posts "
            " WHERE postid = ? ;",
            (postid,)).fetchall()
        if post_owner[0]['owner'] != flask.session['username']:
            flask.abort(403, 'Not your post')
        # Get filename from db and then delete it from uploads
        file_name = connection.execute(
            " SELECT filename "
            " FROM posts "
            " WHERE postid = ? ",
            (postid,)).fetchall()
        path = insta485.app.config["UPLOAD_FOLDER"]/file_name[0]['filename']
        os.remove(path)
        # Delete everything in db related to post.
        connection.execute(
            " DELETE "
            " FROM posts "
            " WHERE postid = ? ;",
            (postid,)).fetchall()
        insta485.model.close_db(False)
        # Redirect to URL
        return flask.redirect(target, code=302)
    insta485.model.close_db(False)
    return flask.redirect(target, code=302)


@insta485.app.route('/explore/', methods=["GET"])
def explore():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # check login status. If not logged in then redirect
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/")
    # connect to the db.
    connection = insta485.model.get_db()
    curr = connection.execute(
        " SELECT username, filename AS profile_pic "
        " FROM users "
        # " INNER JOIN following ON users.username == following.username1 "
        " WHERE users.username NOT IN ( SELECT username2 "
        " FROM following "
        " WHERE username1 == ?) "
        " AND users.username != ?",
        (logname, logname)).fetchall()
    jinja_dict = {'logname': logname}
    cur = {'users': curr}
    jinja_dict.update(cur)
    print("Jinja_dict ", jinja_dict)
    return db_funcs.render_template(jinja_dict, "explore.html")


@insta485.app.route('/comments/', methods=['POST'])
def post_comments():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # connect to the database
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        return flask.redirect("/accounts/login/", code=302)
    connection = insta485.model.get_db()
    # now get all queries from the POST
    args = flask.request.args
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    vals = flask.request.form
    operation = vals.get('operation')
    commentid = vals.get('commentid')
    text = vals.get('text')
    postid = vals.get('postid')
    user_comment = db_funcs.check_comments(connection, commentid)
    user_comment = user_comment['user_made_comment']
    if operation == 'create':
        if not text:
            flask.abort(400, "Comment must have text")
        connection.execute(
            " INSERT INTO comments(owner, postid, text) "
            " VALUES(?, ?, ?);", (logname, postid, text,)
        )
    elif operation == 'delete' and user_comment:
        connection.execute(
            " DELETE "
            " FROM comments "
            " WHERE commentid == ? and owner == ?",
            (commentid, logname,)
        )
    else:
        flask.abort(403, "Cannot delete comment. You do not own it")
    insta485.model.close_db(False)
    return flask.redirect(target, code=302)


def post_delete(user_request: flask.request):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    # check login status. If not logged in then redirect
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        flask.abort(403)
    # Connect to database
    connection = insta485.model.get_db()
    # Check if user exists
    db_funcs.get_username(connection, flask.session['username'])
    args = user_request.args
    target = '/'
    if len(args.getlist('target')) != 0:
        target = args.getlist('target')[0]
    # Delete user profile pic
    file_name = connection.execute(
        " SELECT filename "
        " FROM users "
        " WHERE username = ? ",
        (logname,)).fetchall()
    print("filename", file_name[0]['filename'])
    path = insta485.app.config["UPLOAD_FOLDER"]/file_name[0]['filename']
    print("Path: ", path)
    os.remove(path)
    # Delete users posts pictures
    file_name = connection.execute(
        " SELECT filename "
        " FROM posts "
        " WHERE owner = ? ",
        (logname,)).fetchall()
    for file in file_name:
        print("file: ", file)
        path = insta485.app.config["UPLOAD_FOLDER"] / \
            file['filename']
        os.remove(path)
    # Delete user
    connection.execute(
        " DELETE "
        " FROM users "
        " WHERE username = ? ",
        (logname,))
    insta485.model.close_db(False)
    flask.session.clear()
    return target


def post_edit_account(user_request: flask.request):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    print('Made it into the func')
    # check login status. If not logged in then redirect
    logname = safety_checks.check_login_status(flask.session)
    if logname is False:
        flask.abort(403, "Not logged in")
    target = '/'
    if len(user_request.args.getlist('target')) != 0:
        target = user_request.args.getlist('target')[0]
    vals = flask.request.form
    fullname = vals.get('fullname', False)
    email = vals.get('email', False)
    if not fullname and not email:
        print('Something is empty')
        flask.abort(400, 'email or fullname is empty')
    # now update fullname and email
    # connect to the db.
    connection = insta485.model.get_db()
    connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ? "
        "WHERE username = ?;",
        (str(fullname), str(email), logname))
    file = flask.request.files['file']
    if file.filename != '':
        # Unpack flask object and Save to disk
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        print('Filename: ', filename)
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        # Get filename from db and then delete it from uploads
        file_name = connection.execute(
            " SELECT filename "
            " FROM users "
            " WHERE username = ? ",
            (logname,)).fetchall()
        path = insta485.app.config["UPLOAD_FOLDER"] / \
            file_name[0]['filename']
        os.remove(path)
        # now update image in data base
        connection.execute(
            "UPDATE users "
            "SET filename = ? "
            "WHERE username = ?;",
            (uuid_basename, logname))
    insta485.model.close_db(False)
    return target


@insta485.app.route('/accounts/', methods=["POST", "GET"])
def post_account():
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    operation = str(deepcopy(flask.request.form['operation']))
    operation = operation.strip()
    target = '/'
    if operation == "login":
        target = post_login(flask.request)
    if operation == "logout":
        print("DEBUG Logout:", flask.session['username'])
        flask.session.clear()
        return flask.redirect('/accounts/login/')
    if operation == "create":
        target = create(flask.request)
        return flask.redirect(target, code=302)
        # needs to redirect the user
    if operation == "delete":
        logname = safety_checks.check_login_status(flask.session)
        if logname is False:
            flask.abort(403)
        target = post_delete(flask.request)
    if operation == "edit_account":
        target = post_edit_account(flask.request)
    if operation == "update_password":
        logname = safety_checks.check_login_status(flask.session)
        if logname is False:
            flask.abort(403)
        target = update_password(flask.request)
    return flask.redirect(target, code=302)
    # didn't give a valid operation


@insta485.app.route("/uploads/<image_name>")
def get_image(image_name):
    """
    Pydocstyle summary satisfaction.

    Pydocstle description.
    """
    try:
        logname = safety_checks.check_login_status(flask.session)
        if logname is False:
            flask.abort(403, "No user logged in")
        connection = insta485.model.get_db()
        db_funcs.get_username(connection, flask.session['username'])
        insta485.model.close_db(False)
        return flask.send_from_directory(path=image_name,
                                         as_attachment=True,
                                         directory=UPLOAD_FOLDER)
    except FileNotFoundError:
        flask.abort(404, "File does not exist")
        return 0
######################################
