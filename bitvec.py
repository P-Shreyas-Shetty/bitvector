"""
Provides verilog like Bitvec type
Has both signed and unsigned arithmatic
"""


class BitVec:
    """
    Class for verilog-like bitvector. You can define bitvector of arbitrary size, either
    signed or unsigned.
    Example usage:
    from bitvec import BitVec as bv

    #Define an unsigned bitvec: bit [10:0] a;
    a = bv(11)

    #With size and value; unsigned:
    a = bv(11, 0b10111)

    #With size and value; signed:
    a = bv(11, 0b10111, True)

    Supports:
     - all arithmatic and bitwise operator
     - Verilog style slice indexing and slice assignment. Unlike verilog, also supports
       reverse index
     - concatenation & repetiton through @ operator and concat/C class method
     - Some extra helper function such as get_all_set_bits to return index of all set bits

    """

    val: int
    size: int
    is_signed: bool

    def __init__(self, size=32, val=0, signed=False):
        if isinstance(val, BitVec):
            self.val = val.val
        else:
            self.val = (
                val & ((1 << size) - 1)
                if val >= 0
                else (val + 2**size) & ((1 << size) - 1)
            )
        self.size = size
        self.is_signed = signed

    def get_val(self):
        """
        Get the integer value
        FIXME: Use something other than string conversion
        """
        string_val = str(bin(self.val))[2:].zfill(self.size)
        if self.is_signed:  # if_signed
            # This is pretty crude, using strings like this
            # But we aren't much interested in performance
            if string_val[0] == "1":  # if_negative
                value = 2**self.size - self.val
                str_val = "-" + str(value)
            else:
                str_val = str(self.val)
            return int(str_val)
        else:
            return self.val

    def __int__(self):
        return self.get_val()

    def set_val(self, val):
        """Setter for value"""
        self.val = ((1 << self.size) - 1) & val

    @classmethod
    def assign(cls, lhs, rhs):
        """
        assign allowd you to assign concatenations and other
        bit vector assignment pattern

        bv.assign(x, (y,z)) === x = {y,z} in Verilog
        """
        if isinstance(rhs, BitVec):
            pass
        elif isinstance(rhs, int):
            rhs = BitVec(rhs.bit_length(), rhs)
        else:
            raise TypeError("RHS should be either int or BitVec")
        if isinstance(lhs, BitVec):
            lhs[...] = rhs
        elif isinstance(lhs, tuple):
            shift = 0
            for _, v in enumerate(reversed(lhs)):
                v.set_val(rhs.val >> shift)
                shift = v.size

    @classmethod
    def signed(cls, size=32, val=0):
        """
        Create signed BitVec
        """
        return BitVec(size, val, signed=True)

    @classmethod
    def u2s(cls, ubv):
        """
        Convert unsigned bitvec to signed bitvec
        """
        return BitVec(ubv.size, ubv.get_val(), True)

    @classmethod
    def unsigned(cls, size=32, val=0):
        """
        Create unsigned BitVec
        """
        return BitVec(size, val, signed=False)

    @classmethod
    def from_val(cls, val, signed=False):
        """
        Deduces size from the value
        """
        return BitVec(val.bit_length() if val != 0 else 1, val, signed)

    def __getitem__(self, index):
        if isinstance(index, int):
            if index > self.size - 1:
                raise ValueError(f"index {index} > size-1 {self.size-1}")
            else:
                return BitVec(1, self.val >> index)
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step

            start = self.size if start is None else start
            stop = 0 if stop is None else stop
            step = 1 if step is None else step

            if step < 0:
                start, stop = stop, start
                step = -step

            if start < stop:
                start, stop = stop, start
                rev = 1
            else:
                rev = 0

            bv = BitVec((start - stop + 1) // step, 0)
            bs = bin(self.val)[2::]

            if len(bs) < self.size:
                bs = "0" * (self.size - len(bs)) + bs
            bs = bs[::-1]
            if rev == 0:
                bv.val = int("0b" + bs[stop : start + 1 : step][::-1], base=2)
            else:
                bv.val = int("0b" + bs[stop : start + 1 : step], base=2)
            return bv

    # represent method
    def __repr__(self):
        string_val = str(bin(self.val))[2:].zfill(self.size)
        if self.is_signed:  # if_signed
            if string_val[0] == "1":  # if_negative
                value = 2**self.size - self.val
                return "-" + str(self.size) + "b" + str(bin(value))[2:].zfill(self.size)
            else:
                return str(self.size) + "b" + string_val
        else:
            return "0b" + string_val

    # add method
    def __add__(self, lhs):
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()]) + 1
            val = self.val + lhs
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            size = max([self.size, lhs.size]) + 1
            val = self.val + lhs.val
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # inplace add method
    def __iadd__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = (self.val + lhs) & ((1 << size) - 1)
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            val = (self.val + lhs.val) & ((1 << size) - 1)
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # sub method
    def __sub__(self, lhs):
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()]) + 1
            val = self.val + ~lhs + 1
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            size = max([self.size, lhs.size]) + 1
            val = self.val + ~lhs.val + 1
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # inplace sub method
    def __isub__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val + ~lhs + 1
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            val = self.val + ~lhs.val + 1
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # mul method
    def __mul__(self, lhs):
        if isinstance(lhs, int):
            val = self.val * lhs
            size = val.bit_length()
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            val = self.val * lhs.val
            size = val.bit_length()
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # inplace mul method
    def __imul__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val * lhs & ((1 << size) - 1)
            return BitVec(size=size, val=val, signed=self.is_signed)
        else:
            val = self.val * lhs.val & ((1 << size) - 1)
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # power method
    def __pow__(self, lhs):
        val = self.val**lhs.val
        size = val.bit_length()
        return BitVec(size, val)

    def __ipow__(self, lhs):
        size = self.size
        val = (self.val**lhs.val) & ((1 << size) - 1)
        return BitVec(size, val)

    def __truediv__(self, lhs):
        """
        In case of negative/positive or vice versa, leaves positive reminder
        """
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()])
            val = (-1 if self.get_val() * lhs < 0 else 1) * (
                abs(self.get_val()) // abs(lhs)
            )
            return BitVec(size=size, val=val, signed=self.is_signed)
        elif isinstance(lhs, BitVec):
            size = max([self.size, lhs.size])
            val = (-1 if self.get_val() * lhs.get_val() < 0 else 1) * (
                abs(self.get_val()) // abs(lhs.get_val())
            )
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __floordiv__(self, lhs):
        """
        In case of negative/positive or vice versa, leaves positive reminder
        """
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()])
            val = self.get_val() // lhs
            return BitVec(size=size, val=val, signed=self.is_signed)
        elif isinstance(lhs, BitVec):
            size = max([self.size, lhs.size])
            val = self.get_val() // lhs.get_val()
            return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # inplace div method
    def __itruediv__(self, lhs):
        return lhs / self

    def __ifloordiv__(self, lhs):
        return lhs // self

    def __mod__(self, lhs):
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()])
            val = (-1 if self.get_val() * lhs < 0 else 1) * (
                abs(self.get_val()) % abs(lhs)
            )
            return BitVec(size, val, signed=self.is_signed)
        elif isinstance(lhs, BitVec):
            size = max([self.size, lhs.size])
            val = (-1 if self.get_val() * lhs.get_val() < 0 else 1) * (
                abs(self.get_val()) % abs(lhs.get_val())
            )
            return BitVec(size, val, signed=self.is_signed | lhs.is_signed)

    # inplace modulo method
    def __imod__(self, lhs):
        return lhs % self

    # left shift method
    def __lshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val << lhs
        else:
            val = self.val << lhs.val
        return BitVec(size, val)

    def __ilshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val << lhs
        else:
            val = self.val << lhs.val
        return BitVec(size, val)

    # right shift method
    def __rshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val >> lhs
        else:
            val = self.val >> lhs.val
        return BitVec(size, val)

    def clshift(self, lhs):
        """
        circular left shift method
        """
        size = self.size
        if isinstance(lhs, int):
            val = (self.val << lhs % size) | (self.val >> (size - lhs % size))
        else:
            val = (self.val << lhs.val % size) | (self.val >> (size - lhs.val % size))
        return BitVec(size, val)

    def __irshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val >> lhs
        else:
            val = self.val >> lhs.val
        return BitVec(size, val)

    def crshift(self, lhs):
        """
        circular right shift method
        """
        size = self.size
        if isinstance(lhs, int):
            val = (self.val >> lhs % size) | (self.val << (size - lhs % size))
        else:
            val = (self.val >> lhs.val % size) | (self.val << (size - lhs.val % size))
        return BitVec(size, val)

    # bitwise and method
    def __and__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = max([self.size, lhs.size])
        val = self.val & lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __rand__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = max([self.size, lhs.size])
        val = self.val & lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __iand__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = self.size
        val = self.val & lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # bitwise or method
    def __or__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = max([self.size, lhs.size])
        val = self.val | lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __ror__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs, lhs.bit_length())
        size = max([self.size, lhs.size])
        val = self.val | lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __ior__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = self.size
        val = self.val | lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # bitwise XOR method
    def __xor__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = max([self.size, lhs.size])
        val = self.val ^ lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __rxor__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = max([self.size, lhs.size])
        val = self.val ^ lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    def __ixor__(self, lhs):
        if isinstance(lhs, int):
            lhs = BitVec(lhs.bit_length(), lhs)
        size = self.size
        val = self.val ^ lhs.val
        return BitVec(size=size, val=val, signed=self.is_signed | lhs.is_signed)

    # invert method
    def __invert__(self):
        size = self.size
        val = ~self.val
        return BitVec(size=size, val=val, signed=self.is_signed)

    # to_hex convert method
    def hex(self):
        """
        returns hex string
        """
        return hex(self.get_val())

    def dec(self):
        """
        returns decimal string
        """
        return str(self.get_val())

    def bin(self):
        """
        returns binary string
        """
        return bin(self.val)

    # equal to
    def __eq__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() == lhs
        else:
            bool_var = self.get_val() == lhs.get_val()
        return bool_var

    # less than
    def __lt__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() < lhs
        else:
            bool_var = self.get_val() < lhs.get_val()
        return bool_var

    # less than or equal
    def __le__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() <= lhs
        else:
            bool_var = self.get_val() <= lhs.get_val()
        return bool_var

    # not equal to
    def __ne__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() != lhs
        else:
            bool_var = self.get_val() != lhs.get_val()
        return bool_var

    # greater than
    def __gt__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() > lhs
        else:
            bool_var = self.get_val() > lhs.get_val()
        return bool_var

    # greater than equal
    def __ge__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.get_val() >= lhs
        else:
            bool_var = self.get_val() >= lhs.get_val()
        return bool_var

    def __matmul__(self, lhs):
        """
        Use @ operator for repetition and concatenation
        If one of the argument is integer then it acts like repetition operator
        If both arguments are bitvector, then it concatenates them
        ex: a:BitVec and b:BitVec
        2@a #Repeat a or concatenate a with itself
        a@b #concat a with b
        """
        if isinstance(lhs, int):
            v = self.val
            for _ in range(lhs):
                v = (v << self.size) | self.val
            return BitVec(self.size * lhs, v)
        elif isinstance(lhs, BitVec):
            rsize = self.size + lhs.size
            outval = (self.val << lhs.size) | lhs.val
            return BitVec(rsize, outval)

    def __rmatmul__(self, rhs):
        return self @ rhs

    @classmethod
    def concat(cls, *args):
        """Concatenate vectors
        Under the hood calls concat operator
        If integer is passed, converts it to BitVec using from_val method.
        """
        res = BitVec(0)
        for v in args:
            if isinstance(v, int):
                v = BitVec.from_val(v)
            res @= v
        return res

    C = concat

    @classmethod
    def reduce(cls):
        """
        Returns a Reducer object that can be used to use bitwise operator as reduction operators
        Ex in verilog: |4'b1101 == 1'b1
        Here: bv.R|bv(4, 0b1101) == bv(1,0b1)
        or  : bv.reduce()|bv(4, 0b1101)==bv(1,0b1)
        """
        return Reducer()

    R = reduce

    def __setitem__(self, index, val):
        if isinstance(val, int):
            val = BitVec.from_val(val)
        elif not isinstance(val, BitVec):
            raise TypeError(f"Expected RHS to be either BitVec or int; got {type(val)}")
        if isinstance(index, int):
            if index > (self.size - 1):
                raise IndexError(
                    f"Index {index} out of range; size of the vector is {self.size}"
                )
            elif index < 0:
                shift = self.size + index
                self[shift:shift] = val[0]
            else:
                self[index:index] = val[0]
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None:
                start = self.size - 1
            if stop is None:
                stop = 0
            if not step is None:
                raise IndexError("Step is not supported in BitVector set")
            else:
                if start >= stop:
                    start1, stop1 = start, stop
                else:
                    start1, stop1 = stop, start
                mask = ((1 << (start1 - stop1 + 1)) - 1) << stop1
                val_pshd = (
                    val[start1 - stop1 : 0]
                    if val.size >= (start1 - stop1 + 1)
                    else BitVec((start1 - stop1 + 1 - val.size), 0x0) @ val
                )
                if start < stop:
                    val_pshd = val_pshd[::-1]
                val_pshd = BitVec(val_pshd.size + stop1, val_pshd) << stop1
                mask = BitVec(self.size, mask)
                self.val = ((~mask & self) | val_pshd).val
        elif index is Ellipsis:
            self.val = ((1 << self.size) - 1) & val.val
        else:
            raise IndexError(f"Index of type {type(index)} not expected")

    def __iter__(self):
        for i in range(self.size):
            yield self[i]

    def pattern_match(self, pattern=None):
        """
        Return an iterator returns index on the vector where MSB of the
        pattern coincide with bitvector value
        Ex: a = bv(12, 0b110111011101)
        pat = a.pattern_match(bv(4, 0b1101))
        next(pat) => 3
        next(pat) => 7
        ...

        If no pattern is passed, default is assumed to be bv(1,1)

        """
        if pattern is None:
            pattern = BitVec(1, 1)
        assert isinstance(self, BitVec)
        for index in range(pattern.size - 1, self.size):
            if self[index : (index - pattern.size + 1)] == pattern:
                yield index

    def get_all_set_bits(self):
        """
        Returns list of indices of set bits
        Probably should look for something better, but can
        be used directly as bv.get_all_set_bits(<int>)
        """
        if isinstance(self, int):
            return list(BitVec.from_val(self).pattern_match())
        return list(self.pattern_match())

    def get_all_reset_bits(self):
        """Returns list of all indices of bits not set"""
        if isinstance(self, int):
            arg = BitVec.from_val(self)
        else:
            arg = self
        set_bits = BitVec.get_all_set_bits(arg)
        return [i for i in range(arg.size) if not i in set_bits]

    def get_parity(self):
        """Returns parity of vector"""
        return BitVec.reduce() ^ self


class Reducer:
    """
    This is a helper class to introduce reduce operation in a readable fashion
    Use case:
    from bitvec import Reducer as R

    R| bv(9, 0b1111) => bv(1,1)

    This works on binary bitwise operators (|, &, ^)

    alternatively, this object is provided in bv class as classmethod
    bv.reduce()|bv(9, 0b11010101) or bv.R()|bv(9, 0b11101010) (recommonded)
    """

    def __init__(self) -> None:
        pass

    def __or__(self, op: BitVec) -> BitVec:
        ret = BitVec(1)
        for bit in op:
            ret |= bit
        return ret

    def __and__(self, op: BitVec) -> BitVec:
        ret = BitVec(1)
        for bit in op:
            ret &= bit
        return ret

    def __xor__(self, op: BitVec) -> BitVec:
        ret = BitVec(1)
        for bit in op:
            ret ^= bit
        return ret
