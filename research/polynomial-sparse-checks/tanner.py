"""Reference source-parameter Tanner builder; explicit limits prevent expensive runs.

Rows are bitsets on the first m edges. This implements the construction in
PROOF.md; it does not implement the counting oracle or the accepted theorem.
"""
def rem(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def field(r):
    return next(f for f in range((1 << r) | 1, 1 << (r+1), 2)
                if all(rem(f, g) for k in range(1, r//2+1)
                       for g in range((1 << k) | 1, 1 << (k+1), 2)))


def mul(a, b, f, r):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= f
    return out


def build(n, m, B, *, max_degree=4096, max_work=20_000_000):
    if any(type(x) is not int for x in (n, m, B)) or min(n, m, B) < 1 or m > B*n:
        raise ValueError('requires positive integers and m <= B*n')
    mu = m.bit_length()
    P = 20000*B*B*mu*mu
    D0 = 320000*B*B*mu**3
    d = min(m, D0)
    q = 1
    while q*d < m:
        q *= 2
    c = (d+8*B-1)//(8*B)
    h = (d+100*B*mu-1)//(100*B*mu)-1
    r = (d-1).bit_length()
    # Explicit conservative cap; this is a bounded reference, not a complexity estimate.
    if d > max_degree or q*d*max(c, 1) + d*q*q*max(q, 1) > max_work:
        raise ValueError('reference execution cap exceeded; raise limits deliberately')
    if q == 1:
        shifts = [0]*d
    else:
        denominator = 400*B*mu
        state = [1]*(2*(q-1))
        shifts = []
        for _ in range(d):
            choices = []
            for v in range(q):
                candidate = []
                for b in range(1, q):
                    sign = 1 if (v & b).bit_count() % 2 == 0 else -1
                    candidate.extend((state[2*(b-1)]*(denominator+sign),
                                      state[2*(b-1)+1]*(denominator-sign)))
                choices.append((sum(candidate), v, candidate))
            _, v, state = min(choices)
            shifts.append(v)
    local = [0]*c
    if h:
        assert r*h <= c
        f = field(r)
        for port in range(d):
            power = 1
            for i in range(h):
                for bit in range(r):
                    if power >> bit & 1:
                        local[i*r+bit] |= 1 << port
                power = mul(power, port, f, r)
    rows = []
    for side in (0,1):
        for vertex in range(q):
            for local_row in local:
                row = 0
                for port in range(d):
                    if not (local_row >> port & 1):
                        continue
                    left = vertex if side == 0 else vertex ^ shifts[port]
                    edge = left*d+port
                    if edge < m:
                        row |= 1 << edge
                rows.append(row)
    assert len(rows) <= 3*n and all(row.bit_count() <= D0 for row in rows)
    return {'rows': rows, 'P': P, 'D0': D0, 'q': q, 'd': d, 'h': h, 'c': c}
