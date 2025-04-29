import subprocess
import os

def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Running: {command}")
    if result.returncode != 0:
        print(f"❌ Error:\n{result.stderr}")
    else:
        print(f"✅ Success:\n{result.stdout}")

def push_to_new_remote(repo_path, new_remote_url):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Calculate the relative path to the repo directory from the script location
    repo_path = os.path.join(script_dir, repo_path)

    # Step 1: Set the new remote URL
    run_git_command(f'git -C "{repo_path}" remote set-url origin {new_remote_url}')

    # Step 2: Verify remote
    run_git_command(f'git -C "{repo_path}" remote -v')

    # Step 3: Push all branches
    run_git_command(f'git -C "{repo_path}" push origin --all')

    # Step 4: Push all tags
    run_git_command(f'git -C "{repo_path}" push origin --tags')

# --- Usage ---
repo_directory = "../"  # Relative path to the repository, from the script's location
new_remote = "https://github.com/bishal784411/DetentionData"  # New remote URL

push_to_new_remote(repo_directory, new_remote)
