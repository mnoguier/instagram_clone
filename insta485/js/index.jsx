import React from 'react';
import PropTypes from 'prop-types';
import Posts from './posts';

/* Component Hierarchy
*
* POSTS
*   POST
*     LIKE
*     COMMENTS
*       COMMENT
*/

class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      currUrl: 'holder', postsUrl: 'holder', likesUrl: 'holder', commentsUrl: 'holder',
    };
  }

  // fetch a pages information.
  // url should /api/v1
  componentDidMount() {
    // UNSAFE_componentWillMount(){
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log('data', data)
        this.setState({
          currUrl: data.url,
          postsUrl: data.posts,
          likesUrl: data.likes,
          commentsUrl: data.comments,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { postsUrl } = this.state;
    const { currUrl } = this.state;
    const { likesUrl } = this.state;
    const { commentsUrl } = this.state;

    if (postsUrl === 'holder') {
      return <p>Loading Index...</p>;
    }
    // // console.log('this.state', this.state)
    // // console.log('currUrl', currUrl)
    // // console.log('postsURL', postsUrl)
    // // console.log('likesUrl', likesUrl)
    // // console.log('commentsUrl', commentsUrl)
    return (
      <div>
        <Posts
          postsUrl={postsUrl}
          currUrl={currUrl}
          likesUrl={likesUrl}
          commentsUrl={commentsUrl}
        />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
