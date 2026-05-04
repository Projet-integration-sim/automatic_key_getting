from google.cloud import secretmanager
from pathlib import Path
import subprocess
import os

client = secretmanager.SecretManagerServiceClient()

name = client.secret_path(os.environ["PROJECT_NAME"], os.environ["KEY_NAME"])

value = client.access_secret_version(request={"name": name + "/versions/latest"})

user_ssh_key_path = Path("~/.ssh/id_deploy").expanduser()
with open(user_ssh_key_path, "wb") as f:
    f.write(value.payload.data)
os.chmod(user_ssh_key_path, 0o600)

github_config = r"""
Host github.com
  HostName github.com
  IdentityFile ~/.ssh/id_deploy
  IdentitiesOnly yes
"""

known_hosts = subprocess.run(
    ["ssh-keyscan", "-t", "rsa", "github.com"], capture_output=True
).stdout.decode()

with open(Path("~/.ssh/config").expanduser(), "w") as f:
    f.write(github_config)

with open(Path("~/.ssh/known_hosts").expanduser(), "w") as f:
    f.write(known_hosts)
