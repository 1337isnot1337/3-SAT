"""Exact controls for periodic residue words and shifted Cauchy factors."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('full',HERE/'verify.py')
full=importlib.util.module_from_spec(spec)
spec.loader.exec_module(full)


def mismatch(counts,bits,d):
    p=len(bits)
    return sum(counts[r] for r in range(p) if bits[r] and not bits[(r+d)%p])


def weighted_sum(counts,d,fixed,base):
    """Sum base^(M-N)*(base-1)^N over all compatible words."""
    p=len(counts)
    unseen=set(range(p))
    total=1
    while unseen:
        start=min(unseen)
        cycle=[]
        r=start
        while r not in cycle:
            cycle.append(r)
            unseen.remove(r)
            r=(r+d)%p
        component=0
        for first in (0,1):
            if fixed[start] is not None and fixed[start]!=first: continue
            state=[0,0]
            state[first]=1
            for pos,r in enumerate(cycle):
                next_r=cycle[(pos+1)%len(cycle)]
                nxt=[0,0]
                for b in (0,1):
                    for c in (0,1):
                        if fixed[next_r] is not None and fixed[next_r]!=c: continue
                        if pos==len(cycle)-1 and c!=first: continue
                        factor=(base-1 if b and not c else base)**counts[r]
                        nxt[c]+=state[b]*factor
                state=nxt
            component+=state[first]
        total*=component
    return total


def construct_multi(counts,base):
    p=len(counts[0])
    fixed=[[None]*p for _ in counts]
    def score():
        return sum(__import__('math').prod(weighted_sum(counts[j],d,fixed[j],base)
                       for j in range(len(counts))) for d in range(1,p))
    current=score()
    for j in range(len(counts)):
        for r in range(p):
            trials=[]
            for bit in (0,1):
                fixed[j][r]=bit
                trials.append(score())
            assert sum(trials)==current
            fixed[j][r]=min(range(2),key=lambda bit:trials[bit])
            current=trials[fixed[j][r]]
    return fixed


def main():
    transfer=packet=rows=full_rows=0
    partial_counterexample=None
    examples=[]
    for counts in ([[2,1],[1,2]], [[1,0,2,1],[0,1,1,2]]):
        words=construct_multi(counts,8)
        examples.append({'counts':counts,'words':words,
                         'selected_per_shift':[sum(mismatch(c,w,d) for c,w in zip(counts,words))
                                               for d in range(1,len(counts[0]))]})
    for p in (2,4,8):
        for counts in ([1]*p, [1+(r%3) for r in range(p)], [2 if r%2 else 0 for r in range(p)]):
            for d in range(1,p):
                for fixed in ([None]*p, [0]+[None]*(p-1)):
                    free=[r for r in range(p) if fixed[r] is None]
                    brute=0
                    for vals in product((0,1),repeat=len(free)):
                        bits=list(fixed)
                        for r,v in zip(free,vals): bits[r]=v
                        k=mismatch(counts,bits,d)
                        brute+=7**k*8**(sum(counts)-k)
                    assert weighted_sum(counts,d,fixed,8)==brute
                    transfer+=1
    for length,p in ((4,2),(4,4),(8,2),(8,4)):
        a=length.bit_length()-1
        u=p.bit_length()-1
        occupancies=[set(range(length)),{x for x in range(length) if x%3!=1}]
        for real in occupancies:
            for word in product((0,1),repeat=p):
                forms={}
                polynomial=[F(1)]
                for x in sorted(real):
                    if not word[x%p]: continue # row is unrestricted
                    form=[F(0)]
                    for y in sorted(real):
                        if word[y%p]: form=full.add(form,full.prior.kernel_polynomial(length,x,y))
                    forms[x]=form
                    polynomial=full.mul(polynomial,form)
                assert full.prior.evaluate(polynomial,0)==1
                for t in range(-length,length):
                    if not t%p: continue
                    selected=[x for x in forms if not word[(x+t)%p]]
                    for x in selected:
                        shifted=full.prior.shift(forms[x],t,2*length)
                        assert all(not c or full.prior.valuation(c)>=a+2-u for c in shifted)
                        rows+=1
                        if len(real)==length:
                            assert all(not c or full.prior.valuation(c)>=2*(a-u)+2 for c in shifted)
                            full_rows+=1
                        else:
                            content=min(full.prior.valuation(c) for c in shifted if c)
                            if content < 2*(a-u)+2 and partial_counterexample is None:
                                partial_counterexample={'L':length,'P':p,'real_slots':sorted(real),
                                                        'word':list(word),'row':x,'t':t,
                                                        'content':content,'full_packet_bound':2*(a-u)+2}
                    shifted=full.prior.shift(polynomial,t,2*length)
                    assert all(not c or full.prior.valuation(c)>=len(selected)*(a+2-u) for c in shifted)
                    packet+=1
    assert partial_counterexample is not None
    print(json.dumps({'status':'PASS','cycle_transfer_bruteforce_checks':transfer,
                      'periodic_packet_product_checks':packet,'selected_row_checks':rows,
                      'full_packet_cancellation_row_checks':full_rows,
                      'partial_packet_counterexample':partial_counterexample,
                      'conditional_expectation_examples':examples,
                      'scope':'finite periodic words and two occupied sets per L,P; not an all-size proof'},indent=2))

if __name__=='__main__': main()
