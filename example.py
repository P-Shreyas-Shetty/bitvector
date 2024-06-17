'''
This code generates a self validating data

The data sent consists of two parts: 4b src addr and 28bit seq num

We scrmable the data by XOR with a key then calculate CRC on scrambled data

The final data is produced by interleaving CRC with scrambled data

data = {seq_n[27:0], src_addr[3:0]}
data' = data ^ KEY

crc = crc_calc(CRC_IN, data')

data_out = {data'[7:0], crc[7:0], data'[15:8], crc[15:8], data'[23:16], crc[23:16], data'[31:24], crc[31:24]}


To validate data:
crc = { data_out[7:0 ], data_out[23:16], data_out[39:32], data_out[55:48]} 
data' =  { data_out[15:8], data_out[31:24], data_out[47:40], data_out[63:56]}

crc' = crc_calc(CRC_IN, data')

crc == crc' for validity

'''

from bitvec import BitVec as bv

KEY = bv(32, 0xa21b345c) #this data is used to "scramble" the data fields
CRC_IN = bv(32, 0x1234abcd)

def crc_calc(crc_in, data):
    '''Calculates 32b CRC'''
    crc = bv(32, 0x0)
    crc[0] = crc_in[0] ^ crc_in[1] ^ crc_in[2] ^ crc_in[3] ^ crc_in[4] ^ crc_in[6] ^ crc_in[7] ^ crc_in[8] ^ crc_in[16] ^ crc_in[20] ^ crc_in[22] ^ crc_in[23] ^ crc_in[26] ^ data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[6] ^ data[7] ^ data[8] ^ data[16] ^ data[20] ^ data[22] ^ data[23] ^ data[26]
    crc[1] = crc_in[1] ^ crc_in[2] ^ crc_in[3] ^ crc_in[4] ^ crc_in[5] ^ crc_in[7] ^ crc_in[8] ^ crc_in[9] ^ crc_in[17] ^ crc_in[21] ^ crc_in[23] ^ crc_in[24] ^ crc_in[27] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[7] ^ data[8] ^ data[9] ^ data[17] ^ data[21] ^ data[23] ^ data[24] ^ data[27]
    crc[2] = crc_in[0] ^ crc_in[2] ^ crc_in[3] ^ crc_in[4] ^ crc_in[5] ^ crc_in[6] ^ crc_in[8] ^ crc_in[9] ^ crc_in[10] ^ crc_in[18] ^ crc_in[22] ^ crc_in[24] ^ crc_in[25] ^ crc_in[28] ^ data[0] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6] ^ data[8] ^ data[9] ^ data[10] ^ data[18] ^ data[22] ^ data[24] ^ data[25] ^ data[28]
    crc[3] = crc_in[1] ^ crc_in[3] ^ crc_in[4] ^ crc_in[5] ^ crc_in[6] ^ crc_in[7] ^ crc_in[9] ^ crc_in[10] ^ crc_in[11] ^ crc_in[19] ^ crc_in[23] ^ crc_in[25] ^ crc_in[26] ^ crc_in[29] ^ data[1] ^ data[3] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[9] ^ data[10] ^ data[11] ^ data[19] ^ data[23] ^ data[25] ^ data[26] ^ data[29]
    crc[4] = crc_in[2] ^ crc_in[4] ^ crc_in[5] ^ crc_in[6] ^ crc_in[7] ^ crc_in[8] ^ crc_in[10] ^ crc_in[11] ^ crc_in[12] ^ crc_in[20] ^ crc_in[24] ^ crc_in[26] ^ crc_in[27] ^ crc_in[30] ^ data[2] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[10] ^ data[11] ^ data[12] ^ data[20] ^ data[24] ^ data[26] ^ data[27] ^ data[30]
    crc[5] = crc_in[0] ^ crc_in[3] ^ crc_in[5] ^ crc_in[6] ^ crc_in[7] ^ crc_in[8] ^ crc_in[9] ^ crc_in[11] ^ crc_in[12] ^ crc_in[13] ^ crc_in[21] ^ crc_in[25] ^ crc_in[27] ^ crc_in[28] ^ crc_in[31] ^ data[0] ^ data[3] ^ data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[9] ^ data[11] ^ data[12] ^ data[13] ^ data[21] ^ data[25] ^ data[27] ^ data[28] ^ data[31]
    crc[6] = crc_in[0] ^ crc_in[2] ^ crc_in[3] ^ crc_in[9] ^ crc_in[10] ^ crc_in[12] ^ crc_in[13] ^ crc_in[14] ^ crc_in[16] ^ crc_in[20] ^ crc_in[23] ^ crc_in[28] ^ crc_in[29] ^ data[0] ^ data[2] ^ data[3] ^ data[9] ^ data[10] ^ data[12] ^ data[13] ^ data[14] ^ data[16] ^ data[20] ^ data[23] ^ data[28] ^ data[29]
    crc[7] = crc_in[1] ^ crc_in[3] ^ crc_in[4] ^ crc_in[10] ^ crc_in[11] ^ crc_in[13] ^ crc_in[14] ^ crc_in[15] ^ crc_in[17] ^ crc_in[21] ^ crc_in[24] ^ crc_in[29] ^ crc_in[30] ^ data[1] ^ data[3] ^ data[4] ^ data[10] ^ data[11] ^ data[13] ^ data[14] ^ data[15] ^ data[17] ^ data[21] ^ data[24] ^ data[29] ^ data[30]
    crc[8] = crc_in[0] ^ crc_in[2] ^ crc_in[4] ^ crc_in[5] ^ crc_in[11] ^ crc_in[12] ^ crc_in[14] ^ crc_in[15] ^ crc_in[16] ^ crc_in[18] ^ crc_in[22] ^ crc_in[25] ^ crc_in[30] ^ crc_in[31] ^ data[0] ^ data[2] ^ data[4] ^ data[5] ^ data[11] ^ data[12] ^ data[14] ^ data[15] ^ data[16] ^ data[18] ^ data[22] ^ data[25] ^ data[30] ^ data[31]
    crc[9] = crc_in[0] ^ crc_in[2] ^ crc_in[4] ^ crc_in[5] ^ crc_in[7] ^ crc_in[8] ^ crc_in[12] ^ crc_in[13] ^ crc_in[15] ^ crc_in[17] ^ crc_in[19] ^ crc_in[20] ^ crc_in[22] ^ crc_in[31] ^ data[0] ^ data[2] ^ data[4] ^ data[5] ^ data[7] ^ data[8] ^ data[12] ^ data[13] ^ data[15] ^ data[17] ^ data[19] ^ data[20] ^ data[22] ^ data[31]
    crc[10] = crc_in[0] ^ crc_in[2] ^ crc_in[4] ^ crc_in[5] ^ crc_in[7] ^ crc_in[9] ^ crc_in[13] ^ crc_in[14] ^ crc_in[18] ^ crc_in[21] ^ crc_in[22] ^ crc_in[26] ^ data[0] ^ data[2] ^ data[4] ^ data[5] ^ data[7] ^ data[9] ^ data[13] ^ data[14] ^ data[18] ^ data[21] ^ data[22] ^ data[26]
    crc[11] = crc_in[1] ^ crc_in[3] ^ crc_in[5] ^ crc_in[6] ^ crc_in[8] ^ crc_in[10] ^ crc_in[14] ^ crc_in[15] ^ crc_in[19] ^ crc_in[22] ^ crc_in[23] ^ crc_in[27] ^ data[1] ^ data[3] ^ data[5] ^ data[6] ^ data[8] ^ data[10] ^ data[14] ^ data[15] ^ data[19] ^ data[22] ^ data[23] ^ data[27]
    crc[12] = crc_in[2] ^ crc_in[4] ^ crc_in[6] ^ crc_in[7] ^ crc_in[9] ^ crc_in[11] ^ crc_in[15] ^ crc_in[16] ^ crc_in[20] ^ crc_in[23] ^ crc_in[24] ^ crc_in[28] ^ data[2] ^ data[4] ^ data[6] ^ data[7] ^ data[9] ^ data[11] ^ data[15] ^ data[16] ^ data[20] ^ data[23] ^ data[24] ^ data[28]
    crc[13] = crc_in[0] ^ crc_in[3] ^ crc_in[5] ^ crc_in[7] ^ crc_in[8] ^ crc_in[10] ^ crc_in[12] ^ crc_in[16] ^ crc_in[17] ^ crc_in[21] ^ crc_in[24] ^ crc_in[25] ^ crc_in[29] ^ data[0] ^ data[3] ^ data[5] ^ data[7] ^ data[8] ^ data[10] ^ data[12] ^ data[16] ^ data[17] ^ data[21] ^ data[24] ^ data[25] ^ data[29]
    crc[14] = crc_in[0] ^ crc_in[1] ^ crc_in[4] ^ crc_in[6] ^ crc_in[8] ^ crc_in[9] ^ crc_in[11] ^ crc_in[13] ^ crc_in[17] ^ crc_in[18] ^ crc_in[22] ^ crc_in[25] ^ crc_in[26] ^ crc_in[30] ^ data[0] ^ data[1] ^ data[4] ^ data[6] ^ data[8] ^ data[9] ^ data[11] ^ data[13] ^ data[17] ^ data[18] ^ data[22] ^ data[25] ^ data[26] ^ data[30]
    crc[15] = crc_in[1] ^ crc_in[2] ^ crc_in[5] ^ crc_in[7] ^ crc_in[9] ^ crc_in[10] ^ crc_in[12] ^ crc_in[14] ^ crc_in[18] ^ crc_in[19] ^ crc_in[23] ^ crc_in[26] ^ crc_in[27] ^ crc_in[31] ^ data[1] ^ data[2] ^ data[5] ^ data[7] ^ data[9] ^ data[10] ^ data[12] ^ data[14] ^ data[18] ^ data[19] ^ data[23] ^ data[26] ^ data[27] ^ data[31]
    crc[16] = crc_in[1] ^ crc_in[4] ^ crc_in[7] ^ crc_in[10] ^ crc_in[11] ^ crc_in[13] ^ crc_in[15] ^ crc_in[16] ^ crc_in[19] ^ crc_in[22] ^ crc_in[23] ^ crc_in[24] ^ crc_in[26] ^ crc_in[27] ^ crc_in[28] ^ data[1] ^ data[4] ^ data[7] ^ data[10] ^ data[11] ^ data[13] ^ data[15] ^ data[16] ^ data[19] ^ data[22] ^ data[23] ^ data[24] ^ data[26] ^ data[27] ^ data[28]
    crc[17] = crc_in[2] ^ crc_in[5] ^ crc_in[8] ^ crc_in[11] ^ crc_in[12] ^ crc_in[14] ^ crc_in[16] ^ crc_in[17] ^ crc_in[20] ^ crc_in[23] ^ crc_in[24] ^ crc_in[25] ^ crc_in[27] ^ crc_in[28] ^ crc_in[29] ^ data[2] ^ data[5] ^ data[8] ^ data[11] ^ data[12] ^ data[14] ^ data[16] ^ data[17] ^ data[20] ^ data[23] ^ data[24] ^ data[25] ^ data[27] ^ data[28] ^ data[29]
    crc[18] = crc_in[0] ^ crc_in[3] ^ crc_in[6] ^ crc_in[9] ^ crc_in[12] ^ crc_in[13] ^ crc_in[15] ^ crc_in[17] ^ crc_in[18] ^ crc_in[21] ^ crc_in[24] ^ crc_in[25] ^ crc_in[26] ^ crc_in[28] ^ crc_in[29] ^ crc_in[30] ^ data[0] ^ data[3] ^ data[6] ^ data[9] ^ data[12] ^ data[13] ^ data[15] ^ data[17] ^ data[18] ^ data[21] ^ data[24] ^ data[25] ^ data[26] ^ data[28] ^ data[29] ^ data[30]
    crc[19] = crc_in[0] ^ crc_in[1] ^ crc_in[4] ^ crc_in[7] ^ crc_in[10] ^ crc_in[13] ^ crc_in[14] ^ crc_in[16] ^ crc_in[18] ^ crc_in[19] ^ crc_in[22] ^ crc_in[25] ^ crc_in[26] ^ crc_in[27] ^ crc_in[29] ^ crc_in[30] ^ crc_in[31] ^ data[0] ^ data[1] ^ data[4] ^ data[7] ^ data[10] ^ data[13] ^ data[14] ^ data[16] ^ data[18] ^ data[19] ^ data[22] ^ data[25] ^ data[26] ^ data[27] ^ data[29] ^ data[30] ^ data[31]
    crc[20] = crc_in[0] ^ crc_in[3] ^ crc_in[4] ^ crc_in[5] ^ crc_in[6] ^ crc_in[7] ^ crc_in[11] ^ crc_in[14] ^ crc_in[15] ^ crc_in[16] ^ crc_in[17] ^ crc_in[19] ^ crc_in[22] ^ crc_in[27] ^ crc_in[28] ^ crc_in[30] ^ crc_in[31] ^ data[0] ^ data[3] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[11] ^ data[14] ^ data[15] ^ data[16] ^ data[17] ^ data[19] ^ data[22] ^ data[27] ^ data[28] ^ data[30] ^ data[31]
    crc[21] = crc_in[0] ^ crc_in[2] ^ crc_in[3] ^ crc_in[5] ^ crc_in[12] ^ crc_in[15] ^ crc_in[17] ^ crc_in[18] ^ crc_in[22] ^ crc_in[26] ^ crc_in[28] ^ crc_in[29] ^ crc_in[31] ^ data[0] ^ data[2] ^ data[3] ^ data[5] ^ data[12] ^ data[15] ^ data[17] ^ data[18] ^ data[22] ^ data[26] ^ data[28] ^ data[29] ^ data[31]
    crc[22] = crc_in[2] ^ crc_in[7] ^ crc_in[8] ^ crc_in[13] ^ crc_in[18] ^ crc_in[19] ^ crc_in[20] ^ crc_in[22] ^ crc_in[26] ^ crc_in[27] ^ crc_in[29] ^ crc_in[30] ^ data[2] ^ data[7] ^ data[8] ^ data[13] ^ data[18] ^ data[19] ^ data[20] ^ data[22] ^ data[26] ^ data[27] ^ data[29] ^ data[30]
    crc[23] = crc_in[0] ^ crc_in[3] ^ crc_in[8] ^ crc_in[9] ^ crc_in[14] ^ crc_in[19] ^ crc_in[20] ^ crc_in[21] ^ crc_in[23] ^ crc_in[27] ^ crc_in[28] ^ crc_in[30] ^ crc_in[31] ^ data[0] ^ data[3] ^ data[8] ^ data[9] ^ data[14] ^ data[19] ^ data[20] ^ data[21] ^ data[23] ^ data[27] ^ data[28] ^ data[30] ^ data[31]
    crc[24] = crc_in[2] ^ crc_in[3] ^ crc_in[6] ^ crc_in[7] ^ crc_in[8] ^ crc_in[9] ^ crc_in[10] ^ crc_in[15] ^ crc_in[16] ^ crc_in[21] ^ crc_in[23] ^ crc_in[24] ^ crc_in[26] ^ crc_in[28] ^ crc_in[29] ^ crc_in[31] ^ data[2] ^ data[3] ^ data[6] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[15] ^ data[16] ^ data[21] ^ data[23] ^ data[24] ^ data[26] ^ data[28] ^ data[29] ^ data[31]
    crc[25] = crc_in[1] ^ crc_in[2] ^ crc_in[6] ^ crc_in[9] ^ crc_in[10] ^ crc_in[11] ^ crc_in[17] ^ crc_in[20] ^ crc_in[23] ^ crc_in[24] ^ crc_in[25] ^ crc_in[26] ^ crc_in[27] ^ crc_in[29] ^ crc_in[30] ^ data[1] ^ data[2] ^ data[6] ^ data[9] ^ data[10] ^ data[11] ^ data[17] ^ data[20] ^ data[23] ^ data[24] ^ data[25] ^ data[26] ^ data[27] ^ data[29] ^ data[30]
    crc[26] = crc_in[2] ^ crc_in[3] ^ crc_in[7] ^ crc_in[10] ^ crc_in[11] ^ crc_in[12] ^ crc_in[18] ^ crc_in[21] ^ crc_in[24] ^ crc_in[25] ^ crc_in[26] ^ crc_in[27] ^ crc_in[28] ^ crc_in[30] ^ crc_in[31] ^ data[2] ^ data[3] ^ data[7] ^ data[10] ^ data[11] ^ data[12] ^ data[18] ^ data[21] ^ data[24] ^ data[25] ^ data[26] ^ data[27] ^ data[28] ^ data[30] ^ data[31]
    crc[27] = crc_in[0] ^ crc_in[1] ^ crc_in[2] ^ crc_in[6] ^ crc_in[7] ^ crc_in[11] ^ crc_in[12] ^ crc_in[13] ^ crc_in[16] ^ crc_in[19] ^ crc_in[20] ^ crc_in[23] ^ crc_in[25] ^ crc_in[27] ^ crc_in[28] ^ crc_in[29] ^ crc_in[31] ^ data[0] ^ data[1] ^ data[2] ^ data[6] ^ data[7] ^ data[11] ^ data[12] ^ data[13] ^ data[16] ^ data[19] ^ data[20] ^ data[23] ^ data[25] ^ data[27] ^ data[28] ^ data[29] ^ data[31]
    crc[28] = crc_in[0] ^ crc_in[4] ^ crc_in[6] ^ crc_in[12] ^ crc_in[13] ^ crc_in[14] ^ crc_in[16] ^ crc_in[17] ^ crc_in[21] ^ crc_in[22] ^ crc_in[23] ^ crc_in[24] ^ crc_in[28] ^ crc_in[29] ^ crc_in[30] ^ data[0] ^ data[4] ^ data[6] ^ data[12] ^ data[13] ^ data[14] ^ data[16] ^ data[17] ^ data[21] ^ data[22] ^ data[23] ^ data[24] ^ data[28] ^ data[29] ^ data[30]
    crc[29] = crc_in[0] ^ crc_in[1] ^ crc_in[5] ^ crc_in[7] ^ crc_in[13] ^ crc_in[14] ^ crc_in[15] ^ crc_in[17] ^ crc_in[18] ^ crc_in[22] ^ crc_in[23] ^ crc_in[24] ^ crc_in[25] ^ crc_in[29] ^ crc_in[30] ^ crc_in[31] ^ data[0] ^ data[1] ^ data[5] ^ data[7] ^ data[13] ^ data[14] ^ data[15] ^ data[17] ^ data[18] ^ data[22] ^ data[23] ^ data[24] ^ data[25] ^ data[29] ^ data[30] ^ data[31]
    crc[30] = crc_in[3] ^ crc_in[4] ^ crc_in[7] ^ crc_in[14] ^ crc_in[15] ^ crc_in[18] ^ crc_in[19] ^ crc_in[20] ^ crc_in[22] ^ crc_in[24] ^ crc_in[25] ^ crc_in[30] ^ crc_in[31] ^ data[3] ^ data[4] ^ data[7] ^ data[14] ^ data[15] ^ data[18] ^ data[19] ^ data[20] ^ data[22] ^ data[24] ^ data[25] ^ data[30] ^ data[31]
    crc[31] = crc_in[0] ^ crc_in[1] ^ crc_in[2] ^ crc_in[3] ^ crc_in[5] ^ crc_in[6] ^ crc_in[7] ^ crc_in[15] ^ crc_in[19] ^ crc_in[21] ^ crc_in[22] ^ crc_in[25] ^ crc_in[31] ^ data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[5] ^ data[6] ^ data[7] ^ data[15] ^ data[19] ^ data[21] ^ data[22] ^ data[25] ^ data[31]
    return crc


