#!/bin/bash

# This script is heavily based off the ALMA archive download script.

# This script runs on Linux and MacOS and downloads all the selected files to the current working directory in up to 5 parallel download streams.
# Should a download be aborted just run the entire script again, as partial downloads will be resumed. Please play nice with the download systems
# at the ARCs and do not increase the number of parallel streams.

# connect / read timeout for wget / curl
export TIMEOUT_SECS=300
# how many times do we want to automatically resume an interrupted download?
export MAX_RETRIES=3
# after a timeout, before we retry, wait a bit. Maybe the servers were overloaded, or there was some scheduled downtime.
# with the default settings we have 15 minutes to bring the dataportal service back up.
export WAIT_SECS_BEFORE_RETRY=300
# total size of files to be downloaded
TOTAL_SIZE="<<size>>"
# the files to be downloaded
LIST=(
    "<<links>>"
)

# Cache file to keep track of downloaded files
export CACHE_FILE="downloaded_files_cache.txt"

# Debug mode
export DEBUG=false

# If we terminate the script using CTRL-C during parallel downloads, the remainder of the script is executed, asking if
# the user wants to unpack tar files. Not very nice. Exit the whole script when the user hits CTRL-C.
trap "exit" INT

export failed_downloads=0

# Function to log commands if DEBUG is true
function debug_log {
    if [ "$DEBUG" = true ]; then
        echo "$@"
    fi
}
export -f debug_log

# Function to create cache file if it doesn't exist
function create_cache_file {
    if [ ! -f "${CACHE_FILE}" ]; then
        touch "${CACHE_FILE}"
        debug_log "Created cache file: ${CACHE_FILE}"
    fi
}
export -f create_cache_file

# Function to read cache
function read_cache {
    debug_log "Reading cache file: ${CACHE_FILE}"
    if [ -f "${CACHE_FILE}" ]; then
        cat "${CACHE_FILE}"
    fi
}
export -f read_cache

# Function to update cache
function update_cache {
    local file=$1
    echo "$file" >>"${CACHE_FILE}"
    debug_log "Updated cache file with: $file"
}
export -f update_cache

# download a single file.
# attempt the download up to N times
function dl {
    local file=$1
    local filename=$(basename "$file")
    # the nth attempt to download a single file
    local attempt_num=0

    debug_log "Checking if file $file is already downloaded"
    # Check if the file is already downloaded
    if grep -q "$file" "${CACHE_FILE}"; then
        echo "File $filename already downloaded. Skipping."
        return 0
    fi

    # wait for some time before starting - this is to stagger the load on the server (download start-up is relatively expensive)
    sleep $((($RANDOM % 10) + 2))s

    if command -v "curl" >/dev/null 2>&1; then
        local tool_name="curl"
        local download_command=(curl -S -s -k -O -f --speed-limit 1 --speed-time ${TIMEOUT_SECS})
    elif command -v "wget" >/dev/null 2>&1; then
        local tool_name="wget"
        local download_command=(wget -c -q -nv --timeout=${TIMEOUT_SECS} --tries=1)
    fi

    debug_log "Starting download of $filename"
    # manually retry downloads.
    until [ ${attempt_num} -ge ${MAX_RETRIES} ]; do
        debug_log "Running command: ${download_command[@]} \"$file\""
        "${download_command[@]}" "$file"
        status=$?
        if [ ${status} -eq 0 ]; then
            echo "	    successfully downloaded $filename"
            update_cache "$file"
            break
        else
            failed_downloads=1
            echo "		download $filename was interrupted with error code ${tool_name}/${status}"
            attempt_num=$((${attempt_num} + 1))
            if [ ${attempt_num} -ge ${MAX_RETRIES} ]; then
                echo "	  ERROR giving up on downloading $filename after ${MAX_RETRIES} attempts  - rerun the script manually to retry."
            else
                echo "		download $filename will automatically resume after ${WAIT_SECS_BEFORE_RETRY} seconds"
                sleep ${WAIT_SECS_BEFORE_RETRY}
                echo "		resuming download of $filename, attempt $((${attempt_num} + 1))"
            fi
        fi
    done
}
export -f dl

# temporary workaround for ICT-13558: "xargs -I {}" fails on macos with variable substitution where the length of the variable
# is greater than 255 characters. For the moment we download these long filenames in serial. At some point I'll address this issue
# properly, allowing parallel downloads.
# Array of filenames for download where the filename > 251 characters
# 251? Yes. The argument passed to bash is "dl FILENAME;" In total it cannot exceed 255. So FILENAME can only be 251
export long_files=()
# array of filenames with length <= 255 characters - can be downloaded in parallel.
export ok_files=()
function split_files_list {
    for nextfile in "${LIST[@]}"; do
        length=${#nextfile}
        if [[ $length -ge 251 ]]; then
            long_files+=("$nextfile")
        else
            ok_files+=("$nextfile")
        fi
    done
    debug_log "Split files into ok_files: ${ok_files[@]} and long_files: ${long_files[@]}"
}
export -f split_files_list

function download_files {
    split_files_list
    debug_log "Downloading files in parallel"
    printf "%s\n" "${ok_files[@]}" | xargs -P5 -n1 bash -c 'dl "$@"' _
    for next_file in "${long_files[@]}"; do
        dl "${next_file}"
    done
}
export -f download_files

function check_download_tool {
    if ! (command -v "wget" >/dev/null 2>&1 || command -v "curl" >/dev/null 2>&1); then
        echo "ERROR: neither 'wget' nor 'curl' are available on your computer. Please install one of them."
        exit 1
    fi
    debug_log "Checked download tools: wget and curl"
}
export -f check_download_tool

function print_download_info {
    echo "Downloading the following files in up to 5 parallel streams. Total size is ${TOTAL_SIZE}."
    for file in "${LIST[@]}"; do
        echo "$file"
    done
    echo "In case of errors each download will be automatically resumed up to 3 times after a 5 minute delay"
    echo "To manually resume interrupted downloads just re-run the script."
    echo "Your downloads will start shortly...."
}
export -f print_download_info

# Main body
# ---------

check_download_tool
create_cache_file
print_download_info
download_files

echo "Done."
