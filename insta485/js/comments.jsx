import React from 'react';
import PropTypes from 'prop-types';
import Comment from './comment';

class Comments extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    const { comments } = this.props;
    this.state = {
      comments,
      newComment: '',
    };

    // this.onSubmit = this.onSubmit.bind(this);
    // this.handleChange = this.handleChange.bind(this)
    this.deleteComment = this.deleteComment.bind(this);
  }

  onChange(event) {
    this.state.newComment = event.target.value;
  }

  // Make a comment.
  onSubmit(event) {
    const { comments } = this.state;
    const { newComment } = this.state;
    const { postid } = this.props;
    // prevent the page from refreshing
    event.preventDefault();
    if (newComment === '') {
      return;
    }

    // first make a post request to insert the comment
    fetch(`/api/v1/comments/?postid=${postid}`, {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ text: newComment }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      // Now update the the state with the response from the server
      .then((data) => {
        let logname = false;
        console.log('this is the type', typeof (data.lognameOwnsThis));
        if (data.lognameOwnsThis === 'true') {
          logname = true;
        }

        console.log('this is the type', typeof (data.lognameOwnsThis));
        console.log(data.lognameOwnsThis, 'WHAT TYPE ARE YOU');
        comments.push({
          commentid: data.commentid,
          lognameOwnsThis: logname,
          owner: data.owner,
          ownerShowUrl: data.ownerShowUrl,
          text: data.text,
          url: data.url,
        });
        this.setState({ comments, newComment: '' });
      });
    // wipe the input
    event.target.reset();
  }

  deleteComment(comment) {
    const { comments } = this.state;
    // user can only delete their own post
    if (comment.lognameOwnsThis) {
      console.log('commentid', comment);
      fetch(`/api/v1/comments/${comment.commentid}/`, {
        credentials: 'same-origin',
        method: 'DELETE',
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          // no data is given in the response. Need to find a way to
        })
        .then(() => {
          let index = -1;
          let counter = 0;
          const newComments = comments;
          newComments.forEach((commentToDelete) => {
            if (commentToDelete === comment) {
              index = counter;
            }
            counter += 1;
          });
          console.log('before delete', newComments);
          console.log('we are deleteing', index);
          newComments.splice(index, 1);
          console.log('after delete', newComments);
          this.setState({
            // update the comments with a removed comment
            comments: newComments,
          });
        });
    }
  }

  render() {
    const coms = [];
    const { comments } = this.state;

    comments.forEach((comment) => {
      // console.log('comment', comment);
      coms.push(
        <Comment
          deleteComment={this.deleteComment}
          key={comment.commentid}
          comment={comment}
        // commentid={comment.commentid}
        // lognameLikesThis={comment.lognameLikesThis}
        // owner={comment.owner}

        />,
      );
    }); // forloop
    return (
      <div>
        {/* display the comments that the post has */}
        {coms}
        {/* Displate comment form, text field and submit button */}
        {/* ETHAN IS DOI */}
        {/* https://stackoverflow.com/questions/33211672/how-to-submit-a-form-using-enter-key-in-react-js */}
        {/* <form className="comment-form" method="post" encType="multipart/form-data">
                    <input type="hidden" name="operation" value="create" />
                    <input type="hidden" name="postid" value={this.props.postid} />
                    <input type="text" name="text" value="" required onSubmit={this.make_comment} />
                    <input type="submit" name="comment" value="comment" />
                </form> */}
        <form className="comment-form" onChange={this.onChange.bind(this)} onSubmit={this.onSubmit.bind(this)}>
          <input type="text" placeholder="Comment on Post" />
        </form>
      </div>
    ); // return
  } // render
} // class

Comments.propTypes = {
  postid: PropTypes.number.isRequired,
  // comments should not be string but array and object are forbidden
  comments: PropTypes.arrayOf(PropTypes.shape({
    commentid: PropTypes.number,
    lognameOwnsThis: PropTypes.bool,
    owner: PropTypes.string,
    ownerShowUrl: PropTypes.string,
    text: PropTypes.string,
    url: PropTypes.string,
  })).isRequired,
};

export default Comments;
