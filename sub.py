import subprocess

def run_command(command):
    try:
        # Run the command with shell=True to use a shell context
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()
    except Exception as e:
        return -1, '', str(e)

# Example usage
command = "ls -l"  # Example command to list files in the current directory
return_code, stdout, stderr = run_command(command)
print("Return code:", return_code)
print("Standard Output:")
print(stdout)
print("Standard Error:")
print(stderr)
