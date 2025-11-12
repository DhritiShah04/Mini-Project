// SentimentBarChart.jsx
import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const sampleSentimentData = [
  { user: "Gamers", positive: 42, neutral: 5, negative: 4 },
  { user: "Students", positive: 35, neutral: 1, negative: 6 },
  { user: "Content Creators", positive: 26, neutral: 3, negative: 1 },
  { user: "Casual Users", positive: 34, neutral: 2, negative: 4 },
  { user: "Programmers", positive: 34, neutral: 2, negative: 5 },
];

const SentimentChart = ({data}) => (
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data} margin={{ top: 20, right: 30, bottom: 20, left: 0 }}>
      <XAxis dataKey="user" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="positive" fill="#4caf50" />
      <Bar dataKey="neutral" fill="#ffb300" />
      <Bar dataKey="negative" fill="#e53935" />
    </BarChart>
  </ResponsiveContainer>
);

export default SentimentChart;
