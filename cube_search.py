"""3x3 Rubik's Cube as a search problem (OOP). Same logic as ../app.js.
State: tuple of 54 sticker colours. Action: one of 12 quarter turns (U U' R R' F F' D D' L L' B B')."""
import heapq, math, random, time

FACES = "URFDLB"
NORM = [(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, -1, 0), (-1, 0, 0), (0, 0, -1)]
NAMES = [f + p for f in FACES for p in ("", "'")]
LARGE = 10000.0  # GA hyper-parameter: reward for reaching the goal


def _rot(v, a, s):
    u, w = (a + 1) % 3, (a + 2) % 3
    r = list(v)
    r[u], r[w] = (v[w], -v[u]) if s > 0 else (-v[w], v[u])
    return tuple(r)


def _build():
    axis = lambda n: next(i for i in range(3) if n[i])
    st = [((x, y, z), n, f) for f, n in enumerate(NORM)
          for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1)
          if (x, y, z)[axis(n)] == n[axis(n)]]
    idx = {(c, n): i for i, (c, n, _) in enumerate(st)}
    perms = []
    for n in NORM:
        a = axis(n)
        for s in (n[a], -n[a]):  # clockwise, then counter-clockwise
            perms.append([idx[(_rot(c, a, s), _rot(nn, a, s))] if c[a] == n[a] else i
                          for i, (c, nn, _) in enumerate(st)])
    return tuple(f for _, _, f in st), perms


SOLVED, PERMS = _build()


class Cube:
    """Environment: states, actions, transition, goal test, step cost (=1) and heuristic."""
    def __init__(self, s=SOLVED): self.s = tuple(s)

    def move(self, m):
        out = [0] * 54
        for i, c in enumerate(self.s): out[PERMS[m][i]] = c
        return Cube(out)

    def play(self, seq):
        c = self
        for m in seq: c = c.move(m)
        return c

    def goal(self): return self.s == SOLVED                                   # Boolean goal test
    def misplaced(self): return sum(a != b for a, b in zip(self.s, SOLVED))   # conflict number
    def h(self): return self.misplaced() / 20  # admissible: a quarter turn fixes at most 20 stickers

    @staticmethod
    def scramble(k, rng):
        seq = []
        while len(seq) < k:
            m = rng.randrange(12)
            if not seq or m != seq[-1] ^ 1: seq.append(m)
        return seq


def result(path, n, t): return {"path": path, "expanded": n, "ms": round((time.time() - t) * 1000), "found": path is not None}


class Searcher:
    """Uninformed, informed and local search. Every method returns a result dict."""
    def __init__(self, limit=200000): self.limit = limit

    def best_first(self, start, kind="astar", w=1.0):  # kind: bfs | ucs | greedy | astar
        t, tie, n = time.time(), 0, 0
        pq, seen = [(0, 0, start, [])], {start.s: 0}
        while pq and n < self.limit and len(pq) < 3 * self.limit:  # frontier cap protects memory
            _, _, c, path = heapq.heappop(pq)
            if c.goal(): return result(path, n, t)
            n += 1
            for m in range(12):
                if path and m == path[-1] ^ 1: continue
                d, g = c.move(m), len(path) + 1
                if seen.get(d.s, 99) <= g: continue
                seen[d.s] = g; tie += 1
                pr = {"bfs": tie, "ucs": g, "greedy": d.h(), "astar": g + w * d.h()}[kind]
                heapq.heappush(pq, (pr, tie, d, path + [m]))
        return result(None, n, t)

    def bidir(self, start):  # bidirectional BFS: grow both frontiers, meet in the middle
        t, n = time.time(), 0
        if start.goal(): return result([], 0, t)
        A, B = {start.s: []}, {SOLVED: []}
        qa, qb = [(start, [])], [(Cube(), [])]
        while (qa or qb) and len(A) + len(B) < 3 * self.limit:
            fw = bool(qa) and (len(qa) <= len(qb) or not qb)
            q, me, ot, nq = (qa, A, B, []) if fw else (qb, B, A, [])
            for c, p in q:
                n += 1
                for m in range(12):
                    if p and m == p[-1] ^ 1: continue
                    d = c.move(m)
                    if d.s in me: continue
                    me[d.s] = p + [m]
                    if d.s in ot:
                        f, b = (me[d.s], ot[d.s]) if fw else (ot[d.s], me[d.s])
                        return result(f + [x ^ 1 for x in reversed(b)], n, t)
                    nq.append((d, p + [m]))
            if fw: qa = nq
            else: qb = nq
        return result(None, n, t)

    def ids(self, start, max_depth=6):  # iterative deepening (depth-limited DFS inside)
        t, cnt = time.time(), [0]
        def dls(c, path, d):
            if c.goal(): return path
            if d == 0 or cnt[0] >= self.limit: return None
            for m in range(12):
                if path and m == path[-1] ^ 1: continue
                cnt[0] += 1
                r = dls(c.move(m), path + [m], d - 1)
                if r is not None: return r
        for d in range(max_depth + 1):
            r = dls(start, [], d)
            if r is not None: return result(r, cnt[0], t)
        return result(None, cnt[0], t)

    def ida(self, start, max_depth=8):  # IDA*: depth-first with f = g + h threshold
        t, cnt = time.time(), [0]
        def go(c, path, th):
            f = len(path) + c.h()
            if f > th: return f
            if c.goal(): return path
            nxt = 1e9
            for m in range(12):
                if path and m == path[-1] ^ 1: continue
                if cnt[0] >= self.limit: return nxt
                cnt[0] += 1
                r = go(c.move(m), path + [m], th)
                if isinstance(r, list): return r
                nxt = min(nxt, r)
            return nxt
        th = start.h()
        while th <= max_depth:
            r = go(start, [], th)
            if isinstance(r, list): return result(r, cnt[0], t)
            if cnt[0] >= self.limit: break
            th = math.ceil(r - 1e-9) if r > th + 1e-9 else th + 1
        return result(None, cnt[0], t)

    def hill_climb(self, start, rng, steps=400, sideways=5):  # steepest ascent + sideways + random kicks
        t, c, path, side = time.time(), start, [], 0
        for _ in range(steps):
            if c.goal(): break
            best = min(range(12), key=lambda m: (c.move(m).misplaced(), rng.random()))
            gain = c.misplaced() - c.move(best).misplaced()
            if gain < 0 or (gain == 0 and side >= sideways): best, side = rng.randrange(12), 0  # restart kick
            else: side += gain == 0
            c = c.move(best)
            if path and path[-1] == best ^ 1: path.pop()
            else: path.append(best)
        return result(path if c.goal() else None, len(path), t)

    def anneal(self, start, rng, steps=20000, t0=3.0, cool=0.9995):
        t, c, T, path = time.time(), start, t0, []
        for _ in range(steps):
            if c.goal(): break
            m = rng.randrange(12); d = c.move(m); dE = d.misplaced() - c.misplaced()
            if dE <= 0 or rng.random() < math.exp(-dE / T):
                c = d
                if path and path[-1] == m ^ 1: path.pop()
                else: path.append(m)
            T *= cool
        return result(path if c.goal() else None, steps, t)


