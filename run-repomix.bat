@echo off
npx repomix --ignore "_data/*,topics/*" "docs" --style markdown --remove-comments
pause