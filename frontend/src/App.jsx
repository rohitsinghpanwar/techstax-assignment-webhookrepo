import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    const res = await axios.get('http://localhost:5000/events');
    setEvents(res.data.reverse()); // show newest first
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 15000); // every 15s
    return () => clearInterval(interval);
  }, []);

  const formatEvent = (event) => {
    const date = new Date(event.timestamp).toUTCString();
    if (event.type === 'push') {
      return `${event.author} pushed to ${event.to_branch} on ${date}`;
    } else if (event.type === 'pull_request') {
      return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${date}`;
    } else if (event.type === 'merge') {
      return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${date}`;
    }
  };

  return (
    <div>
      <h1>Github repo history</h1>
      {events.map((event, index) => (
        <p key={index}>{formatEvent(event)}</p>
      ))}
    </div>
  );
};

export default App;
