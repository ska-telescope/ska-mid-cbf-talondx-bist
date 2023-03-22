# Intro

This repository holds the Built In Self Test (BIST) for the Talons. It provides the source code to run the BIST, the bitstream to program, and a script that manages the BIST start, stop, and delay on the target system.

<div align="center">
![BIST Deploymeny Architecture](images/bist_arch.jpg)<br>
Figure 1. BIST Deployment Architecture</div><br>

## How to Use

The BIST is depoloyed through the CAR (central Artifect Repository). The package grabbed from CAR mirros the file system of the target talon boards. This has been done to simplify the process of deplyoment, because once the tar.gz package is unpacked at root, all the necessary files and scripts would be placed at the correct location, granted the structure of this repository was set correctly.

For example a given package `bist_archive.tar.gz` could be unpacked at root:
>tar -xvzf bist_archive.tar.gz -C /

This would place the `bist` script at `/bin`. The user may then call this script to perform various actions.

### Available Actions

The idea is that the BIST will start automatically on each bootup to run a system diagnostic. However, a small delay is placed at before this service is started in case it is required to stop it from running. This delay is managed by `bist.timer` service and could be modified by the `bist` script.

The automatic startup is achived via the systemd service (unit files). The `bist.service` is triggered by `bist.timer`. The user may kill the BIST runner before it is triggered by `bist.timer` via the bist script.

Run the `bist` script (or `bist -h`) to view the available commands.

- "-s             Start the BIST systemd service"
- "-k             Kill the BIST systemd service immediately, aborting the BIST"
- "-r             Run the BIST"
- "-m <time>      Modify the BIST systemd start delay time by <time>"
- "-t             Show the current BIST systemd start delay time"
- "-h             Display the help message"
- "-v             Verify the BIST files are installed correctly"

The `-s` option installs the BIST runner service in systemd

The `-k` option kills and stops the BIST runner service 

The `-t` option shows the current set BIST start delay.

The `-m` option allows the user to modify the delay from within the target environment.
For example to set the start delay to 99 seconds after boot:
> bist -m 99

The `-v` option verifies that the bitstream files and the service files are placed (unpacked) at the correct location.

The `-r` option runs the bist. Note that the systemd `bist.service` uses this same script to run the BIST after the required bootup delay.

### TODOS
- [ ] Display the BIST output results
- [ ] Verify the python dependencies are installed on the target
- [ ] Allow overwrite of the installation path/binary/packages via the `install.sh` and a `CONFIG_FILE`
- [ ] Punblish the results of the BIST to influxdb
