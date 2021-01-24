import React, {useState, useEffect} from 'react';
import './App.css';

function App() {

  const [tweets, setTweet] = useState([1, 2, 3, 4, 5])

  useEffect(() => {
    // do my look up
    const tweetItems = [{"content": "YouThere"}, {"content": "Hello World"}]
    setTweet(tweetItems)
  }, [])

  return (
    <div className="App">
      <p>
        {tweets.map((tweet, index) => {
          return <li>{tweet.content}</li>
        })}
      </p>
    </div>
  );
}

export default App;
