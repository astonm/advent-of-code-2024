from util import *
import aoc

submit = aoc.for_day(15)


@click.group()
def cli():
    pass


DIRS = {
    "^": (0, -1),
    ">": (+1, 0),
    "v": (0, +1),
    "<": (-1, 0),
}


def get_move_path(grid, p, move):
    # path returned will be points for movable unit e.g. "@OOOOOO."
    assert grid.get(p) == "@"
    path = [p]

    d = DIRS[move]
    while grid.get((p[0] + d[0], p[1] + d[1]), None) == "O":
        p = (p[0] + d[0], p[1] + d[1])
        path.append(p)

    if grid.get((p[0] + d[0], p[1] + d[1]), None) == ".":
        path.append((p[0] + d[0], p[1] + d[1]))
        return path


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    parts = read_file(input, "\n\n")
    grid = Grid(list(map(list, parts[0].split("\n"))))
    moves = parts[1].replace("\n", "")

    robot = first(p for p, c in grid.walk() if c == "@")

    for move in moves:
        if path := get_move_path(grid, robot, move):
            for dst, src in pairwise(reversed(path)):
                grid.set(dst, grid.get(src))
                if src == path[0]:
                    robot = dst
            grid.set(path[0], ".")

    return submit.part(1, sum(x + 100 * y for (x, y), c in grid.walk() if c == "O"))


@dataclass
class Box:
    l: tuple
    r: tuple


def get_map(map_str):
    grid = Grid(list(map(list, map_str.split("\n"))))
    boxes = []
    for p, c in grid.walk():
        if c == "[":
            box = Box(
                (p[0] + 0, p[1]),
                (p[0] + 1, p[1]),
            )
            grid.set(box.l, ".")
            grid.set(box.r, ".")
            boxes.append(box)

        if c == "@":
            robot = p
            grid.set(p, ".")

    return grid, robot, boxes


def get_move_path_2d(grid, p, boxes, move):
    # will return robot position then boxes that will move, in adjacent layers
    path = [p]
    d = DIRS[move]
    force = [(p[0] + d[0], p[1] + d[1])]

    while True:
        next_layer = []
        for f in force:
            if grid.get(f) == "#":
                return None
            for box in boxes:
                if f in (box.l, box.r) and box not in next_layer:
                    next_layer.append(box)
        if not next_layer:
            break

        path.append(next_layer)

        if move == "^":
            force = [(p[0], p[1] - 1) for b in next_layer for p in (b.l, b.r)]
        elif move == "v":
            force = [(p[0], p[1] + 1) for b in next_layer for p in (b.l, b.r)]
        elif move == "<":
            force = [(b.l[0] - 1, b.l[1]) for b in next_layer]
        elif move == ">":
            force = [(b.r[0] + 1, b.r[1]) for b in next_layer]

    return path


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    parts = read_file(input, "\n\n")
    parts[0] = (
        parts[0]
        .replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    grid, robot, boxes = get_map(parts[0])
    moves = parts[1].replace("\n", "")

    def draw():
        printable = grid.copy()
        for box in boxes:
            printable.set(box.l, "[")
            printable.set(box.r, "]")
        printable.set(robot, "@")
        printable.print()

    for move in moves:
        path = get_move_path_2d(grid, robot, boxes, move)
        if path:
            d = DIRS[move]
            robot, box_layers = path[0], path[1:]
            robot = robot[0] + d[0], robot[1] + d[1]

            for layer in box_layers:
                for box in layer:
                    box.l = box.l[0] + d[0], box.l[1] + d[1]
                    box.r = box.r[0] + d[0], box.r[1] + d[1]
        # draw()

    draw()
    return submit.part(2, sum(b.l[0] + 100 * b.l[1] for b in boxes))


if __name__ == "__main__":
    cli()
