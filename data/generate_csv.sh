#! /bin/bash

# Configure correct relative path
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )

# Airflow provides env variable, default to local path
DB_PATH=${DB_PATH:-"${PARENT_PATH}/reddit.db"}
OUTPUT_DIR="$(dirname "$DB_PATH")/output"
OUTPUT_FILE="${OUTPUT_DIR}/output-$(date +"%Y-%m-%d_%H-%M-%S").csv"

mkdir -p "$OUTPUT_DIR"

# Run all commands until end of doc
sqlite3 "$DB_PATH" <<EOD

.mode csv
.output $OUTPUT_FILE

SELECT * FROM posts;

.output stdout
.exit

EOD
