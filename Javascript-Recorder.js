// ==UserScript==
// @name         DIVE recorder
// @namespace    http://tampermonkey.net/
// @version      2026-03-12
// @description  a recording system for DIVE
// @author       Gracie 417
// @match        https://alexfink.github.io/dive/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.io
// @grant        none
// ==/UserScript==

// STUFF FOR REPLAYS

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

window.replay = function (rpstr, delay) {
    const moves = rpstr.split(";");
    let count = 0

    const interval = setInterval(() => {
        let info = moves[count].split(",");
        let move = Number(info[0]);
        let tile = new Tile({x:Number(info[1]),y:Number(info[2])},Number(info[3]));
        window.replayMove(window.game, move);
        window.game.grid.insertTile(tile);
        window.game.actuate()
        count++
        if (count >= moves.length-1) {
            clearInterval(interval)
        }}, delay);
};

