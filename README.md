
## About The Project
This project is used to detect routing loops in the data plane



### Built With

The main dependencies of this project are as follows

* [Ubuntu 20.04](https://releases.ubuntu.com/20.04/)
* [Mininet](http://mininet.org/)
* [P4 Language](https://p4.org/)
* [P4Utils](https://github.com/nsg-ethz/p4-utils)

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
* Mininet
  ```
    git clone https://github.com/mininet/mininet
    cd mininet

    sudo PYTHON=python3 mininet/util/install.sh -n
  ```
* P4
  
  For Ubuntu 20.04 and Ubuntu 21.04 it can be installed as follows:
  ```
    . /etc/os-release
    echo "deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/home:p4lang.list
    curl -L "http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
    sudo apt-get update
    sudo apt install p4lang-p4c
  ```

* p4tuils
  ```
    git clone https://github.com/nsg-ethz/p4-utils.git
    cd p4-utils
    sudo ./install.sh
  ```

* install python3 Dependency package
  ```
    sudo pip3 install psutil networkx
  ```

## Introduction

#### Experiment Topology

```
                 
                   
                   +--+
            +------+s2+------+
            |      +--+      |
+--+      +-++              ++-+       +--+
|h1+------+s1|              |s4+-------+h2|
+--+      +-++              ++-+       +--+
            |                |
            |      +--+      |
            +------+s3+------+
                   +--+

         
```

### Usage

1. Clone the repo
   ```sh
   git clone https://gitee.com/lifengfan/p4-consisit.git
   cd p4-consist
   ```
2. 启动mininet
    ```sh
    sudo python3 network.py    
    ```
3. 在mininet环境中
   ```sh
   xterm h1 h2
   ```
4. h2
   ```sh
   python3 receive.py
   ```
5. h1
   ```sh
   python3 send.py --ip 10.0.4.3
   ```
6. bug注入
  * 破坏一致性
  ```sh
   # 将目的ip地址10.10.1.1的数据包的转发路径从 s1->s2->s4 恶意改为 s1->s3->s4,即更改交换机s1中对应的流表规则即可。
   simple_switch_CLI --thrift-port 9090 --thrift-ip 127.0.0.1 --pre SimplePreLAG
   table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 3 00:00:00:00:03:01 3