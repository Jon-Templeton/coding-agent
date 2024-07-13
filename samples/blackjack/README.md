# Blackjack Game

This is a simple web-based Blackjack game implemented using HTML, CSS, and JavaScript.

## How to Play

1. Open the `index.html` file in a web browser to start the game.
2. The game starts automatically with two cards dealt to you and two to the dealer (one face down).
3. Your goal is to get as close to 21 points as possible without going over.
4. Card values:
   - Number cards (2-10) are worth their face value.
   - Face cards (Jack, Queen, King) are worth 10 points.
   - Aces are worth 11 points, but can be reduced to 1 point if it prevents going over 21.
5. You have two options on your turn:
   - Hit: Draw another card to increase your hand's value.
   - Stand: End your turn and let the dealer play.
6. If your hand goes over 21 points, you "bust" and lose the game.
7. After you stand, the dealer reveals their hidden card and must hit until their hand is worth at least 17 points.
8. The winner is determined as follows:
   - If you have Blackjack (21 points with two cards), you win unless the dealer also has Blackjack.
   - If the dealer busts, you win.
   - If neither busts, the hand closest to 21 wins.
   - If both hands have the same value, it's a tie.
9. Click the "New Game" button to start a new round at any time.

## Features

- Simple and intuitive user interface
- Automatic card dealing and score calculation
- Dealer AI that follows standard Blackjack rules
- Responsive design for various screen sizes

Enjoy playing Blackjack!
