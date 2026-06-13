// ==UserScript==
// @name         DIVE AI
// @namespace    http://tampermonkey.net/
// @version      2026-06-10
// @description  A more optimized AI to play DIVE
// @author       Gracie 417
// @match        https://alexfink.github.io/dive/
// @icon         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTne--odO5x8GYoGxFsM2QuH4Bztd1hoCfDOokTCY9ZhYUadMGFHqwNoO4k98j6HMahikkBWCQ3FnBB6qOuSM5VoV1zfwVB1_hHTu72flXEQg&s=10
// @grant        none
// ==/UserScript==

window.g2m = function () {
    const a = window.game.grid.cells;
    var q = []
    for (var x = 0; x < 4; x++) {
        q.push([])
        for (var y = 0; y < 4; y++) {
            if (a[x][y] instanceof Tile) {
                q[x].push(a[x][y].value)
            } else {
                q[x].push(0)
            }
        }
    }
    return new MicroGame(q,window.game.tileTypes, window.game.score, false);
};

window.copy_game = function (game) {
    return new MicroGame(game.grid.map(row => [...row]),[...game.seeds],game.score, false)
}
window.conjugate = function (microgame) {
    var q = []
    for (var x = 0; x < 4; x++) {
        q.push([])
        for (var y = 0; y < 4; y++) {
            q[x].push(microgame.grid[y][x]);
        }
    }
    return new MicroGame(q,[...microgame.seeds],microgame.score, microgame.changed)
};
window.reverse = function (microgame) {
    var q = []
    for (var x = 0; x < 4; x++) {
        q.push([])
        for (var y = 0; y < 4; y++) {
            q[x].push(microgame.grid[x][3-y]);
        }
    }
    return new MicroGame(q,[...microgame.seeds],microgame.score, microgame.changed)
};
window.compress_mut = function (microgame) {
    for (let x = 0; x < 4; x++) {
        let row = microgame.grid[x]
        let write = 0;

        for (let read = 0; read < 4; read++) {
            if (row[read] !== 0) {
                if (read !== write) {
                    microgame.changed = true;
                }
                row[write++] = row[read];
            }
        }

        while (write < 4) {
            row[write++] = 0;
        }
    }
    return microgame
}
window.merge_mut = function (microgame) {
    for (var x = 0; x < 4; x++) {
        for (var y = 0; y < 3; y++) {
            var g = window.GCD(microgame.grid[x][y], microgame.grid[x][y+1])
            if (microgame.grid[x][y] !== 0 && microgame.grid[x][y+1] !== 0 && (g == microgame.grid[x][y] || g == microgame.grid[x][y+1])) {
                microgame.score += Math.min(microgame.grid[x][y],microgame.grid[x][y+1])
                microgame.changed = true;
                microgame.grid[x][y] += microgame.grid[x][y+1]
                var a = window.extractNewPrimes(microgame.grid[x][y], microgame.seeds)
                for (var qua = 0; qua < a.length; qua++) {
                    microgame.seeds.push(a[qua])
                }
                microgame.grid[x][y+1] = 0;
            }
        }
    }
    for (var i = microgame.seeds.length - 1; i >= 0; i--) {
        var bwa = 0;

        for (var X = 0; X < 4; X++) {
            for (var Y = 0; Y < 4; Y++) {
                if (microgame.grid[X][Y] % microgame.seeds[i] === 0) {
                    bwa = 1;
                }
            }
        }

        if (bwa === 0) {
            microgame.score += microgame.seeds[i];
            microgame.seeds.splice(i, 1);
        }
    }
    return microgame
}
window.comp_merge = function (microgame) {
    microgame.changed = false
    var q = window.compress_mut(window.merge_mut(window.compress_mut(window.copy_game(microgame))))
    return q
}
window.GCD = function (a, b) {
    if (a === 0 || b === 0) return 0;
    while(b){
        var temp = b
        b = a%b
        a = temp
    }
    return a;

}
window.extractPrimesFrom = function (tile, ind, seeds) {
    if (tile === 0) return 0;
    if (ind >= seeds.length) return tile;
    var min = window.extractPrimesFrom(tile, ind+1, seeds);
    while (tile % seeds[ind] == 0) {
        tile /= seeds[ind];
        var comparandum = window.extractPrimesFrom(tile, ind+1, seeds)
        if (comparandum < min)
            min = comparandum;
    }
    return min;
}
window.extractNewPrimes = function (tile, seeds) {
    tile = window.extractPrimesFrom(tile, 0, seeds)
    if (tile > 1) {
        return [tile];
    }
    return [];
};
window.micro_move = function (game, dir) {
    if (dir == 0) {
        return window.comp_merge(game)
    } else if (dir == 1) {
        return window.conjugate(window.reverse(window.comp_merge(window.reverse(window.conjugate(game)))))
    } else if (dir == 2) {
        return window.reverse(window.comp_merge(window.reverse(game)))
    } else if (dir == 3) {
        return window.conjugate(window.comp_merge(window.conjugate(game)))
    } else {
        return window.comp_merge(game)}
};
window.equalBoards = function (a, b) {
    var equality = true;
    for (var x = 0; x < 4; x++) {
        for (var y = 0; y < 4; y++) {
            if (a.grid[x][y] != b.grid[x][y]) {
                equality = false
            }
        }
    }
    return equality
}
window.maxindex = function (list) {
    var m = 0;
    var max = -9999;
    for (var i = 0; i < list.length; i++) {
        if (max < list[i]) {
            m = i
            max = list[i]
        }
    }
    return m
}
window.addTile = function (game, tilex, tiley, tileval) {
    if (game.changed) {
        var g = game.grid.map(row => [...row]);
        g[tilex][tiley] = tileval
    }
    return new MicroGame(g, [...game.seeds], game.score, game.changed);
}

