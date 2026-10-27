"""Exploratory charged moment matrices; not a saved certified screen."""
from math import factorial
from charged import moment,partitions
from predecessor import exact_rank

for h in (2,4,6):
    bits=(len(partitions(h))).bit_length()-1
    states=partitions(h)[:2**bits]
    first=[]
    for x in states:
        row=[]
        for v in states:
            zero=dict(moment(x,v,(),0,1))
            if zero.get((),0) != (factorial(h) if x==v else 0):
                raise ValueError(('zeroth moment',h,x,v,zero))
            row.append(dict(moment(x,v,(),1,1)).get((),0))
        first.append(row)
    print({'h':h,'bits':bits,'dimension':len(states),'rank':exact_rank(first),
           'first_moment':first},flush=True)
