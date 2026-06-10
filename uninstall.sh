# This script is the uninstallation script of dlfetch
dir=$(pwd)
echo "Removing saved credentials..."
"$HOME/dlfetch/.venv/bin/python3" -c "import sys; sys.path.insert(0, '$HOME/dlfetch'); from credentials import delete_credentials; delete_credentials()" 2>/dev/null
rm -rf "$HOME/.dlfetch"
echo "Removing dlfetch directory..."
rm -rf "$HOME/dlfetch"
echo "Cleaning up ~/.zshrc..."
sed -i '' '/# DLFetch start/,/# DLFetch end/d' "$HOME/.zshrc"
echo "Removing session..."
rm -f "$HOME/.dlfetch_session"
echo "Uninstallation finished!"
cd "$dir" || exit 1
