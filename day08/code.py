from util import *
import aoc

submit = aoc.for_day(8)


@click.group()
def cli():
    pass


def find_nearby_antinodes(n1, n2):
    n1, n2 = Vector(n1), Vector(n2)
    d = n2 - n1
    return tuple(n1 - d), tuple(n2 + d)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid(read_file(input))
    nodes = {p: c for p, c in grid.walk() if c != "."}

    antinodes = set()
    for node_type, node_positions in group_by(nodes, lambda x: nodes[x]):
        for n1, n2 in combinations(node_positions, 2):
            antinodes.update(find_nearby_antinodes(n1, n2))

    return submit.part(1, sum(1 for an in antinodes if an in grid))


def find_all_antinodes(n1, n2, grid):
    n1, n2 = Vector(n1), Vector(n2)
    d = n2 - n1

    out = set()

    p = n2
    while p in grid:
        out.add(tuple(p))
        p += d

    p = n1
    while p in grid:
        out.add(tuple(p))
        p -= d

    return out


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid(read_file(input))
    nodes = {p: c for p, c in grid.walk() if c != "."}

    antinodes = set()
    for node_type, node_positions in group_by(nodes, lambda x: nodes[x]):
        for n1, n2 in combinations(node_positions, 2):
            antinodes.update(find_all_antinodes(n1, n2, grid))

    return submit.part(2, len(antinodes))


if __name__ == "__main__":
    cli()
