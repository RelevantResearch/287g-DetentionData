import os
import subprocess

def read_first_line(file_path):
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return "UnknownFile"
    with open(file_path, 'r') as f:
        return f.readline().strip()

def push_to_github():
    try:
        base_dir = os.path.dirname(__file__)
        repo_root = os.path.abspath(os.path.join(base_dir, ".."))
        participating_txt = os.path.join(repo_root, 'Monitor', 'last-participating.txt')
        pending_txt = os.path.join(repo_root, 'Monitor', 'last-pending.txt')

        # Read filenames
        participating_filename = read_first_line(participating_txt)
        pending_filename = read_first_line(pending_txt)

        # Prepare commit message
        commit_message = f"New Sheets Alert! {participating_filename} and {pending_filename}"

        # Change directory to repo root
        os.chdir(repo_root)

        # Git commands
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Files successfully pushed to GitHub.")

    except subprocess.CalledProcessError as e:
        print(f" Git command failed: {e}")
    except Exception as ex:
        print(f" Unexpected error: {ex}")