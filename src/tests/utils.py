import re


def strip_leading_spaces(text: str):
    if not text:
        return text

    text = text.splitlines()
    if not text[0]:
        text = text[1:]

    if not text[-1].strip():
        text = text[:-1]

    for line in text:
        if not line.strip():
            continue
        # We now have the first line
        indentation = len(re.search(r'^\s*', line).group())
        break
    else:
        raise ValueError(f"No non-empty lines in text {text!r}")

    result = []
    for i, line in enumerate(text):
        left, right = line[:indentation], line[indentation:]
        if left.strip():
            raise ValueError(f"Line {i + 1} {line.strip()!r} doesn't follow "
                             "text's indentation")
        result.append(right)
    return "\n".join(result)
