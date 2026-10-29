"""Finite independent entry-formula checks for both cyclic Walsh factor cuts."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


field = load('stream_field', ROOT / 'odd-prime-rank-transfer' / 'field.py')
refined = load('stream_refined', ROOT / 'three-bit-macro-walsh' / 'refined.py')


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sign(bits):
    return -1 if bits.bit_count() % 2 else 1


def cyclic_inverse_entry(base, n, s, v, p):
    return pow(base, n-1-((v-s) % n), p) * pow((pow(base,n,p)-1) % p,-1,p) % p


def main():
    data = refined.construct(1)
    n, base = 8, 3
    classes = refined.SCHEME['classes']
    index = {a:i for i,a in enumerate(data['types'])}
    labels = [(a,b) for a in range(n) for b in range(n)]
    summary = []
    comparisons = invalid = 0
    for p in (23,47):
        for piece in data['pieces']:
            def coefficient(values,a,b):
                alpha = tuple(int(j == classes[a,b]) for j in range(6))
                return field.rational_residue(values[index[alpha]],p)
            f = {(a,b):coefficient(piece['function'],a,b) for a,b in labels}
            h = {(a,b):coefficient(piece['transformed'],a,b) for a,b in labels}
            row_labels = [z for z in labels if f[z]]
            col_labels = [z for z in labels if h[z]]
            require(len(row_labels) <= piece['row_support'] and len(col_labels) <= piece['col_support'], 'support')
            ni = pow(n,-1,p)
            def row_left(x,y,a,b):
                coefficient = base*(x == (y^a)) - (((x+1)%n) == (y^a))
                return f[a,b] * ni * sign(b & y) * coefficient % p
            def row_right(u,v,a,b):
                return sign(b & (u^a)) * cyclic_inverse_entry(base,n,u^a,v,p) % p
            def col_left(x,u,c,d):
                nx = (x+1)%n
                value = base*sign(d & x)*(u == (x^c)) - sign(d & nx)*(u == (nx^c))
                return h[c,d] * ni*ni * value % p
            def col_right(y,v,c,d):
                return sign(d & y)*cyclic_inverse_entry(base,n,y^c,v,p) % p
            # Arrays here make the finite exhaustive checker quick. The proof's
            # entry evaluator needs only the current label, indices and field value.
            rl = {(x,y):[row_left(x,y,*z) for z in row_labels] for x in range(n) for y in range(n)}
            rr = {(u,v):[row_right(u,v,*z) for z in row_labels] for u in range(n) for v in range(n)}
            cl = {(x,u):[col_left(x,u,*z) for z in col_labels] for x in range(n) for u in range(n)}
            cr = {(y,v):[col_right(y,v,*z) for z in col_labels] for y in range(n) for v in range(n)}
            def original(r,y,u,s):
                if r^y != u^s:
                    return 0
                return ni*sum(f[r^y,b]*sign(b & (y^s)) for b in range(n)) % p
            for x in range(n):
                for y in range(n):
                    for u in range(n):
                        for v in range(n):
                            direct = 0
                            for r,coefficient_ in ((x,base),((x+1)%n,-1)):
                                s = r^y^u
                                direct += coefficient_*original(r,y,u,s)*cyclic_inverse_entry(base,n,s,v,p)
                            direct %= p
                            rsum = sum(a*b for a,b in zip(rl[x,y],rr[u,v])) % p
                            csum = sum(a*b for a,b in zip(cl[x,u],cr[y,v])) % p
                            require(direct == rsum == csum, 'Factor entry identity')
                            comparisons += 2
            for support, left, right in ((row_labels,row_left,row_right),(col_labels,col_left,col_right)):
                code_bits = max(0,(len(support)-1).bit_length())
                for code in range(1 << code_bits):
                    decoded = support[code] if code < len(support) else None
                    if code >= len(support):
                        def entry_with_code(function, i, j):
                            return 0 if decoded is None else function(i,j,*decoded)
                        require(entry_with_code(left,0,0) == 0 and entry_with_code(right,0,0) == 0,
                                'Invalid code factors must vanish')
                        invalid += 1
                    else:
                        require(decoded == support[code], 'Valid support code')
            summary.append({'prime':p,'row_support':len(row_labels),'col_support':len(col_labels)})
    require(invalid > 0, 'Invalid support codes not exercised')
    paths = [HERE/'PROOF.md',HERE/'verify.py',ROOT/'three-bit-macro-walsh'/'refined.py',
             ROOT/'odd-prime-rank-transfer'/'field.py']
    print(json.dumps({'status':'PASS','scope':'finite factor entries, not full recursion or asymptotic support unranking',
                      'base':base,'n':n,'pieces':len(data['pieces']),'primes':[23,47],
                      'factor_entry_comparisons':comparisons,'invalid_binary_code_slots':invalid,
                      'support_profiles':summary,
                      'sha256':{str(p.relative_to(ROOT.parent)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))


if __name__ == '__main__':
    main()
