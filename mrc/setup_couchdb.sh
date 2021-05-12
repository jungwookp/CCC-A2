#!/usr/bin/bash

export declare -a nodes=('aurin' 'processed_tw' 'raw_tw')
export declare -a ports=(5984 5985 5986)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export masterport=`echo ${ports} | cut -f1 -d' '`
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export declare -a otherports=`echo ${ports[@]} | sed s/${masterport}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'

for i in ${!nodes[@]};do
    sudo docker create\
      --name couchdb${nodes[$i]}\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${nodes[$i]}\""\
      --publish ${ports[$i]}:5984\
      ibmcom/couchdb3:${VERSION}
done

declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

for cont in "${conts[@]}"; do sudo docker start ${cont}; done

for port in ${otherports}; 
do
    curl -XPOST "http://${user}:${pass}@localhost:${masterport}/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"${port}\",\
             \"remote_node\": \"localhost\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

for node in ${othernodes}; 
do
    curl -X PUT "http://admin:admin@localhost:${masterport}/_node/_local/_nodes/couchdb@${node}" -d {}
done
