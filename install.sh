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
echo "Configuring Identity information..."
echo -n "Please enter your username: "
read -r username
echo -n "Please enter your password(will be hidden): "
read -r -s password
cat << EOF >> ~/.zshrc
# DLFetch start
export THISDL_USERNAME="$username"
export THISDL_PASSWORD="$password"
alias dlfetch="source $(pwd)/.venv/bin/activate && python3 $(pwd)/main.py && deactivate"
# DLFetch end
EOF
echo "Installation finished!"
echo "Reopen the terminal and use command \"dlfetch\" to enjoy it!"
cd "$dir" || exit
