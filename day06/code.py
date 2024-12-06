from util import *
import aoc

submit = aoc.for_day(6)


@click.group()
def cli():
    pass


def run_patrol(lab):
    start = next(p for p, c in lab.walk() if c == "^")

    p = Vector(start)
    v = Vector((0, -1))

    seen = set()
    while p in lab:
        record = (tuple(p), tuple(v))

        if record in seen:
            raise RuntimeError("Patrol stuck in loop!")
        else:
            seen.add(record)

        lab.set(p, "X")
        next_p = p + v
        while lab.get(next_p, None) in ("#", "O"):
            v = Vector([-v[1], v[0]])
            next_p = p + v
        p = next_p

    return set(p for p, v in seen)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    lab = Grid([list(line) for line in read_file(input)])
    return submit.part(1, len(run_patrol(lab)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    lab = Grid([list(line) for line in read_file(input)])

    orig = lab.copy()
    patrol_points = run_patrol(orig)

    loop_points = []
    for p in patrol_points:
        new_lab = lab.copy()
        if new_lab.get(p) == "^":
            continue

        new_lab.set(p, "O")
        try:
            run_patrol(new_lab)
        except:
            loop_points.append(p)

    return submit.part(2, len(loop_points))


if __name__ == "__main__":
    cli()
