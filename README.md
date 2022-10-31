# CS4224v Project
Your implementation may be tested on a different cluster of machines. It is important that your
submitted README file clearly explains how to configure and run your implementation, and how
to compile and generate any required executable files.

## YCQL

### Python package
```
pip install pandas
```
### Configure
TODO
### Data
1. Copy project_files.zip to each server
```
scp -r SOURCE_PATH/project_files.zip cs4224v@xcndXX.comp.nus.edu.sg:/temp/cs4224v/
cd /temp/cs4224v/
unzip project_files.zip
```
Where XX is 45-49

2. Preprocess
Create folder at /temp/cs4224v/processed_files/data_files
```
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
```
cd /home/stuproj/cs4224v/cs4224v_project/shell
sh nodeX.sh
```
At cs4224v@xcnd45-49 run node1-5.sh execute transactions concurrently.
### Output
1. Client
```
python3 /home/stuproj/cs4224v/cs4224v_project/src/measurement.py
```
Output client.csv
