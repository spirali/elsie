from ..boxtree.lazy import eval_pair, unpack_point

COMMAND_NARGS = {"M": 1, "L": 1, "C": 3, "S": 2, "Q": 2, "T": 1}


def check_and_unpack_path_commands(commands, box):
    result = []
    for command in commands:
        if (
            not isinstance(command, tuple) and not isinstance(command, list)
        ) or not command:
            raise Exception("Invalid command: '{!r}'".format(command))
        name = command[0]
        nargs = COMMAND_NARGS.get(name)
        if nargs is None:
            raise Exception("Invalid command name: '{}'".format(name))
        if (len(command) - 1) % nargs != 0:
            raise Exception(
                "Invalid number of arguments for command '{}' (got {} arguments)".format(
                    name, len(command) - 1
                )
            )
        unpacked = tuple(unpack_point(p, box) for p in command[1:])
        result.append((name, unpacked))
    return result


def eval_path_commands(commands):
    result = []
    for name, pairs in commands:
        result.append((name, [eval_pair(p) for p in pairs]))
    return result


def path_points_for_end_arrow(commands):
    name, pairs = commands[-1]
    if name not in "CSQT":
        raise Exception(
            "Current version supports path when last command is 'C', 'S', 'Q' ot 'T' "
            "(got '{}')".format(name)
        )
    if len(pairs) >= 2:
        return pairs[-2], pairs[-1]
    if len(commands) >= 2:
        return commands[-2][1][-1], pairs[-1]
    else:
        raise Exception("Unsuported commands for end errow")


def path_update_end_point(commands, point):
    commands[-1][1][-1] = point
