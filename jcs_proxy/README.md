# JCS Proxy 部署 (step by step)

## 整体思路

JCS Proxy 依赖以下组件：

- Python 2.7 和一些第三方包
- [Elasticsearch-6.1.1][1]
- [Zookeeper-3.4.11][2]
- JDK 1.8

下面是详细部署步骤。

## 准备工作

金山分配给我们的虚拟机只有 root 用户，为了防止误操作，我们先向 wheel 组添加一个用户 `cloudfs`，后续的所有操作都由这个用户来执行。

```shell
# 添加用户
$ adduser cloudfs

# 设置密码
$ passwd cloudfs

# 加入 wheel 组，获取 sudo 权限
$ usermod -aG wheel cloudfs
```

为了方便，设置 cloudfs 执行 sudo 命令无需输入密码

```shell
$ visudo
```

然后在文件末尾插入以下内容：

```
cloudfs ALL=(ALL) NOPASSWD: ALL
```

切换至 `cloudfs` 用户

```shell
$ su cloudfs
```

然后将工程拷贝至该用户的主目录下，此时主目录下的结构为：

```txt
/home/cloudfs
├── jcs_portal
├── jcs_proxy
└── requirements.txt
```

## Python 2.7 及依赖包

金山的机器预装了 Python 2.7，但没有安装 pip。

```shell
# 安装 pip
$ sudo yum install python-pip

# 更新至最新
$ sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U

# 更换国内镜像
$ sudo pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

然后安装虚拟环境 virtualenv

```shell
$ sudo pip install virtualenv
```

配置虚拟环境

```shell
# 进入用户主目录
$ cd ~

# 创建名为 env 的虚拟环境
$ virtualenv env

# 激活虚拟环境
$ source env/bin/activate

# 为虚拟环境中的 pip 替换源
$ pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

然后在虚拟环境中安装依赖包，依赖包保存在 requirments.txt 中

```shell
# 首先安装 python-devel，否则下一步会出错
$ sudo yum install python-devel

# 安装依赖包
$ pip install -r requirments.txt
```

此时主目录结构如下：

```txt
/home/cloudfs
├── env
├── jcs_portal
├── jcs_proxy
└── requirments.txt
```

## JDK 1.8 / Zookeeper / ElasticSearch

在用户主目录下新建 software 文件夹

```shell
$ mkdir software
```

将 jdk1.8, zookeeper 和 elasticsearch 的软件包下载到 software 文件夹下，然后分别解压

```shell
# 可以用 rsync 把软件包传过来
$ rsync -av ssh jdk-8u171-linux-x64.tar.gz cloudfs@your-ip-address-here:/home/cloudfs/software

$ cd software
$ tar -zxvf jdk-8u171-linux-x64.tar.gz
$ tar -zxvf elasticsearch-6.1.1.tar.gz
$ tar -zxvf zookeeper-3.4.11.tar.gz
```

配置 Java 环境变量，打开 `~/.bash_profile`，添加以下内容

```shell
JAVA_HOME=/home/cloudfs/software/jdk1.8.0_171
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$JAVA_HOME/bin
```

然后执行 `source` 命令使修改生效

```shell
$ source ~/.bash_profile

# 查看配置是否正确
$ java -version
```

接下来配置 ZooKeeper

```shell
$ cd ~/software/zookeeper-3.4.11/conf

# 复制一份默认配置文件
$ cp zoo_sample.cfg zoo.cfg
```

然后在配置文件 `zoo.cfg` 中增加以下内容

```cfg
# dataDir 是快照存放路径，dataLogDir 是日志存放路径
dataDir=/home/cloudfs/software/zookeeper-3.4.11/data
dataLogDir=/home/cloudfs/software/zookeeper-3.4.11/logs
# 下面的 1,2,3 是每个 zk 节点的编号，如果配置文件中含有以下配置，ZooKeeper 就会以集群模式启动
server.1=10.0.0.19:2888:3888
server.2=your-ip-address-here:2888:3888
server.3=10.0.0.4:2888:3888
```

在 dataDir 下新建 myid 文件，写入该节点的编号。ZooKeeper 在以集群模式启动时会在这个文件中读取自己的编号。

```shell
$ cd data
$ echo 1 > myid
```

其他两台机器的 ZooKeeper 配置文件相同，但 myid 文件需要按照配置文件分别写入不同的编号。

修改 ElasticSearch 的配置文件

```shell
$ cd ~/software/elasticsearch-6.1.1/config/
$ vim elasticsearch.yml
```

添加以下内容：

```yml
network.host: 0.0.0.0
http.port: 9200
transport.host: localhost
transport.tcp.port: 9300
```

## 修改项目配置

`jcs_proxy/config/configuration.py`

```py
# 修改 proxy server 的监听地址
SERVER = {
    "host": "your-ip-address-here",
    "port": 8888,
}

CONFIG = {
    # 部署地域
    "jcsproxy_area": "aliyun-beijing",
    # 修改 zk 地址
    "zk_host": "your-ip-address-here",
    "zk_port": "2181",
    # 下面是 zk 内部数据的存储位置，无需修改
    "zk_user_info_path": "/JCS-Proxy/metadata/user_info",
    "zk_file_info_path": "/JCS-Proxy/metadata/file_info",
    "zk_file_statistics_path": "/JCS-Proxy/metadata/statistics",
    "zk_cloud_bucket_info_path": "/JCS-Proxy/metadata/cloud_bucket_info",
    "test_file_path": "/storage/ivic/jc/jcsproxy_dir/test_file",
    "data_recovery_path": "/storage/ivic/jc/jcsproxy_dir/recovery",
    # program_path 修改为 jcs_proxy 的绝对路径
    "program_path": "/home/cloudfs/jcs_proxy",
}
```

`jcs_proxy/config/cloud_config.py`

**重要**：修改这个文件中的 cloud_bucket_list 时有以下几点需要注意：

- cloud_name 相同的 bucket 共用账户信息，如果是新的 cloud_name 则需要在 cloud_account_list 中添加账户信息
- 同理，所添加的 bucket 拥有新的 cloud_name 时还要更新 cloud_price_list
- 需要在 `jcs_proxy/optimizer/latency_time_aliyun-beijing.json` 中添加该 bucket 的信息
- 需要在 `jcs_portal/index.py` 中添加该 bucket 的信息

## 启动服务

启动 ZooKeeper

```shell
$ cd /home/cloudfs/software/zookeeper-3.4.11
$ bin/zkServer.sh start
```

启动 ElasticSearch

```shell
$ cd /home/cloudfs/software/elasticsearch-6.1.1
$ ./bin/elasticsearch
```

运行 JCS Proxy

```shell
$ cd /home/cloudfs

# 先进入虚拟环境
$ source env/bin/activate

# 运行前先确认工程文件中配置的 ip 地址已经被替换为当前机器的 ip 地址
$ python jcs_proxy/run.py
```

[1]: https://www.ibm.com/developerworks/cn/opensource/os-cn-elk-filebeat/index.html
[2]: http://zookeeper.apache.org/doc/r3.4.3/zookeeperStarted.html#sc_InstallingSingleMode