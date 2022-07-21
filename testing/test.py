ALPHABET = [chr(i) for i in range(65, 91)]
print(ALPHABET)

alphabet = [chr(i) for i in range(97, 123)]
print(alphabet)

print(ord('A'))  # Return Unicode id for string (single character)
print(ord('a'))  # Return Unicode id for string (single character)

string = 'Unicode3в'
array = list(string)
print(array)

def foo(s):
    for i in list(s):
        if not ord(i) in range(32, 128):
            print('Error')

foo(string)