# This script is the installation script of dlfetch
dir=$(pwd)
cd "$HOME" || exit 1
echo "Cloning the repository..."
git clone https://github.com/huangdihd/dlfetch
cd dlfetch || exit 1
echo "Creating virtual environment..."
python3 -m venv ./.venv
echo "Activating virtual environment..."
. ./.venv/bin/activate
echo "Installing dependencies..."
pip install -r ./requirements.txt
cat << EOF >> ~/.zshrc
# DLFetch start
alias dlfetch="source $(pwd)/.venv/bin/activate && python3 $(pwd)/main.py && deactivate"
# DLFetch end
EOF
echo "Installation finished!"
echo "Reopen the terminal and use command \"dlfetch\" to enjoy it!"
echo "On first run you will be asked for your username and password,"
echo "which will be stored securely in the system keyring."
cd "$dir" || exit
