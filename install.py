"""Configures neovim on the system"""
from subprocess import run, Popen, PIPE
from os import path
from platform import system, machine
from shutil import rmtree, which
from sys import executable
from importlib import import_module
from pathlib import Path

def install_import(package: str):
    """Dynamically imports pip modules and installs them if they not exists"""
    pkg = None
    try:
        import_module(package)
    except ImportError:
        run([executable, "-m", "pip", "install", package, "--break-system-packages"], check=True)
    finally:
        pkg = import_module(package)
    return pkg


def install_nvim(sys_name: str):
    """Identifies system and installs neovim"""
    if sys_name in ["Darwin", "Linux"]:
        home = Path.home()
        arch = machine()
        plat = "linux" if sys_name == "Linux" else "macos"
        arch = "arm64" if arch == "aarch64" else arch
        file = f"nvim-{plat}-{arch}.tar.gz"
        run(["curl", "-LO",
            f"https://github.com/neovim/neovim/releases/latest/download/{file}"], check=True)
        run(["sudo", "rm", "-rf", "/opt/nvim"], check=True)
        run(["sudo", "tar", "-C", "/opt", "-xzf", file], check=True)
        run(["rm", file], check=True)

        shellingham = install_import("shellingham")
        rc_path = ""
        s = shellingham.detect_shell()

        if s[0] == "bash":
            rc_path = path.join(home, ".bashrc")

        with open(rc_path, "a", encoding="utf-8") as f:
            f.write(f"\nexport PATH=\"$PATH:/opt/{file[:-7]}/bin\"")

        print("\nRestart shell to use nvim.")


def install_git(sys_name: str):
    """Identifies system and installs git"""
    if sys_name == "Linux":
        distro = install_import("distro")
        distro_name = distro.id()
        if distro_name in ["debian", "ubuntu"]:
            run(["apt-get", "install", "git"], check=True)
        elif distro_name == "fedora":
            manager = "yum" if int(distro.major_version()) <= 21 else "dnf"
            run([manager, "install", "git"], check=True)
    elif sys_name == "Darwin":
        # Install homebrew if not installed
        if which("brew") is None:
            run(["NONINTERACTIVE=1", "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""], check=True)
        run(["brew", "install", "git"], check=True)


def main():
    """Main function"""
    home = Path.home()
    nvim_dir = path.join(home, ".config", "nvim")
    rust_path = path.join(home, ".cargo")
    sys_name = system()

    if path.isdir(nvim_dir):
        while True:
            proceed = input(
                f"There already is a nvim configuration at {nvim_dir}. Replace and continue? (y, n)\n").lower()
            if proceed == "y":
                rmtree(nvim_dir)
                break
            elif proceed == "n":
                return

    # Install neovim if not installed
    if which("nvim") is None:
        print("nvim not found, installing...\n")
        install_nvim(sys_name)

    # install git if not installed
    if which("git") is None:
        print("git not found, installing git...\n")
        install_git(sys_name)

    run(["git", "clone", "https://github.com/MJDevelops/config.nvim.git",
        nvim_dir], check=True)

    # Install Rust
    if not path.isdir(rust_path):
        if sys_name == "Linux":
            p1 = Popen(["curl", "https://sh.rustup.rs"], stdout=PIPE)
            Popen(["sh", "-s", "--", "-y"], stdin=p1.stdout)
            p1.stdout.close()


if __name__ == '__main__':
    main()
