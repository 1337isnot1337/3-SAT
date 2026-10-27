"""Strict 3-CNF DIMACS reader and exponential reference counter for small inputs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CNF:
    nvars: int
    clauses: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if type(self.nvars) is not int or self.nvars < 0:
            raise ValueError("Declared variable count must be a nonnegative integer")
        object.__setattr__(self, "clauses", tuple(tuple(c) for c in self.clauses))
        for clause in self.clauses:
            if len(clause) > 3:
                raise ValueError("This reference reader accepts width at most three")
            for literal in clause:
                if type(literal) is not int or not 1 <= abs(literal) <= self.nvars:
                    raise ValueError("Literal is zero or outside the declared variables")


def parse_dimacs(text: str) -> CNF:
    header = None
    tokens: list[int] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("c"):
            continue
        parts = line.split()
        if parts[0] == "p":
            if header is not None or len(parts) != 4 or parts[1] != "cnf":
                raise ValueError("Expected one 'p cnf VARIABLES CLAUSES' header")
            try:
                header = (int(parts[2]), int(parts[3]))
            except ValueError as exc:
                raise ValueError("Header counts must be integers") from exc
            if min(header) < 0:
                raise ValueError("Header counts must be nonnegative")
        else:
            if header is None:
                raise ValueError("Clause data before header")
            try:
                tokens.extend(int(token) for token in parts)
            except ValueError as exc:
                raise ValueError("Expected integer literals and zero terminators") from exc
    if header is None:
        raise ValueError("Missing DIMACS header")
    clauses = []
    pending = []
    for token in tokens:
        if token == 0:
            clauses.append(tuple(pending))
            pending = []
        else:
            pending.append(token)
    if pending:
        raise ValueError("Unterminated clause")
    if len(clauses) != header[1]:
        raise ValueError("Clause count differs from header")
    return CNF(header[0], tuple(clauses))


def count(formula: CNF, *, max_variables: int = 20) -> int:
    if formula.nvars > max_variables:
        raise ValueError(f"Exhaustive reference limited to {max_variables} variables")
    total = 0
    for bits in range(1 << formula.nvars):
        if all(any(bool(bits & (1 << (abs(lit) - 1))) == (lit > 0)
                   for lit in clause) for clause in formula.clauses):
            total += 1
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", type=Path)
    parser.add_argument("--max-variables", type=int, default=20)
    args = parser.parse_args()
    try:
        result = count(parse_dimacs(args.formula.read_text()),
                       max_variables=args.max_variables)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(result)


if __name__ == "__main__":
    main()
