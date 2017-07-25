from typing import List, Dict, Iterable


def sniff_col_indexes(line: str):
    indexes = list(reversed([i0 + 1 for (i0, v0), v1 in reversed(list(zip(enumerate(line), line[1:] + ' ')))
                             if v0 != ' ' and v1 == ' ']))
    return indexes


def parse_fixed_width(lines: List[str]):
    col_indexes = sniff_col_indexes(lines[0])
    return [[line[i0:i1].strip() for i0, i1 in zip([0] + col_indexes, col_indexes)] + [line[col_indexes[-1]:]]
            for line in lines]


def to_float(string_list: Iterable[str]) -> List[float]:
    floats = []
    for element in string_list:
        try:
            floats.append(float(element))
        except ValueError:
            floats.append(None)
    return floats
