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
                return self.val >> index
        elif(type(index) == slice):
            start, stop, step = index.start, index.stop, index.step
            
            start = self.size if start is None else start
            stop = 0 if stop is None else stop
            step = 1 if step is None else step

            if start<stop:
                start, stop = stop, start
                rev = 1
            else: rev = 0

            bv = BitVec((start-stop)//step, 0)
            bs = bin(self.val)[2::]

            if(len(bs) < self.size):
                bs = '0'*(self.size-len(bs)) + bs
            bs = bs[::-1]
            if(rev==0):
                bv.val = int('0b'+bs[stop:start+1:step][::-1], base=2)
            else:
                bv.val = int('0b'+bs[stop:start+1:step], base=2)
            return bv
    
    def __repr__(self):
        return "0b"+str(bin(self.val))[2:].zfill(self.size) #return bin(self.val)

    def __add__(self, lhs):
        size = max([self.size, lhs.size])
        val = (self.val + lhs.val) & ((1<<size) - 1)
        return BitVec(size, val)

    def __sub__(self, lhs):
        size = max([self.size, lhs.size])
        val = (self.val + ~lhs.val+1)
        return BitVec(size, val)

    def __mul__(self, lhs):
        size = self.size + lhs.size
        val = (self.val * lhs.val)
        return BitVec(size, val)
        
    def __pow__(self, lhs):
        val = (self.val ** lhs.val)
        size = len(bin(val)[2:]) ## should this be used to optimze size for power, mul etc ? given its string operation, can save the size
        return BitVec(size, val)

    def __div__ (self, lhs):
        size = max([self.size, lhs.size])
        num = self.val 
        counter = 0
        while(num>=lhs.val):
            num -= lhs.val 
            counter+=1
        return BitVec(size, val=counter)
  
    def __mod__ (self, lhs):
        size = max([self.size, lhs.size])
        num = self.val 
        counter = 0
        while(num>=lhs.val):
            num -= lhs.val 
            counter+=1
        return BitVec(size, val=num)

    def __lshift__(self, lhs):
        size = self.size
        val = (self.val << lhs.val)
        return BitVec(size, val)
        
    def __rshift__(self, lhs):
        size = self.size
        val = (self.val >> lhs.val)
        return BitVec(size, val)
        
    def __and__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val & lhs.val
        return BitVec(size, val)
    
    def __or__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val | lhs.val 
        return BitVec(size,val)
        
    def __xor__(self, lhs):
        size = max([self.size, lhs.size])
        val = self.val ^ lhs.val 
        return BitVec(size,val)
        
    def __invert__(self):
        size = self.size
        val = ~self.val  
        return BitVec(size,val)

    def hex(self):
        return hex(self.val)

    def dec(self):
        return str(self.val)

    def bin(self):
        return bin(self.val())

    def __eq__(self, lhs):
        bool_val = (self.val == lhs.val)
        return bool_val ## BitVec(size=1, val = int(bool_val))
    
    def __lt__(self, lhs):
        bool_var = self.val < lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))
    
    def __le__(self, lhs):
        bool_var = self.val <= lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))
    
    def __ne__(self, lhs):
        bool_var = self.val != lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))

    def __gt__(self, lhs):
        bool_var = self.val > lhs.val 
        return bool_var ## BitVec(size=1, val = int(bool_val))

    def __ge__(self, lhs):
        bool_var = self.val >= lhs.val
        return bool_var ##BitVec(size=1, val = int(bool_val))


    #TODO: Complete the implementation of set
    #def __setitem__(self, index, val):
    #    if(type(index) == int):
    #        if(index>self.size-1):
    #            raise ValueError(f"index {index} > size-1 {self.size-1}")
    #        else:
    #            self.val = ((1 << index) | self.val) if val else (~(1 << index) & self.val) 
    #    if(type(index)==slice):
    #        start, stop, step = index.start, index.stop, index.step
    #        if(step!=None or step!=1):
    #            raise IndexError("Cannot set discontinuous slice")
    #        else:
    #            subs, ln = val.val, val.size #assuming it's bitveca
    #            ln1 = stop - start + 1

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



