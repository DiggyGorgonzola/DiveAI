// ==UserScript==
// @name         DIVE recorder
// @namespace    http://tampermonkey.net/
// @version      2026-03-14
// @description  a recording system for DIVE
// @author       Gracie 417
// @match        https://alexfink.github.io/dive/
// @icon         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTne--odO5x8GYoGxFsM2QuH4Bztd1hoCfDOokTCY9ZhYUadMGFHqwNoO4k98j6HMahikkBWCQ3FnBB6qOuSM5VoV1zfwVB1_hHTu72flXEQg&s=10
// @grant        none
// ==/UserScript==
console.log(`
-=-DIVE replay system-=-

window.replay(delay, rpstr):
    Plays back the replay provided
    - delay is how many milliseconds between each move
    - rprstr is the replay string

window.showReplay():
    Prints to the console the current game's replay string

`);
var replay_string = "";
var string_a = "";
var string_b = "";

const box = document.createElement("div");
box.innerText = replay_string;

box.style.position = "fixed";
box.style.bottom = "20px";
box.style.right = "20px";
box.style.padding = "15px";
box.style.background = "#bbada0";
box.style.color = "#fff";
box.style.borderRadius = "10px";
box.style.zIndex = "9999";
box.style.boxShadow = "0 0 10px rgba(0,0,0,0.3)";

document.body.appendChild(box);

window.replayMove = function (board, direction) {
    // 0: up, 1: right, 2:down, 3: left
  var self = board;

  if (board.over || board.won) return; // Don't do anything if the game's over

  var cell, tile;

  var vector     = board.getVector(direction);
  var traversals = board.buildTraversals(vector);
  board.moved     = false;
  var newPrimes  = [];

  // Save the current tile positions and remove merger information
  board.prepareTiles();

  var ominosityBound;
  if (self.gameMode && 1) {
    // The idea of this is that a seed is ominous roughly if it exceeds
    // the 2i-th prime, if there are i seeds so far.
    // But add a little more, to be forgiving.
    ominosityBound = self.tileTypes.length * 2;
    ominosityBound *= Math.log(ominosityBound);
    ominosityBound += 8;
  }

  // Traverse the grid in the right direction and move tiles
  traversals.x.forEach(function (x) {
    traversals.y.forEach(function (y) {
      cell = { x: x, y: y };
      tile = self.grid.cellContent(cell);
      if (tile) {
        var positions = self.findFarthestPosition(cell, vector);
        var next      = self.grid.cellContent(positions.next);

        // Only one merger per row traversal?
        if (next && self.div(next.value, tile.value) > 0 && !next.mergedFrom) {
          var merged = new Tile(positions.next, self.div(next.value, tile.value));
          merged.mergedFrom = [tile, next];

          self.grid.insertTile(merged);
          self.grid.removeTile(tile);

          // Converge the two tiles' positions
          tile.updatePosition(positions.next);

          // Update the score
          self.score += Math.min(next.value, tile.value);

          // Unlock new primes, if in that mode
          if (self.gameMode & 1) {
            var primes = self.extractNewPrimes(merged.value);
            newPrimes = newPrimes.concat(primes);
          }
        } else { // if (tile)
          self.moveTile(tile, positions.farthest);
        }

        if (!self.positionsEqual(cell, tile)) {
          self.moved = true; // The tile moved from its original cell!
        }
      }
    });
  });

  if (self.gameMode & 1) {
    // remove duplicates
    if (newPrimes.length >= 2) {
      newPrimes.sort(function (a,b){return a-b});
      for (var i = newPrimes.length - 2; i >= 0; i--)
        if (newPrimes[i] == newPrimes[i+1])
          newPrimes.splice(i,1);
    }
    self.tileTypes = self.tileTypes.concat(newPrimes);
  }

  if (this.moved) {
    if ((self.gameMode & 1) && newPrimes.length) {
      // in mode 1, score for unlocking
      if ((self.gameMode & 3) == 1) {
        self.score += newPrimes.reduce(function(x,y){return x+y});
      }

      self.tilesSeen.push.apply(self.tilesSeen, newPrimes);

      var verb = " unlocked!";
      if (newPrimes.filter(function(x){return x > ominosityBound}).length)
        verb = " unleashed!";
      var list = String(newPrimes.pop());
      if (newPrimes.length) {
        list = newPrimes.join(", ") + " and " + list;
      }
      self.actuator.announce(list + verb);
      self.actuator.updateCurrentlyUnlocked(self.tileTypes);
    } // mode 1 only

    if ((self.gameMode & 3) == 3) {
      // Eliminate primes now absent.
      var eliminatedIndices = [];
      for (var i = 0; i < self.tileTypes.length; i++)
        eliminatedIndices.push(i);

      traversals.x.forEach(function (x) {
        traversals.y.forEach(function (y) {
          cell = { x: x, y: y };
          tile = self.grid.cellContent(cell);
          if (tile) {
            for(var i = 0; i < self.tileTypes.length; i++) {
              if (tile.value % self.tileTypes[i] == 0)
                eliminatedIndices[i] = null;
            }
          }
        });
      });

      eliminatedIndices = eliminatedIndices.filter(function (x) {return x != null});
      if (eliminatedIndices.length) {
        var eliminatedPrimes = eliminatedIndices.map(function (x) {return self.tileTypes[x]});
        self.score += eliminatedPrimes.reduce(function(x,y){return x+y});

        var verb = " eliminated!"
        if (eliminatedPrimes.filter(function(x){return x > ominosityBound}).length)
          verb = " vanquished!";
        var list = String(eliminatedPrimes.pop());
        if (eliminatedPrimes.length) {
          list = eliminatedPrimes.join(", ") + " and " + list;
        }
        self.actuator.announce(list + verb);
        self.actuator.updateCurrentlyUnlocked(self.tileTypes);
      }

      for(var i = eliminatedIndices.length - 1; i >= 0; i--)
        self.tileTypes.splice(eliminatedIndices[i],1);
      self.actuator.updateCurrentlyUnlocked(self.tileTypes);
    } // mode 3

    if (!this.movesAvailable()) { // Game over!
      if ((this.gameMode & 3) == 3)
        this.over = { tileTypes: this.tileTypes,
                      tilesSeen: this.tilesSeen };
      else
        this.over = {};
    }

    board.actuate();
  } // if (moved)
};

