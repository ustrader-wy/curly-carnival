function getSignal() {
  const pair = document.getElementById("pair").value;
  const tf = document.getElementById("timeframe").value;
  const result = document.getElementById("countdown");
  const loader = document.getElementById("loading");

  // Optional: convert timeframe like 5s → 1m
  const intervalMap = {
    "5s": "1m", "15s": "1m", "30s": "1m",
    "1m": "1m", "2m": "3m", "3m": "3m",
    "5m": "5m", "10m": "15m", "15m": "15m",
    "30m": "30m", "1hr": "1h"
  };

  const interval = intervalMap[tf] || "1m";

  loader.style.display = "block";
  result.textContent = "Analyzing...";

  fetch("https://your-backend-url/get-signal", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      pair: pair,
      interval: interval
    })
  })
    .then(response => response.json())
    .then(data => {
      loader.style.display = "none";
      if (data.signal) {
        result.textContent = `📢 SIGNAL: ${data.signal}`;
      } else {
        result.textContent = "❌ No signal received.";
      }
    })
    .catch(error => {
      console.error("Signal Error:", error);
      loader.style.display = "none";
      result.textContent = "⚠️ Error fetching signal";
    });
}
