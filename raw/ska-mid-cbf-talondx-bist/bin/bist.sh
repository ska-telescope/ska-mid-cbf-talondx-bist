#!/bin/sh

usage() {
    echo "Usage:"
    echo "-s             Start the BIST systemd service and extract tar file"
    echo "-k             Kill the BIST systemd service immediately, aborting the BIST"
    echo "-r             Run the BIST"
    echo "-m <time>      Modify the BIST systemd start delay time by <time>"
    echo "-t             Show the current BIST systemd start delay time"
    echo "-p             Program the BIST bitstream"
    echo "-x             Extract the tar file at predefined location"
    echo "-f             Publish the results (.csv) of the BIST to influxdb"
    echo "-c             Print the results (.txt) of the BIST"
    echo "-h             Display the help message"
    echo "-v             Verify the BIST files are installed correctly"
}

# path of the BIST source files
BIST_SRC_PATH="/home/root/packages/bist"
# list of BIST source files
BIST_SRC_FILES="talon_dx-tdc_base-tdc_bist.tar.gz tdc.ipmap"
# path of the BIST systemd service
BIST_SERVICE_PATH="/etc/systemd/system"
# list of systemd service files
BIST_SERVICE_FILES="bist.service bist.timer"
# path of the BIST bitstream archive
BIST_ARCHIVE=$BIST_SRC_PATH/talon_dx-tdc_base-tdc_bist.tar.gz
# path of the BIST bitstream for programming to trigger the overlay
BIST_BITSTREAM_PATH="/sys/kernel/config/device-tree/overlays"
# path of the BIST bitstream package is extracted
BIST_ARCHIVE_PATH=$BIST_SRC_PATH/extract_dir

verify_bist_service_files() {
    # verify that the required systemd service files are placed at right location
    local res=0
    local verbosity=$1
    for file in $BIST_SERVICE_FILES; do
        if ! [ -f $BIST_SERVICE_PATH/$file ]; then
            if [ $verbosity ]; then
                echo "$BIST_SERVICE_PATH/$file not found at $BIST_SERVICE_PATH"
            fi
            res=1
        fi
    done
    return $res
}

verify_bist_bitstream_files() {
    # verify that the required bitstream files are placed at right location
    local res=0
    local verbosity=$1
    for file in $BIST_SRC_FILES; do
        if ! [ -f $BIST_SRC_PATH/$file ]; then
            if [ $verbosity ]; then
                echo "$BIST_SRC_PATH/$file not found at $BIST_SRC_PATH"
            fi
            res=1
        fi
    done
    return $res
}

verify_bist_files() {
    # verify all bist files dependencies
    local verbosity=$1
    local res=0
    verify_bist_service_files $verbosity
    if [ $? -ne 0 ]; then
        res=1
    fi
    verify_bist_bitstream_files $verbosity
    if [ $? -ne 0 ]; then
        res=1
    fi
    return $res
}

verify_bist_service() {
    local res=$(systemctl is-active $BIST_SERVICE_PATH/bist.timer)
    echo $res
}

start_bist_service() {
    echo "Activating BIST service via systemd"
    systemctl enable $BIST_SERVICE_PATH/bist.timer
    return $?
}

stop_bist_service() {
    echo "Stopping BIST service via systemd"
    systemctl disable --now $BIST_SERVICE_PATH/bist.timer #disable and stop immediately
    return $?
}

extract_archive() { 
    # tar command on the Talon boards is from Busybox and 
    # has a limited set of command. tar options such as --get and --wildcards 
    # does not exist.
    echo "Extracting files from tar to $BIST_ARCHIVE_PATH"
    if [ -f $BIST_ARCHIVE ]; then

        # remove the output directory if it exists
        if [ -d "$BIST_ARCHIVE_PATH" ]; then
            echo "Deleting previous tar file output directory"
            rm -rf $BIST_ARCHIVE_PATH
        fi

        mkdir $BIST_ARCHIVE_PATH
        tar -xvzf $BIST_ARCHIVE -C $BIST_ARCHIVE_PATH

    else
        echo "$BIST_ARCHIVE not found, aborting..."
        exit 3
    fi
}

