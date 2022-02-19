# Notes week 0

## 2/15/2022
Git terminal commands:
- git init == creates repo for current folder
- git clone <url> == make local copy of repo
- git checkout -b <branch_name> == make a new branch and move you into to work
- git add <file> == adds file to stage to track and later include in commit
- git status == shows which files have been changed and in stage
- git commit -m "Message" == will commit all changes with the message as the note (include -a to add all changes, even if not staged)
- git diff == shows what is unstaged (--staged or --cached to see what's staged)
- you can ignore specific filetypes with a .gitignore file so git doesn't flag them as unstaged or automatically include them which I thought was cool
<<<<<<< HEAD
- git push origin main
=======
- git push origin <branch>

>>>>>>> Week0
Not git:
- code <file> == open file in visual studio code

## 2/16/2022
### Problem set 0
- Interactive interior design game
- choose room theme first
  - magical (witch room)
  - music (bedroom 3)
  - cottage (bedroom 1)
- Change room colors?
  - green, blue, red, orange
- At least 3 extra things in room?
  - witch room: potion, broom, wizard-toad transform into wizard
  - bedroom 3: keyboard, drums, guitar (click enough times, goes to concert venue)
  - bedroom 1: grasshopper, owl, hare,frog mouse, growing plant (water can)
- make count to determine which room
  - each answer gets a score like in magazine quizzes
  - 0-3: music
  - 4-6: cottage
  - 7-9: witch