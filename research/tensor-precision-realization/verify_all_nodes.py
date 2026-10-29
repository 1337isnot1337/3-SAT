"""Finite controls for the virtual 2L-period all-node construction."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('full',HERE/'verify.py')
full=importlib.util.module_from_spec(spec)
spec.loader.exec_module(full)


def main():
    row_checks=packet_checks=outside_targets=0
    for length in (2,4,8):
        p=2*length
        occupancies=[set(range(length)),{x for x in range(length) if x%2==0},{0,length-1}]
        kernels={(x,y):full.prior.kernel_polynomial(length,x,y)
                 for x in range(length) for y in range(length)}
        for real in occupancies:
            for v in range(1,min(9,p)):
                word=[(v&r).bit_count()&1 for r in range(p)]
                forms={}
                polynomial=[F(1)]
                for x in sorted(real):
                    if not word[x]: continue
                    form=[F(0)]
                    for y in sorted(real):
                        if word[y]: form=full.add(form,kernels[x,y])
                    forms[x]=form
                    if length<=4: polynomial=full.mul(polynomial,form)
                for t in range(-length,length):
                    if not t: continue
                    selected=[x for x in forms if not word[(x+t)%p]]
                    for x in selected:
                        shifted=full.prior.shift(forms[x],t,2*length)
                        assert shifted[0]==0
                        assert all(not c or full.prior.valuation(c)>=1 for c in shifted)
                        if x+t not in real: outside_targets+=1
                        row_checks+=1
                    if length<=4:
                        shifted=full.prior.shift(polynomial,t,2*length)
                        assert not any(shifted[:len(selected)])
                        assert all(not c or full.prior.valuation(c)>=len(selected) for c in shifted)
                        packet_checks+=1
    print(json.dumps({'status':'PASS','selected_row_checks':row_checks,
                      'packet_product_checks':packet_checks,'outside_target_checks':outside_targets,
                      'scope':'L=2,4,8; bounded words and occupancy sets, not an all-size proof'},indent=2))

if __name__=='__main__': main()
