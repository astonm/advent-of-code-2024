from util import *
import aoc

submit = aoc.for_day(21)


@click.group()
def cli():
    pass


DIRS = {
    "<": (-1, 0),
    ">": (+1, 0),
    "^": (0, -1),
    "v": (0, +1),
}


def get_keypad_graph(grid):
    out = defaultdict(dict)
    for p, start in grid.walk():
        for arrow, d in DIRS.items():
            end = grid.get((p[0] + d[0], p[1] + d[1]), ".")
            if end != ".":
                out[start][arrow] = end
    return dict(out)


def get_path_edges(start, end, graph):
    q = [(start, start, "")]
    best = float("inf")
    while q:
        curr_key, curr_path, curr_edges = q.pop(0)
        if curr_key == end:
            if len(curr_path) <= best:
                best = len(curr_path)
                yield curr_edges
            continue

        for next_edge, next_key in graph[curr_key].items():
            if next_key not in curr_path:
                q.append((next_key, curr_path + next_key, curr_edges + next_edge))


def make_keypad(pattern):
    def keypad(seq):
        out = []
        graph = get_keypad_graph(Grid(pattern.split("|")))
        for start, end in pairwise("A" + seq):
            edge_options = list(get_path_edges(start, end, graph))
            out.append(edge_options)

        for edge_parts in product(*out):
            yield "A".join(edge_parts) + "A"

    return keypad


numeric_keypad = make_keypad("789|456|123|.0A")
directional_keypad = make_keypad(".^A|<v>")


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = read_file(input)
    s = 0
    for seq in data:
        options = (
            outer
            for inner in numeric_keypad(seq)
            for middle in directional_keypad(inner)
            for outer in directional_keypad(middle)
        )
        best = min(options, key=len)
        print(seq, best)
        s += len(best) * int(seq[:-1])
    return submit.part(1, s)


@cache
def directional_iterated_length(seq, n):
    if n == 1:
        options = list(directional_keypad(seq))
        return min(len(r) for r in options)
    else:
        best = float("inf")
        for res in directional_keypad(seq):
            parts = res.split("A")[:-1]
            l = 0
            for part in parts:
                dl = directional_iterated_length(part + "A", n - 1)
                l += dl
            best = min(best, l)
        return best


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = read_file(input)
    s = 0
    for seq in data:
        l = float("inf")
        for x in numeric_keypad(seq):
            l = min(l, directional_iterated_length(x, 25))
        s += l * int(seq[:-1])
    return submit.part(2, s)


if __name__ == "__main__":
    cli()