window.replay = function (delay, rpstr) {
    const moves = rpstr.split(";");
    let count = 0
    let gameReplay = new GameManager(4, KeyboardInputManager, HTMLActuator, LocalScoreManager);
    gameReplay.grid.cells = [
        [null,null,null,null],
        [null,null,null,null],
        [null,null,null,null],
        [null,null,null,null],
        ]
    var k = moves[0].split(",");
    for (var i = 0; i <= k.length/2; i += 2) {
        var x = k[i]
        var y = k[i+1]
        gameReplay.grid.insertTile(new Tile({x:Number(x),y:Number(y)},2));
    };
    const interval = setInterval(() => {
        count++
        if (count >= moves.length-1) {
            clearInterval(interval)
            return
        }
        let info = moves[count].split(",");
        let move = Number(info[0]);
        let tile = new Tile({x:Number(info[1]),y:Number(info[2])},Number(info[3]));
        window.replayMove(gameReplay, move);


        gameReplay.grid.insertTile(tile);
        gameReplay.actuate()
        }, delay);
};


function GameWrapper() {
    if (!window.game) {
        requestAnimationFrame(GameWrapper);
        return
    }
    const originalMove = window.game.move;
    const originalART = window.game.addRandomTile;
    window.game.move = function (...args) {
        if (!window.game.over && !window.game.won) {
            var grid_before = []
            for (var x = 0; x < window.game.grid.cells.length; x++) {
                grid_before.push([]);
                for (var y = 0; y < window.game.grid.cells[x].length; y++) {
                    grid_before[x].push(window.game.grid.cells[x][y]);
                };
            };
            originalMove.apply(this, args);
            var moved = false;
            window.game.grid.eachCell(function (x,y,tile) {
                if (grid_before[x][y] !== window.game.grid.cells[x][y]) {
                    moved = true;
                }
            });

            //console.log("MOVED: ",moved);

            if (moved) {
                string_a = `${args[0]},`;
                replay_string += string_a
                replay_string += string_b
            }
        }
        //console.log(replay_string);
        if (window.game.over || window.game.won) {
            console.log(`REPLAY STRING:\n\n${replay_string}`)
        }
    };
    window.game.addRandomTile = function () {
        var a = window.game.grid.randomAvailableCell()
        var value = window.game.tileTypes[Math.floor(Math.random() * window.game.tileTypes.length)];
        var tile = new Tile(a, value);
        window.game.grid.insertTile(tile);
        string_b = `${a.x},${a.y},${value};`;
    };
    window.game.addStartTiles = function () {
        var tempstring = "";
        for (var i = 0; i < window.game.startTiles; i++) {
            var a = window.game.grid.randomAvailableCell()
            var value = window.game.tileTypes[Math.floor(Math.random() * window.game.tileTypes.length)];
            var tile = new Tile(a, value);
            tempstring += `${a.x},${a.y}`;
            window.game.grid.insertTile(tile);
            if (i < window.game.startTiles - 1) {
                tempstring += ",";
            };
        }
        tempstring += ";";
        replay_string += tempstring;
    };

    window.game.restart();
    window.game.inputManager.events.move = [];
    window.game.inputManager.on("move", window.game.move.bind(window.game));
};
GameWrapper();

window.showReplay = function () {
    console.log(replay_string);
};
