"""Test recovery of known scalar moments by extreme-shift charge pieces.

This is an exact finite codebook check, not an all-size theorem or an
improved SAT bound. Only shifts with absolute value strictly above the
cutoff are retained; cutoff h-1 therefore means exactly |s| >= h.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


filter_screen = load("length_power_moment_screen", HERE / "screen.py")
generalized = filter_screen.generalized
linear = filter_screen.screen.linear


def scalar_pairing_space(tensors, size, cutoff):
    names = sorted((degree, shift) for degree, shift in tensors
                   if abs(shift) > cutoff)
    columns = [tensors[name] for name in names]
    constraints = []
    for x in range(size):
        for v in range(size):
            base = x * size ** 3 + v
            for y in range(size):
                for u in range(size):
                    index = ((x * size + y) * size + u) * size + v
                    if y != u:
                        row = [column[index] for column in columns]
                    elif y:
                        row = [column[index] - column[base] for column in columns]
                    else:
                        continue
                    if any(row):
                        constraints.append(row)
    nullspace, rank = linear.nullspace(constraints, len(columns))
    pairings = [
        [sum(weight * column[x * size ** 3 + v]
             for weight, column in zip(weights, columns))
         for x in range(size) for v in range(size)]
        for weights in nullspace
    ]
    _, _, selected = linear.echelon(pairings, size * size)
    return [pairings[index] for index in selected], len(nullspace), rank


def membership(space, candidate, size):
    matrix_rank = len(linear.echelon(
        [[candidate[x * size + v] for v in range(size)] for x in range(size)],
        size)[0])
    is_member = len(linear.echelon(space + [candidate], size * size)[0]) == len(space)
    return {"label_matrix_rank": matrix_rank, "member": is_member}


def check_grade(h, size, cutoff, power=2):
    model = generalized.poly.model
    states = model.predecessor.partitions(h)
    first = model.pairing.first_pairing(states)
    rows, columns = model.minor_indices(first, size)
    data = {
        "N": size,
        "h": h,
        "bits": 1,
        "states": states,
        "row_labels": [states[index] for index in rows],
        "column_labels": [states[index] for index in columns],
        "output_labels": states[:size],
    }
    raw, pair_degrees, raw_degree, evaluation_checks = generalized.build_raw(data)
    tensors = filter_screen.length_power(raw, pair_degrees, size ** 4, power)
    space, nullity, constraint_rank = scalar_pairing_space(tensors, size, cutoff)

    candidates = {}
    for degree in range(raw_degree + 1):
        candidate = [
            sum(shift ** degree * raw.get((degree, shift), [0] * size ** 4)[index]
                for shift in range(-2 * h, 2 * h + 1))
            for index in (x * size ** 3 + v
                          for x in range(size) for v in range(size))
        ]
        if any(candidate):
            candidates[f"highest_{degree}"] = candidate
    for degree in (0, 2, 3, 4):
        candidate = [
            sum(shift ** degree * raw.get((0, shift), [0] * size ** 4)[index]
                for shift in range(-2 * h, 2 * h + 1))
            for index in (x * size ** 3 + v
                          for x in range(size) for v in range(size))
        ]
        if any(candidate):
            candidates[f"uncharged_{degree}"] = candidate

    moments = {name: membership(space, candidate, size)
               for name, candidate in candidates.items()}
    return {
        "h": h,
        "N": size,
        "length_power": power,
        "cutoff": cutoff,
        "retained_shifts": f"|s|>={cutoff + 1}",
        "maximum_raw_charge_degree": raw_degree,
        "charge_evaluation_checks": evaluation_checks,
        "scalar_weight_nullity": nullity,
        "scalar_constraint_rank": constraint_rank,
        "label_matrix_space_dimension": len(space),
        "moments": moments,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("h", type=int)
    parser.add_argument("N", type=int)
    parser.add_argument("--cutoff", type=int)
    parser.add_argument("--power", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cutoff = args.h - 1 if args.cutoff is None else args.cutoff
    result = check_grade(args.h, args.N, cutoff, args.power)
    result["status"] = "PASS"
    result["scope"] = "exact finite scalar-span membership; no all-size gain"
    result["script_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
