# This script is the installation script of dlfetch
dir=$(pwd)
cd ~
echo "Cloning the repository..."
git clone https://github.com/huangdihd/dlfetch
cd dlfetch
echo "Creating virtual environment..."
python3 -m venv ./.venv
echo "Activating virtual environment..."
. ./.venv/bin/activate
echo "Installing dependencies..."
pip install -r ./requirements.txt
echo "Configuring Identity information..."
echo -n "Please enter your username: "
read username
echo -n "Please enter your password(will be hidden): "
read -s password
cat << EOF >> ~/.zshrc
export THISDL_USERNAME="$username"
export THISDL_PASSWORD="$password"
alias dlfetch="source $(pwd)/.venv/bin/activate && python3 $(pwd)/main.py && deactivate"
EOF
echo "Installation finished!"
echo "Reopen the terminal and use command \"dlfetch\" to enjoy it!"
