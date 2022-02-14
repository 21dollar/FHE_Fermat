import random
from scipy.stats import uniform
from scipy.stats import norm


#####################################################################################################################
def gen_F(f):
    return 2 ** 2 ** f + 1


#####################################################################################################################
def uniform_distribution(n,mean,spread):
    start = mean - spread
    width = spread*2
    data_uniform = uniform.rvs(size=n, loc=start, scale=width)
    return data_uniform


#####################################################################################################################
def normal_distribution(n,mean,std):
    data_normal = norm.rvs(size=n, loc=mean, scale=std)
    return data_normal

def get_number_in_blocks(X, H, L, reverse=None):
    # Convert the number to a bitarray
    X_in_bits = get_bitarray(X, H * L)
    # If necessary, convert the bitarray
    X_in_bits = X_in_bits[::-1]
    if reverse is None:
        X_in_bits = X_in_bits[::-1]
    #Get the string which represents the number in its blocks
    string = ""
    for block in range(L):
        # Print one block:
        for bit in range(H):
            string += (str(X_in_bits[bit + block * H]))
            if bit < H - 1:
                string += (",")
        if block < L - 1:
            string += ("__")
    return string

#####################################################################################################################
def get_bitarray(integer,length,reversed = None):
    bit_string = bin(integer)[2:]
    as_array = list(bit_string)
    as_integer_array = [int(numeric_string) for numeric_string in as_array]

    as_integer_array = as_integer_array[::-1]
    while(len(as_integer_array) < length):
        as_integer_array.append(0)
    if reversed == None:
        as_integer_array = as_integer_array[::-1]
    return as_integer_array


#####################################################################################################################
class Encryption:
    def __init__(self, A, B):

        self.A = int(A)
        self.B = int(B)

    def __str__(self) -> str:

        return "A: {}, B: {}".format(self.A,self.B)

    def print(self):
        #print("\n-------- print --------")

        print("A: {}, B: {}".format(self.A,self.B))

    def get_binary_string(self):
        #print("\n-------- get_binary_string --------")

        binary_A = bin(self.A)
        binary_B = bin(self.B)
        binary_string = "A: {}, B: {}".format(binary_A, binary_B)
        return binary_string

    def print_binary(self):
        #print("\n-------- print_binary --------")

        print(self.get_binary_string())
#####################################################################################################################


class FHE_Fermat:
#####################################################################################################################
    def gen_s(self):
        #print("\n-------- gen_s --------")

        s_dec = None
        s_bin = None
        L = self.L
        N = 0

        half_bit = False
        while half_bit == False:
            s_dec = random.randint(0, 2 ** L - 1)
            s_bin = [(s_dec >> bit) & 1 for bit in range(self.L - 1, -1, -1)]
            N = 0
            for i in s_bin:
                if i == 1:
                    N += 1
            self.N = N
            half_bit = N <= L / 2
        #print("Random s (in decimal): {}".format(s_dec))
        #print("Random s (in binary): {}".format(str(s_bin)))
        return s_dec


#####################################################################################################################
    def get_S(self):
        #print("\n-------- get_S --------")

       
        S = 0
        L = self.L
        H = self.H

        s = [(self.s >> bit) & 1 for bit in range(L - 1, -1, -1)]
        s_revers = s[::-1]
        
        for i in range(L):
            value = s_revers[i] * 2 ** (i * H)  
            S += value
        #print("S = {}, in binary: {}".format(S, get_number_in_blocks(S, H, L)))
        return S


#####################################################################################################################
    def encryption_of_zero(self, E=None):
        ##print("\n-------- encryption_of_zero --------")

        if E is None:
            E = 0
        
        A = random.randint(0, self.F)      
        B = (A * self.S + E) % self.F
        ##print("B = (A * S + E) % F = ({} * {} + {}) % {} = {}".format(A, self.S, E, self.F, B))
        
        return Encryption(A, B)


#####################################################################################################################
    def encrypt_number(self, number, E=None):
        ##print("\n-------- encrypt_number --------")

        
        zero_encryption = self.encryption_of_zero(E=E)        
        zero_encryption.B = (zero_encryption.B + number) % self.F      
        ##print("Encrypted number: {}".format(zero_encryption))
        return zero_encryption


