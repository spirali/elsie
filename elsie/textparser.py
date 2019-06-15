
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
