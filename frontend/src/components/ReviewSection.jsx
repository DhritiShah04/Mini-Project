import React, { useEffect, useState } from "react";
import SentimentChart from "./SentimentChart";
import "./ReviewSection.css";

function ReviewSection({ model }) {
  const [reviewAnalysis, setReviewAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    if (!model) return;

    const formattedModelName = model.replace(/ /g, "_");
    const fetchUrl = `http://localhost:5000/api/reviews/reddit/analysis/${formattedModelName}`;

    let isMounted = true;

    const fetchData = () => {
      fetch(fetchUrl)
        .then(res => {
          if (res.status === 404) {
            throw new Error("File not found");
          }
          if (!res.ok) {
            throw new Error("Network response not ok");
          }
          return res.json();
        })
        .then(data => {
          if (isMounted) {
            setReviewAnalysis(data);
            setLoading(false);
          }
        })
        .catch(err => {
          console.error("Fetch error or file not ready:", err);
          if (isMounted) {
            setTimeout(() => {
              setRetryCount(prev => prev + 1);
            }, 3000);
          }
        });
    };

    setLoading(true);   // set loading true before fetch
    fetchData();

    return () => {
      isMounted = false;
    };
  }, [model, retryCount]);

  const sentimentData = reviewAnalysis
    ? Object.entries(reviewAnalysis.sentiment_by_user).map(([user, stats]) => ({
        user,
        positive: stats.positive,
        neutral: stats.neutral,
        negative: stats.negative,
      }))
    : [];

  return (
    <div className="reviews-section">
      <h2>User Reviews & Sentiments</h2>
      <h3>What users on Reddit say:</h3>
      <div className="reviews-section-subhead">
        {loading ? (
          <div className="review-loader-container">
            <div className="review-loader"></div>
            
          </div>
        ) : reviewAnalysis ? (
          <SentimentChart data={sentimentData} />
        ) : (
          <p>Failed to load review data.</p>
        )}
      </div>
    </div>
  );
}

export default ReviewSection;
