from subprocess import run
from os import path
from platform import system
from shutil import rmtree

def main():
    # Clone repo
    nvim_dir = path.join("~", ".config", "nvim")
    rust_path = path.join("~", ".cargo")
    sys = system()

    if path.isdir(nvim_dir):
        while True:
            proceed = input(f"There already is a nvim configuration at {nvim_dir}. Replace and continue? (y, n)\n").lower()
            if proceed == "y":
                rmtree(nvim_dir)
                break
            elif proceed == "n":
                return

    run(["git", "clone", "https://github.com/MJDevelops/config.nvim.git", nvim_dir])

    # Install Rust
    if not path.isdir(rust_path):
        if sys == "Linux":
            run(["curl", "--proto", "'=https'", "--tlsv1.2", "-sSf", "https://sh.rustup.rs", "|", "sh", "-s", "--", "-y"])


if __name__ == '__main__':
    main()
