#!/usr/bin/env python3

import sys
from binascii import hexlify

from jwt.utils import base64url_decode


def jwt2john(jwt):
    jwt_bytes = jwt.encode("ascii")
    parts = jwt_bytes.split(b".")

    data = parts[0] + b"." + parts[1]
    signature = hexlify(base64url_decode(parts[2]))

    return (data + b"#" + signature).decode("ascii")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s JWT" % sys.argv[0])
        exit(1)
    john = jwt2john(sys.argv[1])
    print(john)
