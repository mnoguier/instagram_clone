import React from 'react';
import PropTypes from 'prop-types';

class Like extends React.Component {
  // fetch a pages information.
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      // // convert the time into human readable format
      // url: this.props.url,
      // lognameLikesThis: this.props.lognameLikesThis,
      // likes: this.props.likes,
      likeOrLikes: '',
      button: [],
    };
  }

  // url should /api/v1/posts/<postid>/
  render() {
    let { likeOrLikes } = this.state;
    let { button } = this.state;
    const { lognameLikesThis } = this.props;
    const { likes } = this.props;
    const { like } = this.props;
    const { unlike } = this.props;
    // console.log('like.this', this)
    if (lognameLikesThis) {
      button = (
        <button
          type="button"
          onClick={() => { unlike(); }}
          className="like-unlike-button"
        >
          Unlike
        </button>
      );
    } else {
      button = (
        <button
          type="button"
          onClick={() => { like(); }}
          className="like-unlike-button"
        >
          Like
        </button>
      );
    }
    // console.log('numLikes in like.render', this.props.likes)
    if (likes !== 1) {
      likeOrLikes = ' likes';
    } else {
      likeOrLikes = ' like';
    }
    // join them together to form ex. '0 likes' or '1 like'
    return (
      <div>
        {/* Make call to helper fxn that handles like/unlike. */}
        {/* display the number of likes that the post has */}
        <p>
          {likes}
          {likeOrLikes}
        </p>
        {/* like or unlike button */}
        {button}
      </div>
    );
  }
}

Like.propTypes = {
  likes: PropTypes.number.isRequired,
  like: PropTypes.func.isRequired,
  unlike: PropTypes.func.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
};

export default Like;
