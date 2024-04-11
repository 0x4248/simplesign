# Simple sign
# Easily sign or hash text messages using your private key and sha265 or any hashing algorithm.
# Github:https://www.github.com/0x4248/simplesign
# By: 0x4248

import argparse
import base64
import hashlib
import os
import sys
import yaml


def setup():
    private_key = input("Private key path: ")
    hash = input("Hashing algorithm (sha256, sha512, sha384, sha224, sha1, md5): ")
    name = input("Your name: ")    
    email = input("Your email:")
    config = {
        "private_key": private_key,
        "hash": hash,
        "name": name,
        "email": email
    }
    with open(os.path.expanduser("~/.simplesign.yaml"), "w") as f:
        yaml.dump(config, f)
    print("Config file created at ~/.simplesign.yaml")

def sign_file(filename, private_key, hash):
    with open(filename, "rb") as f:
        data = f.read()
    if hash == "sha256":
        hash = hashlib.sha256(data).digest()
    elif hash == "sha512":
        hash = hashlib.sha512(data).digest()
    elif hash == "sha384":
        hash = hashlib.sha384(data).digest()
    elif hash == "sha224":
        hash = hashlib.sha224(data).digest()
    elif hash == "sha1":
        hash = hashlib.sha1(data).digest()
    elif hash == "md5":
        hash = hashlib.md5(data).digest()
    else:
        print("Error: Invalid hash")
        sys.exit(1)

    with open(private_key, "rb") as f:
        key = b""
        for line in f:
            if not line.startswith(b"-----"):
                key += line

    signature = base64.b64encode(hashlib.new("sha256", hash + key).digest())
    return signature

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File to sign")
    parser.add_argument("-k", "--key", help="Private key")
    parser.add_argument("-a", "--algorithm", help="Hashing algorithm")
    args = parser.parse_args()

    if os.path.exists(os.path.expanduser("~/.simplesign.yaml")):
        with open(os.path.expanduser("~/.simplesign.yaml"), "r") as f:
            config = yaml.safe_load(f)
    else:
        ask = input("Do you want to run the setup>")
        if ask.lower() == "y" or ask.lower() == "yes":
            setup()
            sys.exit(0)
        else:
            print("Error: Config file does not exist")
            sys.exit(1)
    
    if args.file is None:
        os.system("nano /tmp/simplesign")
        args.file = "/tmp/simplesign"

    if args.file == "/tmp/simplesign":
        output = "simplesign.signed.txt"
    else:
        output = args.file + ".signed.txt"
    
    if args.key is None:
        args.key = config["private_key"]
    
    if args.algorithm is None:
        args.algorithm = config["hash"]
    
    signature = sign_file(args.file, args.key, args.algorithm)

    with open(output, "w") as f:
        msg = "---------- BEGIN " + args.algorithm.upper() + " SIGNED MESSAGE ----------\n"
        f.write(msg)
        with open(args.file, "r") as f2:
            f.write(f2.read())
        msg = "------------ BEGIN " + args.algorithm.upper() + " SIGNITURE -------------\n"
        f.write(msg)
        f.write(signature.decode("utf-8"))
        msg = "\n--------------- END SIGNATURE ---------------\n"
        f.write(msg)
        msg = "Signed-off-by: " + config["name"] + " <" + config["email"] + ">\n"
        f.write(msg)

    if args.file == "/tmp/simplesign":
        os.remove(args.file)