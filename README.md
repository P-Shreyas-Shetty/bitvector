# bitvector

This is a bitvector class implementation for python. This should be useful for quick prototyping.

Use case

```
bv = BitVector #create alias for BitVector class

a = bv(32) #Bitvector of length 32 and initial value 0
b = bv(32, 0x0000_ffff) #Bitvector of length 32 and initial value 0x0000ffff

c = a + b #Now c is bitvector of length 32
c[10:0] = 0x0 #Set bit 0 through 10 of c to 0

```

The implementation is still incomplete. I have only worked on a skeleton code for now
