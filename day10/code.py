from util import *
import aoc

submit = aoc.for_day(10)


@click.group()
def cli():
    pass


def process_line(line):
    return list(map(int, line))


def count_trails(topo_map, start, seen):
    c = 0
    curr_val = topo_map.get(start)

    if curr_val == 9:
        return 1

    for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        next_node = start[0] + d[0], start[1] + d[1]
        next_val = topo_map.get(next_node, None)
        if next_node not in seen and next_val == curr_val + 1:
            seen.add(next_node)
            c += count_trails(topo_map, next_node, seen)

    return c


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    topo_map = Grid([process_line(l) for l in read_file(input)])
    trailheads = [p for p, c in topo_map.walk() if c == 0]

    return submit.part(1, sum(count_trails(topo_map, th, set()) for th in trailheads))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    topo_map = Grid([process_line(l) for l in read_file(input)])
    trailheads = [p for p, c in topo_map.walk() if c == 0]

    class Empty(set):  # a set that never adds anything
        def add(self, x):
            pass

    return submit.part(2, sum(count_trails(topo_map, th, Empty()) for th in trailheads))


if __name__ == "__main__":
    cli()
