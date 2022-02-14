from fhe import *

"""
This class offers method to test the encryption functionality
"""


class TestEncryption:
    def __init__(self, instance):
        self.instance = instance

    def encrypt_numbers_test(self, logging):
        print("##### - Encryption without noise:")
        print("")

        # Create two encrypted instances of zero
        print("Encrypt and decrypt two instances of zero:")
        encrypted_zero1 = self.instance.encryption_of_zero()
        print("Encryption of zero1: {}".format(encrypted_zero1))
        encrypted_zero2 = self.instance.encryption_of_zero()
        print("Encryption of zero2: {}".format(encrypted_zero2))
        # Decrypt the instances of zero
        decrypted_zero1 = self.instance.decrypt_number(encrypted_zero1)
        print("Decryption of encrypted zero1: {}".format(decrypted_zero1))
        decrypted_zero2 = self.instance.decrypt_number(encrypted_zero2)
        print("Decryption of encrypted zero2: {}".format(decrypted_zero2))
        # Print blank line
        print("")

        # Instantiate two numbers
        x1 = 4536
        x2 = 8934
        print("Encrypt and decrypt two numbers x1: {} and x2: {}".format(x1, x2))
        # Encrypt both numbers
        x1_encrypted = self.instance.encrypt_number(x1)
        print("Encryption of {}: {}".format(x1, x1_encrypted))
        x2_encrypted = self.instance.encrypt_number(x2)
        print("Encryption of {}: {}".format(x2, x2_encrypted))
        # Decrypt both numbers
        x1_decrypted = self.instance.decrypt_number(x1_encrypted)
        print("Decryption of {}: {}".format(x1_encrypted, x1_decrypted))
        x2_decrypted = self.instance.decrypt_number(x2_encrypted)
        print("Decryption of {}: {}".format(x2_encrypted, x2_decrypted))
        print("")

        noise = 5
        print("##### - Encryption with noise: Test noise = {}".format(noise))
        print("")
        # Create two encrypted instances of zero with noise 5
        print("Encrypt and decrypt two instances of zero with noise {}:".format(noise))
        encrypted_zero1_noise = self.instance.encryption_of_zero(E=noise)
        print("Encryption of zero1 with noise {}: {}".format(noise, encrypted_zero1_noise))
        encrypted_zero2_noise = self.instance.encryption_of_zero(E=noise)
        print("Encryption of zero2 with noise {}: {}".format(noise, encrypted_zero2_noise))
        # Decrypt the instances of zero
        decrypted_zero1_noise = self.instance.decrypt_number(encrypted_zero1_noise)
        print("Decryption of encrypted zero1 with noise {}: {}".format(noise, decrypted_zero1_noise))
        decrypted_zero2_noise = self.instance.decrypt_number(encrypted_zero2_noise)
        print("Decryption of encrypted zero2 with noise {}: {}".format(noise, decrypted_zero2_noise))
        # Print blank line
        print("")

        # Instantiate two numbers
        x1 = 4536
        x2 = 8934
        print("Encrypt and decrypt two numbers x1: {} and x2: {} with noise".format(x1, x2))
        # Encrypt both numbers
        x1_encrypted = self.instance.encrypt_number(x1, E=noise)
        print("Encryption of {} with noise {}: {}".format(x1, noise, x1_encrypted))
        x2_encrypted = self.instance.encrypt_number(x2, E=noise)
        print("Encryption of {} with noise {}: {}".format(x2, noise, x2_encrypted))
        # Decrypt both numbers
        x1_decrypted = self.instance.decrypt_number(x1_encrypted)
        print("Decryption of {} with noise {}: {}".format(x1_encrypted, noise, x1_decrypted))
        x2_decrypted = self.instance.decrypt_number(x2_encrypted)
        print("Decryption of {} with noise {}: {}".format(x2_encrypted, noise, x2_decrypted))

    def add_subtract_numbers_test(self, logging, print_binary=None):
        # TODO Deal with modulus from the right direction
        # TODO With noise
        # Initialize the numbers
        x1 = 289
        x2 = 3174
        if logging > 0:
            print("Integers x1: {} and x2: {} get encrypted, added and decrypted".format(x1, x2))
        if print_binary is not None:
            print("Binary: x1: {}, x2: {} get encrypted, added and decrypted".format(bin(x1), bin(x2)))
        # Encrypt the numbers
        x1_encrypted = self.instance.encrypt_number(x1)
        x2_encrypted = self.instance.encrypt_number(x2)
        if logging > 0:
            print("")
            print("x1 ({}) encrypted: {}".format(x1, x1_encrypted))
        if print_binary is not None:
            print("Binary: x1 ({}) encrypted: {}".format(bin(x1), x1_encrypted.get_binary_string()))
        if logging > 0:
            print("x2 ({}) encrypted: {}".format(x2, x2_encrypted))
        if print_binary is not None:
            print("Binary: x2 ({}) encrypted: {}".format(bin(x2), x2_encrypted.get_binary_string()))
        # Add the encrypted numbers
        sum_encrypted = self.instance.add_int(x1_encrypted, x2_encrypted)
        if logging > 0:
            print("")
            print("Encrypted sum: {}".format(sum_encrypted))
        if print_binary is not None:
            print("Binary: Encrypted sum: {}".format(sum_encrypted.get_binary_string()))
        # Decrypt the encrypted_sum
        sum_decrypted = self.instance.decrypt_number(sum_encrypted)
        if logging > 0:
            print("")
            print("Decrypted sum: {}".format(sum_decrypted))
        if print_binary is not None:
            print("Binary: Decrypted sum: {}".format(bin(sum_decrypted)))

    def bit_vectors_test(self, logging):
        # Initialize the bit vector
        bitvector = [1, 0, 0, 1, 1, 0, 1, 1]
        print("Bit vector: {}".format(bitvector))
        # Encrypt
        bitvector_encrypted = self.instance.encrypt_bit_vector(bitvector)
        print("Encrypted bit vector: {}".format(bitvector_encrypted))
        # Decrypt
        # TODO Implement Decryption

    def encrypt_decrypt_bit_test(self, logging):
        # Initialize two bits
        bit0 = 0
        bit1 = 1
        print("0 and 1 get seperatly encrypted:")
        # Encrypt the bits
        encrypted0 = self.instance.encrypt_bit(bit0)
        print("0 encrypted: {}".format(encrypted0))
        encrypted1 = self.instance.encrypt_bit(bit1)
        print("1 encrypted: {}".format(encrypted1))
        # Decrypt the bits
        decrypted0 = self.instance.decrypt_bit(encrypted0)
        print("0 ({}) decrypted: {} ".format(encrypted0, decrypted0))
        decrypted1 = self.instance.decrypt_bit(encrypted1)
        print("1 ({}) decrypted: {} ".format(encrypted1, decrypted1))

    def noise_test(self, logging, gaussian=None):
        error = self.instance.gen_E(gaussian=gaussian)
        a = 1807
        b = 7845
        c = a + b
        a_encrypted = self.instance.encrypt_number(a, E=error)
        error = self.instance.gen_E()
        b_encrypted = self.instance.encrypt_number(b, E=error)
        c_encrypted = self.instance.add_int(a_encrypted, b_encrypted)

        c_decrypted = self.instance.decrypt_number(c_encrypted)

        if logging > 0:
            print("a: Number {} gets encrypted as {} with error {}".format(a,a_encrypted,error))
            print("b: Number {} gets encrypted as {} with error {}".format(b,b_encrypted,error))
            print("a + b = c = {} + {} = {}".format(a,b,c))
            print("")
            print("Add encrypted a ({}) and encrypted b ({}) = encrypted c ({})".format(a_encrypted,b_encrypted,c_encrypted))
            print("c_calculated: {}; c_decrypted: {}".format(c, c_decrypted))
            print("c_calculated == c_decrypted ? {}".format(c == c_decrypted))

    def mux_test(self, logging):
        I_0 = 5182
        if logging > 0:
            print("Integer 0: {}".format(I_0))

        I_1 = 7845
        if logging > 0:
            print("Integer 1: {}".format(I_1))

        bit = 1
        if logging > 0:
            print("Bit c: {}".format(bit))

        I_0_encrypted = self.instance.encrypt_number(I_0)
        if logging > 0:
            print("Integer 0 encrypted: {}".format(I_0_encrypted))

        I_1_encrypted = self.instance.encrypt_number(I_1)
        if logging > 0:
            print("Integer 1 encrypted: {}".format(I_1_encrypted))
            print("")

        K_L, M_N = self.instance.gen_KL_MN(bit_c=bit)
        if logging > 0:
            # I don't know why this did not print the values appropriatly
            # print("K and L: {}; M and N: {}".format(str(K_L), str(M_N)))
            for i in range(len(K_L)):
                print("K_{}: {}; L_{}: {}".format(i, K_L[i].A, i, K_L[i].B))
            for i in range(len(K_L)):
                print("M_{}: {}; N_{}: {}".format(i, M_N[i].A, i, M_N[i].B))
            print("")
        mux_result = self.instance.mux(I_0=I_0_encrypted, I_1=I_1_encrypted, K_L=K_L, M_N=M_N)
        if logging > 0:
            print("Mux result -> (A_3 + A_0, B_3 + B_0) = ({},{})".format(mux_result.A, mux_result.B))
        result = self.instance.decrypt_number(mux_result)
        if logging > 0:
            print("Decrypted result: {}".format(result))
            if result == I_0:
                print("Result is equal to Integer 0 -> Bit c is 0")
            elif result == I_1:
                print("Result is equal to Integer 1 -> Bit c is 1")
            else:
                print("Some error occured")

    def bit_extraction_algorithm(self, logging):
        x1 = 15800
        if logging > 0:
            print("Number {} gets encrypted:".format(x1))
        x1_encrypted = self.instance.encrypt_number(x1)
        b_p = 3
        b_m = 3
        isIsolated = False
        if logging > 0:
            print("Encryption of number {}: {}".format(x1, x1_encrypted))
            print("Parameters: b_p: {}; b_m: {}, isIsolated: {}".format(b_p, b_m, isIsolated))
            print("")
        # Parameters for new Encryption Instance:
        f_out = 5
        h_out = 2
        l_out = 3
        E_out = 5
        #
        new_encryption_instance = FHE_Fermat(h_out, l_out, f_out, E_out)
        if logging > 0:
            print("New Encryption instance initialized")
            print("Number gets reencrypted with new Encryption instance:")
            print("")
        reencryption, new_encryption_instance = self.instance.bit_extraction_procedure(encrypted_message=x1_encrypted,
                                                                                       b_m=b_m, b_p=b_p,
                                                                                       isIsolated=isIsolated,
                                                                                       new_encryption_instance=new_encryption_instance)
        if logging > 0:
            print("Reencryption: {}".format(reencryption))

        decrypted_value = new_encryption_instance.decrypt_number(reencryption)

        if logging > 0:
            print("Value decrypted with new encryption instance: {}".format(decrypted_value))

    def multiplying_with_scalar_test(self, logging):
        number = 158
        scalar = 12
        if logging > 0:
            print("Number {} will get multiplied with the scalar {}".format(number, scalar))
        encrypted_number = self.instance.encrypt_number(number=number)
        if logging > 0:
            print("Encrypted number: {}".format(encrypted_number))
        encrypted_multiplied_number = self.instance.multiply_with_scalar(encrypted_message=encrypted_number,
                                                                         scalar=scalar)
        if logging > 0:
            print("Encrypted number after multiplication with {} (mod {}): {}".format(scalar, self.instance.F,
                                                                                      encrypted_multiplied_number))
        decrypted_multiplied_number = self.instance.decrypt_number(encryption=encrypted_multiplied_number,
                                                                   )
        if logging > 0:
            print("Decrypted multiplied number: {}".format(decrypted_multiplied_number))
            print("{} == {} ? -> {}".format("{} * {}".format(number, scalar), decrypted_multiplied_number,
                                            number * scalar == decrypted_multiplied_number))