class GA:
    """Genetic algorithm. Individual = fixed-length list of actions."""
    def __init__(self, start, rng, pop=200, length=12, gens=150, pc=0.9, pm=0.08, elite=2,
                 select="tournament", k=4, cross="two", conflict_w=10):
        self.__dict__.update(locals()); del self.__dict__["self"]

    def evaluate(self, ind):  # -> (fitness, conflicts, cost, path)
        c, best, step = self.start, (self.start.misplaced(), 0), 0
        if c.goal(): return LARGE, 0, 0, []
        for i, m in enumerate(ind, 1):
            c = c.move(m)
            if c.goal(): return LARGE - i, 0, i, ind[:i]       # goal reached: big number - path cost
            best = min(best, (c.misplaced(), i))
        return LARGE / 2 - self.conflict_w * best[0] - best[1], best[0], None, None  # big/2 - conflicts - cost

    def select_pairs(self, pop):  # calls fitness itself; fitness -> probability (roulette) or tournament; len/2 parent pairs
        r = self.rng
        self.ev = [self.evaluate(x) for x in pop]; fit = [e[0] for e in self.ev]
        if self.select == "roulette":
            lo = min(fit); cum = list(__import__("itertools").accumulate(f - lo + 1e-9 for f in fit))
            pick = lambda: pop[next(i for i, a in enumerate(cum) if a >= r.random() * cum[-1])]
        else:
            pick = lambda: pop[max(r.sample(range(len(pop)), self.k), key=lambda i: fit[i])]
        pairs = []
        for _ in range(len(pop) // 2):
            a = pick(); b = pick()
            for _ in range(5):
                if b is not a: break
                b = pick()
            pairs.append((a, b))
        return pairs

    def crossover(self, a, b):
        n, r = len(a), self.rng
        i, j = sorted(r.sample(range(1, n), 2)) if self.cross == "two" else (r.randrange(1, n), n)
        return a[:i] + b[i:j] + a[j:], b[:i] + a[i:j] + b[j:]

    def mutate(self, ind): return [self.rng.randrange(12) if self.rng.random() < self.pm else g for g in ind]

    def run(self):
        r, t = self.rng, time.time()
        pop = [[r.randrange(12) for _ in range(self.length)] for _ in range(self.pop)]
        hist, best = [], None
        for g in range(self.gens):
            pairs = self.select_pairs(pop); ev = self.ev; fit = [e[0] for e in ev]
            top = max(range(len(pop)), key=lambda i: fit[i])
            if ev[top][2] is not None and (best is None or ev[top][2] < len(best)): best = ev[top][3]
            hist.append((max(fit), sum(fit) / len(fit), ev[top][1]))
            kids = []
            for a, b in pairs:
                c1, c2 = self.crossover(a, b) if r.random() < self.pc else (a[:], b[:])
                kids += [self.mutate(c1), self.mutate(c2)]
            elite = [pop[i][:] for i in sorted(range(len(pop)), key=lambda i: -fit[i])[:self.elite]]
            pop = elite + kids[:self.pop - self.elite]
        out = result(best, self.gens * self.pop, t); out["history"] = hist
        return out


if __name__ == "__main__":
    rng = random.Random(7)
    scr = Cube.scramble(4, rng); start = Cube().play(scr)
    print("scramble:", " ".join(NAMES[m] for m in scr))
    S = Searcher()
    runs = {"BFS": S.best_first(start, "bfs"), "UCS": S.best_first(start, "ucs"), "Bidirectional": S.bidir(start), "IDS": S.ids(start),
            "Greedy": S.best_first(start, "greedy"), "A*": S.best_first(start, "astar"), "IDA*": S.ida(start),
            "Hill climbing": S.hill_climb(start, rng), "Annealing": S.anneal(start, rng),
            "GA": GA(start, rng, length=10).run()}
    for k, v in runs.items():
        print(f"{k:14}", "found" if v["found"] else "fail ", "len", len(v["path"]) if v["found"] else "-", "nodes", v["expanded"], f'{v["ms"]}ms')
