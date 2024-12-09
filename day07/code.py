from util import *
import aoc

submit = aoc.for_day(7)


@click.group()
def cli():
    pass


def process_line(line):
    nums = ints(line)
    return nums[0], nums[1:]


def evaluate(expr):
    out = expr[0]
    for op, n in grouper(expr[1:], 2):
        if op == "+":
            out += n
        elif op == "*":
            out *= n
        elif op == "||":
            out = int(str(out) + str(n))
        else:
            raise ValueError(op)
    return out


def find_ops(target, nums, all_ops):
    for ops in product(all_ops, repeat=len(nums) - 1):
        l = len(nums) * 2 - 1
        expr = [ops[i // 2] if i % 2 else nums[i // 2] for i in range(l)]
        if evaluate(expr) == target:
            return ops


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(1, sum(t for (t, nums) in data if find_ops(t, nums, ["+", "*"])))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    return submit.part(
        2, sum(t for (t, nums) in data if find_ops(t, nums, ["+", "*", "||"]))
    )


if __name__ == "__main__":
    cli()
