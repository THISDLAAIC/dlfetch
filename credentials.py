import getpass
import hashlib
import json
import os

try:
    import keyring
    import keyring.errors
except ImportError:
    keyring = None

SERVICE = "dlfetch"
config_dir = os.path.expanduser("~/.dlfetch")
config_path = os.path.join(config_dir, "config")
fallback_path = os.path.join(config_dir, "credentials")


def md5_upper(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest().upper()


def _load_username() -> str | None:
    if not os.path.exists(config_path):
        return None
    with open(config_path) as config_file:
        try:
            return json.load(config_file).get("username")
        except ValueError:
            return None


def _save_username(username: str):
    os.makedirs(config_dir, exist_ok=True)
    with open(config_path, 'w') as config_file:
        json.dump({"username": username}, config_file)


def _write_private(path: str, content: str):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as private_file:
        private_file.write(content)


def save_credentials(username: str, password_md5: str):
    _save_username(username)
    if keyring is not None:
        try:
            keyring.set_password(SERVICE, username, password_md5)
            return
        except keyring.errors.KeyringError:
            pass
    print("System keyring unavailable, saving to ~/.dlfetch/credentials (permission 0600) instead.")
    _write_private(fallback_path, password_md5)


def load_credentials() -> tuple[str, str] | None:
    username = _load_username()
    if not username:
        return _migrate_from_env()

    if keyring is not None:
        try:
            password_md5 = keyring.get_password(SERVICE, username)
            if password_md5:
                return username, password_md5
        except keyring.errors.KeyringError:
            pass

    if os.path.exists(fallback_path):
        with open(fallback_path) as fallback_file:
            password_md5 = fallback_file.read().strip()
        if password_md5:
            return username, password_md5

    return None


def delete_credentials():
    username = _load_username()
    if username and keyring is not None:
        try:
            keyring.delete_password(SERVICE, username)
        except keyring.errors.KeyringError:
            pass
    for path in (fallback_path, config_path):
        if os.path.exists(path):
            os.remove(path)


def _migrate_from_env() -> tuple[str, str] | None:
    username = os.environ.get('THISDL_USERNAME')
    password = os.environ.get('THISDL_PASSWORD')
    if not username or not password:
        return None

    password_md5 = md5_upper(password)
    save_credentials(username, password_md5)
    print("Migrated credentials from THISDL_USERNAME/THISDL_PASSWORD to secure storage.")
    print("Please remove the export lines from ~/.zshrc, for example:")
    print("  sed -i '' '/export THISDL_USERNAME/d;/export THISDL_PASSWORD/d' ~/.zshrc")
    return username, password_md5


def prompt_and_save() -> tuple[str, str]:
    username = input("Please enter your username: ").strip()
    password = getpass.getpass("Please enter your password (will be hidden): ")
    password_md5 = md5_upper(password)
    del password
    save_credentials(username, password_md5)
    return username, password_md5
