from util import *
import aoc

submit = aoc.for_day(1)


@click.group()
def cli():
    pass


def process_line(line):
    return ints(line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    left = sorted([d[0] for d in data])
    right = sorted([d[1] for d in data])
    return submit.part(1, sum(abs(x - y) for (x, y) in zip(left, right)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    left = [d[0] for d in data]
    right = Counter(d[1] for d in data)
    return submit.part(2, sum(l * right[l] for l in left))


if __name__ == "__main__":
    cli()
