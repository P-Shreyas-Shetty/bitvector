from bitvec import BitVec as bv

a = bv(16, 0xff0f)

b = bv(16, 0xf0f0)

print(f"a|b={a|b}")
assert (a|b == bv(16, 0xffff))

print(f"a&b={a&b}")
assert (a&b == bv(16, 0xf000))

print(f"a^b={a^b}")
assert(a^b == bv(16, 0x0fff))

print(f"~a={~a}")
print(f"bv(16,0x3)[1:0]={bv(16,0x3)[1:0], (bv(16,0x3)[1:0]).size}")
assert(~a == bv(16, 0x00f0))
a = bv(8, 0xf8)
a[3:2] = 0b01
print(f"set_item: a = {a}")

a = bv(4, 0xa)
for i,v in enumerate(a):
    print(f"a[{i}]={v}")

c = bv(4, 0x0)
s = bv(4, 0x0)

bv.assign((c,s), bv(4,0xf)+bv(4,0x1))
print(f"c,s:{c},{s}")
s[...] = 0xf
print(f"c,s:{c},{s}")
print(f"bv(9,0b111010001)[::-1]={bv(9,0b111010001)[::-1]}")
print(f"a+b={a+b}")
assert(a+b == a.val+b.val)
#print(f"a-b={a-b}")
#assert(a-b == a.val - b.val)
print(f"a*b={(a*b).hex()}")
print(f"a/b={(a/b).hex()}")


print(f"a[3:0]={a[3:0]}")
print(f"a[0]={a[0]}")

print(f"bv(4, 0b1101)[0:3]={bv(4,0b1101)[0:3]}")

print(f"bv(4,0xf)+bv(4,0x1)={bv(4,0xf)+bv(4,0x1)}")