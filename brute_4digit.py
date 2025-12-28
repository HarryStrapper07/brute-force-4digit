import os
import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: python3 brute.py <target_binary>")
    sys.exit(1)

target = sys.argv[1]

# 1️. Check: file exist?
if not os.path.isfile(target):
    print("[-] File does not exist")
    sys.exit(1)

# 2️. Check: executable?
if not os.access(target, os.X_OK):
    print("[-] File is not executable (+x missing)")
    sys.exit(1)

print(f"[+] Target locked: {target}")
print("[+] Starting 4-digit PIN brute force...\n")

for i in range(10000):
    pin = f"{i:04d}"

    try:
        process = subprocess.Popen(
            ["./" + target],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, _ = process.communicate(pin + "\n", timeout=1)

        if "Correct" in output or "Success" in output:
            print(f"\n[✔] PIN FOUND: {pin}")
            print("[✔] Output:\n", output)
            # ✅ Bold credit line
            print("\n\033[1m[+] Tool created by Harry_Strapper\033[0m")
            break

        print(f"Trying PIN: {pin}", end="\r")

    except subprocess.TimeoutExpired:
        process.kill()

else:
    print("\n[-] PIN not found")

