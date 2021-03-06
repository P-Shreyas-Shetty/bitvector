from typing import Union

class BitVec:
    def __init__(self, size = 32, val = 0, signed = False):
        if(type(val)==BitVec):
            self.val = val.val
        else: self.val = val & ((1 << size) - 1) if val>=0 else (val+2**size) & ((1<<size) - 1)#; self.signed = True
        self.size   = size
        self.signed = signed

    def set_val(self, val):
        self.val = ((1<<self.size)-1) & val

    @classmethod
    def assign(cls, lhs, rhs):
        if isinstance(rhs, BitVec):
            pass
        elif isinstance(rhs, int):
            rhs = BitVec(rhs.bit_length(), rhs)
        else:
            raise TypeError(f"RHS should be either int or BitVec")
        if isinstance(lhs, BitVec):
            lhs[...] = rhs
        elif isinstance(lhs, tuple):
            shift = 0
            for i, v in enumerate(reversed(lhs)):
                v.set_val(rhs.val>>shift)
                shift = v.size

    def __getitem__(self, index):
        if(type(index) == int):
            if(index>self.size-1):
                raise ValueError(f"index {index} > size-1 {self.size-1}")
            else:
                return BitVec(1, self.val >> index)
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            
            start = self.size if start is None else start
            stop = 0 if stop is None else stop
            step = 1 if step is None else step

            if step<0:
                start, stop = stop, start
                step = -step

            if start<stop:
                start, stop = stop, start
                rev = 1
            else: rev = 0

            bv = BitVec((start-stop+1)//step, 0)
            bs = bin(self.val)[2::]

            if(len(bs) < self.size):
                bs = '0'*(self.size-len(bs)) + bs
            bs = bs[::-1]
            if(rev==0):
                bv.val = int('0b'+bs[stop:start+1:step][::-1], base=2)
            else:
                bv.val = int('0b'+bs[stop:start+1:step], base=2)
            return bv
    

    # represent method
    def __repr__(self):
        string_val = str(bin(self.val))[2:].zfill(self.size)
        if(self.signed == True): #if_signed
            if(string_val[0] == "1" ): #if_negative
                value = 2**self.size - self.val
                return "-"+str(self.size) + "b" + str(bin(value))[2:].zfill(self.size)
            else:
                return str(self.size) + "b" + string_val 
        else:
            return str(self.size) + "b" + string_val

    #add method
    def __add__(self, lhs):
        if(isinstance(lhs, int)):
            size = max([self.size, lhs.bit_length()]) + 1
            val = (self.val + lhs)
        else:
            size = max([self.size, lhs.size]) + 1
            val = (self.val + lhs.val)
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    # inplace add method
    def __iadd__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = (self.val + lhs) & ((1<<size) - 1)
        else:
            val = (self.val + lhs.val) & ((1<<size) - 1)
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    #sub method
    def __sub__(self, lhs):
        if(isinstance(lhs, int)):
            size = max([self.size, lhs.bit_length()]) + 1
            val = (self.val + ~lhs+1)
        else:
            size = max([self.size, lhs.size]) + 1
            val = (self.val + ~lhs.val+1)
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    #inplace sub method
    def __isub__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = (self.val + ~lhs+1) 
        else:
            val = (self.val + ~lhs.val+1) 
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    #mul method
    def __mul__(self, lhs):
        if(isinstance(lhs, int)):
            val = (self.val * lhs)
            size = val.bit_length()
        else:
            val = (self.val * lhs.val)
            size = val.bit_length()
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    #inplace mul method        
    def __imul__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val * lhs & ((1<<size) - 1)
        else:
            val = self.val * lhs.val & ((1<<size) - 1)
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    #power method
    def __pow__(self, lhs):
        val = (self.val ** lhs.val)
        size = val.bit_length()
        return BitVec(size, val)

    def __ipow__(self, lhs):
        size = self.size
        val = (self.val ** lhs.val) &((1<<size) - 1)
        return BitVec(size, val)

    #div method     --- neg number pending
    def __truediv__ (self, lhs):
        if isinstance(lhs, int):
            size = max([self.size, lhs.bit_length()])
            val = self.val // lhs 
        else:
            size = max([self.size, lhs.size])
            val = self.val // lhs.val
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    #inplace div method
    def __itruediv__ (self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val // lhs
        else:
            val = self.val // lhs.val
        return BitVec(size, val)

    #modulo method   --- neg number pending
    def __mod__ (self, lhs):
        size = max([self.size, lhs.size])
        if isinstance(lhs, int):
            val = self.val % lhs
        else:
            val = self.val % lhs.val
        return BitVec(size, val)
    
    #inplace modulo method
    def __imod__ (self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val % lhs
        else:
            val = self.val % lhs.val
        return BitVec(size, val)

    #left shift method
    def __lshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val << lhs
        else:
            val = (self.val << lhs.val)
        return BitVec(size, val)
        
    def __ilshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val << lhs
        else:
            val = (self.val << lhs.val)
        return BitVec(size, val)
    
    # right shift method        
    def __rshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val >> lhs
        else:
            val = (self.val >> lhs.val)
        return BitVec(size, val)
        
    # circular left shift method
    def clshift(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = (self.val << lhs%size)|(self.val >> (size - lhs%size)) 
        else:
            val = (self.val << lhs.val%size)|(self.val >> (size - lhs.val%size)) 
        return BitVec(size, val)
    
    def __irshift__(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = self.val >> lhs
        else:
            val = (self.val >> lhs.val)
        return BitVec(size, val)
        
    #circular right shift method
    def crshift(self, lhs):
        size = self.size
        if isinstance(lhs, int):
            val = (self.val >> lhs%size) | (self.val << (size - lhs%size)) 
        else:
            val = (self.val >> lhs.val%size) | (self.val << (size - lhs.val%size)) 
        return BitVec(size, val)

    # bitwise and method
    def __and__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = max([self.size, lhs.size])
        val = self.val & lhs.val
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    def __iand__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = self.size
        val = self.val & lhs.val
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    #bitwise or method
    def __or__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = max([self.size, lhs.size])
        val = self.val | lhs.val 
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    def __ior__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = self.size
        val = self.val | lhs.val 
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    #bitwise XOR method
    def __xor__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = max([self.size, lhs.size])
        val = self.val ^ lhs.val 
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)

    
    def __ixor__(self, lhs):
        if(isinstance(lhs, int)):
            lhs = BitVec(lhs, lhs.bit_length())
        size = self.size
        val = self.val ^ lhs.val 
        try:
            return BitVec(size = size, val = val, signed = self.signed | lhs.signed)
        except:
            return BitVec(size = size, val = val, signed = self.signed)
    
    # invert method
    def __invert__(self):
        size = self.size
        val = ~self.val  
        return BitVec(size = size, val = val, signed = self.signed )
    
    #to_hex convert method
    def hex(self):
        string_val = str(bin(self.val))[2:].zfill(self.size)
        if(self.signed == True): #if_signed
            if(string_val[0]=="1"):#if_negative
                value = 2**self.size - self.val
                return "-" + str(self.size) + "h" + hex(value)[2:]
            else:
                return str(self.size) + "h" + hex(self.val)[2:]
        else:
            return str(self.size) + "h" + hex(self.val)[2:]

    #to_dec convert method
    def dec(self):
        string_val = str(bin(self.val))[2:].zfill(self.size)
        if(self.signed == True): #if_signed
            if(string_val[0]=="1"):#if_negative
                value = 2**self.size - self.val
                return  "-" + str(value)
            else:
                return str(self.val)
        else:
            return str(self.val)

    #to_bin convert method
    def bin(self):
            return str(self.size) + "b" + bin(self.val)[2:]

    #equal to 
    def __eq__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val == lhs
        else:
            bool_var = (self.val == lhs.val)
        return bool_var 
   
    #less than
    def __lt__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val < lhs
        else:
            bool_var = (self.val < lhs.val)
        return bool_var

    #less than or equal
    def __le__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val <= lhs
        else:
            bool_var = self.val <= lhs.val 
        return bool_var
    
    #not equal to
    def __ne__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val != lhs
        else:
            bool_var = self.val != lhs.val 
        return bool_var 

    #greater than
    def __gt__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val > lhs
        else:
            bool_var = self.val > lhs.val 
        return bool_var 

    #greater than equal
    def __ge__(self, lhs):
        if isinstance(lhs, int):
            bool_var = self.val >= lhs
        else:
            bool_var = self.val >= lhs.val
        return bool_var 

    def __matmul__(self, lhs):
        '''
        Use @ operator for repetition and concatenation
        If one of the argument is integer then it acts like repetition operator
        If both arguments are bitvector, then it concatenates them
        ex: a:BitVec and b:BitVec
        2@a #Repeat a or concatenate a with itself
        a@b #concat a with b
        '''
        if isinstance(lhs, int):
            v = self.val
            for i in range(lhs):
                v = (v<<self.size) | self.val
            return BitVec(self.size*lhs, v)
        elif (type(lhs)==BitVec):
            rsize = self.size + lhs.size
            outval = (self.val << lhs.size) | lhs.val
            return BitVec(rsize, outval)

    


    def __rmatmul__(self, rhs):
        return self@rhs;


    def __setitem__(self, index, val):
        if isinstance(val, int): val = BitVec(val.bit_length(), val)
        elif not isinstance(val, BitVec): raise TypeError(f"Expected RHS to be either BitVec or int; got {type(val)}")
        if isinstance(index, int):
            if index>(self.size-1):
                raise IndexError(f"Index {index} out of range; size of the vector is {self.size}")
            else:
                self.val = (self.val | (val[0]<<index)) if val[0]==1 else (self.val & ~(val[0]<<index))
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None: start = self.size-1
            if stop is None: stop = 0
            if not step is None:
                raise IndexError(f"Step is not supported in BitVector set")
            else:
                if start>=stop: start1, stop1 = start, stop
                else: start1, stop1 = stop, start
                mask = ((1<<(start1-stop1+1))-1)<<stop1
                val_pshd = val[start1-stop1:0] if val.size>=(start1-stop1+1) else BitVec((start1-stop1+1-val.size), 0x0)@val
                if start<stop: val_pshd = val_pshd[::-1]
                val_pshd = BitVec(val_pshd.size+stop1, val_pshd)<<stop1
                mask = BitVec(self.size, mask)
                self.val = ((~mask&self)|val_pshd).val
        elif index is Ellipsis:
            self.val = ((1<<self.size)-1) & val.val
        else: raise IndexError(f"Index of type {type(index)} not expected")
    
    def __iter__(self):
        for i in range(self.size):
            yield self[i]
            
    def pattern_match(self, pattern=None):
        '''
        Return an iterator returns index on the vector where MSB of the 
        pattern coincide with bitvector value
        Ex: a = bv(12, 0b110111011101)
        pat = a.pattern_match(bv(4, 0b1101))
        next(pat) => 3
        next(pat) => 7
        ...

        If no pattern is passed, default is assumed to be bv(1,1)

        '''
        if pattern is None: pattern = BitVec(1,1)
        assert(isinstance(self, BitVec))
        for index in range(pattern.size-1, self.size):
            if self[index:(index-pattern.size+1)]==pattern:
                yield index




class Concat:
    def __init__(self, *vecs:BitVec) -> None:
        self.__vec_list = list(vecs)

    def __getattribute__(self, name: str) -> BitVec:
        if name == "size":
            size = 0
            for v in self.__vec_list:
                size += v.size
            return size
        elif name == "val":
            vec = BitVec(0, 0)
            for v in self.__vec_list:
                vec = vec @ v
            return vec.val
        elif name == "vec":
            vec = BitVec(0, 0)
            for v in self.__vec_list:
                vec = vec @ v
            return vec
        else:
            raise AttributeError(f"Attribute {name} doesn't exist")
