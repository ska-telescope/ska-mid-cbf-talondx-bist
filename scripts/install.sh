#!/bin/bash

#this script will install the files from the local repo or CAR over network or on the mounted sd-card p2

LOCAL_PACKAGE_NAME="bist.tar.gz"
REPO_NAME="ska-mid-cbf-talondx-bist"

# color codes
RED='\033[0;31m' 
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

overwrite_package_name(){
    LOCAL_PACKAGE_NAME=$1
    echo -e "Overwriting default package name to: ${YELLOW}${LOCAL_PACKAGE_NAME}${NC}"
    return 0
}

generate_local_package(){
    echo "Generating local package..."
    #sanity check warning
    if [ -f $LOCAL_PACKAGE_NAME ]; then
        echo -e "${RED}Package $LOCAL_PACKAGE_NAME already exists. Overwriting...${NC}"
    fi
    # move to folder, generate the package and move back
    cd ./raw/$REPO_NAME/ && tar -cvzf $LOCAL_PACKAGE_NAME * && mv $LOCAL_PACKAGE_NAME ../../ && cd ../../
    return 0
}

get_package_from_car(){
    echo "Downloading package from CAR..."
    local car_version=$1
    local download_link="https://artefact.skatelescope.org/repository/raw-internal/${REPO_NAME}-${car_version}.tar.gz"
    echo -e "${YELLOW}$download_link${NC}"

    #concatenate the CAR version string and overwrite the local name
    local CAR_VERSION_STRING="${REPO_NAME}-${car_version}.tar.gz"

    overwrite_package_name ${CAR_VERSION_STRING}

    wget -O ${LOCAL_PACKAGE_NAME} $download_link
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR downloading package from CAR${NC}"
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
    
   local talon_board=$1
   echo "Pinging $talon_board..."
   talon_ping_status=$(ping -c $PING_ATTEMPTS $talon_board 2>&1)
   echo "$talon_ping_status"

   number_of_ping_packets_received=$(echo "$talon_ping_status" | grep "packets transmitted" | awk '{print $4}')

   echo ""
   echo "number_of_ping_packets_received: $number_of_ping_packets_received"

   if [ "$number_of_ping_packets_received" == "" ]; then
        echo "${RED}ERROR: Could not determine number_of_ping_packets_received.${NC}"
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
    #ping the talon board for sanity check
    local talon_board=$1
    pingTalon $talon_board

    if [ $? -ne "0" ]; then
        echo "$talon_board was unreachable. Aborting programming..."
        exit 1
    else
        #sanity check for file
        if [ -f $LOCAL_PACKAGE_NAME ]; then
            echo "copying file over network and unpacking through ssh"
            #copy the local file over via SCP
            scp $LOCAL_PACKAGE_NAME root@$talon_board:/home/root/packages
            #ssh in and unpack the package at root
            ssh root@$talon_board -n "tar -xvzf /home/root/packages/$LOCAL_PACKAGE_NAME -C /";
            exit 0
        else
            echo -e "${RED}ERROR, file $LOCAL_PACKAGE_NAME does not exist${NC}"
            exit 1
        fi
    fi
}

install_package_mounted(){
    # sanity check for sd-card p2 partition.
    # /home/root/packages should exist if partiton2 of the sdcard
    # is mounted correctly at the given address
    local sd_card_mount_path=$1

    if [ -d $sd_card_mount_path/home/root/packages ]; then
        echo "unpacking $LOCAL_PACKAGE_NAME at $sd_card_mount_path"

        #sanity check for file
        if [ -f $LOCAL_PACKAGE_NAME ]; then
            tar -xvzf $LOCAL_PACKAGE_NAME -C $sd_card_mount_path
            exit 0
        else
            echo -e "${RED}ERROR, file $LOCAL_PACKAGE_NAME does not exist.${NC}"
            exit 1
        fi

    else
        echo -e "${RED}Mount path is incorrect: $sd_card_mount_path${NC}"
        exit 2
    fi
}

usage() {
    echo "Usage:
    -g                  generate local package .tar.gz 
    -n <NAME.tar.gz>    set the name of the package to generate or install on target
    -s <TALON NUMBER>   install the package on target over network (SCP & SSH)
    -i <MOUNT PATH>     install the package on target when sd-card partition2 is mounted
    -c <CAR VERSION>    download the package from CAR, given the CAR version
    -h                  display usage
    "

    echo "\
    Genenate a local package with a given name and install it:
    ./scripts/install.sh -n bist_pkg.tar.gz -g -i /mnt/p2

    Grab the local package and install it at the mounted path of sd-card:
    ./scripts/install.sh -n bist_package.tar.gz -i /mnt/p2/

    Download the package version 0.1.0 from CAR and install it on talon1 over network:
    ./scripts/install.sh -c 0.1.0 -s talon1

    Generate the local package with a given name:
    ./scripts/install.sh -n my_file.tar.gz -g

    Download the package version 0.1.0 from CAR and install it at the mounted path:
    ./scripts/install.sh -c 0.1.0 -i /mnt/p2/

    Install a locally generated package to talon1 over network:
    ./scripts/install.sh -n bist_package.tar.gz -s talon1
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
            echo -e "${$RED}ERROR: -${OPTARG} requires an argument.${NC}"
            ;;
        *)
            usage
            ;;
    esac
done

# In case no options were passed
if [ $OPTIND -eq 1 ]; then usage; fi