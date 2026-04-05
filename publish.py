import sys
import os
import shutil
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Publish godogen skills into a target project directory.")
    parser.add_argument("target_dir", help="Target directory")
    parser.add_argument("--force", action="store_true", help="Delete existing target contents before publishing")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.abspath(__file__))
    target = os.path.abspath(args.target_dir)

    if args.force and os.path.exists(target):
        print(f"Force: cleaning {target}")
        shutil.rmtree(target, ignore_errors=True)

    if not os.path.exists(target):
        os.makedirs(target)

    print(f"Publishing to: {target}")

    skills_target = os.path.join(target, ".claude", "skills")
    os.makedirs(skills_target, exist_ok=True)

    skills_source = os.path.join(repo_root, "skills")

    def ignore_patterns(path, names):
        return [n for n in names if n in ['doc_source', '__pycache__']]

    for item in os.listdir(skills_source):
        s = os.path.join(skills_source, item)
        d = os.path.join(skills_target, item)
        if os.path.isdir(s):
            if item in ['doc_source', '__pycache__']:
                continue
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)
            shutil.copytree(s, d, ignore=ignore_patterns)
        else:
            shutil.copy2(s, d)

    shutil.copy2(os.path.join(repo_root, "game.md"), os.path.join(target, "CLAUDE.md"))
    print("Created CLAUDE.md")

    gitignore_path = os.path.join(target, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write(".claude\nCLAUDE.md\nassets\nscreenshots\n.vqa.log\n.godot\n*.import\n")
        print("Created .gitignore")

    try:
        subprocess.run(["git", "init", "-q"], cwd=target, stderr=subprocess.DEVNULL, check=False)
    except FileNotFoundError:
        # git not installed or not in PATH, skip silently as in the original bash script
        pass

    num_skills = len([name for name in os.listdir(skills_target) if os.path.isdir(os.path.join(skills_target, name))])
    print(f"Done. skills: {num_skills}")

if __name__ == "__main__":
    main()
