
# Git guidelines

+ Only allowed to make changes to main via pull request

+ 2 Approvals are needed before rebase and merge.

+ No commit name scheme but please use proper grammar and imperative mood.

    CORRECT:  `Add some diagrams` or `Fix the bug` 
    
    WRONG: `Added some stuff` or `Fixed this`

## Step-by-step guide

1. Update local repo  
`git pull`

2. Go to the main branch to base your changes upon   
`git checkout main`

3. Create new branch name with good name  
`git checkout -b branch-name`

4. Make your changes

5. Add and commit your changes  
`git add .`
`git commit -m 'Good commit name'`

6. Push changes to new remote branch  
`git push --set-remote-upstream origin branch-name`

7. Create a pull request on Github (with good description)

8. Hope your changes get approved