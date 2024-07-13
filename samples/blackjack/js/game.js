// Card suits and values
const suits = ['♠', '♥', '♦', '♣'];
const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

// Game state variables
let deck = [];
let playerHand = [];
let dealerHand = [];
let gameOver = false;

// DOM elements
const playerHandElement = document.querySelector('#player-hand .cards');
const dealerHandElement = document.querySelector('#dealer-hand .cards');
const hitButton = document.getElementById('hit-button');
const standButton = document.getElementById('stand-button');
const newGameButton = document.getElementById('new-game-button');
const messagesElement = document.getElementById('messages');

// Initialize the game
function initGame() {
    messagesElement.textContent = "";
    deck = createDeck();
    shuffleDeck(deck);
    playerHand = [];
    dealerHand = [];
    gameOver = false;
    
    // Deal initial cards
    playerHand.push(drawCard(), drawCard());
    dealerHand.push(drawCard(), drawCard());
    
    updateUI();
    checkForBlackjack();
}

// Create a new deck of cards
function createDeck() {
    return suits.flatMap(suit => values.map(value => ({ suit, value })));
}

// Shuffle the deck using Fisher-Yates algorithm
function shuffleDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

// Draw a card from the deck
function drawCard() {
    return deck.pop();
}

// Calculate the value of a hand
function calculateHandValue(hand) {
    let value = 0;
    let aceCount = 0;
    
    for (const card of hand) {
        if (card.value === 'A') {
            aceCount++;
            value += 11;
        } else if (['K', 'Q', 'J'].includes(card.value)) {
            value += 10;
        } else {
            value += parseInt(card.value);
        }
    }
    
    // Adjust for Aces
    while (value > 21 && aceCount > 0) {
        value -= 10;
        aceCount--;
    }
    
    return value;
}

// Update the UI with current game state
function updateUI() {
    playerHandElement.innerHTML = '';
    dealerHandElement.innerHTML = '';
    
    playerHand.forEach(card => {
        playerHandElement.appendChild(createCardElement(card));
    });
    
    dealerHand.forEach((card, index) => {
        if (index === 0 || gameOver) {
            dealerHandElement.appendChild(createCardElement(card));
        } else {
            dealerHandElement.appendChild(createCardElement({ suit: '?', value: '?' }));
        }
    });
    
    hitButton.disabled = gameOver;
    standButton.disabled = gameOver;
}

// Create a card element for display
function createCardElement(card) {
    const cardElement = document.createElement('div');
    cardElement.className = 'card';
    cardElement.textContent = `${card.value}${card.suit}`;
    return cardElement;
}

// Check for blackjack at the start of the game
function checkForBlackjack() {
    const playerValue = calculateHandValue(playerHand);
    const dealerValue = calculateHandValue(dealerHand);
    
    if (playerValue === 21 && dealerValue === 21) {
        endGame("It's a tie! Both have Blackjack!");
    } else if (playerValue === 21) {
        endGame("Blackjack! You win!");
    } else if (dealerValue === 21) {
        endGame("Dealer has Blackjack! You lose.");
    }
}

// Player hits (draws a card)
function playerHit() {
    playerHand.push(drawCard());
    const playerValue = calculateHandValue(playerHand);
    
    updateUI();
    
    if (playerValue > 21) {
        endGame("You bust! Dealer wins.");
    } else if (playerValue === 21) {
        playerStand();
    }
}

// Player stands (ends turn)
function playerStand() {
    gameOver = true;
    
    // Dealer's turn
    let dealerValue = calculateHandValue(dealerHand);
    while (dealerValue < 17) {
        dealerHand.push(drawCard());
        dealerValue = calculateHandValue(dealerHand);
    }
    
    updateUI();
    
    // Determine winner
    const playerValue = calculateHandValue(playerHand);
    if (dealerValue > 21) {
        endGame("Dealer busts! You win!");
    } else if (dealerValue > playerValue) {
        endGame("Dealer wins!");
    } else if (dealerValue < playerValue) {
        endGame("You win!");
    } else {
        endGame("It's a tie!");
    }
}

// End the game and display result
function endGame(message) {
    gameOver = true;
    updateUI();
    messagesElement.textContent = message;
}

// Event listeners
hitButton.addEventListener('click', playerHit);
standButton.addEventListener('click', playerStand);
newGameButton.addEventListener('click', initGame);

// Start the game
initGame();