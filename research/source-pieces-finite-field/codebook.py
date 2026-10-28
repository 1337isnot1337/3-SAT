#!/usr/bin/env python3
"""Exact partition-codebook ranking; arithmetic is over integers, not F_p."""


def table(h, p):
    f = [[0]*(h+1) for _ in range(h+1)]
    f[0][0] = 1
    for k in range(1, h+1):
        for n in range(h+1):
            maximum = min(p-1, n//k) if k % p else 0
            f[k][n] = sum(f[k-1][n-m*k] for m in range(maximum+1))
    return f


def unrank(h, p, index, f):
    if not 0 <= index < f[h][h]:
        raise ValueError('rank outside codebook')
    n, result = h, []
    for k in range(h, 0, -1):
        maximum = min(p-1, n//k) if k % p else 0
        for m in range(maximum+1):
            block = f[k-1][n-m*k]
            if index < block:
                result.extend([k]*m)
                n -= m*k
                break
            index -= block
    assert n == 0 and index == 0
    return tuple(sorted(result))


def rank(h, p, parts, f):
    if sum(parts) != h or any(k < 1 or k > h for k in parts):
        raise ValueError('invalid partition')
    n, index = h, 0
    for k in range(h, 0, -1):
        m = parts.count(k)
        maximum = min(p-1, n//k) if k % p else 0
        if m > maximum:
            raise ValueError('partition outside codebook')
        index += sum(f[k-1][n-j*k] for j in range(m))
        n -= m*k
    assert n == 0
    return index


def brute(n, minimum=1):
    if n == 0:
        yield ()
    for k in range(minimum, n+1):
        for rest in brute(n-k, k):
            yield (k,)+rest


def main():
    domains = states = 0
    for p in (2,3,5,7,23):
        for h in range(1,21):
            f = table(h,p)
            expected = {parts for parts in brute(h)
                        if all(k % p and parts.count(k) < p for k in set(parts))}
            assert f[h][h] == len(expected)
            observed = set()
            for index in range(f[h][h]):
                parts = unrank(h,p,index,f)
                assert rank(h,p,parts,f) == index
                observed.add(parts)
                states += 1
            assert observed == expected
            domains += 1
    print(f'PASS: {domains} codebook domains, {states} exact ranking/unranking states')


if __name__ == '__main__':
    main()