#####################################################################################################################    
    def decrypt_number(self, encryption):
        ##print("\n-------- decrypt_number --------")

        number = (encryption.B - (encryption.A * self.S)) % self.F
        ##print("Number to decrypt: {}".format(encryption))
        ##print("Decrypted number: {}".format(number))
        return number


#####################################################################################################################
    def gen_E(self, gaussian=None):
        #print("\n-------- gen_E --------")

        E = 0
        L = self.L

        mean = 0
        e = None
        if gaussian == False:
            spread = 0.001
            e = uniform_distribution(L, mean, spread)
        else:
            std = 5
            e = normal_distribution(L, mean, std)

        e = e[::-1]
        for i in range(L):
            x = e[i] * 2 ** (i * self.H)
            E += x
        #print("Error e generated from distribution: {}".format(str(e)))
        #print("Error E generated from distribution: {}".format(E))
        return E


#####################################################################################################################
    def add_int(self, encryption_1, encryption_2):
        #print("\n-------- add_int --------")

        
        A_new = (encryption_1.A + encryption_2.A) % self.F
        B_new = (encryption_1.B + encryption_2.B) % self.F

        if A_new < 0:
            A_new += self.F

        if B_new < 0:
            B_new += self.F
        #print("new A is: {}".format(A_new))
        #print("new B is: {}".format(B_new))
        return Encryption(A_new, B_new)


#####################################################################################################################
    def sub_int(self, encryption_1, encryption_2):
        #print("\n-------- sub_int --------")

      
        A_new = (encryption_1.A - encryption_2.A) % self.F
        B_new = (encryption_1.B - encryption_2.B) % self.F
       
        if A_new < 0:
            A_new += self.F

        if B_new < 0:
            B_new += self.F
        #print("new A is: {}".format(A_new))
        #print("new B is: {}".format(B_new))
        return Encryption(A_new, B_new)


#####################################################################################################################
    def encrypt_bit(self, x, b_m=None):
        #print("\n-------- encrypt_bit --------")

        if b_m == None:
            b_m = self.H - 2
        message = 2 ** b_m * x

        encrypted_message = self.encrypt_number(number=message)
        #print("Encrypted Message {}".format(encrypted_message))
        return encrypted_message


#####################################################################################################################
    def decrypt_bit(self, encrypted_bit, b_m=None):
        #print("\n-------- decrypt_bit --------")


        if b_m == None:
            b_m = self.H - 2
        message = self.decrypt_number(encryption=encrypted_bit)
       
        approximate_x = message / 2 ** (b_m)
        x = int(approximate_x)
        #print("Rounded to a bit: {}".format(x))
        return x


#####################################################################################################################
    def encrypt_bit_vector(self, bit_vector):
        #print("\n-------- encrypt_bit_vector --------")


        b_m = self.H - 2
       
        bit_vector = bit_vector[::-1]
       
        message = 0
        for i in range(len(bit_vector)):
            x = bit_vector[i] * 2 ** (i * self.H + b_m)
            message += x
       
        encrypted_message = self.encrypt_number(message)
        #print("The encrypted message is: {}".format(encrypted_message))
        return encrypted_message


#####################################################################################################################
    def gen_KL_MN(self, bit_c):
        #print("\n-------- gen_KL_MN --------")

       
        _2__i_c = []
        for i in range(self.H):
            _2__i_c.append(2 ** i * bit_c)

        K_L = []
        for i in _2__i_c:
            i_encrypted = self.encrypt_number(i)
            K_L.append(i_encrypted)

        minus_2__i_c_times_S = []
        for i in range(self.H - 1 + 1):
            minus_2__i_c_times_S.append(- 2 ** i * bit_c * self.S)

        M_N = []
        for i in minus_2__i_c_times_S:
            i_encrypted = self.encrypt_number(i)
            M_N.append(i_encrypted)
        for i in range(self.H - 1 + 1):
            print(" (-2)**i_c * S with S = {} and i = {}: {}, (M_{}= {},N_{} = {}".format(self.S, i,minus_2__i_c_times_S[i],i,M_N[i].A, i, M_N[i].B))
        return K_L, M_N


