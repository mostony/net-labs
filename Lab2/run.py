import subprocess
import argparse
import platform

HEADER_SIZE = 28


def check_size(
    hostname: str, packet_size: int, verbose: bool, timeout: float | None
) -> bool:
    if verbose:
        print(f"Пингуем пакет размера {packet_size}")
    if platform.system().lower() == "Windows":
        command = f"ping {hostname} -f -l {packet_size}"
    else:
        command = f"ping {hostname} -D -c 1 -s {packet_size}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        if verbose:
            if result.returncode == 0:
                print("Succeed")
            else:
                print("Failed")
        return result.returncode == 0
    except Exception as e:
        if verbose:
            print("Failed")
        return False


def find_minimum_mtu(hostname: str, verbose: bool, timeout: float | None) -> int:
    low = 0
    high = 1
    while check_size(hostname, high, verbose, timeout):
        high *= 2
    while high - low > 1:
        mid = (low + high) // 2
        if check_size(hostname, mid, verbose, timeout):
            low = mid
        else:
            high = mid
    return low


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True, help="адрес назначения")
    parser.add_argument(
        "--v", action="store_true", required=False, help="отображение логов"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        required=False,
        default=None,
        help="Максимальное время ожидания пакета",
    )

    args = parser.parse_args()

    hostname = args.host
    verbose = args.v
    timeout = args.timeout

    if verbose:
        print(f"Операционная система: {platform.system().lower()}...")

    if verbose:
        print("Начинаем искать минимальный MTU...")

    if not check_size(hostname, 0, verbose, timeout):
        print(f"Адрес назначения не доступен")
        exit(0)

    min_mtu = find_minimum_mtu(hostname, verbose, timeout)
    min_mtu += HEADER_SIZE

    print(f"Минимальное значение MTU для канала до {hostname}: {min_mtu}")
