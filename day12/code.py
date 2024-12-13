from util import *
import aoc

submit = aoc.for_day(12)


@click.group()
def cli():
    pass


def process_line(line):
    return line


def get_regions(g):
    grouped = set()
    regions = []

    def get_region(p):
        val = g.get(p)
        region = []

        q = [p]
        enqueued = set()
        while q:
            curr = q.pop(0)
            if g.get(curr) != val:
                continue

            grouped.add(curr)
            region.append(curr)

            for n in g.neighbors(curr):
                if n not in grouped and n not in enqueued:
                    q.append(n)
                    enqueued.add(n)

        return region

    for p, _ in g.walk():
        if p not in grouped:
            region = get_region(p)
            grouped.update(region)
            regions.append(region)
    return regions


def get_perimeter(region):
    # count lines on the outside
    lines = Counter()
    dl = [
        ((0, 0), (1, 0)),
        ((0, 0), (0, 1)),
        ((1, 0), (1, 1)),
        ((0, 1), (1, 1)),
    ]
    for p in region:
        for dl1, dl2 in dl:
            line = (
                (p[0] + dl1[0], p[1] + dl1[1]),
                (p[0] + dl2[0], p[1] + dl2[1]),
            )
            lines[line] += 1

    return [l for l in lines if lines[l] == 1]


def get_num_sides(region, debug=False):
    # same as number of corners
    perimeter = get_perimeter(region)

    dirs = defaultdict(set)
    touches = Counter()

    for line in perimeter:
        dl = line[1][0] - line[0][0], line[1][1] - line[0][1]
        for p in line:
            dirs[p].add("horizontal" if dl[0] else "vertical")
            touches[p] += 1

    # 2 dirs => right turn => corner
    # 2 touches per corner, except if it's a corner twice and gets 4 touches
    return sum(touches[p] // 2 for p in dirs if len(dirs[p]) == 2)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = Grid(read_file(input))
    regions = get_regions(data)

    return submit.part(1, sum(len(r) * len(get_perimeter(r)) for r in regions))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = Grid(read_file(input))
    regions = get_regions(data)

    return submit.part(2, sum(len(r) * get_num_sides(r) for r in regions))


if __name__ == "__main__":
    cli()
