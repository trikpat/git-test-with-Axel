import random
import shutil
import sys
import time


def styled(text, color):
    if not sys.stdout.isatty():
        return text
    return f"\033[{color}m{text}\033[0m"


def generate_primes(count):
    number = 2
    primes_found = 0

    while primes_found < count:
        is_prime = True
        for divisor in range(2, int(number**0.5) + 1):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            yield number
            primes_found += 1

        number += 1


def render_screen(primes, candidate, frame, width, height, complete=False):
    rng = random.Random(frame * 7919)
    noise = "      .:;+*/\\|"
    screen = [
        [rng.choice(noise) for _ in range(width)]
        for _ in range(height)
    ]
    colors = ["96" if row % 2 == 0 else "35" for row in range(height)]

    def put(row, column, text, color):
        if not 0 <= row < height or column >= width - 1:
            return
        text = text[:max(0, width - column - 1)]
        screen[row][column:column + len(text)] = text
        colors[row] = color

    def centered(row, text, color):
        if row < height:
            column = max(1, (width - len(text)) // 2)
            put(row, column, text, color)

    if height > 0:
        screen[0] = ["+"] + ["="] * max(0, width - 2) + (["+"] if width > 1 else [])
        colors[0] = "95"
    if height > 1:
        screen[-1] = ["+"] + ["="] * max(0, width - 2) + (["+"] if width > 1 else [])
        colors[-1] = "95"
    for row in range(1, height - 1):
        screen[row][0] = "|"
        screen[row][-1] = "|"

    if height > 9:
        scan_row = 6 + frame % (height - 8)
        screen[scan_row] = ["-"] * width
        colors[scan_row] = "36"

    centered(1, ".   *   NEON CITY PRIME REACTOR   *   .", "93")
    centered(3, "P R I M E   S E Q U E N C E", "96")
    if complete:
        centered(4, "ALL SIGNALS LOCKED // TRANSMISSION COMPLETE", "92")
    else:
        centered(4, f"GENERATING SIGNAL {len(primes):02d}/50 // CANDIDATE {candidate}", "95")

    bar_width = min(36, max(8, width - 12))
    filled = bar_width if complete else bar_width * len(primes) // 50
    bar = "[" + "#" * filled + "." * (bar_width - filled) + "]"
    centered(5, bar, "92")

    columns = max(1, min(10, (width - 2) // 7))
    grid_rows = (50 + columns - 1) // columns
    grid_start = max(7, (height - grid_rows) // 2)
    cell_width = max(7, (width - 2) // columns)

    for index, prime in enumerate(primes):
        row = grid_start + index // columns
        column = 2 + (index % columns) * cell_width
        put(row, column, f"{index + 1:02d}:{prime:>3}", "92")

    footer = (
        "50 SIGNALS GENERATED // END OF TRANSMISSION"
        if complete
        else "50 PRIME SIGNALS // LIVE DATA STREAM"
    )
    centered(height - 3, footer, "96")
    centered(height - 2, " . : + * / NEON//CITY / * + : . ", "95")
    return "\n".join(styled("".join(line), color) for line, color in zip(screen, colors))


opening_credits = [
    ("+------------------------------------------------------------------+", "95"),
    ("|                                                                  |", "96"),
    ("|                 N E O N   C I T Y   P I C T U R E S              |", "93"),
    ("|                       P R E S E N T S                            |", "96"),
    ("|                                                                  |", "96"),
    (r"|        .        *             .             *         .          |", "95"),
    (r"|                 /\                              /\               |", "96"),
    (r"|        /\      /  \       /\         /\        /  \      /\     |", "96"),
    (r"|       /  \    / /\ \     /  \       /  \      / /\ \    /  \    |", "36"),
    (r"|    __/ /\ \__/ /  \ \___/ /\ \_____/ /\ \____/ /  \ \__/ /\ \__ |", "36"),
    (r"|   |__|    |____|  |____|    |_____|    |____|    |____|    |__| |", "36"),
    (r"|     ||       ||      ||       ||         ||      ||       ||    |", "95"),
    ("+------------------------------------------------------------------+", "95"),
    ("|                                                                  |", "96"),
    ("|  ____  ____  ___ __  __ _____       ____ ___ ____ _   _    _     |", "95"),
    (r"| |  _ \|  _ \|_ _|  \/  | ____|     / ___|_ _/ ___| \ | |  / \    |", "95"),
    (r"| | |_) | |_) || || |\/| |  _|       \___ \| | |  _|  \| | / _ \   |", "96"),
    (r"| |  __/|  _ < | || |  | | |___       ___) | | |_| | |\  |/ ___ \  |", "96"),
    (r"| |_|   |_| \_\___|_|  |_|_____|     |____/___\____|_| \_/_/   \_\ |", "95"),
    ("|                                                                  |", "96"),
    ("|                   O N E   C I T Y.                               |", "93"),
    ("|              F I F T Y   P R I M E   S I G N A L S.              |", "93"),
    ("|                                                                  |", "96"),
    ("+==================================================================+", "95"),
    ("|  Hello, world!                                                   |", "92"),
    ("|  Scanning the grid for prime signals...                          |", "96"),
    ("+==================================================================+", "95"),
]

interactive = sys.stdout.isatty()
if interactive:
    width, height = shutil.get_terminal_size(fallback=(80, 24))
    width = max(20, width - 1)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
else:
    for line, color in opening_credits:
        print(styled(line, color))
    print()

try:
    primes = []
    for prime in generate_primes(50):
        primes.append(prime)
        if interactive:
            if len(primes) == 1:
                sys.stdout.write("\033[2J")
            sys.stdout.write(
                "\033[H"
                + render_screen(
                    primes,
                    prime,
                    len(primes),
                    width,
                    height,
                    complete=len(primes) == 50,
                )
            )
            sys.stdout.flush()
            if len(primes) < 50:
                time.sleep(0.04)
        else:
            print(styled(f"[{len(primes):02d}] ", "35") + styled(f"{prime}", "92"))

    if not interactive:
        print()
        print(styled("+==================================================================+", "95"))
        print(styled("|  SCAN COMPLETE // 50 PRIME SIGNALS FOUND                         |", "92"))
        print(styled("|                                                                  |", "96"))
        print(styled("|      .       *       .       END OF TRANSMISSION       *       . |", "95"))
        print(styled("+==================================================================+", "95"))
finally:
    if interactive:
        sys.stdout.write("\033[0m\033[?25h\n")
        sys.stdout.flush()
