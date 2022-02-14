from TestEncryption import TestEncryption
from fhe import FHE_Fermat

"""
File of the main application, always run this file first
The parameter <logging> represents the depth of logging and gets decreased recursively with every function call.
For no logging, choose 
All the if-checks for the logging values and the prints can be removed to increase the performance
"""
############
# Parameters#
h = 3
l = 3
f = h + l
E = 5
############
# TODO: The following points still need to be solved. Unfortunately, I had not enough time for them
# TODO: Print in colours (f.e. 1 in long bitstrings) and make the output better readable
# TODO: Multiplication of two decrypted numbers
# TODO: Error/Noise, Decrypting of every block on it's own/ Create appropriate error and add it to the message
# TODO: Bit extraction algorithm: How to generate S_out?

# Initialize a encryption instance and a test instance. The test instance offers methods to test the encryption functionality
instance = FHE_Fermat(h, l, f, E)
test = TestEncryption(instance)


print("\n\n!!!   encrypt_numbers_test\n\n")
# Test the encryption of numbers
test.encrypt_numbers_test(logging=2)

print("\n\n!!!   add_subtract_numbers_test\n\n")
# Test the Addition and Subtraction of encrypted numbers - Works, but to many new lines and I dont know why
test.add_subtract_numbers_test(logging=2)
# With binary representations
print("\n\n!!!   add_subtract_numbers_test___print_binary\n\n")
test.add_subtract_numbers_test(print_binary=True, logging=2)

print("\n\n!!!   bit_vectors_test\n\n")
# Tests the encryption of a bit vector
test.bit_vectors_test(logging=2)


print("\n\n!!!   encrypt_decrypt_bit_test\n\n")
# Tests the encryption/decryption of a bit
test.encrypt_decrypt_bit_test(logging=2)


print("\n\n!!!   noise_test_____normal\n\n")
# Noise/Error Distribution test, does not work.
# gaussian=False: Use Uniform distribution for the error, gaussian=True: Use normal/gaussian distribution for the error
test.noise_test(00, gaussian=False)
print("\n\n!!!   noise_test_____gaussian\n\n")
test.noise_test(00, gaussian=True)


print("\n\n!!!   mux_test\n\n")
# Test the encryted Mux algorithm, which is necessary for the extraction of a bit into a fresh encryption
test.mux_test(logging=2)


print("\n\n!!!   multiplying_with_scalar_test\n\n")
# Test the multiplication of the encrypted number with a scalar
test.multiplying_with_scalar_test(logging=2)








print("\n\n!!!   bit_extraction_algorithm\n\n")
"""
The algorithm does not work appropriately - I did not figure out how the conversion into a fresh encryption works.
The problem is that the paper does not explain properly, how the new encryptiong key S_0 is generated.
Additionally, some of the computations make not much sense (multiplying a complex term with 0 every time).
I will explain the problems which occured in the final presentation.
"""
# Test the Bit-extraction-algorithm
test.bit_extraction_algorithm(logging=2)


#Use this to measure the time how long it takes to run code
import time
def measure_time():
    timestamp_1 = time.time()
    #Run code here - start
    h2 = 5
    l2 = 5
    f2 = 10
    E2 = 5
    instance2 = FHE_Fermat(h2, l2, f2, E2)
    test2 = TestEncryption(instance2)
    test2.add_subtract_numbers_test()
    #Run code here - end
    timestamp_2 = time.time()
    difference = timestamp_2 - timestamp_1
    print("Time to calculate the function: {} s".format(difference))

#measure_time()