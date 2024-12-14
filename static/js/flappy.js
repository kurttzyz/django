    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    // Game variables
    let bird = { x: 150, y: canvas.height / 2, width: 40, height: 40, dy: 0, image: new Image() };
    bird.image.src = "/static/images/bird2.jpg/"; // Use a bird image sprite for realism
    let pipes = [];
    let moneyItems = []; // Array to hold money items
    let gravity = 0.3;  // Reduced gravity to slow down falling
    let pipeSpeed = 5;  // Slower pipe speed
    let score = 0;
    let gameActive = false;
    let lastTime = 0;
    let frameRate = 1000 / 60; // Frame rate: 60 fps (60 milliseconds per frame)
    let lastFrameTime = 0;
    // Background Image
    let bgImage = new Image();
    bgImage.src = "/static/images/2.jpg/"; // Add a background image to make the game visually appealing
    // Money Image
    let moneyImage = new Image();
    moneyImage.src = "/static/images/coin2.jpg";  // Path to coin image
    // Sound Effects
    let flapSound = new Audio('/static/audio/flap.mp3/');
    let scoreSound = new Audio('/static/audio/score.mp3');
    let hitSound = new Audio('/static/audio/music.mp3');
    flapSound.preload = "auto";
    scoreSound.preload = "auto";
    hitSound.preload = "auto";


    // Touch control
    canvas.addEventListener("touchstart", (e) => {
        if (gameActive) {
            bird.dy = -5;  // Slower flap
            flapSound.play(); // Play flap sound
        }
    });

    // Event listener for bird flap (keyboard fallback)
    document.addEventListener("keydown", (e) => {
        if (e.code === "Space" && gameActive) {
            bird.dy = -5;  // Slower flap
            flapSound.play(); // Play flap sound
        }
    });

     // Responsive canvas
     function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();


    // Used to clone the sound for better syncing 
    function playSound(sound) {
        const clone = sound.cloneNode();
        clone.play();
    }
   
    function playSoundImmediately(sound) {
        sound.currentTime = 0; // Reset playback to the start
        sound.play();
    }

    canvas.addEventListener("touchstart", (e) => {
        if (gameActive) {
            bird.dy = -5;  // Slower flap
            playSoundImmediately(flapSound); // Play flap sound with reduced delay
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.code === "Space" && gameActive) {
            bird.dy = -5;  // Slower flap
            playSoundImmediately(flapSound); // Play flap sound with reduced delay
        }
    });

    // Background Music
    let bgMusic = new Audio('/static/audio/background.mp3'); // Path to your background music
    bgMusic.loop = true; // Enable looping
    bgMusic.volume = 0.5; // Adjust volume as needed
    bgMusic.preload = "auto";

    function startGame() {
        bird.y = canvas.height / 2;
        bird.dy = 0;
        pipes = [];
        moneyItems = [];  // Reset money items
        score = 0;
        gameActive = true;
        document.getElementById("playAgain").style.display = "none";  // Hide the Play Again button
        document.getElementById("startGame").style.display = "none";  // Hide the Start Game button

        createPipes();

        // Play background music
        bgMusic.currentTime = 0; // Start from the beginning
        bgMusic.play();

        gameLoop();
    }

    function endGame() {
        gameActive = false;

        // Pause background music
        bgMusic.pause();

        document.getElementById("playAgain").style.display = "block";  // Show the Play Again button
        document.getElementById("startGame").style.display = "block";  // Show the Start Game button again
    }


    // Create pipes and money
    function createPipes() {
        const gap = 150;
        const pipeWidth = 50;
        const pipeX = canvas.width;

        const topPipeHeight = Math.random() * (canvas.height / 2);
        const bottomPipeY = topPipeHeight + gap;

        // Create pipe object
        pipes.push({
            x: pipeX,
            width: pipeWidth,
            topHeight: topPipeHeight,
            bottomY: bottomPipeY,
        });

        // Create money object (randomly positioned between top and bottom pipes)
        const moneyY = topPipeHeight + Math.random() * (bottomPipeY - topPipeHeight - 20);  // Random position within the gap
        moneyItems.push({
            x: pipeX + pipeWidth,  // Place money right after the pipe
            y: moneyY,
            width: 30,  // Money width
            height: 30,  // Money height
        });
    }

    // Update game state
    function updateGame() {
        if (!gameActive) return;

        // Update bird
        bird.dy += gravity;
        bird.y += bird.dy;

        // Check collisions with ground/ceiling
        if (bird.y <= 0 || bird.y + bird.height >= canvas.height) {
            hitSound.play(); // Play hit sound
            endGame();
        }

        // Update pipes
        pipes.forEach((pipe, index) => {
            pipe.x -= pipeSpeed;

            // Check for collisions with pipes
            if (
                bird.x + bird.width > pipe.x &&
                bird.x < pipe.x + pipe.width &&
                (bird.y < pipe.topHeight || bird.y + bird.height > pipe.bottomY)
            ) {
                hitSound.play(); // Play hit sound
                endGame();
            }

            // Remove off-screen pipes
            if (pipe.x + pipe.width < 0) {
                pipes.splice(index, 1);
                score++;
                scoreSound.play(); // Play score sound
            }
        });

        // Update money
        moneyItems.forEach((money, index) => {
            money.x -= pipeSpeed;

            // Check for collision with money (bird passing over it)
            if (
                bird.x + bird.width > money.x &&
                bird.x < money.x + money.width &&
                bird.y + bird.height > money.y && 
                bird.y < money.y + money.height
            ) {
                score += 10;  // Increase score for collecting money
                moneyItems.splice(index, 1);  // Remove collected money
            }

            // Remove off-screen money
            if (money.x + money.width < 0) {
                moneyItems.splice(index, 1);
            }
        });

        // Create new pipes and money
        if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 300) {
            createPipes();
        }

        // Render everything
        renderGame();
    }

    // Render game elements
    function renderGame() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw background
        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);

        // Draw bird with a smooth animation
        ctx.save();  // Save the current state
        ctx.translate(bird.x, bird.y); // Move to bird position
        ctx.rotate(bird.dy * 0.1); // Small rotation effect based on speed
        ctx.drawImage(bird.image, -bird.width / 2, -bird.height / 2, bird.width, bird.height);  // Draw bird centered
        ctx.restore();  // Restore to the previous state

        // Draw pipes with shadows for depth
        pipes.forEach((pipe) => {
            ctx.fillStyle = "green";
            ctx.shadowColor = "black";
            ctx.shadowBlur = 10;
            ctx.fillRect(pipe.x, 0, pipe.width, pipe.topHeight);
            ctx.fillRect(pipe.x, pipe.bottomY, pipe.width, canvas.height - pipe.bottomY);
            ctx.shadowBlur = 0; // Reset shadow
        });

        // Draw money
        moneyItems.forEach((money) => {
            ctx.drawImage(moneyImage, money.x, money.y, money.width, money.height);
        });

        // Draw score
        ctx.fillStyle = "white";
        ctx.font = "30px Arial";
        ctx.fillText(`Score: ${score}`, 20, 50);
    }

    function startGame() {
        bird.y = canvas.height / 2;
        bird.dy = 0;
        pipes = [];
        moneyItems = [];  // Reset money items
        score = 0;
        gameActive = true;
        document.getElementById("playAgain").style.display = "none";  // Hide the Play Again button
        document.getElementById("startGame").style.display = "none";  // Hide the Start Game button

        createPipes();
        gameLoop();
    }

    // End the game
    function endGame() {
        gameActive = false;
        document.getElementById("playAgain").style.display = "block";  // Show the Play Again button
        document.getElementById("startGame").style.display = "block";  // Show the Start Game button again
    }

    // Game loop with frame rate control
    function gameLoop(timestamp) {
        if (timestamp - lastFrameTime >= frameRate) {
            updateGame();
            lastFrameTime = timestamp;
        }
        if (gameActive) requestAnimationFrame(gameLoop);
    }

    // Event listeners
    document.getElementById("startGame").addEventListener("click", startGame);
    document.getElementById("playAgain").addEventListener("click", startGame);
