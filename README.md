# bitvector

This is a bitvector class implementation for python. This should be useful for quick prototyping.

## Usage

### 1. Importing module

```python
from bitvec import BitVec as bv

a = bv(12, 0xfff) #Inialization explained below
a.val #: Integer value stored under the hood
      #  This is always stored as positive integer
      #  Negative number stored as 2's complement
a.size # Size of bitvector

# Display options
print(a) #Prints binary by default
         #If signed vector, prints as signed number

# To print decimal, hex, binary
print(a.dec()) #12'hfff
print(a.hex()) #4095
print(a.bin()) #12b111111111111
```

### 2. Initiailizing 

```python

# Unsigned 
a = bv(12, 0xfff) #12hfff
#The above statement is equivalent to:
# bit [11:0] a = 'hfff;

#If val is negative in unsigned number, treated as 2's complement
a1 = bv(10, -0xf) 

#signed
b = bv(12, 0xfff, True)
# The above statement is equivalent to:
# bit signed [11:0] a = 'hfff;

#Vector with default size 0 and signed and unsigned
c = bv(12, signed=True) #signed vector
d = bv(12) #unsigned vector
#Above two statements are same as:
#bit [11:0] c;
#bit signed [11:0] d;

#Signed vector: second approach
e = bv.signed(12, -0xf) #==> bit signed [11:0] e = -'hf;

#Method to construct from value only; size is set as size of input value
#Default unsigned
f = bv.from_val(0xf) #unsigned; size=4bit
```

### 3.Assignment, Indexing and Casting
```python
# Declare vectors
b0 = bv(12, 0xfff)
b1 = bv(12, 0x000)
a0 = bv(20)
a1 = bv(2)

#Assign vectors
bv.assign([a1, a0], [b0,b1]) #<==> {a1, a0} = {b0, b1}
bv.assign(a0, [b0, b1]) #<==> a0 = {b0, b1}

# Signed to unsigned
s = bv(12, 0xf, signed=True)
us = bv(12, s)

#Unsigned to signed
s = bv.signed(12, us)
#or
s = bv(12, us, signed=True)

#Indexing
a = bv(4, 0b1101)
b0 = a[0] #b0 = bv(1,1)
b1 = a[1:0] #b1 = bv(2, 0b01)
b2 = a[0:1] #b2 = bv(2, 0b10)
b3 = a[::-1] #Reverses

a = bv(2,0)
a[1:0] = 0b10  #a = bv(2, 0b10)
a[0:1] = a[1:0] #Part assignment in reverse order

```

### 4. Basic Operations
- Addition and subtraction always returns vector of size max(arg1, arg2) + 1 to avoid loosing carry bit. To retain size, use bv.assign method

```python
a = bv(4, 0)
b = bv(4, 0xf)
c = bv(1,0)
s = bv(4,0)

a = a+1 # a = bv(5, 1)
bv.assign((c,s), a+b) # {c,s}=a+b;

# Subtraction is similar: can operate between integer or another bitvec
a = a - 1
a = a - b
```

- Multiplication operation returns bitvec of size arg1.size+arg2.size.

```
a = bv(4, 0xf)*bv(4, 0xf) # a = bv(8, 0b11100001)
```

- Division operation has two variants. Both variants behave similarly in case of unsigned arguments. In case operations between signed and unsigned numbers, ```/``` operator will return such that reminder is negative. For a Python like behaviour (positive reminder always), ```//``` operator is overloaded 

- All bit-wise operations behave as expected.
- For circular shift operation, ```clshift``` and ```crshift``` methods are provided


- ```@``` operator is used for repeatition as well as concatenation

```python
a = bv(8, 123)
a1 = a@a #a1 = {a, a}
a2 = 5@a #a2 = {5{a}}
```

### 5. More useful methods

- ```pattern_match(pattern)``` : 
     Returns iterator that gives next occurance of pattern in vector.
     Ex: 
     ```python
     a = bv(12, 0xabab)
     p = bv(4,0xb)
     l = a.pattern_match(p)
     next(l) #==> 3
     next(l) #==>11
     ```

- ```get_all_set_bits()``` : Returns list of all the set bits' indices.

```python
a = bv(12, 0b1000000100010)
a.get_all_set_bits() #==>[1, 5]
```

- ```get_val()``` : Returns integer value of vector
```python
a = bv(12, -0xf)
b = bv(12, -0xf, signed=True)
a.get_val() #==>4081
b.get_val() #==>-15
```



