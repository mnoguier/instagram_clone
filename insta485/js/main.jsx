import React from 'react';
import ReactDOM from 'react-dom';
// import Post from './post';
import Index from './index';// this is for testing by ethan

// This method is only called once
ReactDOM.render(
  // Insert the post component into the DOM
  // <Posts url="/api/v1/posts/" />,
  <Index url="/api/v1/" />,
  document.getElementById('reactEntry'),
);
