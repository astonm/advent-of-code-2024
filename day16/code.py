from util import *
import aoc

submit = aoc.for_day(16)


@click.group()
def cli():
    pass


def process_line(line):
    return line


DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def best_paths(start, end, grid):
    curr_dir = (1, 0)

    q = PriorityQueue()
    q.put((0, start, curr_dir, (start,)))
    min_cost = defaultdict(lambda: float("inf"))
    while not q.empty():
        curr_cost, curr_pos, curr_dir, curr_path = q.get()
        min_cost[(curr_pos, curr_dir)] = min(min_cost[(curr_pos, curr_dir)], curr_cost)

        if curr_pos == end:
            if all(curr_cost <= min_cost[(curr_pos, d)] for d in DIRS):
                yield (curr_cost, curr_path)
            continue

        for next_dir in DIRS:
            next_cost = curr_cost + 1
            if next_dir != curr_dir:
                next_cost += 1000
            next_pos = curr_pos[0] + next_dir[0], curr_pos[1] + next_dir[1]
            next_path = curr_path + (next_pos,)
            valid_pos = next_pos in grid and grid.get(next_pos) != "#"

            if valid_pos and next_cost <= min_cost[(next_pos, next_dir)]:
                q.put((next_cost, next_pos, next_dir, next_path))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid(read_file(input))
    start = first(p for (p, c) in grid.walk() if c == "S")
    end = first(p for (p, c) in grid.walk() if c == "E")

    return submit.part(1, first(best_paths(start, end, grid))[0])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid(read_file(input))
    start = first(p for (p, c) in grid.walk() if c == "S")
    end = first(p for (p, c) in grid.walk() if c == "E")

    path_points = set()
    for _, path in best_paths(start, end, grid):
        path_points.update(path)
    return submit.part(2, len(path_points))


if __name__ == "__main__":
    cli()
