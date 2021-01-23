class BitVec:
    def __init__(self, size, val=0):
        if(type(val)==BitVec):
            self.val = val.val
        else: self.val = val & ((1 << size) - 1) if val>=0 else (val+2**size) & ((1<<size) - 1)
        self.size = size

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
        return "0b"+str(bin(self.val))[2:].zfill(self.size) #return bin(self.val)
    
    #add method
    def __add__(self, lhs):
        size = max([self.size, lhs.size]) + 1
        val = (self.val + lhs.val)
        return BitVec(size, val)
    
    # inplace add method
    def __iadd__(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = (self.val + lhs) & ((1<<size) - 1)
        else:
            val = (self.val + lhs.val) & ((1<<size) - 1)
        return BitVec(size, val)

    #sub method
    def __sub__(self, lhs):
        size = max([self.size, lhs.size]) + 1
        val = (self.val + ~lhs.val+1)
        return BitVec(size, val)

    #inplace sub method
    def __isub__(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = (self.val + ~lhs+1) 
        else:
            val = (self.val + ~lhs.val+1) 
        return BitVec(size, val)
    
    #mul method
    def __mul__(self, lhs):
        val = (self.val * lhs.val)
        size = val.bit_length()
        return BitVec(size, val)
           
    #inplace mul method        
    def __imul__(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = self.val * lhs & ((1<<size) - 1)
        else:
            val = self.val * lhs.val & ((1<<size) - 1)
        return BitVec(size, val)
    
    #power method
    def __pow__(self, lhs):
        val = (self.val ** lhs.val)
        size = val.bit_length()
        return BitVec(size, val)

    #div method
    def __truediv__ (self, lhs):
        size = max([self.size, lhs.size])
        val = self.val // lhs.val
        return BitVec(size, val)

    #inplace div method
    def __itruediv__ (self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = self.val // lhs
        else:
            val = self.val // lhs.val
        return BitVec(size, val)

    #modulo method
    def __mod__ (self, lhs):
        size = max([self.size, lhs.size])
        val = self.val % lhs.val
        return BitVec(size, val)
    
    #inplace modulo method
    def __imod__ (self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = self.val % lhs
        else:
            val = self.val % lhs.val
        return BitVec(size, val)

    #left shift method
    def __lshift__(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = self.val << lhs
        else:
            val = (self.val << lhs.val)
        return BitVec(size, val)
        
    # right shift method        
    def __rshift__(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = self.val >> lhs
        else:
            val = (self.val >> lhs.val)
        return BitVec(size, val)
        
    # circular left shift method
    def clshift(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = (self.val << lhs%size)|(self.val >> (size - lhs%size)) 
        else:
            val = (self.val << lhs.val%size)|(self.val >> (size - lhs.val%size)) 
        return BitVec(size, val)
    
    #circular right shift method
    def crshift(self, lhs):
        size = self.size
        if(type(lhs) is int):
            val = (self.val >> lhs%size) | (self.val << (size - lhs%size)) 
        else:
            val = (self.val >> lhs.val%size) | (self.val << (size - lhs.val%size)) 
        return BitVec(size, val)

    # bitwise and method
    def __and__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val & lhs.val
        return BitVec(size, val)
    
    #bitwise or method
    def __or__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val | lhs.val 
        return BitVec(size,val)
    
    #bitwise XOR method
    def __xor__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val ^ lhs.val 
        return BitVec(size,val)
    
    # invert method
    def __invert__(self):
        size = self.size
        val = ~self.val  
        return BitVec(size,val)
    
    #to_hex convert method
    def hex(self):
        return hex(self.val)

    #to_dec convert method
    def dec(self):
        return str(self.val)

    #to_bin convert method
    def bin(self):
        return bin(self.val())

    #equal_to method
    def __eq__(self, lhs):
        bool_val = (self.val == lhs.val)
        return bool_val ## BitVec(size=1, val = int(bool_val))
    
    #less than method
    def __lt__(self, lhs):
        bool_var = self.val < lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_valo))
    
    #less than or equal to method
    def __le__(self, lhs):
        bool_var = self.val <= lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))
    
    # not equal to method
    def __ne__(self, lhs):
        bool_var = self.val != lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))

    # greater than method
    def __gt__(self, lhs):
        bool_var = self.val > lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))

    #greater than or equal to method
    def __ge__(self, lhs):
        bool_var = self.val >= lhs.val
        return bool_var ##BitVec(size=1, val = int(bool_val))

    def __matmul__(self, lhs):
        '''
        Use @ operator for repetition and concatenation
        If one of the argument is integer then it acts like repetition operator
        If both arguments are bitvector, then it concatenates them
        ex: a:BitVec and b:BitVec
        2@a #Repeat a or concatenate a with itself
        a@b #concat a with b

        '''
        if (type(lhs)==int):
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

                    

                

    #TODO: Complete the implementation for the following
    #Operators to be supported
    # +,-,/,*,**, |, &, ^, ~, <<, >>

    #Other implementation details
    #Let the results of operations be computed for highest available width and then reduced 
    #Further add implementation such that one is able to assign to declared vector
    #Ex: c = bv(32) #declare 32 biit vector
    #    c[...] = 0x10 #Option 1
    #    c.v    = 0x10 #add an attr v and write setattr for that
    #    c[_]   = 0x10 #similar to first option; but declare a variable _ in the library



