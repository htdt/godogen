import sys
import os
import subprocess

def main():
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tools_dir = os.path.join(skill_dir, "tools")
    doc_source = os.path.join(skill_dir, "doc_source")
    doc_api = os.path.join(skill_dir, "doc_api")

    if os.path.isdir(doc_api) and os.path.isfile(os.path.join(doc_api, "_common.md")):
        sys.exit(0)

    print("Bootstrapping doc_api...")

    doc_classes_dir = os.path.join(doc_source, "godot", "doc", "classes")
    if not os.path.isdir(doc_classes_dir):
        os.makedirs(doc_source, exist_ok=True)
        godot_dir = os.path.join(doc_source, "godot")

        try:
            subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                            "https://github.com/godotengine/godot.git", godot_dir], check=True)
            subprocess.run(["git", "-C", godot_dir, "sparse-checkout", "set", "doc/classes"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone Godot docs: {e}")
            sys.exit(1)

    env = os.environ.copy()
    env["PYTHONPATH"] = tools_dir

    cmd = [
        sys.executable, os.path.join(tools_dir, "godot_api_converter.py"),
        "-i", doc_classes_dir,
        "--split-dir", doc_api,
        "--class-desc", "full",
        "--method-desc", "full",
        "--property-desc", "full",
        "--signal-desc", "full",
        "--constant-desc", "full",
        "--include-virtual",
        "--full-signals"
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert Godot docs: {e}")
        sys.exit(1)

    print(f"doc_api ready at {doc_api}")

if __name__ == "__main__":
    main()
