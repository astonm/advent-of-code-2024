from util import *
import aoc

submit = aoc.for_day(18)


@click.group()
def cli():
    pass


def process_line(line):
    return ints(line)


def get_square_grid(size):
    return Grid([list("." * size) for _ in range(size)])


def shortest_path(grid):
    start = 0, 0
    end = grid.width - 1, grid.height - 1

    seen = set()
    q = [(start, 0)]
    while q:
        curr_pos, curr_steps = q.pop(0)
        if curr_pos in seen:
            continue
        seen.add(curr_pos)

        if curr_pos == end:
            return curr_steps

        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_pos = curr_pos[0] + d[0], curr_pos[1] + d[1]
            if next_pos in grid and grid.get(next_pos) != "#" and next_pos not in seen:
                q.append((next_pos, curr_steps + 1))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    size = 71 if "input" in input.name else 7
    n = 1024 if "input" in input.name else 12

    grid = get_square_grid(size)
    data = [process_line(l) for l in read_file(input)]
    for p in data[:n]:
        grid.set(p, "#")

    submit.part(1, shortest_path(grid))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    size = 71 if "input" in input.name else 7

    grid = get_square_grid(size)
    data = [process_line(l) for l in read_file(input)]

    for x, y in data:
        grid.set((x, y), "#")
        if not shortest_path(grid):
            return submit.part(2, f"{x},{y}")


if __name__ == "__main__":
    cli()
