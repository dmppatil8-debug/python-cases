import re
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "server.log"

LOG_PATTERN = re.compile(
    r"^"
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r"\s*\|\s*"
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
    r"\s*\|\s*"
    r"(?P<method>GET|POST|PUT|DELETE)"
    r"\s+"
    r"(?P<endpoint>/\S+)"
    r"\s*\|\s*"
    r"(?P<status>\d+)"
    r"\s*\|\s*"
    r"(?P<response_time>\d+)ms"
    r"$"
)


def read_lines(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


def parse_line(line):
    match = LOG_PATTERN.match(line)

    if not match:
        return None

    data = match.groupdict()

    return {
        "timestamp": data["timestamp"],
        "ip": data["ip"],
        "method": data["method"],
        "endpoint": data["endpoint"],
        "status": int(data["status"]),
        "response_time": int(data["response_time"])
    }


def parsed_lines(path):
    for line in read_lines(path):
        yield parse_line(line)


def valid_lines(path):
    for record in parsed_lines(path):
        if record is not None:
            yield record


def analyze_logs(path):
    total_requests = 0
    broken_lines = 0
    error_requests = 0

    ip_counter = Counter()
    hourly_counter = Counter()

    endpoint_times = defaultdict(list)

    for record in parsed_lines(path):

        if record is None:
            broken_lines += 1
            continue

        total_requests += 1

        if record["status"] >= 400:
            error_requests += 1

        ip_counter[record["ip"]] += 1

        hour = record["timestamp"][:13]
        hourly_counter[hour] += 1

        endpoint_times[record["endpoint"]].append(
            record["response_time"]
        )

    error_rate = 0

    if total_requests > 0:
        error_rate = (error_requests / total_requests) * 100

    endpoint_averages = {}

    for endpoint, times in endpoint_times.items():
        endpoint_averages[endpoint] = sum(times) / len(times)

    slowest_endpoints = sorted(
        endpoint_averages.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    print("\n" + "=" * 50)
    print("SERVER LOG ANALYSIS")
    print("=" * 50)

    print(f"\nTotal requests : {total_requests:,}")
    print(f"Broken lines   : {broken_lines:,}")
    print(f"Error requests : {error_requests:,}")
    print(f"Error rate     : {error_rate:.2f}%")

    print("\nTop 5 IPs")
    print("-" * 30)

    for ip, count in ip_counter.most_common(5):
        print(f"{ip:<18} {count:,} requests")

    print("\n5 Slowest Endpoints")
    print("-" * 45)

    for endpoint, average in slowest_endpoints:
        print(f"{endpoint:<25} {average:.2f} ms average")

    print("\nRequests Per Hour")
    print("-" * 45)

    for hour, count in sorted(hourly_counter.items()):
        print(f"{hour}:00    {count:,} requests")


if __name__ == "__main__":
    if not LOG_FILE.exists():
        print("server.log not found.")
        print("Run generate_logs.py first.")
    else:
        analyze_logs(LOG_FILE)