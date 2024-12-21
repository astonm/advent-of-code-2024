from util import *
import aoc

submit = aoc.for_day(20)


@click.group()
def cli():
    pass


def process_line(line):
    return line


DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def find_path(start, end, grid):
    q = PriorityQueue()
    seen = set()
    q.put((start,))
    while not q.empty():
        curr_path = q.get()
        curr_pos = curr_path[-1]
        seen.add(curr_pos)

        if curr_pos == end:
            return curr_path

        for next_dir in DIRS:
            next_pos = curr_pos[0] + next_dir[0], curr_pos[1] + next_dir[1]
            next_path = curr_path + (next_pos,)

            if next_pos in seen:
                continue

            if grid.get(next_pos) == "#":
                continue

            q.put(next_path)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid(read_file(input))
    start = first(p for (p, c) in grid.walk() if c == "S")
    end = first(p for (p, c) in grid.walk() if c == "E")

    path = find_path(start, end, grid)
    pos_times = {p: t for (t, p) in enumerate(path)}

    res = []
    for p in path:
        for step1, step2 in product(DIRS, repeat=2):
            cheat1 = (p[0] + step1[0], p[1] + step1[1])
            cheat2 = (cheat1[0] + step2[0], cheat1[1] + step2[1])
            if grid.get(cheat1) == "#" and cheat2 in path and cheat2 != p:
                time_saved = pos_times[cheat2] - pos_times[p] - 2
                if time_saved > 0:
                    res.append((time_saved, (cheat1, cheat2)))

    if "ex" in input.name:
        cheats_by_delta = defaultdict(set)
        for delta, cheat in res:
            cheats_by_delta[time_saved].add((cheat1, cheat2))
        for delta, cheats in sorted(cheats_by_delta.items()):
            if delta > 0:
                print(f"There are {len(cheats)} cheats that save {delta} picoseconds.")

    return submit.part(1, sum(1 for delta, cheat in res if delta >= 100))


def cheat_reach(start, end, grid, max_cheats, cache={}):
    if abs(start[0] - end[0]) + abs(start[1] - end[1]) > max_cheats:
        return False

    dx = sign(end[0] - start[0])
    dy = sign(end[1] - start[1])

    seen = set()

    q = [(start, 0)]
    while q:
        curr_pos, curr_cheats = q.pop(0)

        if curr_pos == end:
            return curr_cheats

        adj = [(curr_pos[0] + dx, curr_pos[1]), (curr_pos[0], curr_pos[1] + dy)]
        for next_pos in adj:
            if next_pos in grid and next_pos not in seen:
                next_cheats = curr_cheats + 1
                if next_cheats <= max_cheats:
                    q.append((next_pos, next_cheats))
                    seen.add(next_pos)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid(read_file(input))
    start = first(p for (p, c) in grid.walk() if c == "S")
    end = first(p for (p, c) in grid.walk() if c == "E")
    min_saved = 50 if "ex" in input.name else 100

    path = find_path(start, end, grid)
    good_cheats = 0
    summary = Counter()
    for i, p in enumerate(path):
        for j, q in enumerate(path[i + 1 :], start=i + 1):
            if dist := cheat_reach(p, q, grid, 20):
                time_saved = j - i - dist
                if time_saved >= min_saved:
                    summary[time_saved] += 1
                    good_cheats += 1

    if "ex" in input.name:
        for delta, n in sorted(summary.items()):
            print(f"There are {n} cheats that save {delta} picoseconds.")

    return submit.part(2, good_cheats)


if __name__ == "__main__":
    cli()