#####################################################################################################################
    def mux(self, I_0, I_1, K_L, M_N):
        #print("\n-------- mux --------")

        
        A0 = I_0.A
        B0 = I_0.B
        A1 = I_1.A
        B1 = I_1.B

        A2 = A1 - A0
        B2 = B1 - B0
        I_2_0 = Encryption(A2, B2)
        I_2_1 = self.sub_int(I_1, I_0)
        I_2 = I_2_1
        # TODO solve problem with negative numbers
        if I_2_0 is not I_2_1:
            I_2_0.A = (I_2_0.A + self.F) % self.F
            I_2_0.B = (I_2_0.B + self.F) % self.F
            I_2_1.A = (I_2_1.A + self.F) % self.F
            I_2_1.B = (I_2_1.B + self.F) % self.F

        A2_binary_array = get_bitarray(I_2.A, 2 ** self.f)
        B2_binary_array = get_bitarray(I_2.B, 2 ** self.f)
        A2_binary_array_reversed = A2_binary_array[::-1]
        B2_binary_array_reversed = B2_binary_array[::-1]

        A2_regroup = []
        B2_regroup = []

        for i in range(self.H):
            A2_regroup.append(0)
            for j in range(self.L - 1 + 1):
                value = A2_binary_array_reversed[j * self.H + i] * 2 ** (j * self.H)
                A2_regroup[i] += value

        for i in range(self.H - 1 + 1):
            B2_regroup.append(0)
            for j in range(self.L - 1 + 1):
                value = B2_binary_array_reversed[j * self.H + i] * 2 ** (j * self.H)
                B2_regroup[i] += value

        A3 = 0
        for i in range(self.H):
            value = B2_regroup[i] * K_L[i].A
            A3 += value
            value = A2_regroup[i] * M_N[i].A
            A3 += value
        A3 = A3 % self.F

        B3 = 0
        for i in range(self.H):
            value = B2_regroup[i] * K_L[i].B
            B3 += value
            value = A2_regroup[i] * M_N[i].B
            B3 += value

        B3 = B3 % self.F

        decrypted_value = self.decrypt_number(Encryption(A3, B3))

        A_new = A3 + A0 % self.F
        B_new = B3 + B0 % self.F
        #print("A3 + A0 mod F = {} + {} mod {} = {}".format(A3, A0, self.F, A_new))
        #print("B3 + B0 mod F = {} + {} mod {} = {}".format(B3, B0, self.F, B_new))
        return Encryption(A_new, B_new)


#####################################################################################################################
    def mux_with_c(self, c, I_0, I_1):
        #print("\n-------- mux_with_c --------")


        K_L, M_N = self.gen_KL_MN(bit_c=c)
        mux_result = self.mux(I_0=I_0, I_1=I_1, K_L=K_L, M_N=M_N)

        return mux_result

 
 #####################################################################################################################   
    def decompose_number_into_binary(self, number):
        #print("\n-------- decompose_number_into_binary --------")

        L = self.L
        H = self.H

        number_in_bits = get_bitarray(number, H * L)
        reversed_number_in_bits = number_in_bits[::-1]

        A_i = []

        for i in range(L):
            block = reversed_number_in_bits[i * H:i * H + H]
            block = block[::-1]
            A_i.append(block)

        return A_i


#####################################################################################################################
    def decomposed_binary_to_decimal_blocks(self, blocks):
        #print("\n-------- decomposed_binary_to_decimal_blocks --------")


        for block in blocks:
            block = block[::-1]
        blocks = blocks[::-1]

        H = self.H
        L = self.L
        A_i_in_decimal = []

        for block_number in range(len(blocks)):
            blocks[block_number] = blocks[block_number][::-1]

        blocks = blocks[::-1]

        for block_number in range(len(blocks)):
            block_value = 0
            for j in range(len(blocks[block_number])):
                value = blocks[block_number][j] * 2 ** (j + block_number * H)
                block_value += value

            A_i_in_decimal.append(block_value)
        return A_i_in_decimal

