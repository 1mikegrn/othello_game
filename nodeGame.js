const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  });

//3 things to represent what state any square has at any given time: B, W, E
let gameBoard = [
  ["e", "e", "e", "e", "e", "e", "e", "e"],
  ["e", "e", "e", "e", "e", "e", "e", "e"],
  ["e", "e", "e", "e", "e", "e", "e", "e"],
  ["e", "e", "e", "w", "b", "e", "e", "e"],
  ["e", "e", "e", "b", "w", "e", "e", "e"],
  ["e", "e", "e", "e", "e", "e", "e", "e"],
  ["e", "e", "e", "e", "e", "e", "e", "e"],
  ["e", "e", "e", "e", "e", "e", "e", "e"],
];

for (i = 0; i < gameBoard.length; i++) {
  let row = "";
  for (p = 0; p < gameBoard[i].length; p++) {
    row += gameBoard[i][p];
    //NOT THIS ONE
  }
  console.log(row);
}

let blackPieces = 30;
let whitePieces = 30;

let player = "black";
let isWinner = false;

// Game Loop
while (!isWinner) {
  //take input from the user mkay
  readline.question(`Input please: `, userInput => {
    //is the input a valid move? 
    let move = userInput
    //nah bro 
    if(move)
    //tell the ppl nah pick something else
    // console.log(input)
    readline.close();
  });
  isWinner = true;
}


//there is a package that does this synchronously: https://www.npmjs.com/package/readline-sync