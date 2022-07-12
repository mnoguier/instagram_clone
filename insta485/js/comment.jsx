import React from 'react';
import PropTypes from 'prop-types';

class Comment extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    const { comment } = this.props;
    this.state = {
      // convert the time into human readable format
      comment,
      // button: [],
    };
  }

  // make individual comments
  render() {
    const { comment } = this.state;
    let { button } = 'Hello?';
    const { deleteComment } = this.props;
    // console.log('comment line 22', comment);
    console.log('Comment.lognameOwnsThis', comment.lognameOwnsThis);
    if (comment.lognameOwnsThis) {
      // it is their comment, so show delete button
      button = (
        <button
          type="button"
          className="delete-comment-button"
          onClick={() => { deleteComment(comment); }}
        >
          Delete Comment
        </button>
      );
    } else {
      // it is not their comment, they can not delete
      button = '';
    }
    return (
      <div>

        <p>
          <a href={comment.ownerShowUrl}>{comment.owner}</a>
          {' '}
          {comment.text}
        </p>
        {button}
      </div>
    ); // return
  } // render
} // Class

Comment.propTypes = {
  deleteComment: PropTypes.func.isRequired,
  // key: PropTypes.number.isRequired,
  // comments should not be string but array and object are forbidden
  comment: PropTypes.shape({
    commentid: PropTypes.number,
    lognameOwnsThis: PropTypes.bool,
    owner: PropTypes.string,
    ownerShowUrl: PropTypes.string,
    text: PropTypes.string,
    url: PropTypes.string,
  }).isRequired,
};

export default Comment;
