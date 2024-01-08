import Head from 'next/head'
import { Inter } from '@next/font/google'

import React, { useEffect, useState } from 'react';
import fileData from '../data.json';
// import {TwitterTimelineEmbed} from 'react-twitter-embed';



function KeyDisplay() {
  const [lastKey, setLastKey] = useState(null);

  useEffect(() => {
    const handleKeyPress = (event) => {
      setLastKey(event.key);
      setTimeout(() => {
        setLastKey(null);
      }, 1500);
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, []);

  return (
    <div>
      <table>
        <tr>
          <td>K</td>
          <td>Keep</td>
        </tr>
        <tr>
          <td>U</td>
          <td>Unfollow</td>
        </tr>
        <tr>
          <td>M</td>
          <td>Maybe</td>
        </tr>
      </table>
      {lastKey ? `Last key pressed: ${lastKey}` : 'Press a key'}
    </div>
  );
}

// const headers = {
//   'Content-Type': 'application/json'
// };

// function updateState(currentItemIndex, state) {
//   let rowId = currentItemIndex;
//   // Update local storage
//   let localData = JSON.parse(localStorage.getItem('data'));
//   localData[rowId]['state'] = state;
//   localStorage.setItem('data', JSON.stringify(localData));
// }

function downloadData() {
  let localData = JSON.parse(localStorage.getItem('data'));
  const element = document.createElement("a");
  const file = new Blob([JSON.stringify(localData)], { type: 'text/plain' });
  element.href = URL.createObjectURL(file);
  element.download = "sortedData.json";
  document.body.appendChild(element);
  element.click();
}

function TwitterProfile({ username }) {
  const twitterUrl = `https://twitter.com/${username}?ref_src=twsrc%5Etfw`;

  return (
    <div>
      <a 
        className="twitter-timeline" 
        data-height="400" 
        href={twitterUrl}
      >
        Tweets by {username}
      </a> 
      <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>
  );
}


function Item({ item }) {
  if (!item) {
    return <div></div>;
  }
  return (
    <div className="Box">
      <img src={item.profile_picture_link} alt={item.name} />
      <h2>{item.name}</h2>
      <h3>@{item.username}</h3>
      <p>{item.description}</p>
      <h4>First Two Tweets:</h4>
      {item.first_two_tweets && (
        <ul>
          {item.first_two_tweets.map((tweet, index) => (
            <li key={index}>{tweet}</li>
          ))}
        </ul>
      )}
      <p>State: {item.state}</p>
    </div>
  );
}


export default function Home() {
  const [items, setItems] = useState()
  // const [numNotes, setNumNotes] = useState(0)
  const [currentItemIndex, setCurrentItemIndex] = useState(-1)

  const updateState = (itemIndex, newState) => {
    let updatedItems = [...items];
    updatedItems[itemIndex].state = newState;
    setItems(updatedItems);
  }
  useEffect(() => {

    const handleKeyPress = (event) => {
      const key = event.key.toLowerCase();
      if (key === 'arrowleft') {
        decrementIndex();
      } else if (key === 'arrowright') {
        incrementIndex();
      } else if (key === 'u') {
        updateState(currentItemIndex, 'unfollow');
        incrementIndex();
        console.log('Unfollow');
      } else if (key === 'k') {
        updateState(currentItemIndex, 'keep');
        incrementIndex();
        console.log('Keep');
      } else if (key === 'm') {
        updateState(currentItemIndex, 'maybe');
        incrementIndex();
        console.log('Maybe');
      }
    };

    window.addEventListener('keydown', handleKeyPress);

    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [currentItemIndex]);

  const getData = () => {
    console.log('getData')

    if (!items || items.length === 0) {
      let localStorageData = null;
      try {
        const unparsedData = localStorage.getItem('data')
        console.log(typeof unparsedData);
        console.log(unparsedData)
        if (unparsedData) {
          localStorageData = JSON.parse(unparsedData);
        } else {
          console.error("No data in local storage");
        }
      } catch (error) {
        console.error("Parsing error:", error);
      }
      if (localStorageData) {
        setItems(localStorageData);        
        const firstUnprocessedIndex = localStorageData.findIndex(item => !item.state);
        console.log(`${firstUnprocessedIndex}`)
        setCurrentItemIndex(firstUnprocessedIndex !== -1 ? firstUnprocessedIndex : 0);
      } else {
        // let transformedData = Object.values(fileData);
        // transformedData = transformedData.filter(item => Object.keys(item).length > 0);
        // setItems(transformedData);
        setItems(fileData)
        // setItems(fileData);
        const firstUnprocessedIndex = fileData.findIndex(item => !item.state);
        console.log(`${firstUnprocessedIndex}`)
        setCurrentItemIndex(firstUnprocessedIndex !== -1 ? firstUnprocessedIndex : 0);
        // Existing data will get overwritten
        // localStorage.setItem('data', JSON.stringify(transformedData));
        localStorage.setItem('data', JSON.stringify(fileData));

      }
    }
  }

  const incrementIndex = () => {
    if (currentItemIndex + 1 < items.length) { setCurrentItemIndex(currentItemIndex + 1) }
  }
  const decrementIndex = () => {
    if (currentItemIndex - 1 >= 0) {
      setCurrentItemIndex(currentItemIndex - 1)
    }

  }

  useEffect(() => { getData() }, [])
  useEffect(() => {
    // Update localStorage whenever items change
    if (items && items.length > 0) {
      localStorage.setItem('data', JSON.stringify(items));
    }
  }, [items]);

  const clearData = () => {
    localStorage.clear();
    setItems([]);
  }

  return (
    <>
      <Head>
        <title>Reviewer App</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {!items || items.length === 0 ? <p>No Data to display</p> : <p>{currentItemIndex}/{items.length}</p>}
      {items && currentItemIndex >= 0 && currentItemIndex < items.length ?
          <div>
          <Item item={items[currentItemIndex]} />
          <KeyDisplay />
          <button onClick={downloadData}>
            Download Sorted Data
          </button>
          <button onClick={clearData}>
            Clear Data
          </button>
        </div>

        :
        <div>Loading</div>
      }    </>
  )
}