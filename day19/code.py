from util import *
import aoc

submit = aoc.for_day(19)


@click.group()
def cli():
    pass


def process_file(file):
    towels, *patterns = read_file(file)
    return towels.split(", "), patterns


def pattern_graph(target, options):
    def get_next(curr):
        for o in options:
            val = curr + o
            if len(val) <= len(target) and target[: len(val)] == val:
                yield val

    return get_next


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    towels, patterns = process_file(input)

    c = 0
    for pattern in patterns:
        graph = graph_from_func(pattern_graph(pattern, towels))
        if count_paths("", pattern, graph):
            c += 1

    return submit.part(1, c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    towels, patterns = process_file(input)

    c = 0
    for pattern in patterns:
        graph = graph_from_func(pattern_graph(pattern, towels))
        c += count_paths("", pattern, graph)

    return submit.part(2, c)


if __name__ == "__main__":
    cli()
