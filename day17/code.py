from util import *
import aoc

submit = aoc.for_day(17)


@click.group()
def cli():
    pass


def process_line(line):
    if line:
        vals = ints(line)
        if len(vals) == 1:
            return vals[0]
        else:
            return vals


def run_program(prg, reg, match=None):
    if "ip" not in reg:
        reg["ip"] = 0
    if "out" not in reg:
        reg["out"] = []

    def combo(x):
        if x < 4:
            return x
        if x == 4:
            return reg["A"]
        if x == 5:
            return reg["B"]
        if x == 6:
            return reg["C"]
        raise ValueError(x)

    Op = fancytuple("name f, dst")
    ops = {
        0: Op("adv", lambda x: reg["A"] // (2 ** combo(x)), "A"),
        1: Op("bxl", lambda x: reg["B"] ^ x, "B"),
        2: Op("bst", lambda x: combo(x) % 8, "B"),
        3: Op("jnz", lambda x: reg["ip"] if reg["A"] == 0 else x - 2, "ip"),  # -2+2=0
        4: Op("bxc", lambda x: reg["B"] ^ reg["C"], "B"),
        5: Op("out", lambda x: reg["out"] + [combo(x) % 8], "out"),
        6: Op("bdv", lambda x: reg["A"] // 2 ** combo(x), "B"),
        7: Op("cdv", lambda x: reg["A"] // 2 ** combo(x), "C"),
    }

    def repr_op(opcode, arg):
        op = ops[opcode]
        arg_val = combo(arg) if opcode not in (1, 3, 4) else arg
        return f"{op.name}({arg_val}) <- {opcode} {arg} ({bin(arg)[2:]})"

    while reg["ip"] < len(prg):
        opcode, arg = prg[reg["ip"] : reg["ip"] + 2]
        op = ops[opcode]
        reg[op.dst] = op.f(arg)
        reg["ip"] += 2
        if match and match[: len(reg["out"])] != reg["out"]:
            raise ValueError(f"unexpected output: {reg['out']}")

    return reg


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    reg = {
        "A": data[0],
        "B": data[1],
        "C": data[2],
        "ip": 0,
        "out": [],
    }
    prg = data[3]

    out = run_program(prg, reg)
    return submit.part(1, ",".join(str(o) for o in reg["out"]))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    prg = ints(read_file(input)[-1])

    def translated_program(a):
        out = []
        while a:
            b = a & 7
            b = b ^ 0b101
            c = a >> b
            b = b ^ 0b110
            a = a >> 3
            b = b ^ c
            out.append(b & 7)
        return out

    # verify i correctly pythonized my puzzle input from part 1
    assert translated_program(34615120) == [1, 2, 3, 1, 3, 2, 5, 3, 1]

    # the program relies just on A and operates
    # we should be able to solve for A one output at a time
    # working backwards, we can build A up incrementally
    A = 0
    for n in range(1, len(prg) + 1):
        exp = prg[-n:]
        for bits in count():  # i don't know why i need to go bigger than 0b111!
            A_try = A << 3 | bits
            out = translated_program(A_try)
            if out == exp:
                A = A_try
                break
        else:
            raise RuntimeError("failed to find good A bits")

    return submit.part(2, A)


if __name__ == "__main__":
    cli()
