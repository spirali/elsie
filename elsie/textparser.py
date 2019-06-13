
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

    # Remove trailing empty lines
    if result and result[-1][0] == "newline":
        result.pop()
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
