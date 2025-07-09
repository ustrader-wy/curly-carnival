function getSignal() {
  const loading = document.getElementById("loading");
  const countdown = document.getElementById("countdown");
  loading.style.display = "flex";
  let timeLeft = 60;

  const timer = setInterval(() => {
    countdown.textContent = `NEXT SIGNAL IN 00:${timeLeft < 10 ? '0' + timeLeft : timeLeft}`;
    timeLeft--;

    if (timeLeft < 0) {
      clearInterval(timer);
      countdown.textContent = "✅ SIGNAL: UP 🔼 or DOWN 🔽";
    }
  }, 1000);
}
