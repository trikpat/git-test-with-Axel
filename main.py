import sys


def styled(text, color):
    if not sys.stdout.isatty():
        return text
    return f"\033[{color}m{text}\033[0m"


print(styled("+--------------------------------------------------+", "35"))
print(styled("|  NEON//CITY       PRIME SEQUENCE TERMINAL        |", "96"))
print(styled("+--------------------------------------------------+", "35"))
print(styled(">> Hello, world!", "92"))
print(styled(">> Scanning the grid for prime signals...", "36"))
print()

primes_found = 0
number = 2

while primes_found < 50:
    is_prime = True
    for divisor in range(2, int(number**0.5) + 1):
        if number % divisor == 0:
            is_prime = False
            break

    if is_prime:
        index = primes_found + 1
        print(styled(f"[{index:02d}] ", "35") + styled(f"{number}", "92"))
        primes_found += 1

    number += 1

print()
print(styled(">> SCAN COMPLETE // 50 PRIME SIGNALS FOUND", "96"))