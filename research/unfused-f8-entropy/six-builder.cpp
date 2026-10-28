#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>
using namespace std;
using A = array<int, 10>;
using P = array<int, 10>;
uint64_t key(const A &a) {
  uint64_t z = 0;
  for (int i = 0; i < 10; i++)
    z |= uint64_t(a[i]) << (4 * i);
  return z;
}
A perm(const A &a, const P &p) {
  A b{};
  for (int i = 0; i < 10; i++)
    b[p[i]] = a[i];
  return b;
}
int mul(int a, int b) {
  int r = 0;
  while (b) {
    if (b & 1)
      r ^= a;
    b >>= 1;
    a <<= 1;
    if (a & 8)
      a ^= 11;
  }
  return r;
}
int tr(int a) {
  int a2 = mul(a, a);
  return a ^ a2 ^ mul(a2, a2);
}
void gen(int n, int i, A a, vector<A> &v) {
  if (i == 9) {
    a[i] = n;
    v.push_back(a);
    return;
  }
  for (int x = 0; x <= n; x++) {
    a[i] = x;
    gen(n - x, i + 1, a, v);
  }
}
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  int dual[8];
  for (int b = 0; b < 8; b++) {
    dual[b] = -1;
    for (int B = 0; B < 8; B++) {
      bool ok = 1;
      for (int a = 0; a < 8; a++)
        ok &= (tr(mul(a, B)) == (__builtin_popcount((unsigned)(a & b)) % 2));
      if (ok)
        dual[b] = B;
    }
    if (dual[b] < 0)
      return 3;
  }
  auto cls = [&](int a, int b) {
    int B = dual[b];
    return a == 0 && B == 0 ? 0 : a == 0 ? 1 : B == 0 ? 2 : 2 + mul(a, B);
  };
  int C[10][10]{};
  bool initialized[10]{};
  for (int c = 0; c < 8; c++)
    for (int d = 0; d < 8; d++) {
      int row[10]{};
      for (int a = 0; a < 8; a++)
        for (int b = 0; b < 8; b++)
          row[cls(a, b)] +=
              __builtin_popcount((unsigned)((b & c) ^ (a & d))) % 2 ? -1 : 1;
      int i = cls(c, d);
      for (int j = 0; j < 10; j++) {
        if (initialized[i] && C[i][j] != row[j])
          return 4;
        C[i][j] = row[j];
      }
      initialized[i] = true;
    }
  P f{}, sw{}, id{};
  for (int i = 0; i < 10; i++)
    id[i] = i;
  f = id;
  sw = id;
  sw[1] = 2;
  sw[2] = 1;
  for (int i = 1; i < 8; i++)
    f[2 + i] = 2 + mul(i, i);
  vector<P> group;
  for (int t = 0; t < 3; t++)
    for (int flip = 0; flip < 2; flip++) {
      P p = id;
      for (int k = 0; k < t; k++)
        for (int i = 0; i < 10; i++)
          p[i] = f[p[i]];
      if (flip)
        for (int i = 0; i < 10; i++)
          p[i] = sw[p[i]];
      for (int i = 0; i < 10; i++)
        for (int j = 0; j < 10; j++)
          if (C[i][j] != C[p[i]][p[j]])
            return 5;
      group.push_back(p);
    }
  vector<A> rows;
  gen(6, 0, A{}, rows);
  map<uint64_t, int> idx;
  for (int i = 0; i < (int)rows.size(); i++)
    idx[key(rows[i])] = i;
  vector<int> rowrep(rows.size(), -1), eligible(rows.size());
  vector<vector<int>> inorbits;
  int nr = 0;
  for (int i = 0; i < (int)rows.size(); i++)
    if (rowrep[i] < 0) {
      for (auto &g : group)
        rowrep[idx.at(key(perm(rows[i], g)))] = nr;
      nr++;
    }
  for (int i = 0; i < (int)rows.size(); i++) {
    auto a = rows[i];
    int n2 = 0, n3 = 0, ma = 0;
    for (int j = 1; j < 10; j++) {
      n2 += a[j] == 2;
      n3 += a[j] == 3;
      ma = max(ma, a[j]);
    }
    if ((a[0] == 0 && ma <= 3 && (n3 == 0 || (n3 == 1 && n2 == 0))) ||
        (a[0] == 1 && ma <= 2 && n2 <= 1))
      eligible[i] = 1;
  }
  for (int i = 0; i < (int)rows.size(); i++)
    if (eligible[i] == 1) {
      vector<int> o;
      for (auto &g : group) {
        int j = idx.at(key(perm(rows[i], g)));
        if (eligible[j] == 1) {
          o.push_back(j);
          eligible[j] = 2;
        }
      }
      inorbits.push_back(o);
    }
  int nc = inorbits.size();
  cerr << "rows " << rows.size() << " orbits " << nr << " " << nc << "\n";
  if (rows.size() != 5005)
    return 6;
  vector<int> canonical(nr, -1);
  for (int i = 0; i < (int)rows.size(); i++)
    if (canonical[rowrep[i]] < 0)
      canonical[rowrep[i]] = i;
  unordered_map<uint64_t, int> repidx;
  for (int j = 0; j < nr; j++)
    repidx[key(rows[canonical[j]])] = j;
  vector<int64_t> matrix((size_t)(nr + 1) * nc);
  for (int col = 0; col < nc; col++) {
    A a = rows[inorbits[col][0]];
    unordered_map<uint64_t, long long> q{{0, 1}};
    for (int i = 0; i < 10; i++)
      for (int k = 0; k < a[i]; k++) {
        unordered_map<uint64_t, long long> next;
        for (auto [z, x] : q)
          for (int j = 0; j < 10; j++)
            if (C[i][j])
              next[z + (uint64_t(1) << (4 * j))] += x * C[i][j];
        q.swap(next);
      }
    vector<long long> out(nr);
    vector<int> seen;
    for (auto &g : group) {
      int target = idx.at(key(perm(a, g)));
      if (find(seen.begin(), seen.end(), target) != seen.end())
        continue;
      seen.push_back(target);
      for (auto [z, x] : q) {
        uint64_t zz = 0;
        for (int i = 0; i < 10; i++)
          zz |= ((z >> (4 * i)) & 15) << (4 * g[i]);
        auto it = repidx.find(zz);
        if (it != repidx.end())
          out[it->second] += x;
      }
      auto it = repidx.find(key(rows[target]));
      if (it != repidx.end())
        out[it->second] -= 262144; // 8^6
    }
    for (int r = 0; r < nr; r++) {
      matrix[(size_t)r * nc + col] = out[r];
    }
    int pair = 0;
    for (int i : inorbits[col]) {
      int exponent = 0;
      for (int k = 3; k < 10; k++)
        exponent += rows[i][k] * tr(k - 2);
      pair += exponent % 2 ? -1 : 1;
    }
    matrix[(size_t)nr * nc + col] = pair;
    if (col % 100 == 0)
      cerr << "built " << col << "\n";
  }
  ofstream meta(string(argv[1]) + ".meta");
  meta << nr << " " << nc << "\n";
  for (auto &o : inorbits) {
    for (int x : rows[o[0]])
      meta << x << " ";
    meta << "\n";
  }
  meta.close();
  ofstream out(argv[1], ios::binary);
  out.write((char *)matrix.data(), matrix.size() * sizeof(int64_t));
  if (!out)
    return 7;
  cerr << "done\n";
}
