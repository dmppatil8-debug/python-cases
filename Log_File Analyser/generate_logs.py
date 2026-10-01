import random
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "server.log"

ips = [
    f"192.168.1.{i}"
    for i in range(1, 51)
]

endpoints = [
    "/api/users",
    "/api/orders",
    "/api/products",
    "/api/login",
    "/api/payments",
    "/api/profile",
    "/api/search",
    "/api/cart"
]

methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

status_codes = [
    200,
    201,
    400,
    404,
    500
]


def generate_logs(filename, total_lines):
    start_time = datetime(2026, 9, 20, 0, 0, 0)

    with open(filename, "w", encoding="utf-8") as file:
        for _ in range(total_lines):

            if random.random() < 0.01:
                broken_lines = [
                    "this is a broken log line",
                    "2026-09-20 14:32:07 | 192.168.1.14 | GET /api/users",
                    "2026-09-20 14:32:07 | not-an-ip | GET /api/users | abc | xyzms",
                    "missing | fields | here",
                    "2026-09-20 14:32:07 | 192.168.1.14 | GET /api/users | 200"
                ]

                file.write(random.choice(broken_lines) + "\n")
                continue

            current_time = start_time + timedelta(
                seconds=random.randint(0, 86399)
            )

            ip = random.choice(ips)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice(status_codes)
            response_time = random.randint(50, 3000)

            line = (
                f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{ip} | "
                f"{method} {endpoint} | "
                f"{status} | "
                f"{response_time}ms\n"
            )

            file.write(line)


if __name__ == "__main__":
    generate_logs(LOG_FILE, 200000)
    print("server.log generated successfully!")