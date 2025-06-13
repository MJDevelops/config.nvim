from subprocess import run, check_call
from os import path
from platform import system, machine
from shutil import rmtree, which
from sys import executable
from importlib import import_module
from pathlib import Path

def install_import(package):
    try:
        import_module(package)
    except ImportError:
        check_call([executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = import_module(package)

def main():
    home = Path.home()
    nvim_dir = path.join(home, ".config", "nvim")
    rust_path = path.join(home, ".cargo")
    sys_name = system()

    if path.isdir(nvim_dir):
        while True:
            proceed = input(f"There already is a nvim configuration at {nvim_dir}. Replace and continue? (y, n)\n").lower()
            if proceed == "y":
                rmtree(nvim_dir)
                break
            elif proceed == "n":
                return

    # Install neovim if not installed
    if which("nvim") is None:
        if sys_name == "Linux" or sys_name == "Darwin":
            arch = machine()
            plat = "linux" if sys_name == "Linux" else "macos"
            arch = "arm64" if arch == "aarch64" else arch
            file = f"nvim-{plat}-{arch}.tar.gz"
            run(["curl", "-LO", f"https://github.com/neovim/neovim/releases/latest/download/{file}"])
            run(["sudo", "rm", "-rf", "/opt/nvim"])
            run(["sudo", "tar", "-C", "/opt", "-xzf", file])
            run(["rm", file])


    # install git if not installed
    if which("git") is None:
        print("git not found, installing git...\n")
        if sys_name == "Linux":
            install_import("distro")
            distro_name = distro.id()
            if distro_name == "ubuntu" or distro_name == "debian":
                run(["apt-get", "install", "git"])
            elif distro_name == "fedora":
                manager = "dnf"
                if int(distro.major_version()) <= 21:
                    manager = "yum"
                run([manager, "install", "git"])
        elif sys_name == "Darwin":
            # Install homebrew if not installed
            if which("brew") is None:
                run(["NONINTERACTIVE=1", "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""])
            run(["brew", "install", "git"])

    run(["git", "clone", "https://github.com/MJDevelops/config.nvim.git", nvim_dir])

    # Install Rust
    if not path.isdir(rust_path):
        if sys_name == "Linux":
            run(["curl", "--proto", "'=https'", "--tlsv1.2", "-sSf", "https://sh.rustup.rs", "|", "sh", "-s", "--", "-y"])

if __name__ == '__main__':
    main()
