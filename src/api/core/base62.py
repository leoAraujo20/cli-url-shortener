def encode_base62(num):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    encoded = ""
    
    if num == 0:
        return characters[0]
    
    while num > 0:
        remainder = num % base
        encoded = characters[remainder] + encoded
        num //= base
    
    return encoded


def decode_base62(encoded):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    num = 0
    
    for char in encoded:
        num = num * base + characters.index(char)
    
    return num