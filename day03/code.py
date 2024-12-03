from util import *
import aoc
import re

submit = aoc.for_day(3)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = "".join(read_file(input))
    pairs = re.findall(r"mul\((\d+),(\d+)\)", data)
    return submit.part(1, sum(int(x) * int(y) for x, y in pairs))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = "".join(read_file(input))
    insts = re.findall(r"(mul|do|don't)\(((\d+),(\d+))?\)", data)

    prods = []
    enabled = True
    for func, args, x, y in insts:
        if func == "do" and not args:
            enabled = True
        elif func == "don't" and not args:
            enabled = False
        elif func == "mul" and args:
            if enabled:
                prods.append(int(x) * int(y))

    return submit.part(2, sum(prods))


if __name__ == "__main__":
    cli()
