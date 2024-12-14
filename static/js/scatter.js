
document.addEventListener("DOMContentLoaded", () => {
  const symbols = [
    { icon: "/static/images/red.jpg/", name: "red", payout: 2 },
    { icon: "/static/images/yellow.jpg/", name: "yellow", payout: 3 },
    { icon: "/static/images/coin2.jpg/", name: "coin", payout: 5 }, // Scatter
    { icon: "/static/images/pig.jpg/", name: "pig", payout: 4 },
    { icon: "/static/images/bomb.jpg/", name: "black", payout: 3 },
  ];

  const rows = 3;
  const columns = 5;
  const slotMachine = document.getElementById("slot-machine");
  const spinButton = document.getElementById("spin-btn");
  const resultDisplay = document.getElementById("result");

  // Generate slot machine grid dynamically
  const reels = [];
  for (let i = 0; i < rows * columns; i++) {
    const reel = document.createElement("div");
    reel.classList.add("reel");
    slotMachine.appendChild(reel);
    reels.push(reel);
  }

  spinButton.addEventListener("click", () => {
    resultDisplay.textContent = "Spinning...";
    spinButton.disabled = true;

    // Add spin animation
    reels.forEach(reel => reel.classList.add("spin"));

    // Simulate spinning effect
    setTimeout(() => {
      const grid = [];
      let totalPayout = 0;

      reels.forEach((reel, index) => {
        const randomIndex = Math.floor(Math.random() * symbols.length);
        const symbol = symbols[randomIndex];
        reel.innerHTML = `<img src="${symbol.icon}" alt="${symbol.name}">`;
        reel.classList.remove("spin");

        const row = Math.floor(index / columns);
        if (!grid[row]) grid[row] = [];
        grid[row].push(symbol.name);
      });

      const scatterCount = countScatter(grid, "Star");
      const lineWin = checkLineWin(grid);

      // Evaluate results
      if (scatterCount >= 2) {
        const scatterPayout = scatterCount * symbols.find(s => s.name === "Star").payout;
        totalPayout += scatterPayout;
        resultDisplay.textContent = `🎉 Scatter Bonus! ⭐ x${scatterCount} → ${scatterPayout}x payout!`;
      } else if (lineWin) {
        const { symbol, count } = lineWin;
        const payout = symbols.find(s => s.name === symbol).payout * count;
        totalPayout += payout;
        resultDisplay.textContent = `🎊 Line Win! ${symbol} x${count} → ${payout}x payout!`;
      } else {
        resultDisplay.textContent = "❌ Try Again!";
      }

      // Log results to backend
      logResult(grid, totalPayout);

      spinButton.disabled = false;
    }, 2000);
  });

  // Check for scatter symbols
  function countScatter(grid, scatterSymbol) {
    return grid.flat().filter(symbol => symbol === scatterSymbol).length;
  }

  // Check for line matches
  function checkLineWin(grid) {
    for (const row of grid) {
      const firstSymbol = row[0];
      if (row.every(symbol => symbol === firstSymbol)) {
        return { symbol: firstSymbol, count: row.length };
      }
    }
    return null; // No line match
  }

  // Log results to backend
  async function logResult(grid, payout) {
    try {
      await fetch("/log-result", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ grid, payout }),
      });
    } catch (error) {
      console.error("Failed to log results:", error);
    }
  }
});
