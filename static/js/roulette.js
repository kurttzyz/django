
document.addEventListener("DOMContentLoaded", () => {
    const countdownTimer = document.getElementById("countdown-timer");
    const wheel = document.getElementById("wheel");
    const placeBetButton = document.getElementById("place-bet");
    const betAmountInput = document.getElementById("bet-amount");
    const balanceElement = document.getElementById("balance");
    const betOptions = document.querySelectorAll(".bet-option");
    const historyContainer = document.getElementById('roll-history');
    
    let countdown = 10;
    let balance = parseFloat(balanceElement.textContent);
    let countdownInterval;

    // Countdown Timer
    function startCountdown() {
        countdown = 10;
        countdownTimer.textContent = countdown;

        // Clear previous interval if any
        if (countdownInterval) clearInterval(countdownInterval);

        countdownInterval = setInterval(() => {
            countdown--;
            countdownTimer.textContent = countdown;
            if (countdown <= 0) {
                clearInterval(countdownInterval);
                spinWheel();
            }
        }, 1000);
    }

    // Spin Wheel
    function spinWheel() {
        // Clear any existing animations (if any) before starting a new one
        wheel.style.animation = 'none'; // Reset animation
        // Trigger reflow by accessing offsetHeight
        wheel.offsetHeight; // This will force the browser to reflow the element
        wheel.style.animation = "spin 3s ease-in-out"; // Apply animation again

        // Simulate result after 3 seconds (time matches the spin duration)
        setTimeout(() => {
            // Update history or UI here
            alert("Result is available!");
            updateRollHistory();
        }, 3000);
    }

    // Handle Place Bet
    placeBetButton.addEventListener("click", () => {
        const betAmount = parseFloat(betAmountInput.value);
        const selectedOption = Array.from(betOptions).find(option => option.classList.contains("selected"));

        // Validate bet amount and selection
        if (isNaN(betAmount) || betAmount <= 0) {
            alert("Please enter a valid bet amount.");
            return;
        }

        if (betAmount > balance) {
            alert("Insufficient balance!");
            return;
        }

        if (!selectedOption) {
            alert("Please select a bet option.");
            return;
        }

        const multiplier = parseFloat(selectedOption.dataset.multiplier);
        balance -= betAmount;
        balanceElement.textContent = balance.toFixed(2);

        alert(`Bet placed on ${selectedOption.textContent} with ${betAmount}₱.`);

        // Reset inputs
        betAmountInput.value = '';
        selectedOption.classList.remove("selected");

        // Optionally send bet data to the server
        fetch('/api/place-bet/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ bet: betAmount, option: selectedOption.textContent }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Bet successfully recorded!");
                updateRollHistory();
            } else {
                alert("Error placing bet.");
            }
        })
        .catch(err => console.error("Error:", err));
    });

    // Handle bet option selection
    betOptions.forEach(option => {
        option.addEventListener("click", () => {
            betOptions.forEach(opt => opt.classList.remove("selected"));
            option.classList.add("selected");
        });
    });

    // Fetch and update roll history
    function updateRollHistory() {
        fetch('/api/roll-history/')
            .then(response => response.json())
            .then(data => {
                historyContainer.innerHTML = '';
                data.rolls.forEach(roll => {
                    const rollItem = document.createElement('div');
                    rollItem.textContent = `${roll.result} - Bet: ${roll.bet}`;
                    historyContainer.appendChild(rollItem);
                });
            })
            .catch(err => console.error("Error fetching roll history:", err));
    }

    // Start a new round
    startCountdown();
});
