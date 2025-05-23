#!/usr/bin/env bash

#-----------------------------------------------------------------------------
# AGE-PRO Data Download Script
# Generated by the AGE-PRO Data Archive <TODO: insert link>
#
# AGE-PRO - The ALMA Survey of Gas Evolution in PROtoplanetary Disks
#
# This script downloads ALMA data products from the AGE-PRO Large Program.
#
# Features:
# - Parallel downloads: Downloads multiple files simultaneously
# - Caching: Tracks downloaded files to avoid re-downloading
# - Automatic retries: Resumes interrupted downloads
# - Organized structure: Saves files in Region/Disk/Band/Molecule hierarchy
#
# Usage:
#   chmod +x download_script.sh
#   ./download_script.sh
#
# Requirements:
#   - Bash 4.0 or higher
#   - curl or wget
#
# For more information about AGE-PRO data, visit: <TODO: insert link>
#-----------------------------------------------------------------------------

# Check for Bash version 4.0 or higher
if [ "${BASH_VERSINFO[0]}" -lt 4 ]; then
    echo "Error: This script requires Bash 4.0 or higher."
    echo "You are currently using Bash ${BASH_VERSION}"
    echo ""
    echo "To install a newer version on macOS:"
    echo "  1. Install Homebrew if you don't have it already:"
    echo "     /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  2. Install a newer version of Bash:"
    echo "     brew install bash"
    echo "  3. Try running the script again"
    echo ""
    echo "On Linux:"
    echo "  Use your package manager to install a newer version of Bash."
    echo "  For example, on Ubuntu/Debian: sudo apt-get update && sudo apt-get install bash"
    echo ""
    echo "Troubleshooting:"
    echo "  If you still see this message after installing a newer version of Bash, you may need to:"
    echo "  - Use the full path to run the script: /usr/local/bin/bash $0"
    echo "    (or on Apple Silicon Macs: /opt/homebrew/bin/bash $0)"
    echo "  - Or set the new Bash as your default shell:"
    echo "    1. Add to /etc/shells: echo \"/usr/local/bin/bash\" | sudo tee -a /etc/shells"
    echo "    2. Change default shell: chsh -s /usr/local/bin/bash"
    echo "    3. Restart your terminal"
    echo ""
    exit 1
fi

# This script downloads files from specified URLs using wget or curl.
# It supports resuming interrupted downloads and allows parallel downloads.

# Configuration
export TIMEOUT_SECS=300
export MAX_RETRIES=3
export WAIT_SECS_BEFORE_RETRY=300
export MAX_PARALLEL_DOWNLOADS=5
export CACHE_FILE="downloaded_files_cache.txt"
export DEBUG=false

# Parameters
TOTAL_SIZE="<<size>>"
declare -A LINKS_TO_TARGETS
"<<url_to_dir_mapping>>"

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

# Function to update cache
update_cache() {
    local file=$1
    echo "$file" >>"${CACHE_FILE}"
    debug_log "Updated cache file with: $file"
}
export -f update_cache

# Function to download a single file with retries
download() {
    local file=$1
    local filename=$(basename "$file")
    local target_dir="${LINKS_TO_TARGETS["$file"]}"
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
            echo "--Successfully downloaded $filename"

            debug_log "Moving $filename to $target_dir"
            mv "$filename" "$target_dir"

            debug_log "Updating cache with $file"
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
export -f download

# Function to limit the number of concurrent jobs
limit_jobs() {
    while [ "$(jobs | wc -l)" -ge "${MAX_PARALLEL_DOWNLOADS}" ]; do
        sleep 1
    done
}
export -f limit_jobs

# Function to download files
download_files() {
    debug_log "Downloading files in parallel"

    # Download files in parallel with job control
    for nextfile in "${!LINKS_TO_TARGETS[@]}"; do
        limit_jobs
        (
            download "$nextfile"
        ) &
    done

    # Wait for all background jobs to complete
    wait
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

# Function to create directories following the region/disk/band/molecule structure
create_directories() {
    for dir in "${LINKS_TO_TARGETS[@]}"; do
        mkdir -p "$dir"
    done
}
export -f create_directories

# Function to print download info
print_download_info() {
    echo "Downloading the following files in up to 5 parallel streams. Total size is ${TOTAL_SIZE}."
    for url in "${!LINKS_TO_TARGETS[@]}"; do
        echo "$url"
    done
    echo "In case of errors each download will be automatically resumed up to 3 times after a 5 minute delay."
    echo "To manually resume interrupted downloads just re-run the script."
    echo "Your downloads will start shortly...."
}
export -f print_download_info

# Main script execution
check_download_tool
create_cache_file

echo "Creating directories..."
create_directories

print_download_info
download_files

echo "Download script execution completed."
