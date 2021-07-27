#!/bin/sh


TARGET=$1
ENVIRONMENT=$2

TARGET_DIR="./tdrs-$TARGET"
REPORT_NAME=owasp_report.html
REPORTS_DIR="tdrs-$target/reports"
REPORT_PATH="$REPORTS_DIR/$REPORT_NAME"

cd $TARGET_DIR


if [ "$ENVIRONMENT" = "nightly" ]; then

    CONFIG_FILE="$REPORTS_DIR/zap.conf"
    APP_URL="https://tdp-$TARGET-staging.app.cloud.gov/"

elif [ "$ENVIRONMENT" = "circle" ]; then

    CONFIG_FILE="$REPORTS_DIR/zap.conf"
    APP_URL="http://tdp-$TARGET/"

else
    APP_URL="http://tdp-$TARGET/"
fi

if command -v sha256sum >/dev/null ; then
	SHASUM=sha256sum
elif command -v shasum >/dev/null ; then
	SHASUM=shasum
fi

docker-compose down
docker-compose up -d --build

# do an OWASP ZAP scan
export ZAP_CONFIG=" \
  -config globalexcludeurl.url_list.url\(0\).regex='.*/robots\.txt.*' \
  -config globalexcludeurl.url_list.url\(0\).description='Exclude robots.txt' \
  -config globalexcludeurl.url_list.url\(0\).enabled=true \
  -config spider.postform=true"

echo "================== OWASP ZAP tests =================="
# Ensure the reports directory can be written to
chmod 777 $REPORT_PATH

if [ -z ${CONFIG_FILE+x} ]; then
    echo "Config file $ENVIRONMENT"
    docker-compose run zaproxy zap-full-scan.py \
                   -t $APP_URL \
                   -m 5 \
                   -z "${ZAP_CONFIG}" \
                   -c "$CONFIG_FILE" \
                   -r  "$REPORT_PATH"  | tee /dev/tty | grep -q "FAIL-NEW: 0"
else

    echo "No config file"
    docker-compose run zaproxy zap-full-scan.py \
                   -t $APP_URL \
                   -m 5 \
                   -z "${ZAP_CONFIG}" \
                   -r "$REPORT_PATH" | tee /dev/tty | grep -q "FAIL-NEW: 0"
fi


# The `grep -q` piped to the end of the previous command will return a
# 0 exit code if the term is found and 1 otherwise.
ZAPEXIT=$?

docker-compose down --remove-orphan

EXIT=0

if [ "$ZAPEXIT" = 1 ] ; then
	echo "OWASP ZAP scan failed"
	EXIT=1
fi

exit $EXIT
