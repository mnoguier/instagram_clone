import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Comments from './comments';
import Like from './like';

class Post extends React.Component {
  // fetch a pages information.
  // url should /api/v1/posts/<postid>/
  // call like
  // call comments
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      comments: 'holder',
      // convert the time into human readable format
      created: 'holder',
      imgUrl: 'holder',
      likes: 'holder',
      owner: 'holder',
      ownerImgUrl: 'holder',
      ownerShowUrl: 'holder',
      //   postShowUrl: 'holder',
      postid: 'holder',
      url: 'holder',
    };
    // This binding is necessary to make `this` work in the callback
    this.like = this.like.bind(this);
    this.unlike = this.unlike.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    // Call REST API,  GET /api/v1/posts/<postid>/
    const { url } = this.props;
    fetch(url, {
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'text/plain',
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(({
          comments: data.comments,
          // convert the time into human readable format
          created: moment(data.created, 'YYYY-MM-DD hh:mm:ss').fromNow(),
          imgUrl: data.imgUrl,
          likes: data.likes,
          numLikes: data.likes.numLikes,
          lognameLikesThis: data.likes.lognameLikesThis,
          likesurl: data.likes.url,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          //   postShowUrl: data.postShowUrl,
          postid: data.postid,
          url: data.url,
        }));
      })
      .catch((error) => console.log(error));
  }

  like() {
    const { lognameLikesThis } = this.state;
    const { postid } = this.state;
    if (lognameLikesThis === false) {
      this.setState((prevState) => ({
        numLikes: prevState.numLikes + 1,
        lognameLikesThis: true,
      }));
      // console.log('numLikes', numLikes)
      // console.log('lognameLikesThis', lognameLikesThis)
      fetch(`/api/v1/likes/?postid=${postid}`, {
        credentials: 'same-origin',
        method: 'POST',
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
            likesurl: data.url,
          });
        });
    }
  }

  unlike() {
    const { likesurl } = this.state;
    // console.log('Got to Unlike')
    // console.log('numlikes', this.state.numLikes, "likesThis", this.state.lognameLikesThis)
    this.setState((prevState) => ({
      numLikes: prevState.numLikes - 1,
      lognameLikesThis: false,
    }));
    fetch(likesurl, {
      credentials: 'same-origin',
      method: 'DELETE',
    });
    // console.log('numlikes', this.state.numLikes, "likesThis", this.state.lognameLikesThis)
  }

  render() {
    const { comments } = this.state;
    const { created } = this.state;
    const { imgUrl } = this.state;
    const { likes } = this.state;
    const { owner } = this.state;
    const { ownerImgUrl } = this.state;
    const { ownerShowUrl } = this.state;
    const { postid } = this.state;
    const { url } = this.state;
    const { numLikes } = this.state;
    const { lognameLikesThis } = this.state;
    // url = likes.url;
    // console.log()
    if (imgUrl === 'holder' || likes === 'holder' || comments === 'holder') {
      return <p>Loading a post...</p>;
    }
    // console.log('likes', this.state.likes.numLikes)
    let postidUrl = '/posts/'.concat(postid);
    postidUrl = postidUrl.concat('/');
    // console.log('post.this', this)
    return (

      <div>
        {/* User img, username, timestamp */}
        <a href={ownerShowUrl} className="owner">
          {owner}
          <img
            className="Owner Picture"
            src={ownerImgUrl}
            alt=""
            width="70"
            height="70"
          />
        </a>
        <a href={postidUrl} className="Timestamp">{created}</a>
        <p>{'\n'}</p>
        <img
          onDoubleClick={this.like}
          className="PostPicture"
          src={imgUrl}
          alt=""
          width="350"
          height="350"
        />
        <p>{'\n'}</p>
        {/* Likes */}
        <Like
          like={this.like}
          unlike={this.unlike}
          likes={numLikes}
          lognameLikesThis={lognameLikesThis}
          url={url}
        />
        <p>{'\n'}</p>
        {/* Comments */}
        <Comments
          comments={comments}
          postid={postid}
        />
        {/* <p>{'\n'}</p>
                <p>{'\like={this.}n'}</p>
                <p>{'\n'}</p> */}
      </div>
    );
  }
}

// Post.defaultProps = {
//   numLikes: 0,
//   lognameLikesThis: false,
// };

Post.propTypes = {
  url: PropTypes.string.isRequired,
  // numLikes: PropTypes.number,
  // lognameLikesThis: PropTypes.bool,
  // likesurl: PropTypes.string.isRequired,
  //   likes: PropTypes.string,
  //   posts: PropTypes.array.isRequired,
  //   next: PropTypes.string.isRequired,
};

export default Post;
