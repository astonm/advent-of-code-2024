from util import *
import aoc

submit = aoc.for_day(5)


@click.group()
def cli():
    pass


def process_line(line):
    return list(map(ints, line.split("\n")))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    rules, updates = [process_line(l) for l in read_file(input, "\n\n")]

    def rules_violated(update):
        lookup = {n: i for (i, n) in enumerate(update)}
        for before, after in rules:
            if before in lookup and after in lookup:
                if lookup[before] > lookup[after]:
                    return True

    return submit.part(1, sum(u[len(u) // 2] for u in updates if not rules_violated(u)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    rules, updates = [process_line(l) for l in read_file(input, "\n\n")]

    cmp_table = defaultdict(dict)
    for before, after in rules:
        cmp_table[before][after] = -1
        cmp_table[after][before] = 1

    def rule_cmp(x, y):
        return cmp_table[x][y] if x != y else 0

    def rule_sort(update):
        return sorted(update, key=cmp_to_key(rule_cmp))

    ans = 0
    for update in updates:
        sorted_update = rule_sort(update)
        if update != sorted_update:
            ans += sorted_update[len(sorted_update) // 2]

    return submit.part(2, ans)


@cli.command()
@click.argument("input", type=click.File())
def part2_explicit_sort(input):
    rules, updates = [process_line(l) for l in read_file(input, "\n\n")]

    cmp_table = defaultdict(dict)
    for before, after in rules:
        cmp_table[before][after] = -1
        cmp_table[after][before] = 1

    def rule_sort(l):
        if not l:
            return l

        left, center, right = [], l[0], []
        for x in l[1:]:
            if cmp_table[x][center] < 0:
                left.append(x)
            else:
                right.append(x)

        return rule_sort(left) + [center] + rule_sort(right)

    ans = 0
    for update in updates:
        sorted_update = rule_sort(update)
        if update != sorted_update:
            ans += sorted_update[len(sorted_update) // 2]

    return submit.part(2, ans)


if __name__ == "__main__":
    cli()
