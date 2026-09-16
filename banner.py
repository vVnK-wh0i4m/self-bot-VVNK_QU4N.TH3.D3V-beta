import platform
import discord

__NAME__ = 'VVNK'

def show_banner():
    guild_count = 0
    python_ver = platform.python_version()
    discord_ver = discord.__version__
    banner = f"""\033[1;33m
                  QU4N.TH3.D3V\033[0m
\033[1;36m    ██╗   ██╗██╗   ██╗███╗   ██╗██╗  ██╗   \033[0m
\033[1;36m    ██║   ██║██║   ██║████╗  ██║██║ ██╔╝   \033[0m
\033[1;36m    ██║   ██║██║   ██║██╔██╗ ██║█████╔╝    \033[0m
\033[1;36m    ╚██╗ ██╔╝╚██╗ ██╔╝██║╚██╗██║██╔═██╗    \033[0m
\033[1;36m     ╚████╔╝  ╚████╔╝ ██║ ╚████║██║  ██╗   \033[0m
\033[1;36m      ╚═══╝    ╚═══╝  ╚═╝  ╚═══╝╚═╝  ╚═╝   \033[0m
    """
    print(banner)
    print(f"\033[1;36m[>] Bot:\033[0m \033[1;32m{__NAME__}\033[0m")
    print(f"\033[1;36m[>] Author:\033[0m \033[1;32mQU4N.TH3.D3V\033[0m")
    print(f"\033[1;36m[>] Python:\033[0m \033[1;32m{python_ver}\033[0m")
    print(f"\033[1;36m[>] Discord.py:\033[0m \033[1;32m{discord_ver}\033[0m")
    print(f"\033[1;36m{'='*54}\033[0m")
    print(f"\033[1;32m[INFO] Banner loaded. Waiting for bot...\033[0m")

if __name__ == "__main__":
    show_banner()
    import time
    while True:
        time.sleep(1)
