#!/usr/bin/env python

import sys
import git
import os
import argparse

NO_MERGE_STRING = "do not merge down"
NO_MERGE_ANC_STRING = NO_MERGE_STRING + " ancestors"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-details", action="store_true", default=False)
    parser.add_argument("--ignore", default=None, metavar='COMMIT')
    parser.add_argument("--ignore-ancestors", default=None, metavar='COMMIT')
    parser.add_argument(
        "branch_hierarchy",
        default=[],
        metavar='BRANCH',
        nargs="*")

    args = parser.parse_args(argv)

    repo = git.Repo(os.getcwd())

    if args.ignore:
        repo.git.notes('add', '-m', NO_MERGE_STRING, args.ignore)
    elif args.ignore_ancestors:
        repo.git.notes('add', '-m', NO_MERGE_ANC_STRING, args.ignore_ancestors)
    else:

        if args.no_details:
            git_format = "--pretty=%Cred%h%Creset"
        else:
            git_format = "--pretty=%Cred%h %Cgreen%<(19,mtrunc)%an %Creset%<(51,trunc)%s"

        print_audit(args.branch_hierarchy, git_format)


def print_audit(branches, git_format):
    repo = git.Repo(os.getcwd())

    for i in range(len(branches)-1):
        branch = branches[i]
        upstream = branches[i+1]

        print '\033[94m', branch, "-->", upstream, '\033[0m'

        banned = []
        notes = repo.git.notes()
        if len(notes) > 0:
          for commit in [c.split()[1] for c in notes.split("\n")]:
              if contains_note(commit, NO_MERGE_STRING):
                  banned.append(commit)
              if contains_note(commit, NO_MERGE_ANC_STRING):
                  banned.extend(
                      repo.git.log(commit, '--pretty=%H').split('\n'))

        for commit in magic_cherry(upstream, branch):
            if commit not in banned:
                print repo.git.log(commit, '-1', git_format)


def contains_note(commit, note):
    repo = git.Repo(os.getcwd())
    try:
        notes = repo.git.notes('show', commit)
    except git.exc.GitCommandError as err:
        if "No note found for object" in str(err):
            return False
        else:
            raise err

    if note in notes:
        return True
    else:
        return False


def magic_cherry(upstream, branch):
    repo = git.Repo(os.getcwd())
    cherry = repo.git.cherry(upstream, branch)
    if len(cherry) == 0:
      return []
    else:
      return [y.strip("+ ") for y in filter(
          lambda x: x[0] == "+",
          cherry.split('\n'))]

if __name__ == '__main__':
    main(sys.argv[1:])