const cache = new Map();

window.search = function(game, depth) {
    const key = game.hash + "|" + depth;

    if (cache.has(key)) {
        return cache.get(key);
    }

    if (depth === 0) {
        const result = [game.eval, -1];
        cache.set(key, result);
        return result;
    }

    let best = -Infinity;
    let bestDir = -1;

    for (let dir = 0; dir < 4; dir++) {
        const moved = window.micro_move(game, dir);
        if (moved.changed === false) continue;
        //if (moved.eval < best * .9) continue;
        const value = depth===1?window.search(moved,depth-1)[0]:window.expectNode(moved, depth - 1)[0] /*+ window.score(moved)*/;

        if (value > best) {
            best = value;
            bestDir = dir;
        }
    }
    if (best === -Infinity) {
        best = game.eval;
    }
    const result = [best, bestDir];
    cache.set(key, result);
    return result;
};
const expectCache = new Map();
window.expectNode = function (game, depth) {

    const key = game.hash + "|" + depth;
    if (expectCache.has(key)) {
        return [expectCache.get(key)];
    }
    let zeros = game.getZeros();

    let total = 0;
    let count = 0;

    if (zeros.length <= 6) {
        for (let z of zeros) {
            for (let s of game.seeds) {
                let g2 = window.addTile(game, z.x, z.y, s);
                let q = window.search(g2, depth)
                total += q[0];
                count++;
            }
        }
    } else {
       for (var i = 0; i < 4; i++) {
           var pos = zeros[Math.floor(Math.random() * zeros.length)]
           for (let s of game.seeds) {
                let g2 = window.addTile(game, pos.x, pos.y, s);
                let q = window.search(g2, depth)
                total += q[0];
                count++;
           }
       }
    }
    const result = total / count;
    expectCache.set(key, result);
    return [result];
}
window.DoBestMove = function (depth) {
    var g = window.search(window.g2m(),depth)
    console.log(g)
    window.game.move(g[1])
    return g
}
window.Run = function (searchdepth, timedelay) {
    console.time("test")
    console.log("ACTIVATING! •̀⩊•́")
    const h = setInterval(() => {
        var q = window.g2m()
        searchdepth = 3
        if (q.score > 6500) {
            searchdepth = 4
        }
        var g = window.search(q, searchdepth);
        console.log(g);

        if (g[1] === -1) {
            clearInterval(h);
            console.timeEnd("test")
            return;
        }

        window.game.move(g[1]);
    }, timedelay);
};

window.faux = function (searchdepth, debug=false) {
    function getBase() {
        var h = ""
        var g = window.g2m()
        for (let x = 0; x < 4; x++) {
            for (let y = 0; y < 4; y++) {
                if (g.grid[x][y] > 0) {
                    if (h.length === 0) {
                        h += x.toString() + "," + y.toString() + ","
                    } else {
                        h += x.toString() + "," + y.toString()
                    }
                }
            }
        }
        h += ";"
        return h
    }
    var base = window.g2m()
    var t = 0
    var temp = 0
    var g = [0,0]
    var stringy = getBase()
    console.time("faux")
    while (t < 10000) {
        g = window.search(base, searchdepth)
        stringy += g[1].toString() + ","
        if (g[1] === -1) {
            break
        }
        base = window.micro_move(base, g[1])
        var z = base.getZeros()
        var q = z[Math.floor(Math.random() * z.length)]
        stringy += q.x.toString() + "," + q.y.toString() + ","
        if (base.getZeros().length > 0) {
            var m = base.seeds[Math.floor(Math.random()*base.seeds.length)]
            stringy += m.toString() + ";"
            base = window.addTile(base, q.x, q.y, m)
        }
        t++
        if (t%100===0&&debug) {
            console.log(t, base);
        }
    }
    console.log(stringy)
    console.timeEnd("faux")
    return base
}

window.listify = function (searchdepth,num) {
    let list = []
    for (let i = 0; i < num; i++) {
        console.log(Math.round((100/num*i)).toString() + "% DONE")
        list.push(window.faux(searchdepth))
    }
    return list
}
window.avg = function (searchdepth,num) {
    console.log("AVG OF " + num.toString() + ": ", window.listify(searchdepth,num).reduce((sum,obj) => sum+obj.score, 0)/num)
}

class MicroGame {
    constructor(grid, seeds, score, changed) {
        this.grid = grid
        this.seeds = seeds
        this.score = score
        this.changed = changed
        this.hash = JSON.stringify(this.grid) + ":" + this.seeds.join(",");
        this.getZeros = function () {
            var q = []
            for (var x = 0; x < 4; x++) {
                for (var y = 0; y < 4; y++) {
                    if (this.grid[x][y] == 0) {
                        q.push({x:x,y:y})
                    }
                }
            }
            return q
        }
        this.getLargestTile = function () {
            var max = 0
            for (var x = 0; x < 4; x++) {
                for (var y = 0; y < 4; y++) {
                    if (this.grid[x][y] > max) {
                        max = this.grid[x][y]
                    }
                }
            }
            return max
        }
        this.eval = this.getZeros().length - 2*this.seeds.length
    }
};
