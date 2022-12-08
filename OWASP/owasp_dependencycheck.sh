#!/bin/sh

DC_VERSION="latest"

DC_DIRECTORY=$HOME/OWASP-Dependency-Check

DC_PROJECT="dependency-check scan:$(pwd)"

DATA_DIRECTORY="$DC_DIRECTORY/data"

REPORT_DIRECTORY="$DC_DIRECTORY/reports"

SCAN_PATH=$1

if [ ! -d "$DATA_DIRECTORY" ]; then

    echo "Initially creating persistent directory: $DATA_DIRECTORY"

    mkdir -p "$DATA_DIRECTORY"

    chmod -R 777 "$DATA_DIRECTORY"

fi

if [ ! -d "$REPORT_DIRECTORY" ]; then

    echo "Initially creating persistent directory: $REPORT_DIRECTORY"

    mkdir -p "$REPORT_DIRECTORY"

    chmod -R 777 "$REPORT_DIRECTORY"

fi

# Make sure we are using the latest version

docker pull owasp/dependency-check:$DC_VERSION

docker run --rm -e user=$USER -u $(id -u ${USER}):$(id -g ${USER}) --volume $(pwd):/src --volume "$DATA_DIRECTORY":/usr/share/dependency-check/data --volume "$REPORT_DIRECTORY":/report --volume "$SCAN_PATH:/usr/owasp_source" owasp/dependency-check --scan /usr/owasp_source --format ALL --project "$DC_PROJECT" --out /report

    # Use suppression like this: (where /src == $pwd)

    # --suppression "/src/security/dependency-check-suppression.xml"
