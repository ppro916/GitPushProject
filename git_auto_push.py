import os
from subprocess import run, CalledProcessError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def ask_input(prompt):
    return input(Fore.CYAN + prompt + Fore.YELLOW)

def git_command(cmd, cwd=None):
    try:
        run(cmd, cwd=cwd, check=True)
        print(Fore.GREEN + "✔ " + " ".join(cmd))
    except CalledProcessError:
        print(Fore.RED + "✘ Command failed:", " ".join(cmd))

def main():
    print(Fore.MAGENTA + Style.BRIGHT + "\n=== Git Auto Push Tool ===\n")

    repo_url = ask_input("👉 Enter your GitHub repo URL: ")
    dir_path = ask_input("👉 Enter your local directory path: ")
    token = ask_input("👉 Enter your GitHub Access Token: ")
    username = ask_input("👉 Enter your Git username: ")
    email = ask_input("👉 Enter your Git email: ")

    # Final token URL
    token_url = repo_url.replace("https://", f"https://{token}@")

    if not os.path.exists(dir_path):
        print(Fore.RED + "✘ Directory not found!")
        return

    os.chdir(dir_path)

    # Git config
    git_command(["git", "config", "user.name", username])
    git_command(["git", "config", "user.email", email])

    # Init repo
    git_command(["git", "init"])

    # Add & commit
    git_command(["git", "add", "."])
    git_command(["git", "commit", "-m", "Initial commit"])

    # Branch
    git_command(["git", "branch", "-M", "main"])

    # Force push
    git_command(["git", "push", "--force", token_url, "main"])

    print(Fore.GREEN + Style.BRIGHT + "\n🎉 Upload complete!\n")

if __name__ == "__main__":
    main()