#####################################################################################################################
    def bit_extraction_procedure(self, encrypted_message, b_p, b_m, isIsolated, new_encryption_instance):
        #print("\n-------- bit_extraction_procedure --------")


        F_in = self.F
        L_in = self.L
        H_in = self.H
        S_in = self.S
        s = get_bitarray(integer=self.s, length=L_in)
        s_revers = s[::-1]

        S_in_binary = get_bitarray(integer=S_in, length=H_in * L_in, reversed=True)
        E_in = self.E
        e_in = 0
        A_in = encrypted_message.A
        B_in = encrypted_message.B

        f_out = new_encryption_instance.f
        F_out = gen_F(f_out)
        l_out = new_encryption_instance.l
        L_out = 2 ** l_out
        h_out = new_encryption_instance.h
        H_out = 2 ** h_out
        E_out = new_encryption_instance.E
        S_out = None
        e_out = None
        A_out = None
        B_out = None

        V = (B_in - A_in * S_in) % F_in

        V_0 = V % (2 ** H_in)

        decomposed_A = self.decompose_number_into_binary(A_in)
        decomposed_B = self.decompose_number_into_binary(B_in)
        decomposed_A_decimal = self.decomposed_binary_to_decimal_blocks(decomposed_A)
        decomposed_B_decimal = self.decomposed_binary_to_decimal_blocks(decomposed_B)

        C = 0
        V_0_long_formula = decomposed_B_decimal[0] - decomposed_A_decimal[0] * s_revers[0]
        for i in range(1, L_in):
            V_0_long_formula += decomposed_A_decimal[i] * s_revers[L_in - i] + C
        V_0_long_formula = V_0_long_formula % 2 ** H_in

        W_0 = decomposed_B_decimal[0] - decomposed_A_decimal[0] * s_revers[0]
        for i in range(1, L_in):
            W_0 += decomposed_A_decimal[i] * s_revers[L_in - i]
        W_0 = W_0 % 2 ** (b_p + 1)

        v_offset = None

        # 3 
        A_dash = 0
        B_dash = 0
        for i in range(L_out):
            B_dash += 2 ** (i * H_out + b_m - 1)

        # 4
        if isIsolated:
            v_offset = 2 ** (l_out - 1)
        else:
            v_offset = 2 ** (l_out - 2)

        # 5
        v0 = (int(round(decomposed_B_decimal[0] / 2 ** (b_p - l_out))) + v_offset) % (2 * L_out)

        # 6
        v1 = (int(round((decomposed_B_decimal[0] - decomposed_A_decimal[0]) / 2 ** (b_p - l_out))) + v_offset) % (
                2 * L_out)

        # 7
        # TODO This makes no sense because A_dash = 0
        A_0 = (2 ** (v0 * H_out) * A_dash) % F_out
        B_0 = (2 ** (v0 * H_out) * B_dash) % F_out
        I_0 = Encryption(A_0, B_0)

        # 8
        # TODO This makes no sense because A_dash = 0
        A_1 = (2 ** (v1 * H_out) * A_dash) % F_out
        B_1 = (2 ** (v1 * H_out) * B_dash) % F_out
        I_1 = Encryption(A_1, B_1)

        # 9 
        # TODO What is s_0 ?
        encryption_out = self.mux_with_c(s_revers[0], I_0, I_1)
        A_out = encryption_out.A
        B_out = encryption_out.B

        # 10, 11, 12, 13 and 14 
        for i in range(1, H_in):
            v1 = int(round(decomposed_A_decimal[i] / 2 ** (b_p - l_out))) % (2 * L_out)

            A_1 = (2 ** (v1 * H_out) * A_out) % F_out
            B_1 = (2 ** (v1 * H_out) * B_out) % F_out
            I_1 = Encryption(A_1, B_1)

            encryption_out = self.mux_with_c(s_revers[L_in - i], encryption_out, I_1)
            A_out = encryption_out.A
            B_out = encryption_out.B

        result = Encryption(A_out, (B_out + 2 ** (b_m - 1) % F_out))
        #print("Bit-extraction result = {}".format(result))
        return result, new_encryption_instance

 
##################################################################################################################### 
    def multiply_with_scalar(self, encrypted_message, scalar):
        #print("\n-------- multiply_with_scalar --------")

       
        A = encrypted_message.A
        B = encrypted_message.B

        encrypted_message.A = (encrypted_message.A * scalar) % self.F
        encrypted_message.B = (encrypted_message.B * scalar) % self.F
        #print("A * scalar mod F = {} * {} mod {} = {}".format(A, scalar, self.F, encrypted_message.A))
        #print("B * scalar mod F = {} * {} mod {} = {}".format(B, scalar, self.F, encrypted_message.B))
        return encrypted_message


#####################################################################################################################
    def __init__(self, h, l, f, E):


        if not h + l == f:
            raise ValueError('h + l == f must hold')
        self.h = h
        self.l = l
        self.f = f
        self.E = E

        self.F = gen_F(self.f)
        self.H = 2 ** self.h
        self.L = 2 ** self.l
        self.s = self.gen_s()
        self.S = self.get_S()
#####################################################################################################################

