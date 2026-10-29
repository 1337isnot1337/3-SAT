#!/usr/bin/env python3
"""Compress actual polynomial generators with exact FLINT Hermite forms.

Optional experiment dependency: python-flint 0.9.0. No floating arithmetic.
The small runs cross-check the uncompressed standard-library calculation.
"""
import argparse
import hashlib
import json
from math import comb, prod
from pathlib import Path
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flint-path', required=True)
    parser.add_argument('--L', type=int, choices=[2, 4, 8], required=True)
    parser.add_argument('--precision', type=int, default=320)
    args = parser.parse_args()
    sys.path.insert(0, args.flint_path)
    import flint
    from flint import fmpz_mat, fmpz_poly
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import recovery
    L, precision = args.L, args.precision
    degree = L * (2*L-1)
    dim = degree + 1
    den = prod(-s for s in range(-L, L) if s)
    denominator = den ** L
    vden = recovery.valuation(abs(denominator), 100000)
    modulus = 1 << precision
    numerator_modulus = 1 << (precision+vden)
    unit_inverse = pow(denominator >> vden, -1, modulus)
    basis = [[int(i == j)*numerator_modulus for j in range(dim)] for i in range(dim)]
    kernel = {}
    for d in range(1-L, L):
        p = fmpz_poly([1])
        for t in range(-L, L):
            if t != d:
                p *= fmpz_poly([-t, 1])
        kernel[d] = p
    generators = []
    count = 0
    started = time.monotonic()
    for X in range(1 << L):
        row_forms = [sum((kernel[y-x] for y in range(L) if X >> y & 1), fmpz_poly([0])) for x in range(L)]
        polynomials = [fmpz_poly([1])]
        for mask in range(1 << L):
            if mask:
                bit = mask & -mask
                polynomials.append(polynomials[mask-bit] * row_forms[bit.bit_length()-1])
            p = polynomials[mask] * den**(L-mask.bit_count())
            coeffs = [int(x) % numerator_modulus for x in p.coeffs()]
            generators.append(coeffs + [0]*(dim-len(coeffs)))
            count += 1
        if (X+1) % 4 == 0 or X+1 == 1 << L:
            A = fmpz_mat(basis+generators)
            if L <= 4:
                H, T = A.hnf(transform=True)
                assert H == T*A
            else:
                H = A.hnf()
            basis = [[int(H[i,j]) for j in range(dim)] for i in range(dim)]
            assert all(basis[i][i] > 0 and basis[i][i] & (basis[i][i]-1) == 0 for i in range(dim))
            assert all(not H[i,j] for i in range(dim, H.nrows()) for j in range(dim))
            generators = []
        if (X+1) % 16 == 0 or X+1 == 1 << L:
            print(json.dumps({'progress_X':X+1,'of':1 << L,'generators':count,'seconds':round(time.monotonic()-started,3)}),flush=True)
    numerator_polys = [fmpz_poly(b) for b in basis]
    target = []
    for b in basis:
        assert b[0] % (1 << vden) == 0
        target.append((b[0] >> vden)*unit_inverse % modulus)
    results = []
    for u in range(1,L.bit_length()):
        nodes = [t for t in range(1-L,L) if t and recovery.valuation(abs(t),precision)<u]
        rows = []
        for t in nodes:
            columns = []
            for p in numerator_polys:
                chart = p(fmpz_poly([t,2*L]))
                values = [int(x) for x in chart.coeffs()]
                values += [0]*(dim-len(values))
                assert all(x % (1 << vden) == 0 for x in values)
                columns.append([(x >> vden)*unit_inverse % modulus for x in values])
            rows.extend([list(row) for row in zip(*columns)])
        result = recovery.diagonalize(rows,target,precision,certificates=True)
        if L <= 4:
            original, original_target = recovery.joint_data(L,nodes,precision,range(1 << L))
            direct = recovery.diagonalize(original,original_target,precision,certificates=True)
            assert result['required_precision'] == direct['required_precision']
            result['uncompressed_crosscheck'] = True
        # The source charges precision divided by D_i, not uniform precision.
        # At common modulus 2^precision, multiply each row by 2^(precision-p_i).
        def weighted(q, certificates=False):
            precisions = [q*(L >> recovery.valuation(abs(t),precision)) for t in nodes]
            assert max(precisions) <= precision
            scaled = [[(x << (precision-precisions[i//dim])) % modulus for x in row]
                      for i,row in enumerate(rows)]
            answer = recovery.diagonalize(scaled,target,precision,certificates=certificates)
            return answer, precisions
        low, high = 0, precision//L
        high_result, _ = weighted(high)
        assert high_result['status'] == 'finite_exact_threshold'
        while high-low > 1:
            middle = (low+high)//2
            candidate, _ = weighted(middle)
            if candidate['status'] == 'finite_exact_threshold':
                high = middle
            else:
                low = middle
        paid_upper, profile = weighted(high, certificates=True)
        paid_lower, _ = weighted(high-1, certificates=True)
        assert paid_lower['status'] == 'cutoff_unresolved'
        assert paid_lower['cutoff_kernel_certificate_verified']
        result['minimum_integer_q_for_precision_qD'] = high
        result['qD_precisions'] = profile
        result['qD_endpoint_certificates_verified'] = bool(paid_upper['upper_certificate_verified'] and paid_lower['cutoff_kernel_certificate_verified'])
        result.update(L=L,u=u,nodes=nodes)
        results.append(result)
        print(json.dumps({'result':result}),flush=True)
    basis_hash = hashlib.sha256(json.dumps(basis,separators=(',',':')).encode()).hexdigest()
    report={'L':L,'precision':precision,'numerator_precision':precision+vden,
            'generators':count,'basis_sha256':basis_hash,'flint_version':flint.__version__,
            'results':results,'limits':'Finite actual polynomial-generator lattice; not a uniform recovery theorem or SAT bound.'}
    destination = Path(__file__).resolve().parent / f'lattice-L{L}.json'
    destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'saved':str(destination),'seconds':round(time.monotonic()-started,3)}),flush=True)


if __name__ == '__main__':
    main()
