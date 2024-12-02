from util import *
import aoc

submit = aoc.for_day(2)


@click.group()
def cli():
    pass


def process_line(line):
    return ints(line)


def is_safe(levels):
    dl = deltas(levels)
    monotonic = all(sign(dl[0]) == sign(d) for d in dl)
    in_range = all(1 <= abs(d) <= 3 for d in dl)
    return monotonic and in_range


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(is_safe(report) for report in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    def options(levels):
        for i in range(len(levels)):
            yield levels[:i] + levels[i + 1 :]

    answer = sum(any(is_safe(o) for o in options(report)) for report in data)
    return submit.part(2, answer)


if __name__ == "__main__":
    cli()
