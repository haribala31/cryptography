import math
import random
from functools import lru_cache

# combinatorial nCk
def C(n, k):
    if k < 0 or k > n: 
        return 0
    return math.comb(n, k)

# Problem parameters
total_lanes = 25
bitrate_lanes = 1024 // 64   # = 16
capacity_lanes = total_lanes - bitrate_lanes  # = 9

# Precompute denominator: choose 16 of 25
denom = C(total_lanes, bitrate_lanes)

# Probability that, given s already-covered capacity lanes, exactly j new capacity lanes are hit
# There remain (capacity_lanes - s) uncovered capacity lanes.
def p_new_hits(s, j):
    remaining_capacity = capacity_lanes - s
    others = total_lanes - remaining_capacity
    numerator = C(remaining_capacity, j) * C(others, bitrate_lanes - j)
    return numerator / denom
E = [0.0] * (capacity_lanes + 1)
E[capacity_lanes] = 0.0

for s in range(capacity_lanes - 1, -1, -1):
    remaining = capacity_lanes - s
    p0 = p_new_hits(s, 0)
    sum_term = 0.0
    for j in range(1, remaining + 1):
        pj = p_new_hits(s, j)
        sum_term += pj * E[s + j]
    if 1 - p0 <= 0:
        E[s] = float('inf')
    else:
        E[s] = (1.0 + sum_term) / (1.0 - p0)

print("Analytic expected number of permutations (rounds) to hit all capacity lanes:")
print(f"  Starting from 0 covered capacity lanes -> E = {E[0]:.6f} rounds")
for s in range(capacity_lanes + 1):
    print(f"  E[{s}] (covered {s}/{capacity_lanes}) = {E[s]:.6f}")
def one_trial():
    targets = set(range(capacity_lanes))
    covered = set()
    rounds = 0
    while len(covered) < capacity_lanes:
        rounds += 1
        chosen = set(random.sample(range(total_lanes), bitrate_lanes))
        hit = targets.intersection(chosen)
        covered.update(hit)
    return rounds
trials = 200000
acc = 0
for _ in range(trials):
    acc += one_trial()
mc_mean = acc / trials
print(f"\nMonte-Carlo estimate over {trials} trials: mean rounds = {mc_mean:.6f}")
from collections import Counter
def distribution(trials=20000):
    cnt = Counter()
    for _ in range(trials):
        cnt[one_trial()] += 1
    for t in range(min(cnt)+0, max(cnt)+1):
        if t in cnt:
            print(f"  P(T = {t}) = {cnt[t]/trials:.4f}")
    return cnt
