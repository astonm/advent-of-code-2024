from util import *
import aoc

submit = aoc.for_day(4)


@click.group()
def cli():
    pass


def process_line(line):
    return line


def match(grid, pattern, origin):
    for c, p in pattern:
        if grid.get((origin[0] + p[0], origin[1] + p[1]), None) != c:
            return False
    return True


def xmas_variations_part1():
    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        if dx == dy == 0:
            continue

        out = []
        p = (0, 0)
        for c in "XMAS":
            out.append((c, p))
            p = (p[0] + dx, p[1] + dy)

        yield out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid([process_line(l) for l in read_file(input)])
    matches = 0
    for p, _ in grid.walk():
        for v in xmas_variations_part1():
            if match(grid, v, p):
                matches += 1
    return submit.part(matches, matches)


def xmas_variations_part2():
    pattern = [
        ("M", (0, 0)),
        ("S", (2, 0)),
        ("A", (1, 1)),
        ("M", (0, 2)),
        ("S", (2, 2)),
    ]

    for rotations in range(4):
        out = []
        for c, p in pattern:
            for _ in range(rotations):
                p = -p[1], p[0]  # 90 degree rotation
            out.append((c, p))
        yield out


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid([process_line(l) for l in read_file(input)])
    matches = 0
    for p, _ in grid.walk():
        for v in xmas_variations_part2():
            if match(grid, v, p):
                matches += 1
    return submit.part(2, matches)


if __name__ == "__main__":
    cli()
