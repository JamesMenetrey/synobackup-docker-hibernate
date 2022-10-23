from datetime import datetime
import time
import subprocess
import sys

import docker


def log(message):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{date_time}] {message}")


# Read the mandatory arguments
if len(sys.argv) != 4:
    print("synobackup_docker_interrupt, ver.1.1.0. Written by Jämes Ménétrey.")
    print(f"Usage: {sys.argv[0]} <container_timeout> <initial_backup_check> <interval_backup_check>")
    print("\t- container_timeout: time [s] to shut down gracefully a container before it's killed.")
    print("\t- initial_backup_check: time [s] to check whether a backup is occurring for the first time.")
    print("\t- interval_backup_check: time interval [s] to check whether a backup occurs after the first time.")
    print("The exit code is zero when the script completes successfully, otherwise non-zero.")
    print()
    print("Note: initial_backup_check is used after the containers are stopped, while interval_backup_check is")
    print("      used on a regular basis once the first check has occurred. This allows for planning a shutdown of the")
    print("      containers with a more significant interval before the backup operation occurs.")
    sys.exit(1)

exit_code = 0
container_timeout = int(sys.argv[1])
initial_backup_check = int(sys.argv[2])
interval_backup_check = int(sys.argv[3])

log(f"{sys.argv[0]} started, container_timeout={container_timeout}, initial_backup_check={initial_backup_check}, "
    f"initial_backup_check={initial_backup_check}.")

# Retrieve the list of the running containers
client = docker.from_env()
snapshot_of_running_containers = client.containers.list()

# Stop the containers with the provided timeout
for running_container in snapshot_of_running_containers:
    log(f"Stopping container {running_container.name} ({running_container.short_id})..")
    try:
        running_container.stop(timeout=container_timeout)
    except Exception as e:
        log(f"Cannot stop container {running_container.name} ({running_container.short_id}): {e}")
        exit_code = 1

# Wait for the backup process to finish
log("Waiting the backup process to finish..")
time.sleep(initial_backup_check)
while subprocess.run(["synobackup", "--is-backup-restore-running"]).returncode == 1:
    time.sleep(interval_backup_check)

# Restart the previously running containers
for stopped_container in snapshot_of_running_containers:
    log(f"Starting container {stopped_container.name} ({stopped_container.short_id})..")
    try:
        stopped_container.start()
    except Exception as e:
        log(f"Cannot start container {stopped_container.name} ({stopped_container.short_id}): {e}")
        exit_code = 1

log(f"{sys.argv[0]} ended.")
sys.exit(exit_code)
