import React from 'react'
import { useParams } from 'react-router-dom';
import "./CompareLaptops.css";

// Define the keys we want to display and format them
const DISPLAY_KEYS = [
    "_id",
    "model",
    "cpu",
    "ram",
    "storage",
    "gpu",
    "display",
    "battery",
    "price_inr",
    "why",
];

function CompareLaptops({ laptops }) {
  return (
    <div id='main-cont'>
      <h2 id='recom'>Compare our Recommendations</h2>
    </div>
  )
}

export default CompareLaptops