from util import *
import aoc

submit = aoc.for_day(9)


@click.group()
def cli():
    pass


def process_line(line):
    return map(int, line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    disk_map = first(process_line(l) for l in read_file(input))

    ids = count()
    ops = deque()
    unplaced = deque()
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            ops.extend(["fwd"] * size)
            unplaced.extend([next(ids)] * size)
        else:
            ops.extend(["rev"] * size)

    blocks = []
    while unplaced:
        op = ops.popleft()
        block = unplaced.popleft() if op == "fwd" else unplaced.pop()
        blocks.append(block)

    return submit.part(1, sum(i * b for (i, b) in enumerate(blocks)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    disk_map = first(process_line(l) for l in read_file(input))

    File = fancytuple("id size")
    Gap = fancytuple("size")

    disk = []
    ids = count()
    files = []
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            file = File(id=next(ids), size=size)
            disk.append(file)
            files.append(file)
        else:
            disk.append(Gap(size=size))

    for file in reversed(files):
        move_from = first(i for i, item in enumerate(disk) if item is file)
        move_to = first(
            i
            for i, item in enumerate(disk)
            if type(item) is Gap and item.size >= file.size
        )

        if move_to is None or move_to > move_from:
            continue

        gap = disk[move_to]
        to_insert = [file]
        if file.size < gap.size:
            to_insert.append(Gap(size=gap.size - file.size))

        disk[move_from] = Gap(size=file.size)
        disk[move_to : move_to + 1] = to_insert

        # collapse adjacent gap, if any
        adj = move_to + 1
        maybe_double_gap = map(type, disk[adj : adj + 2])
        if maybe_double_gap == [Gap, Gap]:
            gap1 = disk[adj]
            gap2 = disk.pop(adj + 1)
            disk[adj] = Gap(size=gap1.size + gap2.size)

    checksum = 0
    positions = count()

    for item in disk:
        for _ in range(item.size):
            pos = next(positions)
            if type(item) is File:
                checksum += item.id * pos

    return submit.part(2, checksum)


if __name__ == "__main__":
    cli()
