from util import *
import aoc

submit = aoc.for_day(22)


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


def secrets(seed, n):
    out = [seed]
    val = seed
    for _ in range(n):
        val ^= val * 64
        val %= 16777216
        val ^= val // 32
        val %= 16777216
        val ^= val * 2048
        val %= 16777216
        out.append(val)
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(last(secrets(x, 2000)) for x in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    buyer_prices = [[s % 10 for s in secrets(x, 2000)] for x in data]
    buyer_deltas = list(map(deltas, buyer_prices))

    totals = Counter()
    for buyer, ds in enumerate(buyer_deltas):
        seen = set()
        for price_ind, seq in enumerate(windowed(ds, 4), start=4):
            if seq not in seen:
                seen.add(seq)
                totals[seq] += buyer_prices[buyer][price_ind]

    return submit.part(2, totals.most_common()[0][1])


if __name__ == "__main__":
    cli()
