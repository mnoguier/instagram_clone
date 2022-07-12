import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Posts extends React.Component {
  // Constructor
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
    /*   posts: 'holder', */results: 'holder', next: 'holder', postsArr: [],
    };
    this.fetchmore = this.fetchmore.bind(this);
    // const posts_arr = [];
  }

  // fetch a pages information.
  // url should /api/v1/posts/
  // Careful about ?=pages, ?=size, ?=postid_lte
  componentDidMount() {
    const { postsUrl } = this.props;
    // console.log('this', this)
    fetch(postsUrl, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('data', data)
        this.setState({
          //   posts: data.url,
          results: data.results,
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  fetchmore() {
    const { next } = this.state;
    fetch(next, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          //   posts: data.url,
          results: data.results,
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { results } = this.state;
    const { postsArr } = this.state;
    if (results === 'holder') {
      return <p>Loading all Posts...</p>;
    }
    // render each individual post
    // const posts_arr = [];
    // this.state.posts_arr.push("test")
    results.forEach((post) => {
      postsArr.push(
        <div key={post.postid}>
          {' '}
          <Post url={post.url} postid={post.postid} />
          {' '}
        </div>,
      );
    });

    return (
      <div>
        <InfiniteScroll
          dataLength={postsArr.length}
          next={this.fetchmore}
          hasMore
          loader={<h4>Loading Posts IS...</h4>}
          endMessage={(
            <p style={{ textAlign: 'center' }}>
              <b>Yay! You have seen it all</b>
            </p>
          )}
        >
          {
            <div>
              {/* <Post /> */}

              {postsArr}
            </div>
          }
        </InfiniteScroll>
      </div>
    );
  }
}

Posts.defaultProps = {
  postsUrl: '',
};
Posts.propTypes = {
  //   posts: PropTypes.string,
  //   curr_url: React.PropTypes.string,
  postsUrl: PropTypes.string,
  //   likes_url: PropTypes.string,
  //   comments_url: PropTypes.string,
};

export default Posts;
