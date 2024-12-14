from util import *
import aoc

submit = aoc.for_day(14)


@click.group()
def cli():
    pass


Robot = fancytuple("p v")


def process_line(line):
    px, py, vx, vy = ints(line)
    return Robot(p=Vector([px, py]), v=Vector([vx, vy]))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    robots = [process_line(l) for l in read_file(input)]
    dim = (101, 103) if "input" in input.name else (11, 7)

    def move(robot, t):
        p = robot.p + t * robot.v
        return p[0] % dim[0], p[1] % dim[1]

    def quadrant(p):
        qw, qh = (dim[0] + 1) // 2, (dim[1] + 1) // 2
        if p[0] == qw - 1 or p[1] == qh - 1:
            return None
        else:
            return p[0] // qw + 2 * (p[1] // qh)

    quads = Counter()
    for robot in robots:
        pos = move(robot, 100)
        quads[quadrant(pos)] += 1
    return submit.part(1, quads[0] * quads[1] * quads[2] * quads[3])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    robots = [process_line(l) for l in read_file(input)]
    dim = (101, 103) if "input" in input.name else (11, 7)

    def step(robot):
        p = robot.p + robot.v
        return robot._replace(p=Vector([p[0] % dim[0], p[1] % dim[1]]))

    def draw():
        grid = GridN(default=" ")
        for robot in robots:
            grid.set(tuple(robot.p), "*")
        grid.print()

    def max_run_len(vals):
        prev = vals[0]
        max_run = run = 1
        for v in vals[1:]:
            if v == prev + 1:
                run += 1
            else:
                max_run = max(run, max_run)
                run = 1
            prev = v
        return max_run

    def has_horiz_line():
        by_y = groupby(robots, lambda r: r.p[1])
        for _, group in by_y:
            xs = sorted(set(r.p[0] for r in group))
            if xs and max_run_len(xs) > 10:
                return True

    for seconds in count(1):
        robots = [step(r) for r in robots]
        if has_horiz_line():
            draw()
            return submit.part(2, seconds)


if __name__ == "__main__":
    cli()
