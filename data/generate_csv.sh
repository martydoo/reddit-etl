#! /bin/bash

# Configure correct relative path
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $PARENT_PATH

DB_PATH="reddit.db"
OUTPUT_PATH="output/output-$(date +"%Y-%m-%d_%H-%M-%S").csv"

# Run all commands until end of doc
sqlite3 $DB_PATH <<EOD

.mode csv
.output $OUTPUT_PATH

SELECT * FROM posts;

.output stdout
.exit

EOD
