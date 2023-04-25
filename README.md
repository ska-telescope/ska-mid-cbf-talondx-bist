# Intro

This repository holds the Built In Self Test (BIST) for the Talons. It provides the source code to run the BIST, the bitstream to program, and a script that manages the BIST start, stop, and delay on the target system.

<div align="center">
![BIST Deployment Architecture](images/bist_arch.jpg)<br>
Figure 1. BIST Deployment Architecture</div><br>

## How to Install
### Manual Method
1. Grab the package from CAR.
2. Transfer the package to the target device via SCP: 
   
    ```
    scp <bist_archive.tar.gz> root@<target>:/home/root/packages
    ```

3. SSH into the the target device and unpack the package at root on the target device: 

    ```
    $ssh root@<target>
    $tar -xvzf bist_archive.tar.gz -C /
    ```

4. On the target device, run `bist.sh -v` to verify the files.
5. On the target device, run `bist.sh -s` to install the BIST systemd service and extract the required BIST bitstream files.
6. Restart the target device; the BIST will run automatically on boot-up.
   
### Using the scripts
You have the following options for placing the BIST package onto a board/sd-card:
- Install the BIST package on target board and set it up (end-to-end):<br>
  - `./scripts/install.sh -n my_bist.tar.gz -g -s talon1 -b talon1`<br>
  - `./scripts/install.sh -c 0.1.0 -s talon1 -b talon1`<br>
- Only generate a local package:<br>`./scripts/install.sh -n my_bist.tar.gz -g`
- Only download the package from CAR:<br>`./scripts/install.sh -c 0.1.0`
- Only install the package over network (SCP & SSH):<br>
    - CAR:<br>`./scripts/install.sh -c 0.1.0 -s talon1`
    - LOCAL:<br>`./scripts/install.sh -n my_bist.tar.gz -s talon1`
- Only install the package if the sd-card is mounted:<br>
    - CAR:<br>`./scripts/install.sh -c 0.1.0 -i /mnt/p2/`
    - LOCAL:<br>`./scripts/install.sh -n my_bist.tar.gz -i /mnt/p2/`

If end-to-end method is not used, users may then run the `bist.sh <flags>` scripts on the target to verify and install the services themselves. 
## How to Use the on-board "\bin\bist.sh" script

The package grabbed from CAR (Central Artifact Repository) mirrors the file system of the target talon boards. This has been done to simplify the process of deployment, because once the tar.gz package is unpacked at root on a given target talon board, all the necessary files and scripts would be placed at the correct location, granted the structure of this repository was set correctly.

For example a given package `bist_archive.tar.gz` could be unpacked at root:
```
$ssh root@<target>
$tar -xvzf bist_archive.tar.gz -C /
```
This would place the `bist.sh` script at `/bin`. The user may then call this script to perform various actions.

### Available Actions

The intent is that the BIST will start automatically on each boot-up to run a system diagnostic. However, a small delay is introduced before this service is started in case it is required to stop it from running. This delay is managed by `bist.timer` service and could be modified by the `bist.sh` script.

The automatic startup is achieved via the systemd service (unit files). The `bist.service` is triggered by `bist.timer`. The user may kill the BIST runner before it is triggered by `bist.timer` via the bist script.

Run the `bist.sh` script to view the available commands.

- -s&emsp;--> Start the BIST systemd service and exract tar file
- -k&emsp;--> Kill the BIST systemd service immediately, aborting the BIST
- -r&emsp;--> Run the BIST
- -m [time] --> Modify the BIST systemd start delay time by <time>
- -t&emsp;--> Show the current BIST systemd start delay time
- -p&emsp;--> Program the BIST bitstream
- -x&emsp;--> Extract the tar file at predefined location
- -f&emsp;--> Publish the results (.csv) of the BIST to influxdb
- -c&emsp;--> Print the results (.log) of the BIST
- -h&emsp;--> Display the help message
- -v&emsp;--> Verify the BIST files are installed correctly

The `-s` option installs the BIST runner service in systemd and extracts the BIST bitstream related files. The user might need to run this command only once per BIST package installation.

The `-k` option kills and stops the BIST runner service. Note that this also prevents the start of the BIST on future bootups, the user may run the `-s` option to reinstall the service.

The `-t` option shows the current set BIST start delay.

The `-m` option allows the user to modify the delay from within the target environment.
For example to set the start delay to 99 seconds after boot:
```
$ssh root@<target>
$bist -m 99
```

The status of a given systemd service could be read by:
```
$ssh root@<target>
$systemctl status bist.timer
$systemctl status bist.service
$journalctl -u bist.timer
```

The `-v` option verifies that the bitstream files and the service files are placed (unpacked) at the correct location.

The `-r` option runs the bist. Note that the systemd `bist.service` uses this same script to run the BIST after the required bootup delay.

The `-x` option extracts the BIST bitstream related package (.tar.gz) at a predefined location. The execution of the BIST and programming of the FPGA relies on the existence of this directory.

The `-c` option prints the results (.txt) of the most recent BIST to the screen with $cat command. 

The `-f` publishes the results of the most recent BIST output (.csv) to the influxdb database. It publishes the results via the influx CLI and requires the bucket named `talon` to exist on the target and the influxdb credentials are already setup on the board.

## TODOS
- [x] Display the BIST output results
- [ ] Verify the python dependencies are installed on the target
- [x] Install the package using `install.sh` from CAR downloaded package or locally generated package
- [x] Support bublishing the results of the BIST to influxdb
- [ ] Add the official .ipmap
- [ ] Add the official bitstream archive.tar.gz