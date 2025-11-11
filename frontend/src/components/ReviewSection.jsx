import React, { useEffect, useState } from "react";
import SentimentChart from "./SentimentChart";
import "./ReviewSection.css";

function ReviewSection({ model }) {
  const [reviewAnalysis, setReviewAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retryCount, setRetryCount] = useState(0);  // optional, limit retries if desired

  useEffect(() => {
    if (!model) return;

    const formattedModelName = model.replace(/ /g, "_");
    const fetchUrl = `http://localhost:5000/api/reviews/reddit/analysis/${formattedModelName}`;
    // const fetchUrl = `/api/reviews/reddit/analysis/${formattedModelName}`;
    console.log("Fetching review analysis for:", formattedModelName);
    console.log("API Endpoint:", fetchUrl);

    
    let isMounted = true; // to avoid state updates if unmounted

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
            console.log("Review data received:", data);
            setReviewAnalysis(data);
            setLoading(false);
          }
        })
        .catch(err => {
          console.error("Fetch error or file not ready:", err);
          if (isMounted) {
            // Retry after delay (e.g., 3 seconds)
            setTimeout(() => {
              setRetryCount(prev => prev + 1);
            }, 3000);
          }
        });
    };

    fetchData();

    return () => {
      isMounted = false;  // cleanup on unmount
    };
  }, [model, retryCount]);  // retryCount triggers re-fetch

  if (loading) return <p>Loading review data...</p>;
  if (!reviewAnalysis) return <p>Failed to load review data.</p>;

  const sentimentData = Object.entries(reviewAnalysis.sentiment_by_user).map(([user, stats]) => ({
    user,
    positive: stats.positive,
    neutral: stats.neutral,
    negative: stats.negative,
  }));

  return (
    <div className="reviews-section">
      <h2>User Reviews & Sentiments</h2>
      <h3>What users on Reddit say:</h3>
      <div className="reviews-section-subhead">
        <SentimentChart data={sentimentData} />
        {/* Add more visualizations/components here */}
      </div>
    </div>
  );
}

export default ReviewSection;
