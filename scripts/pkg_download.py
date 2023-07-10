import sys
import os
import subprocess
import shutil

class TestRequirements():
    """Test availability of required packages."""
    def __init__(self, target_board, requirement_file):
        self.board = target_board
        self.req_file = requirement_file

    def bootstrap_pip_remote(self):
        cmd = f'ssh root@{self.board} python3 -m ensurepip'
        try:
            sub = subprocess.run(cmd, capture_output=True, shell=True, check=True, timeout=40)
        except Exception as e:
            print(f'exception: {e}')
        else:
            print(f"error code: {sub.returncode}")
            print(sub.stdout.decode())

    def download_python_packages(self):
        if os.path.exists('./req_downloads'):
            print("Deleting the req_downloads directory")
            shutil.rmtree('./req_downloads')

        cmd = f'python3 -m pip download --dest req_downloads -r {self.req_file}'
        try:
            sub = subprocess.run(cmd, capture_output=True, shell=True, check=True, timeout=40)
        except Exception as e:
            print(f'exception: {e}')
        else:
            print(f"error code: {sub.returncode}")
            print(sub.stdout.decode())   

    def transfer_package_remote(self):
        if os.path.exists('./req_downloads'):
            cmd = f'scp -r req_downloads root@{self.board}:/home/root/packages'
            cmd_2 = f'scp {self.req_file} root@{self.board}:/home/root/packages'
            try:
                sub = subprocess.run(cmd, capture_output=True, shell=True, check=True, timeout=40)
                sub = subprocess.run(cmd_2, capture_output=True, shell=True, check=True, timeout=40)
            except Exception as e:
                print(f'exception: {e}')
            else:
                print(f"error code: {sub.returncode}")
                print(sub.stdout.decode())
        else:
            print("req_downloads directory does not exist!")

    def install_packages_remote(self):
        cmd = f'ssh root@{self.board} python3 -m pip install --no-index --find-links=/home/root/packages/req_downloads -r /home/root/packages/{self.req_file}'
        try:
            sub = subprocess.run(cmd, capture_output=True, shell=True, check=True, timeout=40)
        except Exception as e:
            print(f'exception: {e}')
        else:
            print(f"error code: {sub.returncode}")
            print(sub.stdout.decode())


def main():
    if len(sys.argv) == 3:
        board=sys.argv[1]
        req_file=sys.argv[2]
        tester = TestRequirements(board, req_file)
        tester.download_python_packages()
        tester.bootstrap_pip_remote()
        tester.transfer_package_remote()
        tester.install_packages_remote()
    else:
        print("python3 pkg_download.py TALON_BOARD REQUIREMENTS.TXT")

if __name__ == "__main__":
    main()
