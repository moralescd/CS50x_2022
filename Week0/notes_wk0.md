# Notes week 0

## 2/16/2022
Today I learned how to use git through the terminal.
Some git commands:
- git init == creates repo for current folder
- git clone <url> == make local copy of repo
- git checkout -b <branch_name> == make a new branch and move you into to work
- git add <file> == adds file to stage to track and later include in commit
- git status == shows which files have been changed and in stage
- git commit -m "Message" == will commit all changes with the message as the note (include -a to add all changes, even if not staged)
- git diff == shows what is unstaged (--staged or --cached to see what's staged)
- you can ignore specific filetypes with a .gitignore file so git doesn't flag them as unstaged or automatically include them which I thought was cool

Not git:
- code <file> == open file in visual studio code