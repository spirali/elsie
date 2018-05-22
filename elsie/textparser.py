
def number_of_lines(parsed_text):
    lines = 1
    for (token, value) in parsed_text:
        if token == "newline":
            lines += value
    return lines


def normalize_tokens(tokens):
    # Remove empty texts
    tokens = [kv for kv in tokens if kv[0] != "text" or kv[1]]

    # Merge lines
    i = 1
    while i < len(tokens):
        token_name, value = tokens[i]
        if token_name == "newline" and tokens[i - 1][0] == "newline":
            value2 = tokens[i - 1][1]
            del tokens[i]
            del tokens[i - 1]
            tokens.insert(i - 1, ("newline", value + value2))
            continue
        i += 1

    # Remove trailing empty lines
    if tokens and tokens[-1][0] == "newline":
        tokens = tokens[:-1]
    return tokens


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
            result.append(("end", None))
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
            final_result.append(("newline", 1))
            final_result.append(("text", line))
    if counter > 0:
        raise Exception("Invalid format, unclosed command")

    return normalize_tokens(final_result)
