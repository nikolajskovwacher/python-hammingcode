### Custom functions
def decimal_to_binary(n):
    return bin(n).replace("0b", "")
    
def binary_to_decimal(bin):
    return sum(x*(2**pos) for pos, x in enumerate(reversed(bin)))

###########
# Encoder #
###########

def encoder(data_bits: list) -> list:
    """takes 4-bit input and encodes it into 7-bit

      Returns
   -------
   list
       A list with 7 binary values containing the encoded message.

       Example
   --------
   >>> encoder([1,0,0,0])
          
   [1,1,1,0,0,0,0]"""
    # Error handling
    if type(data_bits) is not list:
        raise TypeError("Input is not a list.")
    if not all(x in [0,1] for x in data_bits): # Check if only 0 or 1 in list
        raise ValueError("Input is not binary.") # Error handling (in case of wrong input)
    if not len(data_bits) == 4: # Checks that input list contains 4 integers (bits)
        raise ValueError("Input does not contain 4-bits.")

    parity_bits = [0]*3
    pos_pb = [pow(2,x) for x in range(3)]
    pos_db = [x for x in range(1,8) if x not in pos_pb]

    # Establish parity bits, save them in list 'parity_bits'
    for index, bit in enumerate(data_bits):
        if bit == 1: # Parity bits only change if bit equals 1
            for x, i in enumerate(reversed(decimal_to_binary(pos_db[index]))):
                if int(i) == 1: 
                    parity_bits[x] = not parity_bits[x]
    
    # Build encoded array with data bits and parity bits
    output = []
    for i in range(7):
        if i+1 in pos_pb: # Insert parity bit
            output.append(int(parity_bits[0]))
            parity_bits.pop(0)
        else: # Insert next databit
            output.append(data_bits[0])
            data_bits.pop(0)
    return output

###########
# Decoder #
###########

def decoder(input: list) -> list:
    """takes 7-bit input and decodes it into 4-bits
  
      Returns
   -------
   list
       A list with 4 binary values containing the decoded message.

       Example
   --------
   >>> decoder([0,0,1,0,1,1,0])
          
   [1,1,1,0]"""
    # Error handling
    if type(input) is not list:
        raise TypeError("Input is not a list.")
    if not all(x in [0,1] for x in input): # Check if only 0 or 1 in list
        raise ValueError("Input is not binary.") # Error handling (in case of wrong input)
    if not len(input) == 7: # Checks that input list contains 7 integers (bits)
        raise ValueError("Input list does not contain 7 digits.")

    input.reverse() # For practicality reason when checking for errors
    parity = [0]*3 # Empty list for checking parity bits
    # Check if output is correct
    for x, i in enumerate(input):
        if i == 1:
            pos_bin_str = decimal_to_binary(7-x) # Convert integer to binary (string to list)
            pos_bin_str_rev = pos_bin_str[::-1] # Reverse binary string
            for po, l in enumerate(pos_bin_str_rev): # Switch parity (backwards in case binary value has less than 3 digits)
                if l == "1": # Only switch when odd/even changes
                    parity[2-po] = not parity[2-po] # Swap parity
    
    if any(parity): # Because parity bits are not all zeros there is a mistake 
        position = 7-binary_to_decimal(parity) # Position to make bitflip
        input[position] = int(not input[position]) # Make bitflip at position

    input.reverse() # List is reversed again
    output = [] # Empty list to be filled
    for pos in [2,4,5,6]: # Loop through validated input list, take out the databits and append to output list
        output.append(input[pos]) # Fill output with databits

    return output

###########
# Testing #
###########

### Simple testing
Input = [1,1,1,0]
Input == decoder(encoder(list(Input)))

Input = [1,0,1,0]
output_enc = encoder(list(Input)) # Encode
output_enc[0] = not output_enc[0] # Bitflip
output_dec = decoder(output_enc) # Decode
output_dec == Input

### Unit tests
import unittest

class TestNotebook(unittest.TestCase):
    # Encoder
    def test_encoder(self):
        self.assertEqual(encoder([1,0,0,0]), [1,1,1,0,0,0,0])
        self.assertEqual(encoder([0,1,0,0]), [1,0,0,1,1,0,0])
        self.assertEqual(encoder([0,0,1,0]), [0,1,0,1,0,1,0])
        self.assertEqual(encoder([0,0,0,1]), [1,1,0,1,0,0,1])
        self.assertEqual(encoder([0,1,0,1]), [0,1,0,0,1,0,1])
        self.assertEqual(encoder([1,1,1,0]), [0,0,1,0,1,1,0])
    
    # Decoder
    def test_decoder(self):
        self.assertEqual(decoder([0,0,1,0,1,1,0]), [1,1,1,0])
        self.assertEqual(decoder([1,0,1,0,1,1,0]), [1,1,1,0]) # With bitflip
        self.assertEqual(decoder([0,0,0,0,1,1,0]), [1,1,1,0]) # With bitflip

    # Error handling (Encoder)    
    def test_error_handling_encoder(self):
        with self.assertRaises(ValueError)as error: encoder([1,2,3,4])
        self.assertEqual(str(error.exception), "Input is not binary.")

        with self.assertRaises(TypeError)as error: encoder("string")
        self.assertEqual(str(error.exception), "Input is not a list.")
        
        with self.assertRaises(ValueError)as error: encoder([0,1,1])
        self.assertEqual(str(error.exception),"Input does not contain 4-bits.")

    # Error handling (Decoder)    
    def test_error_handling_decoder(self):
        with self.assertRaises(ValueError)as error: decoder([1,2,3,4,5,6,7])
        self.assertEqual(str(error.exception), "Input is not binary.")

        with self.assertRaises(TypeError)as error: decoder("string")
        self.assertEqual(str(error.exception), "Input is not a list.")
        
        with self.assertRaises(ValueError)as error: decoder([0,0,0,1])
        self.assertEqual(str(error.exception),"Input list does not contain 7 digits.")

unittest.main(argv=[''], verbosity=2, exit=False)