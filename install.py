import subprocess
import sys

PACKAGES = [
    "discord.py-self",
    "aiohttp",
    "requests",
    "pynacl",
    "pytz",
    "psutil",
    "colour",
    "python-dateutil",
    "instaloader",
]

def install_package(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"  [+] {package} - thành công")
        return True
    except subprocess.CalledProcessError:
        print(f"  [-] {package} - thất bại")
        return False

def main():
    print("=" * 50)
    print("  VVNK - Cài đặt thư viện")
    print("=" * 50)
    print()

    success = 0
    fail = 0

    for pkg in PACKAGES:
        result = install_package(pkg)
        if result:
            success += 1
        else:
            fail += 1

    print()
    print(f"  Hoàn thành: {success} thành công, {fail} thất bại")
    print()

    if fail > 0:
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
