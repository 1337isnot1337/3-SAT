"""Finite checks for complete dyadic blocks in partially occupied packets."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('full',HERE/'verify.py')
full=importlib.util.module_from_spec(spec)
spec.loader.exec_module(full)


def retained(length,p,block,real):
    h=length//p
    result=set()
    for r in range(p):
        for start in range(0,h,block):
            group={r+p*j for j in range(start,start+block)}
            if group<=real: result.update(group)
    return result


def main():
    checks=packets=0
    observed=[]
    for length,p,block in ((4,2,2),(8,2,2),(8,2,4),(8,4,2)):
        a=length.bit_length()-1; u=p.bit_length()-1; b=block.bit_length()-1
        occupancies=[set(range(length)),set(range(length))-{1},
                     {x for x in range(length) if (x%p)==0 or x%3!=1},
                     {x for x in range(length) if x%2==0}]
        kernels={(x,y):full.prior.kernel_polynomial(length,x,y)
                 for x in range(length) for y in range(length)}
        for real in occupancies:
            good=retained(length,p,block,real)
            observed.append({'L':length,'P':p,'block':block,'real':len(real),'retained':len(good)})
            for word in product((0,1),repeat=p):
                for x in sorted(good):
                    if not word[x%p]: continue
                    form=[F(0)]
                    for y in sorted(good):
                        if word[y%p]: form=full.add(form,kernels[x,y])
                    for t in range(-length,length):
                        if not t%p or word[(x+t)%p]: continue
                        shifted=full.prior.shift(form,t,2*length)
                        assert shifted[0]==0
                        assert all(not c or full.prior.valuation(c)>=a+2-u+b+1 for c in shifted)
                        checks+=1
                packets+=1
    print(json.dumps({'status':'PASS','selected_row_checks':checks,
                      'packet_word_cases':packets,'occupancy_counts':observed,
                      'scope':'finite checks on four occupancy patterns, not an all-size proof'},indent=2))

if __name__=='__main__': main()