program_bist_bitstream() {

    echo "Programming the BIST bitstream..."
    # fetch the files
    bs_core=$(ls $BIST_ARCHIVE_PATH/*.rbf) 
    dtb=$(ls $BIST_ARCHIVE_PATH/*.dtb)
    # sanity check
    if [ -z "$dtb" ] || [ -z "$bs_core" ]; then
        echo ".dtb or .rbf file(s) missing. Aborting bitstream programming!"
        exit 3
    else 
        rmdir $BIST_BITSTREAM_PATH/*
        mkdir $BIST_BITSTREAM_PATH/base
        echo $BIST_ARCHIVE_PATH/$dtb > $BIST_BITSTREAM_PATH/base/path
        dmesg | tail -n 10
    fi
}

execute_bist() {
    echo "Executing BIST..."
    # fetch the files
    json=$(ls $BIST_SRC_PATH/extract_dir/*.json)
    ipmap=$(ls $BIST_SRC_PATH/*ipmap)
    # sanity check
    if [ -z "$json" ] || [ -z "$ipmap" ]; then
        echo "ipmap or json file(s) missing. Aborting BIST execution!"
        exit 1
    else
        python3 $BIST_SRC_PATH/src/run_bist_tests.py $BIST_ARCHIVE_PATH/$json $BIST_SRC_PATH/$ipmap
    fi
}

run_bist() {
    verify_bist_bitstream_files true
    local res=$?
    if [ $res -eq 0 ]; then
        program_bist_bitstream
        execute_bist
    fi
    return $res
}

get_bist_results() {
    # print the results of the BIST
    if [ -f $BIST_SRC_PATH/tdc_base_bist_logfile.txt ]; then
        echo $BIST_SRC_PATH/src/tdc_base_bist_logfile.txt
        return 0
    else
        echo "$BIST_SRC_PATH/src/tdc_base_bist_logfile.txt not found"
        exit 1
    fi
}

publish_bist_results_to_influxdb() {
    # publish the results to the influxdb. The python script that runs
    # the BIST is responsible for producing a valid .csv file
    if [ -f $BIST_SRC_PATH/src/tdc_base_bist_logfile.csv ]; then
        echo "Publishing $BIST_SRC_PATH/src/tdc_base_bist_logfile.csv to influxdb"
        influx write --bucket bist --file $BIST_SRC_PATH/src/tdc_base_bist_logfile.csv
        return 0
    else 
        echo "$BIST_SRC_PATH/src/tdc_base_bist_logfile.csv not found."
        exit 1
    fi
}

get_bist_start_delay() { 
    verify_bist_service_files true
    if [ $? -eq 0 ]; then
        local val=$(cat $BIST_SERVICE_PATH/bist.timer | grep seconds)
        echo $val
    fi
}

modify_bist_start_delay() {
    verify_bist_service_files true
    if [ $? -eq 0 ]; then
        echo "Setting the BIST start-up delay to ${1} seconds"
        sed -i "/OnBootSec=/c\OnBootSec=${1}seconds" $BIST_SERVICE_PATH/bist.timer
    else
        exit 1
    fi
}

while getopts ":hskrm:vtpxfc" arg; do
    case $arg in
        s)
            start_bist_service
            if [ $? -ne 0 ]; then
                echo "Error starting the BIST service"
                exit 5
            fi
            # also extract the bitstream
            extract_archive
            ;;
        k)
            stop_bist_service
            if [ $? -ne 0 ]; then
                echo "Error killing the BIST service"
                exit 4
            fi
            ;;
        r)
            run_bist
            ;;
        t)
            get_bist_start_delay
            ;;
        x)
            extract_archive
            ;;
        m)
            start_delay=${OPTARG}
            if [[ "$start_delay" =~ [^0-9] ]]; then #check if the argument passed is only digits
                echo "delay has to be a positive integer in seconds"
            else
                modify_bist_start_delay $start_delay
                get_bist_start_delay
            fi
            ;;
        v)
            verify_bist_files true
            if [ $? -ne 0 ]; then
                exit 1
            fi
            ;;
        p)
            program_bist_bitstream
            ;;
        c)
            get_bist_results
            ;;
        f)
            publish_bist_results_to_influxdb
            ;;
        h)
            usage
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument."
            ;;
        *)
            usage
            ;;
    esac
done

# In case no options were passed
if [ $OPTIND -eq 1 ]; then usage; fi