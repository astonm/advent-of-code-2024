from util import *
import aoc

import networkx as nx

submit = aoc.for_day(23)


@click.group()
def cli():
    pass


def process_file(input):
    data = [l.split("-") for l in read_file(input)]
    graph = nx.Graph()
    for x, y in data:
        graph.add_edge(x, y)
    return graph


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    graph = process_file(input)
    clique3 = (c for c in nx.enumerate_all_cliques(graph) if len(c) == 3)
    return submit.part(1, sum(1 for c in clique3 if any(x[0] == "t" for x in c)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    graph = process_file(input)
    largest = max(nx.enumerate_all_cliques(graph), key=len)
    return submit.part(2, ",".join(sorted(largest)))


if __name__ == "__main__":
    cli()
