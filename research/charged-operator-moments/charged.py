"""Experimental charged variant of the predecessor's finite exact operators.

The predecessor is copied unmodified and source-hashed in SOURCES.json.
Only this module adds D_0=charge*Id to the normal-ordered fields.
No complete SAT algorithm or asymptotic improvement is implemented.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
from math import comb

from predecessor import (add_scaled, binomial, dual_polynomial, dual_scale,
                         freeze, partitions)


@lru_cache(maxsize=300_000)
def operator(monomial,mode,argument,charge):
    target = sum(argument)+mode
    if target<0:
        return ()
    if not monomial:
        return ((argument,1),) if mode==0 else ()
    n,tail = monomial[0],monomial[1:]
    result = {}
    for created in range(n,target+1):
        scale = comb(created-1,n-1)
        for output,value in operator(tail,mode-created,argument,charge):
            output = tuple(sorted(output+(created,),reverse=True))
            result[output] = result.get(output,0)+scale*value
    add_scaled(result,operator(tail,mode,argument,charge),(-1)**(n-1)*charge)
    for destroyed,multiplicity in Counter(argument).items():
        reduced = list(argument)
        reduced.remove(destroyed)
        scale = binomial(-destroyed-1,n-1)*destroyed*multiplicity
        add_scaled(result,operator(tail,mode+destroyed,tuple(reduced),charge),scale)
    return freeze(result)


def direct_operator(monomial,mode,argument,charge):
    energy,target = sum(argument),sum(argument)+mode
    if target<0:
        return ()
    if not monomial:
        return ((argument,1),) if mode==0 else ()
    choices = tuple(range(-target,0))+(0,)+tuple(range(1,energy+1))
    result = {}
    for indices in product(choices,repeat=len(monomial)):
        if sum(indices) != -mode:
            continue
        scale = charge**indices.count(0)
        output = list(argument)
        for n,index in zip(monomial,indices):
            scale *= binomial(-index-1,n-1)
        if not scale:
            continue
        for index in indices:
            if index>0:
                multiplicity = output.count(index)
                if not multiplicity:
                    scale=0
                    break
                scale *= index*multiplicity
                output.remove(index)
        if scale:
            output.extend(-index for index in indices if index<0)
            output=tuple(sorted(output,reverse=True))
            result[output]=result.get(output,0)+scale
    return freeze(result)


@lru_cache(maxsize=100_000)
def dual_operator(partition,taper,mode,argument,charge):
    h=sum(partition)
    result={}
    for monomial,value in dual_polynomial(partition):
        scale=value*binomial(sum(monomial)+h,taper)
        add_scaled(result,operator(monomial,mode,argument,charge),scale)
    return freeze(result)


def piece_vector(x,v,argument,shift,charge,reverse=False):
    h=sum(x)
    if sum(v)!=h:
        raise ValueError("Inconsistent label grades")
    result={}
    for i in range(2*h+1):
        scale=(-1)**i*dual_scale(v)
        if reverse:
            first=dual_operator(x,i,shift-h+i,argument,charge)
            for intermediate,value in first:
                add_scaled(result,operator(v,h-shift-i,intermediate,charge),scale*value)
        else:
            first=operator(v,h-shift-i,argument,charge)
            for intermediate,value in first:
                add_scaled(result,dual_operator(x,i,shift-h+i,intermediate,charge),scale*value)
    return freeze(result)


def moment(x,v,argument,degree,charge):
    bound=sum(argument)+sum(x)
    result={}
    for shift in range(-bound,bound+1):
        add_scaled(result,piece_vector(x,v,argument,shift,charge),shift**degree)
    return freeze(result)
