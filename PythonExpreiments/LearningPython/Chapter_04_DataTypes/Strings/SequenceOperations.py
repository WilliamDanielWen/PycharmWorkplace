# String is actually an array
test_str="abcdefgABCDEFG"
print  test_str[3]

#index back
print test_str[-1] #last index

#concatation : using +
print  "abc"+"DEF"


# str.join(iterable)
# Return a string which is the concatenation of the strings in the iterable iterable.
# A TypeError will be raised if there are any non-string values in iterable, including bytes objects.
# The separator between elements is the string providing this method.

iterable=[' first ',' second ',' third ']
print  "123".join(iterable)
print  ''.join(iterable)



#repetition
print  "abc "*8