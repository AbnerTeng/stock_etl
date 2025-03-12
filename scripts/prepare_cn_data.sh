#!/bin/bash

# Get the download date from command line argument
DOWNLOAD_DATE=$1

# Check if date parameter was provided
if [ -z "$DOWNLOAD_DATE" ]; then
    echo "Error: No date provided. Usage: $0 YYYY-MM-DD"
    exit 1
fi

# Set target directory
TARGET_DIR=~/.qlib/qlib_data/cn_data

# Create target directory if it doesn't exist
mkdir -p $TARGET_DIR

echo "Downloading data for date: $DOWNLOAD_DATE"

# Download the file
wget -q --show-progress "https://github.com/chenditc/investment_data/releases/download/${DOWNLOAD_DATE}/qlib_bin.tar.gz"

# Extract the file
echo "Extracting data to $TARGET_DIR"
tar -zxf qlib_bin.tar.gz -C $TARGET_DIR --strip-components=1

# Clean up
rm qlib_bin.tar.gz

echo "Data preparation completed successfully."