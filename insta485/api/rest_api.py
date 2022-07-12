"""REST API for posts."""
import json
import flask
import insta485
from insta485 import safety_checks
from insta485 import db_funcs

# """
# Ethan:
# DONE /api/v1/
# SKIPPED FOR NOW. CONFUSED.
# ON NOW /api/v1/posts/<postid>/
# WILL FINISH TONIGHT /api/v1/comments/?postid=<postid>

# Nick:
# DELETE /api/v1/comments/<commentid>/
# /api/v1/likes/?postid=<postid>
# /api/v1/likes/<likeid>/

# Matthew:
# /api/v1/posts/?page=N
# /api/v1/posts/
# /api/v1/posts/?postid_lte=N
# /api/v1/posts/?size=N

# """
# Every REST API route should return 403 if a user is not authenticated


def authentication_check(request, session, connection):
    """
    Style summary.

    Style description
    Ethan
    """
    # check if we should authorize through http or session cookie
    if request.authorization is not None:
        # http chosen
        username = request.authorization['username']
        password = request.authorization['password']
        db_pass = db_funcs.get_password(connection, username).split('$')
        # check password given and db password match.
        hashed_pass = safety_checks.hash_password(
            password, db_pass[0], db_pass[1], False)
        if db_pass[2] != hashed_pass.split('$')[2]:
            return False
        return request.authorization['username']

    # session cookie chosen
    if 'username' not in session:
        return False
    return session['username']


@insta485.app.route('/api/v1/')
def get_links():
    """
    Style summary satisfaction.

    Style description satisfaction
    Ethan
    """
    print('\n', ' ENTERING /api/v1/', '\n')
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


