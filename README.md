# git audit

A simple tool for comparing branches.

## Goal

Answer the question: "What is in this branch that is not in that branch?"

## Usage

git audit "this branch" "that branch"

## Install

```
mkdir -p ~/bin/
git clone git@github.com:jrs526/git-audit.git ~/bin/git-audit
git config --global alias.audit '!~/bin/git-audit/git-audit.py'
```
