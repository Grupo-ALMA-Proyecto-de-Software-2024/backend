#!/bin/bash

# This script downloads files from specified URLs using wget or curl.
# It supports resuming interrupted downloads and allows parallel downloads.

# Configuration
export TIMEOUT_SECS=300
export MAX_RETRIES=3
export WAIT_SECS_BEFORE_RETRY=300
export CACHE_FILE="downloaded_files_cache.txt"
export DEBUG=false

# Parameters
TOTAL_SIZE="<<size>>"
LINKS_LIST=(
    "<<links>>"
)

# Initialize failed_downloads counter
export failed_downloads=0

# Trap CTRL-C to exit the script
trap "exit" INT

# Function to log commands if DEBUG is true
debug_log() {
    if [ "$DEBUG" = true ]; then
        echo "$@"
    fi
}
export -f debug_log

# Function to create cache file if it doesn't exist
create_cache_file() {
    if [ ! -f "${CACHE_FILE}" ]; then
        touch "${CACHE_FILE}"
        debug_log "Created cache file: ${CACHE_FILE}"
    fi
}
export -f create_cache_file

# Function to read cache
read_cache() {
    debug_log "Reading cache file: ${CACHE_FILE}"
    if [ -f "${CACHE_FILE}" ]; then
        cat "${CACHE_FILE}"
    fi
}
export -f read_cache

# Function to update cache
update_cache() {
    local file=$1
    echo "$file" >>"${CACHE_FILE}"
    debug_log "Updated cache file with: $file"
}
export -f update_cache

# Function to download a single file with retries
dl() {
    local file=$1
    local filename=$(basename "$file")
    local attempt_num=0

    debug_log "Checking if file $file is already downloaded"
    # Check if the file is already downloaded
    if grep -q "$file" "${CACHE_FILE}"; then
        echo "File $filename already downloaded. Skipping."
        return 0
    fi

    # Wait before starting to stagger the load
    sleep $((($RANDOM % 10) + 2))s

    # Determine download tool
    local tool_name=""
    local download_command=()
    if command -v "curl" >/dev/null 2>&1; then
        tool_name="curl"
        download_command=(curl -S -s -k -O -f --speed-limit 1 --speed-time ${TIMEOUT_SECS})
    elif command -v "wget" >/dev/null 2>&1; then
        tool_name="wget"
        download_command=(wget -c -q -nv --timeout=${TIMEOUT_SECS} --tries=1)
    fi

    if [ -z "$tool_name" ]; then
        echo "ERROR: No download tool found (wget or curl)."
        exit 1
    fi

    echo "Starting download of $filename"
    # Retry logic
    until [ ${attempt_num} -ge ${MAX_RETRIES} ]; do
        debug_log "Running command: ${download_command[@]} \"$file\""
        "${download_command[@]}" "$file"
        status=$?
        if [ ${status} -eq 0 ]; then
            echo "Successfully downloaded $filename"
            update_cache "$file"
            break
        else
            failed_downloads=1
            echo "Download $filename was interrupted with error code ${tool_name}/${status}"
            attempt_num=$((attempt_num + 1))
            if [ ${attempt_num} -ge ${MAX_RETRIES} ]; then
                echo "ERROR: Giving up on downloading $filename after ${MAX_RETRIES} attempts."
            else
                echo "Download $filename will automatically resume after ${WAIT_SECS_BEFORE_RETRY} seconds"
                sleep ${WAIT_SECS_BEFORE_RETRY}
                echo "Resuming download of $filename, attempt $((${attempt_num} + 1))"
            fi
        fi
    done
}
export -f dl

# Function to split files into long and short filenames
split_files_list() {
    export long_files=()
    export ok_files=()
    for nextfile in "${LINKS_LIST[@]}"; do
        local length=${#nextfile}
        if [[ $length -ge 251 ]]; then
            long_files+=("$nextfile")
        else
            ok_files+=("$nextfile")
        fi
    done
    debug_log "Split files into ok_files: ${ok_files[@]} and long_files: ${long_files[@]}"
}
export -f split_files_list

# Function to download files
download_files() {
    split_files_list
    debug_log "Downloading files in parallel"
    printf "%s\n" "${ok_files[@]}" | xargs -P5 -n1 bash -c 'dl "$@"' _
    for next_file in "${long_files[@]}"; do
        dl "${next_file}"
    done
}
export -f download_files

# Function to check if download tool is available
check_download_tool() {
    if ! (command -v "wget" >/dev/null 2>&1 || command -v "curl" >/dev/null 2>&1); then
        echo "ERROR: neither 'wget' nor 'curl' are available on your computer. Please install one of them."
        exit 1
    fi
    debug_log "Checked download tools: wget and curl"
}
export -f check_download_tool

# Function to print download info
print_download_info() {
    echo "Downloading the following files in up to 5 parallel streams. Total size is ${TOTAL_SIZE}."
    for file in "${LINKS_LIST[@]}"; do
        echo "$file"
    done
    echo "In case of errors each download will be automatically resumed up to 3 times after a 5 minute delay."
    echo "To manually resume interrupted downloads just re-run the script."
    echo "Your downloads will start shortly...."
}
export -f print_download_info

# Main script execution
check_download_tool
create_cache_file
print_download_info
download_files
echo "Done."
