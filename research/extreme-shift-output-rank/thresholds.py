"""Exact finite grade scan of the conservative extreme-shift rank budget."""
import json


def main():
    limit = 2000
    counts = [0] * (limit + 1)
    counts[0] = 1
    for n in range(1, limit + 1):
        k, value = 1, 0
        while k * (3*k-1) // 2 <= n:
            first, second = k*(3*k-1)//2, k*(3*k+1)//2
            sign = 1 if k % 2 else -1
            value += sign * counts[n-first]
            if second <= n:
                value += sign * counts[n-second]
            k += 1
        counts[n] = value
    if counts[:11] != [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]:
        raise ValueError('Partition recurrence controls failed')
    p0, p1, total, weighted = [], [], 0, 0
    for k, count in enumerate(counts):
        total += count
        weighted += k*count
        p0.append(total)
        p1.append(weighted)
    results = {f'{a}/{b}': {'first_passing_grade': None, 'passing_events': 0,
                            'later_failing_grades': []} for a, b in [(1, 4), (1, 2), (3, 4)]}
    nlabels, events = 2, 0
    last = None
    for h in range(2, limit + 1):
        rank = counts[h] - counts[h-1]
        while rank >= nlabels:
            bits = nlabels.bit_length() - 1
            last = {'h': h, 'bits': bits}
            events += 1
            for a, b in [(1, 4), (1, 2), (3, 4)]:
                result = results[f'{a}/{b}']
                m = (b-a)*h//b
                # For both signs, sum K_s over |s| >= ceil((1+a/b)h).
                budget = 2*((m+1)*p0[m]-p1[m])
                if budget < nlabels:
                    if result['first_passing_grade'] is None:
                        result['first_passing_grade'] = {'h': h, 'bits': bits}
                    result['passing_events'] += 1
                elif result['first_passing_grade'] is not None:
                    result['later_failing_grades'].append(h)
            nlabels *= 2
    print(json.dumps({'status': 'PASS', 'scope': 'finite exact rank-budget scan; no eventual monotonicity claim',
                      'maximum_grade': limit, 'number_of_grade_events': events,
                      'last_grade_event': last, 'results': results}, indent=2))


if __name__ == '__main__':
    main()
