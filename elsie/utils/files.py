def read_helper(source):
    if isinstance(source, str):
        with open(source, "rb") as f:
            return f.read()
    elif isinstance(source, bytes):
        return source
    else:
        return source.read()
