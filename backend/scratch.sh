#! /bin/bash

# ========================= config parameters ==================================
if [ -z $CCC_DATABASE ]; then
    CCC_DATABASE="http://172.26.134.68:5984"
fi

if [ -z $CCC_DB_USER ]; then
    CCC_DB_USER="admin:admin"
fi

if [ -z $CCC_CONFIG_DB ]; then
    CCC_CONFIG_DB="config"
fi

if [ -z $CCC_TWITTER_DB ]; then
    CCC_TWITTER_DB="melbourne"
fi

echo $CCC_DATABASE/$CCC_TWITTER_DB/_design/aggr/_view/zone/
curl $CCC_DATABASE/$CCC_TWITTER_DB/_design/aggr/_view/zone/ --user $CCC_DB_USER \
    -G\
    --data-urlencode limit=10\
    --data-urlencode group=true\
    --data-urlencode reduce=true
