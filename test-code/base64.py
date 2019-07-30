import base64

string_to_encode = "super secret password"
int_to_encode = 13

encode = base64.b64encode(string_to_encode.encode())

decode = base64.b64decode(encode)

print("encode: ", encode)
print("decode: ", decode)

base64_decode_bytes = base64.b64encode(str(int_to_encode).encode()).decode()

print(base64.b64encode(str(int_to_encode).encode()))

print(base64_decode_bytes)

