import subprocess


def run_command(command):
    """Execute a shell command and print its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(
            f"Command: {command}\nOutput: {result.stdout.decode()}\nError: {result.stderr.decode()}"
        )
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr.decode()}")


def main():
    commands = [
        "git reset --hard",
        "git fetch origin",
        "git reset --hard origin/main",
        "chmod 664 /home/coreyms/emilys_luxury/db.sqlite3",
        "chown www-data:www-data /home/coreyms/emilys_luxury/db.sqlite3",
        "chmod 775 /home/coreyms/emilys_luxury",
        "chown www-data:www-data /home/coreyms/emilys_luxury",
        "sudo systemctl restart apache2",
    ]

    for command in commands:
        run_command(command)


if __name__ == "__main__":
    main()
