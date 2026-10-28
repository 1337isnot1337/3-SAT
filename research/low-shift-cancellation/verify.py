#!/usr/bin/env python3
"""Check the two-partition low-shift cancellation against exact operators."""
from collections import Counter, defaultdict
from itertools import product
from fractions import Fraction
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/anthropic-operator-ranks'))
from operators import piece_vector, modular_rank  # noqa: E402


def normal_order(h, output):
    """Exact Laurent coefficients for x=v=1^h, y=(h), odd-length output."""
    counts = Counter(output)
    r = (len(output) + 1)//2
    base = math.comb(h, r)**2 * math.factorial(h-r)
    terms = defaultdict(int)
    for choices in product(*(range(n+1) for n in counts.values())):
        split = dict(zip(counts, choices))
        count_z = sum(choices)
        denominator = math.prod(math.factorial(split[k])*math.factorial(n-split[k])
                                for k, n in counts.items())
        weight = sum(k*n for k, n in split.items())
        numerator = h*r*math.factorial(r-1)*math.factorial(r)
        if count_z == r-1:
            terms[weight-r-h] += numerator//denominator
        if count_z == r:
            terms[weight-r] += numerator//denominator
    coefficients = defaultdict(int)
    for exponent, value in terms.items():
        for j in range(2*r+1):
            coefficients[exponent+j] += base*value*math.comb(2*r, j)*(-1)**j
    alpha = (base*math.factorial(2*r)*h
             // math.prod(math.factorial(n) for n in counts.values()))
    return {s: v for s, v in coefficients.items() if v}, alpha



def three_partitions(h):
    for a in range(1, h//3+1):
        for b in range(a, (h-a)//2+1):
            yield (h-a-b, b, a)


def closed_three(h, output):
    counts = Counter(output)
    denominator = math.prod(math.factorial(n) for n in counts.values())
    factor = 4*h*math.comb(h, 2)**2*math.factorial(h-2)
    coefficients = defaultdict(int)
    for part, count in counts.items():
        assert factor*count % denominator == 0
        scalar = factor*count//denominator
        for j in range(5):
            value = scalar*math.comb(4, j)*(-1)**j
            coefficients[part-h-2+j] += value
            coefficients[h-part-2+j] += value
    return {s: v for s, v in coefficients.items() if v}


def closed_diagonal(h):
    result = defaultdict(int)
    result[0] = math.factorial(h)
    scale = h*h*math.factorial(h)
    for j in range(3):
        value = scale*math.comb(2,j)*(-1)**j
        result[h-1+j] += value
        result[-h-1+j] += value
    return {s: v for s, v in result.items() if v}


def two_to_two(h, output):
    a, b = output
    denom = math.prod(math.factorial(n) for n in Counter(output).values())
    common = 4*(h-1)*math.comb(h,2)**2*math.factorial(h-2)
    assert common % denom == 0
    result = defaultdict(int)
    for exponent in (-h, h, 1-a, a-1, 1-b, b-1):
        for j in range(5):
            result[exponent-2+j] += (common//denom)*math.comb(4,j)*(-1)**j
    return {s: v for s, v in result.items() if v}


def general_two_to_two(h, input_part, output_part):
    p, a = input_part, output_part
    y, u = (h-p, p), (h-a, a)
    assert p != h-p and not set(y).intersection(u)
    denom = math.prod(math.factorial(n) for n in Counter(u).values())
    common = 4*p*(h-p)*math.comb(h,2)**2*math.factorial(h-2)
    assert common % denom == 0
    result = defaultdict(int)
    for exponent in (-h, h, a-p, p-a, h-p-a, -h+p+a):
        for j in range(5):
            result[exponent-2+j] += (common//denom)*math.comb(4,j)*(-1)**j
    return {s: v for s, v in result.items() if v}


def second_input_diagonal(h):
    result = defaultdict(int, two_to_two(h, (h-1, 1)))
    result[0] += math.factorial(h)
    factor = h*math.factorial(h)
    for exponent, scalar in ((h-2, h-1), (-h, h-1), (0, 1), (-2, 1)):
        for j in range(3):
            result[exponent+j] += factor*scalar*math.comb(2,j)*(-1)**j
    return {s: v for s, v in result.items() if v}


def divide_four(values, h):
    """Return z^(h+2)*values/(z-1)^4 and assert exact division."""
    numerator = [values.get(i-(h+2), 0) for i in range(2*h+3)]
    quotient = []
    for i, value in enumerate(numerator):
        for j in range(1, min(4, i)+1):
            value -= (-1)**j * math.comb(4,j)*quotient[i-j]
        quotient.append(value)
    assert all(value == 0 for value in quotient[-4:])
    return quotient[:-4]


def closed_two(h, output):
    counts = Counter(output)
    denom = math.prod(math.factorial(n) for n in counts.values())
    assert h*math.factorial(h) % denom == 0
    factor = -h*math.factorial(h)//denom
    terms = defaultdict(int)
    terms[-h-2] += h+1
    terms[-h-1] -= h-1
    for part, count in counts.items():
        terms[part-2] -= count*(part-1)
        terms[part-1] += count*(part+1)
    result = defaultdict(int)
    for exponent, value in terms.items():
        for j in range(4):
            result[exponent+j] += factor*value*math.comb(3,j)*(-1)**(3-j)
    return {s: v for s, v in result.items() if v}


def closed_reverse_two(h, output):
    counts = Counter(output)
    denom = math.prod(math.factorial(n) for n in counts.values())
    c = h*(h-1)//2
    assert c*h*math.factorial(h) % denom == 0
    factor = c*h*math.factorial(h)//denom
    result = defaultdict(int)
    def add(exponent, value, degree):
        for j in range(degree+1):
            result[exponent+j] += factor*value*math.comb(degree,j)*(-1)**(degree-j)
    add(h-2, 2*(h-2), 3)
    add(h-2, -(h+1), 4)
    for part, count in counts.items():
        add(part-h-2, 2*(h-2)*count, 3)
        add(-part-2, (part-1)*count, 4)
    return {s: v for s, v in result.items() if v}


def one_sided(output, reference):
    difference = Counter(output)
    difference.subtract(reference)
    result = defaultdict(int)
    for part, count in difference.items():
        for j in range(4):
            value = count*math.comb(3,j)*(-1)**(3-j)
            result[part-2+j] -= value*(part-1)
            result[part-1+j] += value*(part+1)
    return {s: v for s, v in result.items() if v}


def high_row(h):
    factor = -(h-1)*math.factorial(h)
    terms = ((-h-1,h), (-h,-(h-2)), (-3,2), (h-1,h+1), (h-2,-(h-1)))
    result = defaultdict(int)
    for exponent, value in terms:
        for j in range(4):
            result[exponent+j] += factor*value*math.comb(3,j)*(-1)**(3-j)
    return {s: v for s, v in result.items() if v}


def g_one(h):
    k = h//2
    factor = -math.comb(h-2,k-1)*math.comb(h,k+1)*math.factorial(h-k-1)*h
    bracket = defaultdict(int)
    if h % 2 == 0:
        bracket[-h-2] = h+1
        bracket[-h-1] = -1
        bracket[0] = h+2
        degree = h+1
    else:
        for exponent, value in ((-h,k*(k-1)), (-h-1,k*(k+1)),
                                (1,k*(k+1)), (0,k*(k+1))):
            bracket[exponent] += 2*value
        n2 = {-h-1: -(h+1)*(k-1)+(k-1),
              -h-2: -(h+1)*(k+1), 0: k+1}
        for exponent, value in n2.items():
            bracket[exponent+1] += value
            bracket[exponent] -= value
        degree = h
    result = defaultdict(int)
    for exponent, value in bracket.items():
        for j in range(degree+1):
            result[exponent+j] += factor*value*math.comb(degree,j)*(-1)**(degree-j)
    return {s: v for s, v in result.items() if v}


def de_three(h, output):
    """Five-event normal-order formula for d,e labels and input (h-1,1)."""
    events = (-(h-1), -1) + tuple(output)
    denom = math.prod(math.factorial(n) for n in Counter(output).values())
    factor = -(h-2)*(h-1)*math.factorial(h)
    assert factor % denom == 0
    factor //= denom
    result = defaultdict(int)
    for i in range(5):
        for j in range(i+1, 5):
            t = events[i]+events[j]
            for k in range(6):
                value = factor*math.comb(5,k)*(-1)**(5-k)
                result[t-2+k] += value*(t+2)
                result[t-3+k] -= value*(t-2)
    return {s: v for s, v in result.items() if v}


def odd_weights(h):
    k = (h-1)//2
    x = [Fraction(0)]*(h-2)
    x[1] = 1
    delta = Fraction(1)
    for a in range(2, k+1):
        delta *= Fraction(-(a-1), h-a-1)
        x[a] = x[a-1]+delta
    total = x[k-1]+x[k]
    for a in range(2, k+1):
        x[h-a-1] = total-x[a-1]
    q = [Fraction(0)]*(h+1)
    for t in range(h-2):
        q[t+3] = x[t]+3*q[t+2]-3*q[t+1]+q[t]
    assert x[0] == 0 and x[1] == 1 and x[2] != 2
    return q


def run():
    prime = 1000003
    formula_cases = 0
    recurrence_rows = 0
    two_part_cases = 0
    two_part_recurrence_rows = 0
    reverse_recurrence_rows = 0
    diagonal_recurrence_rows = 0
    second_input_recurrence_rows = 0
    second_diagonal_recurrence_rows = 0
    general_input_recurrence_rows = 0
    high_recurrence_rows = 0
    odd_break_recurrence_rows = 0
    odd_break_cases = 0
    for h in range(4, 41):
        rows = []
        symmetric_polynomials = []
        one = (1,)*h
        d = (2,) + (1,)*(h-2)
        g, r = g_one(h), high_row(h)
        ge = g.get(-h-2, 0)
        gd = g.get(-h-1, 0)-g.get(h+1, 0)
        re = r.get(-h-2, 0)-r.get(h+2, 0)
        rd = r.get(-h-1, 0)-r.get(h+1, 0)
        assert ge and re and rd*ge != gd*re
        assert rd*(h+1) == -(3*h+2)*re
        k = h//2
        if h % 2 == 0:
            assert gd == -h*ge
        else:
            assert gd*(k+1)**2 == -(2*k**3+3*k**2+4*k+2)*ge
        if h <= 6:
            output = one if h % 2 == 0 else d
            for y, u, expected in (((h,), output, g), ((h-1,1), (h,), r)):
                direct = {shift: dict(piece_vector(d, one, y, shift)).get(u, 0)
                          for shift in range(-2*h, 2*h+1)}
                assert {j: value for j, value in direct.items() if value} == expected
                high_recurrence_rows += 1
        for output in three_partitions(h):
            vector = [output.count(j) for j in range(1, h-1)]
            rows.append(vector)
            expected = closed_three(h, output)
            denom = math.prod(math.factorial(n) for n in Counter(output).values())
            symmetric_polynomials.append((vector[0], {s: denom*v for s, v in expected.items()}))
            enumerated, _ = normal_order(h, output)
            assert expected == enumerated
            assert all(expected.get(-shift, 0) == value for shift, value in expected.items())
            if h <= 6:
                direct = {shift: dict(piece_vector(one, one, (h,), shift)).get(output, 0)
                          for shift in range(-2*h, 2*h+1)}
                assert {s: value for s, value in direct.items() if value} == expected
                recurrence_rows += 1
            formula_cases += 1
        reference = next(row for row in rows if row[0])
        low_rows = [[reference[0]*value-row[0]*base
                     for value, base in zip(row, reference)] for row in rows]
        assert modular_rank(rows, prime) == h-3
        assert modular_rank(low_rows, prime) == h-4
        ref_count, ref_poly = next((n, v) for n, v in symmetric_polynomials if n)
        symmetric_low = [[ref_count*poly.get(j, 0)-n*ref_poly.get(j, 0)
                          for j in range(-h, h+1)] for n, poly in symmetric_polynomials]
        diagonal = closed_diagonal(h)
        ref_raw = closed_three(h, (h-2, 1, 1))
        diag_low = {j: (h-1)*diagonal.get(j, 0)-ref_raw.get(j, 0)
                    for j in set(diagonal)|set(ref_raw)}
        assert all(not value or abs(j) <= h for j, value in diag_low.items())
        assert sum(diag_low.values()) == (h-1)*math.factorial(h)
        symmetric_low.append([diag_low.get(j, 0) for j in range(-h, h+1)])
        if h >= 6:
            u, v = (h-2, 2), (h-3, 3)
            pu, pv = two_to_two(h, u), two_to_two(h, v)
            zu = math.prod(math.factorial(n) for n in Counter(u).values())
            zv = math.prod(math.factorial(n) for n in Counter(v).values())
            row = {j: zu*pu.get(j, 0)-zv*pv.get(j, 0) for j in set(pu)|set(pv)}
            assert all(not value or abs(j) <= h for j, value in row.items())
            assert sum(row.values()) == 0
            symmetric_low.append([row.get(j, 0) for j in range(-h, h+1)])
            ydiag = second_input_diagonal(h)
            center = {j: (h-1)*(ydiag.get(j, 0)-zu*pu.get(j, 0)-diagonal.get(j, 0))
                           + ref_raw.get(j, 0)
                      for j in set(ydiag)|set(pu)|set(diagonal)|set(ref_raw)}
            assert all(not value or abs(j) <= h for j, value in center.items())
            assert sum(center.values()) == 0
            quotient = divide_four(center, h)
            assert quotient[h] == 2*h*(h-1)**2*(h-2)*math.factorial(h)
            symmetric_low.append([center.get(j, 0) for j in range(-h, h+1)])
            if h == 6:
                y = (h-1, 1)
                for state, expected in ((u, pu), (v, pv)):
                    direct = {shift: dict(piece_vector(one, one, y, shift)).get(state, 0)
                              for shift in range(-2*h, 2*h+1)}
                    assert {j: value for j, value in direct.items() if value} == expected
                    second_input_recurrence_rows += 1
                direct = {shift: dict(piece_vector(one, one, y, shift)).get(y, 0)
                          for shift in range(-2*h, 2*h+1)}
                assert {j: value for j, value in direct.items() if value} == ydiag
                second_diagonal_recurrence_rows += 1
        if h <= 6:
            direct = {shift: dict(piece_vector(one, one, (h,), shift)).get((h,), 0)
                      for shift in range(-2*h, 2*h+1)}
            assert {s: value for s, value in direct.items() if value} == diagonal
            diagonal_recurrence_rows += 1
        if h >= 9:
            u, v = (h-2, 2), (h-4, 4)
            pu, pv = general_two_to_two(h, 3, 2), general_two_to_two(h, 3, 4)
            zu = math.prod(math.factorial(n) for n in Counter(u).values())
            zv = math.prod(math.factorial(n) for n in Counter(v).values())
            row = {j: zu*pu.get(j, 0)-zv*pv.get(j, 0) for j in set(pu)|set(pv)}
            assert all(not value or abs(j) <= h for j, value in row.items())
            quotient = divide_four(row, h)
            common = 12*(h-3)*math.comb(h,2)**2*math.factorial(h-2)
            expected = {5: common, 2*h-5: common, 7: -common, 2*h-7: -common}
            assert {j: value for j, value in enumerate(quotient) if value} == expected
            symmetric_low.append([row.get(j, 0) for j in range(-h, h+1)])
        if h == 7:
            y, u = (h-1, 1), (3, 2, 2)
            direct = {shift: dict(piece_vector(d, one, y, shift)).get(u, 0)
                      for shift in range(-2*h, 2*h+1)}
            assert {j: value for j, value in direct.items() if value} == de_three(h, u)
            odd_break_recurrence_rows += 1
        if h >= 11 and h % 2:
            q = odd_weights(h)
            u, v = (h-6, 3, 3), (h-7, 4, 3)
            pu, pv = de_three(h, u), de_three(h, v)
            zu = math.prod(math.factorial(n) for n in Counter(u).values())
            zv = math.prod(math.factorial(n) for n in Counter(v).values())
            row = {j: zu*pu.get(j, 0)-zv*pv.get(j, 0) for j in set(pu)|set(pv)}
            assert all(not value or abs(j) <= h for j, value in row.items())
            assert sum(row.values()) == 0
            assert sum(value*j*j for j, value in row.items()) == 0
            moment = sum((q[j] if j > 0 else -q[-j])*value
                         for j, value in row.items() if j and value)
            numerator = -(h-2)*(6*h**4-182*h**3+2042*h**2-9986*h+18024)
            denominator = math.prod(h-j for j in range(5,10))
            factor = -(h-2)*(h-1)*math.factorial(h)
            assert moment == factor*Fraction(numerator, denominator) and moment
            odd_break_cases += 1
        if h == 7:
            y, u = (5, 2), (4, 3)
            direct = {shift: dict(piece_vector(one, one, y, shift)).get(u, 0)
                      for shift in range(-2*h, 2*h+1)}
            assert {j: value for j, value in direct.items() if value} == general_two_to_two(h, 2, 3)
            general_input_recurrence_rows += 1
        reference = (h-2, 2)
        if h <= 6:
            d = (2,) + (1,)*(h-2)
            output = (h-1, 1)
            direct = {shift: dict(piece_vector(d, one, (h,), shift)).get(output, 0)
                      for shift in range(-2*h, 2*h+1)}
            assert {s: value for s, value in direct.items() if value} == closed_two(h, output)
            reverse = {shift: dict(piece_vector(one, d, (h,), shift)).get(output, 0)
                       for shift in range(-2*h, 2*h+1)}
            assert {s: value for s, value in reverse.items() if value} == closed_reverse_two(h, output)
            two_part_recurrence_rows += 1
            reverse_recurrence_rows += 1
        one_sided_rows = []
        q = odd_weights(h) if h % 2 and h >= 5 else None
        combined_positive = []
        combined_negative = []
        reverse_ref = closed_reverse_two(h, reference)
        ref_denom = math.prod(math.factorial(n) for n in Counter(reference).values())
        for a in range(2, h//2+1):
            output = (h-a, a)
            values = one_sided(output, reference)
            assert all(0 <= shift <= h for shift in values)
            for degree in range(1, 5):
                assert sum(value*shift**degree for shift, value in values.items() if shift) == 0
            if q is not None:
                assert sum(value*q[shift] for shift, value in values.items() if shift) == 0
            one_sided_rows.append([values.get(j, 0) for j in range(h+1)])
            combined_positive.append([values.get(j, 0) for j in range(-h, h+1)])
            reverse_values = closed_reverse_two(h, output)
            denom = math.prod(math.factorial(n) for n in Counter(output).values())
            difference = {j: denom*reverse_values.get(j, 0)-ref_denom*reverse_ref.get(j, 0)
                          for j in set(reverse_values)|set(reverse_ref)}
            assert all(not value or -h <= j <= 0 for j, value in difference.items())
            for degree in range(1, 5):
                assert sum(value*(-j)**degree for j, value in difference.items() if j) == 0
            if q is not None:
                assert sum(value*q[-j] for j, value in difference.items() if j and value) == 0
            combined_negative.append([difference.get(j, 0) for j in range(-h, h+1)])
            if h <= 6:
                d = (2,) + (1,)*(h-2)
                direct = {shift: dict(piece_vector(d, one, (h,), shift)).get(output, 0)
                          for shift in range(-2*h, 2*h+1)}
                assert {s: value for s, value in direct.items() if value} == closed_two(h, output)
                reverse = {shift: dict(piece_vector(one, d, (h,), shift)).get(output, 0)
                           for shift in range(-2*h, 2*h+1)}
                assert {s: value for s, value in reverse.items() if value} == reverse_values
                two_part_recurrence_rows += 1
                reverse_recurrence_rows += 1
            two_part_cases += 1
        assert modular_rank(one_sided_rows, prime) == max(0, h//2-2)
        assert modular_rank(symmetric_low + combined_positive + combined_negative, prime) == (
            h-3 + 2*max(0, h//2-2) + 2*(h >= 6) + (h >= 9))
    print(json.dumps({'h_range': [4, 40], 'three_partition_formula_cases': formula_cases,
                      'complete_recurrence_row_comparisons': recurrence_rows,
                      'multiplicity_and_kernel_rank_cases': 37,
                      'one_sided_rank_cases': 37, 'odd_recurrence_h_range': [5, 39],
                      'two_part_cases': two_part_cases,
                      'two_part_recurrence_rows': two_part_recurrence_rows,
                      'reverse_recurrence_rows': reverse_recurrence_rows,
                      'diagonal_recurrence_rows': diagonal_recurrence_rows,
                      'second_input_recurrence_rows': second_input_recurrence_rows,
                      'second_diagonal_recurrence_rows': second_diagonal_recurrence_rows,
                      'general_input_recurrence_rows': general_input_recurrence_rows,
                      'high_recurrence_rows': high_recurrence_rows,
                      'odd_break_cases': odd_break_cases,
                      'odd_break_recurrence_rows': odd_break_recurrence_rows,
                      'prime': prime}, indent=2))


if __name__ == '__main__':
    run()
