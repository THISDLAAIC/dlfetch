# DLFetch
> A simple command-line tool to fetch data from xiaobao system of THISDL.
---
## Demonstration
[![asciicast](https://asciinema.org/a/8ZBfi32rtrvu7j6rKgNyY4DwK.svg)](https://asciinema.org/a/8ZBfi32rtrvu7j6rKgNyY4DwK)
---
## Installation
### 1. Install a Chrome browser  
You can download it at [here](https://www.google.com/chrome)
If you don't know the administrator password, please contact IT for help.
### 2. Clone this repository and change to the directory  
Open a terminal and run command `git clone https://github.com/huangdihd/dlfetch` to clone it.
Use command `cd dlfetch` to change to the directory.
### 3. Create virtual environment
Use command `python3 -m venv ./.venv` to create a virtual environment.
### 4. Configure identity information and add command alias  
Edit and run this command:
```zsh
cat <<EOF >> ~/.zshrc && source ~/.zshrc
export THISDL_USERNAME="your username"
export THISDL_PASSWORD="your password"
alias dlfetch=". $(pwd)/.venv/bin/activate&&python3 $(pwd)/main.py&&deactivate"
EOF
```
### 5. Install dependencies
Use command `python3 -m pip install -r requirements.txt` to install dependencies.
### 6. Enjoy it!
Use command `dlfetch` to fetch your data anywhere!

---
**If you like this project, please give me a star!**
