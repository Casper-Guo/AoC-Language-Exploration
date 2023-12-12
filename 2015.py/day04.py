import hashlib


def get_hex(key: str, salt: int) -> str:
    hash = hashlib.md5((key + str(salt)).encode())
    return hash.hexdigest()


with open("input04.txt", "r") as f:
    # part 1
    key = f.read()
    salt = 1

    while True:
        hex = get_hex(key, salt)
        # if hex.startswith("00000"):
        #     print(salt)
        #     break

        # part 2
        if hex.startswith("000000"):
            print(salt)
            break
        salt += 1
