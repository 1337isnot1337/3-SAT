"""Compare asymptotic exponent envelopes using exact rational powers.

An envelope represents n^a (log n)^b (log log n)^c inside 2^O(...).
This compares eventual symbolic upper envelopes, not finite runtimes or
algorithms. Realizability and completeness of a proposed model need a proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path


def rational(value: object) -> Fraction:
    if type(value) not in (str, int):
        raise ValueError("Powers must be exact integers or rational strings")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"Invalid rational power: {value!r}") from exc


@dataclass(frozen=True, order=True)
class Envelope:
    n: Fraction
    log: Fraction
    loglog: Fraction

    @classmethod
    def read(cls, value: dict) -> Envelope:
        if not isinstance(value, dict) or set(value) != {"n", "log", "loglog"}:
            raise ValueError("An envelope needs exactly n, log and loglog powers")
        result = cls(*(rational(value[key]) for key in ("n", "log", "loglog")))
        if result.n < 0:
            raise ValueError("Negative powers of n are outside this model")
        return result

    def as_dict(self) -> dict[str, str]:
        return {key: str(getattr(self, key)) for key in ("n", "log", "loglog")}


def contraction_cost(network: Envelope, saving: Fraction) -> Envelope:
    # For fixed a>0, log(n^a log^b n loglog^c n) = Theta(log n).
    if network.n <= 0:
        raise ValueError("Network size must have a positive fixed power of n")
    if saving <= 0:
        raise ValueError("The contraction saving must be positive")
    return Envelope(network.n, network.log - saving, network.loglog)


def analyze(model: dict) -> dict:
    if model.get("schema_version") != 1:
        raise ValueError("Unsupported model schema")
    network = Envelope.read(model["network_size"])
    saving = rational(model["contraction_log_saving"])
    terms = [("composed contraction", contraction_cost(network, saving))]
    names = {terms[0][0]}
    for item in model["overheads"]:
        name = item["name"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("Cost names must be nonempty and unique")
        names.add(name)
        terms.append((name, Envelope.read(item["scale"])))
    dominant = max(term for _, term in terms)
    if dominant.n == 1:
        alpha = str(-dominant.log)
        alpha_scope = "Fixed iterated-log powers do not change alpha"
    elif dominant.n < 1:
        alpha = None
        alpha_scope = "Envelope is below n/(log n)^a for every fixed a"
    else:
        alpha = None
        alpha_scope = "Envelope has power of n greater than one; no finite alpha here"
    return {
        "name": model.get("name", "Unnamed hypothetical model"),
        "scope": "Asymptotic bookkeeping under supplied assumptions only; no new algorithm certified",
        "dominant_envelope": dominant.as_dict(),
        "dominant_terms": [name for name, term in terms if term == dominant],
        "alpha": alpha,
        "alpha_scope": alpha_scope,
        "terms": [{"name": name, "envelope": term.as_dict()} for name, term in terms],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.model.read_text()))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
