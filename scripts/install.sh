#!/bin/sh

#this script will install the files from the local repo or CAR

LOCAL_PACKAGE_NAME="bist.tar.gz"
REPO_NAME="ska-mid-cbf-talondx-bist"

# color codes
RED='\033[0;31m' 
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

overwrite_package_name(){
    LOCAL_PACKAGE_NAME=$1
    echo -e "overwriting default package name to: ${YELLOW}${LOCAL_PACKAGE_NAME}${NC}"
    return 0
}

generate_local_package(){
    cd ./raw/$REPO_NAME/ && tar -cvzf $LOCAL_PACKAGE_NAME * && mv $LOCAL_PACKAGE_NAME ../../
    return 0
}

get_package_from_car(){
    local car_version=$1
    local download_link="https://artefact.skatelescope.org/repository/raw-internal/${REPO_NAME}-${car_version}.tar.gz"
    echo -e "${YELLOW}$download_link${NC}"

    #concatenate the CAR version string and overwrite the local name
    local CAR_VERSION_STRING="${REPO_NAME}-${car_version}.tar.gz"

    overwrite_package_name ${CAR_VERSION_STRING}

    wget -O ${LOCAL_PACKAGE_NAME} $download_link
    if [ $? -ne 0 ]; then
        echo "error downloading package from CAR"
        #remove the empty zombie file
        rm $CAR_VERSION_STRING
        exit 1
    fi
    return 0
}

PING_ATTEMPTS=5
PING_ECHOES_NEEDED_FOR_SUCCESS=1

# Ping Talon Boards
pingTalon(){
    
   talon=$1
   echo "Pinging $talon..."
   talon_ping_status=$(ping -c $PING_ATTEMPTS $talon 2>&1)
   echo "$talon_ping_status"

   number_of_ping_packets_received=$(echo "$talon_ping_status" | grep "packets transmitted" | awk '{print $4}')

   echo ""
   echo "number_of_ping_packets_received: $number_of_ping_packets_received"

   if [ "$number_of_ping_packets_received" == "" ]; then
        echo "ERROR: Could not determine number_of_ping_packets_received."
        return "1"
   fi

   if [ "$number_of_ping_packets_received" -lt "$PING_ECHOES_NEEDED_FOR_SUCCESS" ]; then
        echo "Received $number_of_ping_packets_received/$PING_ATTEMPTS packets. Talon not pingable."
        return "1"
   else
        echo "Received $number_of_ping_packets_received/$PING_ATTEMPTS packets. Talon pingable."
        return "0"
   fi
}

install_package_scp(){
    #ping the talon board for sanity
    pingTalon $talon
    if [ $? -ne "0" ]; then
        echo "$talon was unreachable. Aborting programming..."
        exit 1
    else
        #sanity check for file
        if [ -f $LOCAL_PACKAGE_NAME ]; then
            echo "copying file over network and unpacking through ssh"
            #copy the local file over via SCP
            scp $LOCAL_PACKAGE_NAME root@$talon:/home/root/packages
            #ssh in and unpack the package at root
            ssh root@$talon -n "tar -xvzf /home/root/packages/$LOCAL_PACKAGE_NAME -C /";
            exit 0
        else
            echo "error, file $LOCAL_PACKAGE_NAME does not exist"
            exit 1
        fi
    fi
}

install_package_mounted(){
    # sanity check for sd-card p2 partition.
    # /home/root/packages should exist if partiton2 of the sdcard
    # is mounted correctly at the given address
    local sd_card_mount_path=$1
    echo "$sd_card_mount_path"

    if [ -d $sd_card_mount_path/home/root/packages ]; then
        echo "unpacking $LOCAL_PACKAGE_NAME at $sd_card_mount_path"

        #sanity check for file
        if [ -f LOCAL_PACKAGE_NAME ]; then
            #tar -xvzf $LOCAL_PACKAGE_NAME -C $sd_card_mount_path
            exit 0
        else
            echo "error, file $LOCAL_PACKAGE_NAME does not exist"
            exit 1
        fi

    else
        echo "mount path is incorrect!"
        exit 2
    fi
}

usage() {
    echo "Usage:"
    echo "
    -g                  generate local package .tar.gz 
    -n <NAME.tar.gz>    set the name of the package to generate or install on target
    -s <TALON NUMBER>   install the package at target over network (SCP)
    -i <MOUNT PATH>     install the package on target when 
    -c <CAR VERSION>    download the package from CAR, given the CAR version
    -h                  display usage
    "

    echo "
    ./scripts/install.sh -n bist_package.tar.gz -i /mnt/p2/
    ./scripts/install.sh -i 0.1.0 -s talon1
    ./scripts/install.sh -n my_file.tar.gz -g
    "
}

while getopts ":hgc:i:s:n:" arg; do
    case $arg in
        n)
            pkg_name=${OPTARG}
            overwrite_package_name $pkg_name
            ;;
        g)
            generate_local_package
            ;;
        c)
            car_version=${OPTARG}
            get_package_from_car $car_version
            ;;
        i)
            mount_path=${OPTARG}
            install_package_mounted $mount_path
            ;;
        s)  
            talon_board=${OPTARG}
            install_package_scp $talon_board
            ;;
        h)
            usage
            ;;
        :)
            echo -e "Error: -${OPTARG} requires an argument."
            ;;
        *)
            usage
            ;;
    esac
done

# In case no options were passed
if [ $OPTIND -eq 1 ]; then usage; fi