def data_generator(src_addr):
    '''
    This is a data generator module

    It takes src addr as argument. Subsequent next calls
    on generator will give the next valid data
    '''
    cnt = bv(28, 0x0)
    src_addr = bv(4, src_addr)
    while True:
        data = (cnt @ src_addr) ^ KEY
        crc = crc_calc(CRC_IN, data)
        cnt[::] += 1
        data_out = bv.C(data[7 :0 ], crc[7 :0 ],
                        data[15:8 ], crc[15:8 ],
                        data[23:16], crc[23:16],
                        data[31:24], crc[31:24])

        yield data_out

def data_checker(src_addr):
    '''
    This is a generator that validates the input data
    It takes as argument src addr on geneartor creation

    gen.send(<data>)  will yield a dictionary containing field if the data is
    valid, is it from the correct src addr, as well it is the sequence number, i.e if there are drops or
    anything else wrong
    '''

    p_seqn = bv(28, 0x0)
    is_first_data = True
    while True:
        data = yield
        crc        = bv.C( data[7:0 ], data[23:16], data[39:32], data[55:48])
        data_field = bv.C( data[15:8], data[31:24], data[47:40], data[63:56])
        #check if crc is valid
        crc_c = crc_calc(CRC_IN, data_field)

        data_unscr = data_field ^ KEY
        data_addr = data_unscr[3:0]
        data_seqn = data_unscr[31:4]

        out = {
            'GOOD': True, 
            'DROP': False, 
            'CRC_PASS': True, 
            'IS_VLD_ADRR': True, 
            'PREV_SEQN': p_seqn.get_val(), 
            'PRESENT_SEQN': data_seqn.get_val() 
        }

        if crc != crc_c:
            out['GOOD'] = False
            out['CRC_PASS'] = False
        elif data_addr != src_addr:
            out['GOOD'] = False
            out['IS_VLD_ADRR'] = False
        elif is_first_data:
            is_first_data = False
            p_seqn = data_seqn
        else:
            bv.assign(p_seqn, p_seqn+1)
            if p_seqn!=data_seqn:
                out['DROP'] = True
                p_seqn.set_val(data_seqn.get_val())
        yield out



if __name__ == '__main__':
    gen = data_generator(bv(4, 0x1))
    checker = data_checker(bv(4, 0x1))
    next(checker)
    for i in range(8):
        data = next(gen)

        print(f"\n{i}: data={data.hex()}")
        #corrupting a single bit
        if i%3==3:
            print("   Corrupting data...")
            data[0] ^= 1
        check = checker.send(data)
        print(f"   CHECK: {check}")
        next(checker)
