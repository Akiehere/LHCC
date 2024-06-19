# LHCC NS-3 simulator

## HPCC
It is based on NS-3 version 3.17.

### Quick Start

#### Build
`./waf configure`

Please note if gcc version > 5, compilation will fail due to some ns3 code style.  If this what you encounter, please use:

`CC='gcc-5' CXX='g++-5' ./waf configure`

#### Experiment config
Please see `mix/config.txt` for example. 

`mix/config_doc.txt` is a explanation of the example (texts in {..} are explanations).

`mix/fat.txt` is the topology used in HPCC paper's evaluation, and also in PINT paper's HPCC-PINT evaluation.

#### Run
The direct command to run is:
`./waf --run 'scratch/third mix/1/config.txt' >mix/1/log.txt`


### add or modify for LHCC 

/simulation/src/network/utils/int-header.h
/simulation/src/network/utils/custom-header.h
/simulation/src/point-to-point/model/NT-header.h
/simulation/src/point-to-point/model/qbb-net-device.h
/simulation/src/point-to-point/model/rdma-hw.h
/simulation/src/point-to-point/model/rdma-queue-pair.h
/simulation/src/point-to-point/model/switch-node.h


### run
 
python start.py <folder>

python start.py 1 -> /mix/1