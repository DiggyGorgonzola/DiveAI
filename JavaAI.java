import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 1; i++) {
            AVG(5, 50000, 10000, true);
        }
    }




    /* Runs N games and gives you metrics on them */
    public static String[] AVG(int searchDepth, int num, int threshold,boolean debug)  {
        ArrayList<String[]> GameArrayList = new ArrayList<>();
        int x2 = 0;
        int max = 0;
        for (int i = 0; i < num; i++) {
            if (i % 100 == 0) {
                cache1.clear();
                cache2.clear();
            }
            String[] h = Run(searchDepth, false);
            GameArrayList.add(h);
            int x = (int) Integer.parseInt(h[0])/threshold;
            if (x > x2) {
                x2 = x;
            }
            if (Integer.parseInt(h[0]) > max) {
                try {
                    Files.writeString(
                        Path.of("output.txt"),
                        h[0] + ":\n\n" + h[1]
                    );
                } catch (IOException e) {
                    e.printStackTrace();
                }
                max = Integer.parseInt(h[0]);
            }
            if (debug) {
                System.out.println(h[3] + " ms - " + h[2] + " moves - " + i + "/" + num + "*".repeat(Math.max(x,0)) + "         (" + "*".repeat(Math.max(x2,0)) + ")");
            }
        }

        GameArrayList.sort((a,b) -> Integer.compare(Integer.parseInt(a[0]), Integer.parseInt(b[0])));

        long totalruntime = 0;
        double totalscore = 1;
        int totalmoves = 0;
        int maxscore = Integer.parseInt(GameArrayList.get(GameArrayList.size()-1)[0]);
        int maxmoves = Integer.parseInt(GameArrayList.get(GameArrayList.size()-1)[3]);
        String rp = GameArrayList.get(GameArrayList.size()-1)[1];

        for (int i = 0; i < GameArrayList.size() - 1; i++) {
            String[] q = GameArrayList.get(i);
            totalscore *= Math.pow(Integer.parseInt(q[0]),(double) 1/num);
            totalmoves += Integer.parseInt(q[2]);
            totalruntime += Long.parseLong(q[3]);
        }

        System.out.println("\n\n");
        System.out.println(rp + "\n");
        System.out.println("M/S ratio for max score: " + maxscore/maxmoves);
        System.out.println("Max score reached: " + maxscore);
        System.out.print("\n");
        System.out.println("G. mean score of " + num + ": " + Double.toString(totalscore));
        System.out.print("\n");
        System.out.println("A. mean moves of " + num + ": " + Integer.toString(totalmoves / num));
        System.out.println("A. mean runtime: " + Long.toString(totalruntime / num) + " ms");
        return new String[]{"Hi"};
    }



    public static String[] Run(int searchDepth, boolean debug) {
        int[] grid = {
            2,0,0,0,
            0,0,2,0,
            0,0,0,0,
            0,0,0,0
        };
        ArrayList<Integer> seeds = new ArrayList<>();
        seeds.add(2);
        String hello = "0,0,1,2;";
        Game game = new Game(grid, seeds, 0, false, 0);
        Random rand = new Random();
        long time1 = System.nanoTime();
        while (!game.isOver()) {
            float[] g = doBestMove(game, searchDepth);
            game = MicroMove(game, (int) g[1]);
            hello += (int) g[1] + ",";
            int[][] zeros = game.getZeros();
            if (zeros.length > 0) {
                int a = game.seeds.get(rand.nextInt(game.seeds.size()));
                int[] b = zeros[rand.nextInt(zeros.length)];
                hello += b[0] + "," + b[1] + "," + a + ";";
                game = game.addTile(a,b[0],b[1]);
            } else {
                break;
            }
        }
        long time2 = System.nanoTime();
        long runtime = (time2 - time1) / (long) 1000000.0;
        return new String[]{Integer.toString(game.score), hello, Integer.toString(game.totalmoves), Long.toString(runtime)};

    }





    /* Game evaluation weights */
    private static final double EMPTY_CELLS = .02; // .02
    private static final double ADJ_EMPTY_CELLS = 0.02; // .02
    private static final double SCORE = 1.4; // 1.4
    private static final double SEED_RATIO = 1.5; // 1.5
    private static final double SEEDS_LENGTH = .033; // .033
    private static final double MOVE_TO_SCORE = 0.;
    private static final double ADJ_MERGES = 0;




    /* Game class */
    public static class Game {
        public int[] grid;
        public ArrayList<Integer> seeds;
        public int score;
        public boolean changed;
        public float eval;
        public boolean over;
        public int totalmoves;
        public Game(int[] grid, ArrayList<Integer> seeds, int score, boolean changed, int totalmoves) {
            this.grid = grid;
            this.seeds = seeds;
            this.score = score;
            this.changed = changed;
            this.totalmoves = totalmoves;
        }; 
        public String hash() {
            return Arrays.toString(grid) + "|" + seeds.toString();
        }
        public int getMerges() {
            int merges = 0;
            // x = i//4, y = i % 4
            for (int i = 0; i < 16; i++) {
                int[] coords = getCoords(i);
                if (coords[0] < 3) {
                    int g = gcd(grid[i], grid[i+4]);
                    if (g == grid[i] || g == grid[i+4]) {
                        merges++;                         
                    }                 
                }
                if (coords[1] < 3) {
                    int g = gcd(grid[i], grid[i+1]);
                    if (g == grid[i] || g == grid[i+1])
                        merges++;
                }
            }

            return merges;
        }
        public ArrayList<Integer>  uniqueTiles() {
            ArrayList<Integer> q = new ArrayList<>();
            for (int a : this.grid) {
                if (a > 0) {
                    q.add(a);
                }
            }
            ArrayList<Integer> h = new ArrayList<>();
            for (int x : q) {
                if (!h.contains(x)) {
                    h.add(x);
                }
            }
            h.sort(Integer::compareTo);
            return h;
        }
        public double evaluate() {
            /*
            ArrayList<Integer> a = this.uniqueTiles();
            int largest = a.get(a.size() - 1);
            int divisor = a.get(Math.min(1, a.size() - 1));
            */

            /*
            int max = seeds.get(0);
            for (int i = 1; i < seeds.size(); i++) {
                if (seeds.get(i) > max) {
                    max = seeds.get(i);
                }
            }*/
            ArrayList<Integer> v = new ArrayList<>();
            for (int s : seeds) {
                v.add(s);
            }
            v.sort(Integer::compareTo);
            double score = this.score;
            return
                EMPTY_CELLS * score * this.numZeros()
                + ADJ_EMPTY_CELLS * this.numAdjacentZeros(this.getLargest()) * score
                + SCORE * score
                + SEED_RATIO * v.get(this.seeds.size()-1) / v.get(Math.max(v.size()-2,0))
                - SEEDS_LENGTH * score * this.seeds.size()
                - ADJ_MERGES * score * this.getMerges()
                + MOVE_TO_SCORE * score / this.totalmoves

                ;
        }
        public int getLargest() {
            int max = 0;
            int pos = 0;
            for (int i = 0; i < 16; i++) {
                if (grid[i] > max) {
                    max = grid[i];
                    pos = i;
                }
            }
            return pos;
        }
        public int numAdjacentZeros(int pos) {
            int zeros = 0;
            for (int i = 0; i < 16; i++) {
                if (i + 4 == pos) {
                    zeros++;
                }
                else if (i - 4 == pos) {
                    zeros++;
                }
                else if (i + 1 == pos) {
                    zeros++;
                }
                else if (i - 1 == pos) {
                    zeros++;
                }
            }
            return zeros;
        }
        public boolean isOver() {
            return (this.getMerges() == 0 && this.numZeros() == 0);
        }
        public String printgrd() {
            String h = "";
            for (int i = 0; i < 16; i++) {
                int[] coords = getCoords(i);

                h += this.grid[i];
                if (coords[1] < 3) {
                    h += ",";
                } else {
                    h += "\n";
                }
            }
            return h;
        }
        public Game addTile(int tile, int x, int y) {
            Game g = this.copy();
            g.grid[x * 4 + y] = tile;
            return g;
        }
        public int numZeros() {
            int t = 0;
            for (int x = 0; x < 16; x++) {
                if (this.grid[x] == 0) {
                    t++;
                }
            }
            return t;
        }
        public int[][] getZeros() {
            java.util.List<int[]> zeros = new java.util.ArrayList<>();
            for (int i = 0; i < 16; i++) {
                if (this.grid[i] == 0) {
                    zeros.add(new int[] {FD(i,4), i%4});
                }
            }

            return zeros.toArray(new int[zeros.size()][]);
        }
        public Game copy() {
            int[] newGrid = new int[16];

            System.arraycopy(grid, 0, newGrid, 0, 16);

            return new Game(newGrid, new ArrayList<>(seeds), score, false, totalmoves);
        }
    };
    



    /* Stolen from Alex Fink */
    public static int extractPrimesFrom(int tile, int ind, ArrayList<Integer> seeds) {
        if (ind >= seeds.size()) {
            return tile;
        }
        if (tile == 0) {
            return 0;
        }

        int min = extractPrimesFrom(tile, ind + 1, seeds);

        while (tile % seeds.get(ind) == 0) {
            tile /= seeds.get(ind);
            int comparandum = extractPrimesFrom(tile, ind + 1, seeds);
            if (comparandum < min) {
                min = comparandum;
            }
        }
        return min;
    }



    public static int[] extractNewPrimes(int tile, ArrayList<Integer> seeds) {
        tile = extractPrimesFrom(tile, 0, seeds);
        if (tile > 1) {
            return new int[] { tile };
        }
        return new int[0];
    };
    

    
    
    /*misc */
    public static int[] getCoords(int i) {
        int[] a = {FD(i,4), i%4};
        return a;
    }
    
    
    
    public static int FD(float a,float b) {
        return (int) Math.floor(a/b);
    }
    
    
    
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return Math.abs(a);
    }




    /* move functions */
    public static Game conjugate(Game microgame) {
        int[] q = new int[16];
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                q[x * 4 + y] = microgame.grid[y * 4 + x];
            }
        }
        return new Game(q,new ArrayList<>(microgame.seeds),microgame.score, microgame.changed, microgame.totalmoves);
    };



    public static Game reverse(Game microgame) {
        int[] q = new int[16];
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                q[x * 4 + y] = microgame.grid[x * 4 + (3 - y)];
            }
        }
        return new Game(q,new ArrayList<>(microgame.seeds),microgame.score, microgame.changed, microgame.totalmoves);
    };



    public static Game compress_mut(Game microgame) {
        for (int row = 0; row < 4; row++) {
            int rowStart = row * 4;
            int write = 0;

            for (int read = 0; read < 4; read++) {
                int value = microgame.grid[rowStart + read];

                if (value != 0) {
                    if (read != write) {
                        microgame.changed = true;
                    }

                    microgame.grid[rowStart + write] = value;
                    write++;
                }
            }

            while (write < 4) {
                microgame.grid[rowStart + write] = 0;
                write++;
            }
        }

        return microgame;
    }
    
    
    
    public static Game merge_mut(Game game) {
        ArrayList<Integer> seeds = new ArrayList<>();
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 3; y++) {
                int left = game.grid[x*4 + y];
                int right = game.grid[x*4 + y + 1];

                if (left == 0 || right == 0) {
                    continue;
                }

                int g = gcd(left, right);
                if (g != left && g != right) {
                    continue;
                }

                game.score += Math.min(left, right);
                game.changed = true;

                int mergedValue = left + right;
                game.grid[x*4 + y] = mergedValue;
                game.grid[x*4 + y + 1] = 0;

                int[] newPrimes = extractNewPrimes(mergedValue, game.seeds);
                for (int prime : newPrimes) {
                    if (!seeds.contains(prime)) {
                        seeds.add(prime);
                    }
                }
            }
        }
        game.seeds.addAll(seeds);
        for (int i = game.seeds.size() - 1; i >= 0; i--) {
            boolean found = false;
            for (int x = 0; x < 4; x++) {
                for (int y = 0; y < 4; y++) {
                    if (game.grid[x * 4 + y] > 0 && game.grid[x * 4 + y] % game.seeds.get(i) == 0) {
                        found = true;
                        break;
                    }
                }
            }
            if (!found) {
                game.score += game.seeds.get(i);
                game.seeds.remove(i);
            }
        }
        return game;
    }
    
    
    
    public static Game compress_merge(Game microgame) {
        return compress_mut(merge_mut(compress_mut(microgame)));
    }
    
    
    
    public static Game MicroMove(Game game, int dir) {
        Game g = game.copy();
        g.totalmoves++;
        switch (dir) {
            case 0:
                return compress_merge(g);
            case 1:
                return conjugate(reverse(compress_merge(reverse(conjugate(g)))));
            case 2:
                return reverse(compress_merge(reverse(g)));
            case 3:
                return conjugate(compress_merge(conjugate(g)));
            default:
                g.totalmoves--;
                return g;
        }
    }
    
    

    public static float[] doBestMove(Game game, int depth) {
        float[] guh = Search(game, depth);
        return guh;
    }




    
    /* expectimax algorithm */
    private static final Map<String, float[]> cache1 = new HashMap<>();
    private static final Map<String, float[]> cache2 = new HashMap<>();



    public static float[] Search(Game game, int depth) {
        if (depth == 0) {
            float[] result = {(float) game.evaluate(), -1};
            return result;
        }
        String a = game.hash() + depth;
        if (cache1.containsKey(a)) {
            float[] r = cache1.get(a);
            return new float[]{r[0], r[1]};
        }
        float[] guh = {Float.NEGATIVE_INFINITY, -1};
        for (int dir = 0; dir < 4; dir++) {
            Game moved = MicroMove(game, dir);

            if (!moved.changed) {
                continue;
            }

            float score = (float)(expectNode(moved, depth - 1) + (float) (depth/50+ 1) * moved.evaluate());
            if (score > guh[0]) {
                guh = new float[]{score, dir};
            }
        };
        cache1.put(a, guh);
        return guh;
        };
    
    
    
    public static float expectNode(Game game, int depth) {
        String a = game.hash() + depth;
        if (cache2.containsKey(a)) {
            return cache2.get(a)[0];
        }
        float total = 0;
        int count = 0;
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                if (game.grid[x * 4 + y] == 0) {
                    for (int s : game.seeds) {
                        game.addTile(s,x, y);
                        float[] q = Search(game, depth);
                        game.grid[x * 4 + y] = 0;
                        total += q[0];
                        count++;
                    }
                }
            }
        }
        float result = count>0?total / count:Float.NEGATIVE_INFINITY;
        cache2.put(a, new float[]{result});
        return result;
    }
}

