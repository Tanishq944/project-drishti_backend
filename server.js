const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

let realTimeMetrics = []; // Store recent metrics

// Endpoint to receive metrics from Vertex AI Vision
app.post("/metrics", (req, res) => {
  const data = req.body;
  realTimeMetrics.push(data);

  // Keep only last 100 metrics
  if (realTimeMetrics.length > 100) realTimeMetrics.shift();

  res.json({ status: "success" });
});

// Endpoint to fetch last metrics (for testing)
app.get("/metrics", (req, res) => {
  res.json(realTimeMetrics);
});

app.listen(5000, () => console.log("Backend running on port 5000"));
