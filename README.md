# CS4224v Project

## YCQL

### Python package
```
pip install pandas
```
### Configure
Our goal is to Create a 5-node cluster with replication factor of 3 in our 5 allocated servers: xcnd45-xcnd49.
1. Install the yugabyteDB in 5 servers under /temp/cs4224/ directory. Follow the link in https://docs.yugabyte.com/preview/quick-start/linux/
2. Configure the yugabyteDB in 5 servers. Follow the link in https://docs.yugabyte.com/preview/deploy/manual-deployment/
    1. Start YB-Masters in first 3 nodes following  https://docs.yugabyte.com/preview/deploy/manual-deployment/start-masters/. Our 5 machines' ip start from 192.168.51.8 to 192.168.51.12. We choose 192.168.51.8, 192.168.51.9, 192.168.51.10 as our master nodes, using the following config file.
    ```shell
    --master_addresses=192.168.51.8:7101,192.168.51.9:7101,192.168.51.10:7101
    --rpc_bind_addresses=192.168.51.8:7101
    --fs_data_dirs=/temp/cs4224v/yb-data1,/temp/cs4224v/yb-data2
    --placement_cloud=nus
    --placement_region=sg
    --placement_zone=sg
    --webserver_port=7001
    ```
    We change all the default ports used by yugabyteDB to the original ports plus 1 in order to avoid port collision. Note that the rpc_bind_addresses in the config file need to be changed as well for each server.
    Then we run 

        nohup ./bin/yb-master --flagfile ../master.conf >& /temp/cs4224v/yb-master.out &
    
    2. Start YB-TServers in five nodes following  https://docs.yugabyte.com/preview/deploy/manual-deployment/start-tservers/

    We create the following config file for the tserver.
    ```
    --tserver_master_addrs=192.168.51.8:7101,192.168.51.9:7101,192.168.51.10:7101
    --rpc_bind_addresses=192.168.51.8:9101
    --enable_ysql
    --pgsql_proxy_bind_address=192.168.51.8:5434
    --cql_proxy_bind_address=192.168.51.8:9043
    --fs_data_dirs=/temp/cs4224v/yb-data1,/temp/cs4224v/yb-data2
    --placement_cloud=nus
    --placement_region=sg
    --placement_zone=sg
    --redis_proxy_bind_address=192.168.51.8:6380
    --webserver_port=9001
    --pgsql_proxy_webserver_port=13001
    --cql_proxy_webserver_port=12001
    --redis_proxy_webserver_port=11001
    ```
    Noted: 5 server's config file's ip need to be changed to the current server's IP.
    And then we run 

        nohup ./bin/yb-tserver --flagfile  ../tserver.conf >& /temp/cs4224v/yb-tserver.out &

    Then the yugabyteDB cluster is set up successfully in our machines.
    We can use `./bin/yb-admin \
--master_addresses 192.168.51.8:7101,192.168.51.9:7101,192.168.51.10:7101 \
list_all_masters ` to check the status and use `./bin/ycqlsh 192.168.51.10 9043` to connect to ycql client.

### Data
1. Copy project_files.zip to each server
    ```
    scp -r SOURCE_PATH/project_files.zip cs4224v@xcndXX.comp.nus.edu.sg:/temp/cs4224v/
    cd /temp/cs4224v/
    unzip project_files.zip
    ```
    Where XX is 45-49

2. Preprocess
    
    Create folder at /temp/cs4224v/processed_data
    ```
    mkdir /temp/cs4224v/processed_data
    python3 /home/stuproj/cs4224v/cs4224v_project/src/preprocess.py
    ```
3. Load
    ```
    cd /temp/cs4224v/yugabyte-2.15.2.1
    ./bin/ycqlsh 192.168.51.8 9043
    ```
    In YCQL run:
    ```
    SOURCE '/home/stuproj/cs4224v/cs4224v_project/load_cql.cql';
    ```
### Run Transactions
First, create folder at /home/stuproj/cs4224v/cs4224v_project/output, and /home/stuproj/cs4224v/cs4224v_project/output/measurement.
```
mkdir /home/stuproj/cs4224v/cs4224v_project/output
mkdir /home/stuproj/cs4224v/cs4224v_project/output/measurement
```
Then, run transactions by shell scripts. At cs4224v@xcnd45-49 run node1-5.sh execute transactions concurrently.
```
cd /home/stuproj/cs4224v/cs4224v_project/shell
sh nodeX.sh
```

### Output

```
python3 /home/stuproj/cs4224v/cs4224v_project/src/measurement.py
```
Output client.csv, throuput.csv, dbstate.csv.
