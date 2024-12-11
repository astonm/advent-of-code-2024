from util import *
import aoc

submit = aoc.for_day(11)


@click.group()
def cli():
    pass


def process_line(line):
    return ints(line)


def blink(stones):
    out = []
    for stone in stones:
        sstone = str(stone)
        if stone == 0:
            out.append(1)
        elif len(sstone) % 2 == 0:
            out.append(int(sstone[: len(sstone) // 2]))
            out.append(int(sstone[len(sstone) // 2 :]))
        else:
            out.append(stone * 2024)
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    stones = first([process_line(l) for l in read_file(input)])
    for _ in range(25):
        stones = blink(stones)
    return submit.part(1, len(stones))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    memo = {}
    stones = first([process_line(l) for l in read_file(input)])

    def count_stones(stone, blinks):
        sstone = str(stone)
        key = (stone, blinks)
        if key in memo:
            return memo[key]

        if blinks == 0:
            return 1

        if stone == 0:
            out = count_stones(1, blinks - 1)
        elif len(sstone) % 2 == 0:
            l = int(sstone[: len(sstone) // 2])
            r = int(sstone[len(sstone) // 2 :])
            out = count_stones(l, blinks - 1) + count_stones(r, blinks - 1)
        else:
            out = count_stones(stone * 2024, blinks - 1)

        memo[key] = out
        return out

    return submit.part(2, sum(count_stones(s, 75) for s in stones))


if __name__ == "__main__":
    cli()
