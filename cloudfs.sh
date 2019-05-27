#!/bin/sh

cd /home/cloudfs

case $1 in
startzk)
    echo "Starting ZK & ES ..."
    # zookeeper
    cd /home/cloudfs/software/zookeeper-3.4.11
    ./bin/zkServer.sh start
    # elasticsearch
    cd /home/cloudfs/software/elasticsearch-6.1.1
    echo Starting ElasticSearch ...
    nohup ./bin/elasticsearch > nohup.log 2>&1 &
    echo Done
    echo "ZK & ES STARTED"
    ;;
start)
    source env/bin/activate
    echo Starting Cloudfs ...
    # proxy
    cd /home/cloudfs/jcs_proxy
    echo Starting Proxy ...
    nohup python run.py > nohup.log 2>&1 &
    echo Done
    # portal_frontend
    cd /home/cloudfs/jcs_portal/frotend
    echo Starting Portal_frontend ...
    nohup npm run dev > /dev/null 2>&1 &
    echo Done
    # portal_backend
    cd /home/cloudfs/jcs_portal
    echo Starting Portal_backend ...
    nohup python index.py > nohup.log 2>&1 &
    echo Done
    echo Cloudfs STARTED
    ;;
stopzk)
    echo "Stopping ZK & ES ..."
    # zookeeper
    cd /home/cloudfs/software/zookeeper-3.4.11
    ./bin/zkServer.sh stop
    # elasticsearch
    cd /home/cloudfs/software/elasticsearch-6.1.1
    echo Stopping ElasticSearch ...
    ps -ef | grep elasticsearch | grep -v grep | awk '{print $2}' | xargs kill
    echo Done
    echo "ZK & ES STOPPED"
    ;;
stop)
    source env/bin/activate
    echo Stopping Cloudfs ...
    # proxy
    cd /home/cloudfs/jcs_proxy
    echo Stopping Proxy ...
    ps -ef | grep run.py | grep -v grep | awk '{print $2}' | xargs kill
    echo Done
    # portal_frontend
    cd /home/cloudfs/jcs_portal/frotend
    echo Stopping Portal_frontend ...
    ps -ef | grep npm | grep -v grep | awk '{print $2}' | xargs kill
    echo Done
    # portal_backend
    cd /home/cloudfs/jcs_portal
    echo Stopping Portal_backend ...
    ps -ef | grep index.py | grep -v grep | awk '{print $2}' | xargs kill
    echo Done
    echo Cloudfs STOPPED
    ;;
status)
    service=(zookeeper elasticsearch run.py npm index.py)
    for ((i=0; i<5; i++)); do
        flag=$(ps -ef | grep ${service[i]} | grep -v grep | wc -l)
        if [ $flag == 0 ]; then
            echo "`date +"%Y-%m-%d %H:%M:%S"` ${service[i]} is not running"
        else
            pid=$(pgrep -f ${service[i]})
            echo "`date +"%Y-%m-%d %H:%M:%S"` ${service[i]} is running with pid $pid"
        fi
    done
    ;;
*)
    echo "Usage: $0 {start|stop|startzk|stopzk|status}" >&2
esac

cd /home/cloudfs
