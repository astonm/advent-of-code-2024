from util import *
import aoc

submit = aoc.for_day(13)


@click.group()
def cli():
    pass


def process(desc):
    a, b, prize = desc.split("\n")
    return (
        parse("Button A: X+{dx:d}, Y+{dy:d}", a),
        parse("Button B: X+{dx:d}, Y+{dy:d}", b),
        parse("Prize: X={x:d}, Y={y:d}", prize),
    )


def find_cheapest(machine):
    a, b, prize = machine
    ways = []
    for a_press in range(101):
        for b_press in range(101):
            x = a["dx"] * a_press + b["dx"] * b_press
            y = a["dy"] * a_press + b["dy"] * b_press
            if x == prize["x"] and y == prize["y"]:
                price = 3 * a_press + b_press
                ways.append((price, a_press, b_press))
    return first(sorted(ways))


def find_cheapest_fast(machine, prize_offset=0):
    a, b, prize = machine
    prize = {"x": prize["x"] + prize_offset, "y": prize["y"] + prize_offset}

    # did some algebra...
    a_press_numer = prize["x"] - prize["y"] * Fraction(b["dx"], b["dy"])
    a_press_denom = a["dx"] - b["dx"] * Fraction(a["dy"], b["dy"])

    a_press = a_press_numer / a_press_denom
    b_press = (prize["y"] - a_press * a["dy"]) / b["dy"]

    if a_press.is_integer() and b_press.is_integer():
        return (3 * a_press + b_press, a_press, b_press)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process(m) for m in read_file(input, "\n\n")]
    cheapest_ways = map(find_cheapest, data)
    return submit.part(1, sum(w[0] for w in cheapest_ways if w))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process(m) for m in read_file(input, "\n\n")]
    cheapest_ways = [find_cheapest_fast(m, prize_offset=10000000000000) for m in data]
    return submit.part(2, sum(w[0] for w in cheapest_ways if w))


if __name__ == "__main__":
    cli()
