#!/usr/bin/env python3
import os
import subprocess
import sys

# रंग
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def run(cmd, cwd=None, check=True):
    print(f"{CYAN}> {' '.join(cmd)}{RESET}")
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        print(f"{RED}⚠️ Command failed: {' '.join(cmd)}{RESET}")
        sys.exit(result.returncode)
    return result

def main():
    print(f"{YELLOW}\n=== GitHub Force Push Script ==={RESET}\n")

    # Inputs
    repo_url = input(f"{GREEN}👉 Enter GitHub repo URL:{RESET} ").strip()
    path = input(f"{GREEN}👉 Enter local directory path:{RESET} ").strip()
    token = input(f"{GREEN}👉 Enter GitHub access token:{RESET} ").strip()
    git_name = input(f"{GREEN}👉 Enter your Git username:{RESET} ").strip()
    git_email = input(f"{GREEN}👉 Enter your Git email:{RESET} ").strip()

    if not repo_url or not path or not token:
        print(f"{RED}❌ Repo URL, path, and token are required!{RESET}")
        return
    if not os.path.isdir(path):
        print(f"{RED}❌ Directory not found: {path}{RESET}")
        return

    path = os.path.abspath(path)
    print(f"{YELLOW}\n📂 Using directory: {path}{RESET}")

    os.chdir(path)

    # Git setup
    if not os.path.isdir(os.path.join(path, ".git")):
        run(["git", "init"])

    run(["git", "config", "user.name", git_name])
    run(["git", "config", "user.email", git_email])

    run(["git", "remote", "remove", "origin"], check=False)
    run(["git", "remote", "add", "origin", repo_url])

    # Add + Commit
    run(["git", "add", "."])
    commit = subprocess.run(["git", "commit", "-m", "Upload from force_push.py"], cwd=path)
    if commit.returncode != 0:
        print(f"{YELLOW}⚠️ Nothing new to commit. Creating empty commit...{RESET}")
        run(["git", "commit", "--allow-empty", "-m", "Initial empty commit"], cwd=path)

    run(["git", "branch", "-M", "main"])

    # Tokenized URL
    token_url = repo_url.replace("https://", f"https://{token}@", 1)

    # Force push
    print(f"{YELLOW}\n🚀 Force pushing to GitHub...{RESET}")
    run(["git", "push", token_url, "main", "--force"])

    # Reset to clean URL
    run(["git", "remote", "set-url", "origin", repo_url])

    print(f"\n{GREEN}✅ Upload complete!{RESET}")

if __name__ == "__main__":
    main()
