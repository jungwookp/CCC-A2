#! /bin/bash

# ========================= config parameters ==================================
if [ -z $CCC_DATABASE ]; then
    CCC_DATABASE="172.26.134.68:5984"
fi

if [ -z $CCC_DB_USER ]; then
    CCC_DB_USER="admin:admin"
fi

if [ -z $CCC_CONFIG_DB ]; then
    CCC_CONFIG_DB="config"
fi

db_addr=http://$CCC_DATABASE

ON_ZYS="true"

if [ -z $ON_ZYS ]; then
  # TEST DB EXISTS, if not try create config db
  exists=$(curl -s -I -o /dev/null -w "%{http_code}" $db_addr/$CCC_CONFIG_DB --user $CCC_DB_USER)
  if [ $exists -eq "404" ]; then
      echo "CONFIG_DB does not EXIST, try create new database: $CCC_CONFIG_DB on $CCC_DATABASE."
      ok=$(curl -X PUT -s -I -o /dev/null -w "%{http_code}" $db_addr/$CCC_CONFIG_DB --user $CCC_DB_USER)
      if [ $ok != "200" ]; then
          echo "Failed creating config db"
          exit 1
      fi
      echo "Successfully creating config db: $CCC_CONFIG_DB."
  else
      echo "CONFIG DB $CCC_CONFIG_DB exists."
  fi
fi

config_db_addr=http://$CCC_DB_USER@$CCC_DATABASE/$CCC_CONFIG_DB
config_file_id=backend0
echo $config_db_addr
echo $config_file_id

python3 ./main.py $config_db_addr $config_file_id
