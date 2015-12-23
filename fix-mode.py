import os
import argparse
import shlex
from subprocess import call
from git import Repo, InvalidGitRepositoryError


parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("-d", action="store_true")
args = parser.parse_args()


def get_permission_changes(diff):
    to_change = []
    for i in xrange(len(diff)):
        try:
            if diff[i].startswith("diff") and diff[i+1].startswith("old") and diff[i+2].startswith("new"):
                to_change.append([line.split(" ")[-1] for line in diff[i:i+3]])
        except IndexError:
            continue

    return map(lambda arr: [x.replace("b/", "").replace("100", "") for x in arr], to_change)


def make_change(change_info):
    cmd = shlex.split("chmod %s %s" % (change_info[1], os.path.join(path, change_info[0])))
    if not args.d:
        call(cmd)
    print("chmod %s: %s => %s" % (change_info[0], change_info[2], change_info[1]))


def main(path):
    print("\nChecking %s" % path)
    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        print("It is not a repository")
        return
    if not repo.active_branch.is_valid():
        print("No commits in this repository.")
        return
    print("It is a repository!")
    try:
        t = repo.head.commit.tree
        diff = repo.git.diff(t).split("\n")
        changes = get_permission_changes(diff)
        map(make_change, changes)
    # had a repo with files that were last saved on Windows, raising en exception... TODO: fix it
    except UnicodeDecodeError:
        print("The diff on this repo contains problematic characters, skipping.")


if __name__ == "__main__":
    if args.d:
        print("Dry run, not changing file modes.")
    for root, dirs, files in os.walk(args.path):
        if not (".git" in root or "node_modules" in root):
            path = root
            main(root)