# this needs to get size number of posts on a
# certain page that are not newer than postid_lte
def get_posts_rest_api(page, size, postid_lte):
    """
    Pydocstyle summary.

    Display / route.
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary

    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error
    post_dict = {}
    post_query = connection.execute(
        " SELECT postid "
        " FROM posts "
        " WHERE posts.owner IN "
        " ( SELECT username2 "
        " FROM following "
        " WHERE username1 == ? ) "
        " OR posts.owner == ? "
        " AND posts.postid <= ? "
        " ORDER BY postid DESC "
        " LIMIT ? "
        " OFFSET ? ",
        (authorized, authorized, postid_lte, size, page*size,)).fetchall()
    if not post_query:
        post_dict.update({"next": ""})
    elif int(post_query[0]['postid']) - int(post_query[-1]['postid'])+1 < size:
        post_dict.update({"next": ""})
    else:
        post_dict.update({"next": "/api/v1/posts/?size=" + str(size) +
                          "&page=" + str(page + 1) +
                          "&postid_lte=" + str(postid_lte)})
    url_dict = []
    for post in post_query:

        url_dict.append({"postid": post['postid'], "url": "/api/v1/posts/"
                         + str(post['postid']) + "/"})

    post_dict.update({"results": url_dict})
    post_dict.update({"url": "/" + flask.request.url.split('/', 3)[3]})
    return_data = flask.jsonify(**post_dict)
    print('I am returning this\n\n', return_data, '\n\n')
    return_data.status_code = 200
    return return_data


@insta485.app.route("/api/v1/posts/", methods=['GET'])
def post_rest_api():
    """
    Pydocstyle summary.

    Display / route.
    """
    connection = insta485.model.get_db()

    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error
    most_recent_post = connection.execute(
        " SELECT postid "
        " FROM posts "
        " WHERE posts.owner IN "
        " ( SELECT username2 "
        " FROM following "
        " WHERE username1 == ? ) "
        " OR posts.owner == ? ",
        (authorized, authorized,)).fetchall()
    if most_recent_post:
        most_recent_post = most_recent_post[-1]['postid']
    else:
        most_recent_post = 0

    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    postid_lte = flask.request.args.get('postid_lte',
                                        default=int(most_recent_post),
                                        type=int)

    # print("return data" , return_data)
    if size < 0 or page < 0:
        error_message = {"message": "Bad Request", "status_code": 400}
        error = flask.jsonify(**error_message)
        error.status_code = 400
        return error
    return get_posts_rest_api(page, size, postid_lte)


@insta485.app.route('/api/v1/posts/<int:postid>/')
def get_one_post(postid):
    """
    Style summary.

    Style description
    Ethan
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary
    print(authorized)
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error
    # now get data from the db
    post_dict = {}
    # owner db below
    owner_info = connection.execute(
        "SELECT posts.owner as owner, posts.filename as imgUrl, "
        "posts.created, "
        "users.filename as ownerShowUrl "
        "FROM posts "
        "INNER JOIN users ON users.username = posts.owner "
        "WHERE postid = ?",
        (postid,)).fetchall()
    if len(owner_info) == 0:
        error = flask.jsonify(**{"message": "NOT FOUND", "status_code": 404})
        error.status_code = 404
        return error
    owner_show_url = {'ownerShowUrl': '/users/' + owner_info[0]['owner'] + '/'}
    owner_info[0]['imgUrl'] = '/uploads/' + owner_info[0]['imgUrl']
    # comments db below
    comments = connection.execute(
        "SELECT comments.commentid, comments.owner, comments.text, "
        "CASE "
        "WHEN comments.owner = ? THEN True "
        "ELSE False "
        "END AS lognameOwnsThis "
        "FROM comments "
        "INNER JOIN posts ON comments.postid = posts.postid "
        "WHERE posts.postid = ? ",
        (authorized, postid, )).fetchall()
    for comment in comments:
        comment.update({"url": "/api/v1/comments/" +
                       str(comment['commentid']) + '/'})
        comment.update({"ownerShowUrl": "/users/" + comment['owner'] + '/'})
        if comment['lognameOwnsThis']:
            comment['lognameOwnsThis'] = True
        else:
            comment['lognameOwnsThis'] = False
    # likes db below
    likeid = connection.execute(
        "SELECT likes.likeid "
        "FROM likes "
        "INNER JOIN posts ON likes.postid = posts.postid "
        "WHERE posts.postid = ? ",
        (postid, )).fetchall()
    like_url = ''
    if len(likeid) != 0:
        likeid = likeid[0]['likeid']
        like_url = {'url': "/api/v1/likes/" + str(likeid) + "/"}
    else:
        likeid = None
        like_url = {'url': None}
    likes = connection.execute(
        "SELECT COUNT(likes.likeid) as numLikes, "
        "CASE "
        "WHEN likes.owner = ? THEN 1 "
        "ELSE 0 "
        "END AS lognameLikesThis "
        "FROM likes "
        "INNER JOIN posts ON likes.postid = posts.postid "
        "WHERE posts.postid = ? ",
        (authorized, postid, )).fetchall()

    if len(likes) != 0 and likes[0]['lognameLikesThis']:
        likes[0]['lognameLikesThis'] = True
        print('DEBUG HERE: ', likes[0]['lognameLikesThis'])
        print('LIKES: ', likes)
    else:
        likes[0]['lognameLikesThis'] = False
    likes[0].update(like_url)
    # HINT: sqlite3 provides a special function to retrieve the
    # ID of the most recently inserted item: SELECT last_insert_rowid().
    # now put it all in the big dict
    for sub_dict in owner_info:
        post_dict.update(sub_dict)
    post_dict.update({'postid': postid})
    post_dict.update({"comments": comments})
    post_dict.update({'url': '/api/v1/posts/' + str(postid)+'/'})
    post_dict.update(owner_show_url)
    post_dict.update({'likes': likes[0]})
    post_dict.update({'postShowUrl': '/posts/'+str(postid)+'/'})
    print(owner_info[0])
    post_dict.update({'ownerImgUrl': '/uploads/' +
                     owner_info[0]['ownerShowUrl']})
    insta485.model.close_db(False)
    # return str(post_dict)
    return_data = flask.jsonify(**post_dict)
    return_data.status_code = 200
    return return_data


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """
    Pydocstyle summary.

    Display / route.
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary
    print(authorized)
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error

    # now get data from the db
    post_dict = {}
    status_code = 200
    # postid = ''
    # Getting target from route

    if flask.request.args.get('postid', False):
        postid = flask.request.args.get('postid', False)
        print('enter')
    # Check if user has liked post __
    likes = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner == ? and postid == ?; ",
        (authorized, postid, )).fetchall()
    if len(likes) == 0:
        status_code = 201
        print('username: ', authorized, ' PostID: ', postid)
        connection.execute(
            "INSERT INTO likes (owner, postid) "
            "VALUES (?, ?); ",
            (authorized, postid, ))
        likes = connection.execute(
            "SELECT last_insert_rowid() as likeid; ").fetchall()

    # update post_dict
    post_dict.update({"likeid": likes[0]['likeid'],
                      "url": "/api/v1/likes/" + str(likes[0]['likeid']) + "/"})
    return_data = flask.jsonify(**post_dict)
    return_data.status_code = status_code
    return return_data


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """
    Pydocstyle summary.

    Display / route.
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error

    # now get data from the db
    post_dict = {}
    # status_code = 200
    # Check if user has liked post __
    likes = connection.execute(
        "SELECT owner "
        "FROM likes "
        "WHERE likeid == ? ",
        (likeid, )).fetchall()
    if len(likes) == 0:
        status_code = 404
    elif likes[0]['owner'] != authorized:
        status_code = 403
    else:
        status_code = 204
        connection.execute(
            " DELETE "
            " FROM likes "
            " WHERE owner == ? and likeid == ?",
            (authorized, likeid, ))
    # update post_dict
    return_data = flask.jsonify(**post_dict)
    return_data.status_code = status_code
    return return_data


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    """
    Style summary.

    Style description
    Ethan
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error
    # text is stored as a bytes object. Need to do black magic to get it
    # to be a dictionary
    data = json.loads(str(flask.request.data.decode()))
    print('\n\ndata here :', data)
    text = data['text']
    postid = flask.request.args.get('postid')

    if not text:
        # need to return a html request
        error_message = {
            "message": "Comment must have text", "status_code": 400}
        return_data = flask.jsonify(**error_message)
        return_data.status_code = 400
        return return_data

    # insert the comment
    connection.execute(
        " INSERT INTO comments(owner, postid, text) "
        " VALUES(?, ?, ?);",
        (authorized, postid, text,))

    # get the return data
    # HINT: sqlite3 provides a special function to retrieve the
    # ID of the most recently inserted item: SELECT last_insert_rowid().
    commentid = connection.execute(
        "SELECT last_insert_rowid() as commentid;").fetchall()[0]['commentid']
    print(commentid)
    post_dict = {"commentid": commentid, "lognameOwnsThis": 'true', "owner":
                 authorized, "ownerShowUrl": "/users/" + authorized + "/",
                 "text": text, "url": "/api/v1/comments/"
                 + str(commentid) + '/'}
    return_data = flask.jsonify(**post_dict)
    return_data.status_code = 201
    return return_data


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """
    Pydocstyle summary.

    Display / route.
    """
    connection = insta485.model.get_db()
    authorized = authentication_check(flask.request, flask.session, connection)
    # need to add them to one big dictionary
    print(authorized)
    if authorized is False:
        error_message = {"message": "Forbidden", "status_code": 403}
        error = flask.jsonify(**error_message)
        error.status_code = 403
        return error

    # now get data from the db
    post_dict = {}
    # status_code = 200
    # Check if user has liked post __
    comment = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid == ? ",
        (commentid, )).fetchall()
    if len(comment) == 0:
        status_code = 404
    elif comment[0]['owner'] != authorized:
        status_code = 403
    else:
        # actually get the post id that is relevant
        status_code = 204
        connection.execute(
            " DELETE "
            " FROM comments "
            " WHERE owner == ? and commentid == ?",
            (authorized, commentid, ))
    # update post_dict
    return_data = flask.jsonify(**post_dict)
    return_data.status_code = status_code
    print("I am returning this after deleting a comment\n", return_data)
    return return_data
