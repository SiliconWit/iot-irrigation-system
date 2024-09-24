import subprocess
import datetime
import os
import time
import sys

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    return output + error, process.returncode

def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()

def main():
    commands = [
        "pio run --target clean",
        "pio run",
        "pio run --target upload"
    ]

    report = "# PlatformIO Upload Report\n\n"
    report += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    print("Starting PlatformIO upload process...")
    
    for i, command in enumerate(commands, 1):
        print(f"\nExecuting: {command}")
        print_progress(0, 100, prefix='Progress:', suffix='Complete', length=30)
        
        start_time = time.time()
        output, return_code = run_command(command)
        end_time = time.time()

        print_progress(100, 100, prefix='Progress:', suffix='Complete', length=30)
        
        execution_time = end_time - start_time
        status = "Success" if return_code == 0 else "Failed"

        report += f"## Command: `{command}`\n\n"
        report += f"**Status:** {status}\n\n"
        report += f"**Execution Time:** {execution_time:.2f} seconds\n\n"
        report += "**Output:**\n\n"
        report += f"```\n{output}\n```\n\n"
        report += "---\n\n"

    report_file = "upload_report.md"
    with open(report_file, "w") as f:
        f.write(report)

    print(f"\nUpload process completed. Report saved in '{report_file}'")

if __name__ == "__main__":
    main()