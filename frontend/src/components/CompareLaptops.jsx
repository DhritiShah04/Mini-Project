import React from 'react'
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
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
    <div class='main-cont-coompare'>
      <div className='heading-comp'>
          {/* <div className="go-back-comp"> */}
            <Link to='/recommendations' id='link-part'> 
            <button class= "go-back-comp">
                <i class="fa-solid fa-arrow-left-long"></i>
                <h4>Back to Laptops</h4>
              </button>
            </Link>
          {/* </div> */}
      </div>
      <h2 class='recom'>Compare our Recommendations</h2>  

      <div className='actual-comp-table'>
        <div className="titles-comp">
          <div className="inner-cont-comp-left">
            <h3>Features</h3>
          </div>
          {laptops.map((laptop, index) => {
              // Determine if this is the last column to apply inner-cont-comp-right
              const isLast = index === laptops.length - 1;
              const className = isLast ? "inner-cont-comp-right" : "inner-cont-comp";
              
              return (
                  <div key={laptop._id || laptop.model} className={className}>
                      <h3>{laptop.model || "Unknown Model"}</h3>
                  </div>
              );
          })}
        </div>
        <div className="cont-comp">
          <div className="inner-cont-comp-left">
              <p className='features-comp'>Price</p>
              <p className='features-comp'>Battery</p>
              <p className='features-comp'>Display</p>
              <p className='features-comp'>Storage</p>
              <p className='features-comp'>RAM</p>
              <p className='features-comp'>CPU</p>
              <p className='features-comp'>GPU</p>
              {/* <p className='features-comp'>Why?</p> */}
          </div>
          {laptops.map((laptop, index) => {
            const isLast = index === laptops.length - 1;
            const className = isLast? "inner-cont-comp-right" : "inner-cont-comp";
            return (
              <div className={className}>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>Rs {laptop.price_inr}/-</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.battery}</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.display}</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.storage}</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.ram}</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.cpu}</p>
                </div>
                <div key={laptop.price_inr} className = {`$ features-comp`}>
                  <p>{laptop.gpu}</p>
                </div>
                {/* <div key={laptop.price_inr} className = {`$features-comp`}>
                  <p>{laptop.why}</p>
                </div> */}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default CompareLaptops;