
END_MARKER = ("end", None)
NEWLINE_1 = ("newline", 1)


def number_of_lines(parsed_text):
    lines = 1
    for (token, value) in parsed_text:
        if token == "newline":
            lines += value
    return lines


def normalize_tokens(tokens):
    result = []

    for token in tokens:
        key, value = token
        if key == "text" and not value:
            continue  # Remove empty texts

        if key == "newline" and result and result[-1][0] == "newline":
            result[-1] = ("newline", result[-1][1] + value)
            continue

        result.append(token)

    if result:
        i = len(result) - 1
        while i >= 0 and result[i][0] == "end":
            i -= 1
        if i >= 0 and result[i][0] == "newline":
            del result[i]

    return result


def add_line_numbers(tokens):
    lines_len = len(str(number_of_lines(tokens)))
    begin = ("begin", "code_lineno")
    result = [begin, ("text", "1".zfill(lines_len) + " "), END_MARKER]
    line = 1
    for token in tokens:
        if token[0] != "newline":
            result.append(token)
            continue
        for i in range(token[1]):
            line += 1
            result.append(NEWLINE_1)
            result.append(begin)
            result.append(("text", str(line).zfill(lines_len) + " "))
            result.append(END_MARKER)
    return result


def parse_text(text, escape_char="~", begin_char="{", end_char="}"):
    result = []
    start = 0
    i = 0
    counter = 0
    while i < len(text):
        c = text[i]
        if c == escape_char:
            result.append(("text", text[start:i]))
            i += 1
            start = i
            while i < len(text) and text[i] != begin_char:
                i += 1
            result.append(("begin", text[start:i]))
            i += 1
            start = i
            counter += 1
        elif c == end_char and counter >= 1:
            result.append(("text", text[start:i]))
            result.append(END_MARKER)
            i += 1
            start = i
            counter -= 1
        else:
            i += 1
    if i != start:
        result.append(("text", text[start:i]))

    final_result = []
    for r in result:
        if r[0] != "text":
            final_result.append(r)
            continue
        lines = r[1].split("\n")
        final_result.append(("text", lines[0]))
        for line in lines[1:]:
            final_result.append(NEWLINE_1)
            final_result.append(("text", line))
    if counter > 0:
        raise Exception("Invalid format, unclosed command")

    return normalize_tokens(final_result)


def _open_blocks(tokens):
    blocks = []
    for token in tokens:
        if token[0] == "begin":
            blocks.append(token)
        elif token[0] == "end":
            blocks.pop()
    return blocks


def _open_blocks_count(tokens):
    count = 0
    for token in tokens:
        if token[0] == "begin":
            count += 1
        elif token[0] == "end":
            count -= 1
    return count


def _get_block_end_index(tokens, index):
    assert tokens[index][0] == "begin"
    index += 1
    count = 0

    while index < len(tokens):
        name, value = tokens[index]
        if name == "begin":
            count += 1
        elif name == "end":
            count -= 1
            if count < 0:
                return index
        index += 1


def extract_line(tokens, index):
    b = index
    while b >= 0 and tokens[b][0] != "newline":
        b -= 1
    b += 1

    e = index
    while e < len(tokens) and tokens[e][0] != "newline":
        e += 1

    open_blocks = _open_blocks(tokens[:b])
    result = open_blocks + tokens[b:e]
    result += [END_MARKER] * _open_blocks_count(result)
    return result, index - b + len(open_blocks)


def extract_styled_content(tokens, index):
    assert tokens[index][0] == "begin"
    start = index
    index += 1
    count = 0
    while index < len(tokens):
        name = tokens[index][0]
        if name == "end":
            count -= 1
            if count < 0:
                break
        elif name == "begin":
            count += 1
        break
        index += 1
    result = _open_blocks(tokens[:start]) + tokens[start:index + 1]
    return result + [END_MARKER] * _open_blocks_count(result)


def tokens_to_text_without_style(tokens):
    result = []
    for name, value in tokens:
        if name == "text":
            result.append(value)
        elif name == "newline":
            result.append("\n" * value)
    return "".join(result)


def tokens_merge(tokens1, tokens2):
    tokens = _tokens_merge_helper(tokens1, tokens2)
    result = []
    opened = []
    for token in tokens:
        if token[0] != "_block":
            result.append(token)
            continue

        _, index, t = token
        if t[0] == "begin":
            opened.append(token)
            result.append(t)
            continue
        assert t[0] == "end"
        reopen = []
        pos = -1
        for _, i2, t2 in reversed(opened):
            result.append(END_MARKER)
            if i2 != index:
                pos -= 1
                reopen.append(t2)
            else:
                break
        del opened[pos]
        result.extend(reopen)
    assert not opened
    return normalize_tokens(result)


def _tokens_merge_helper(tokens1, tokens2):
    result = []

    tokens = (tokens1, tokens2)
    last = [None, None]
    indices = [0, 0]
    stacks = ([], [])

    def read(i):
        index = indices[i]
        if index >= len(tokens[i]):
            last[i] = ("<END>", None)
        else:
            last[i] = tokens[i][index]
        indices[i] += 1
        return last[i]

    def new_block(i):
        result.append(("_block", i, last[i]))
        read(i)

    read(0)
    read(1)
    while True:
        ((n1, v1), (n2, v2)) = last

        if n1 == "end" and (n2 != "end" or stacks[0] > stacks[1]):
            stacks[0].pop()
            new_block(0)
            continue

        if n2 == "end":
            stacks[1].pop()
            new_block(1)
            continue

        if n1 == "begin":
            i1 = indices[0] - 1
            if n2 == "begin":
                # Find which block is shorter
                i2 = indices[1] - 1
                t1 = tokens_to_text_without_style(tokens[0][i1:_get_block_end_index(tokens[0], i1)])
                t2 = tokens_to_text_without_style(tokens[1][i2:_get_block_end_index(tokens[1], i2)])
                if len(t1) > len(t2):
                    stacks[0].append(i1)
                    new_block(0)
                    continue
            else:
                stacks[0].append(i1)
                new_block(0)
                continue

        if n2 == "begin":
            stacks[1].append(indices[0] - 1)
            new_block(1)
            continue

        if n1 == "<END>" or n2 == "<END>":
            assert n1 == "<END>" and n2 == "<END>"
            break

        if n1 == "newline" or n2 == "newline":
            assert n1 == "newline" and n2 == "newline"
            assert v1 == v2
            result.append(last[0])
            read(0)
            read(1)
            continue

        assert n1 == "text" and n2 == "text"
        if len(v1) == len(v2):
            result.append(last[0])
            read(0)
            read(1)
            continue

        if len(v1) < len(v2):
            result.append(last[0])
            read(0)
            last[1] = ("text", v2[len(v1):])
        else:
            result.append(last[1])
            read(1)
            last[0] = ("text", v1[len(v2):])
    return result