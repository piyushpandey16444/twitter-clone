import React, {useState, useEffect} from 'react';
import './App.css';

// call the function for sending ajax get request > takes element as argument that is to be replaced.
function loadTweets(callBack){
  const url = "http://localhost:8000/api/tweets/"
  const method = 'GET'
  const xhr = new XMLHttpRequest()
  const responseType = "json"
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = () => {
    callBack(xhr.response, xhr.status)
  }
  xhr.onerror = function(e){
    callBack({"message": "Was an error !"})
  }
  xhr.send()
}

function App() {
  
  // use state hooks --> used for initialization
  const [tweets, setTweet] = useState([])

  // use effect used for call back function to call data from ajax request 
  useEffect(() => {
    const myCallBack = (response, status) =>{
      console.log(response)
      if (status === 200 ){
        setTweet(response, status)
      }
    }
    loadTweets(myCallBack)
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
