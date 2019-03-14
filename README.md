
# oscillo

记录命令执行过程中对系统产生的负载，以图片的形式展现出来

Record the system load at the execution of the command line and display it graphically

![demo](https://raw.githubusercontent.com/raomuyang/cmd-oscillo/master/demo/metrix.log.png)

![demo](https://raw.githubusercontent.com/raomuyang/cmd-oscillo/master/demo/cli.png)

## 安装方式 / Installation
* Install from pypi
```shell
pip install oscillo
```

* Install from local
```shell
python setup.py install
```


## 使用方式 / Usage


* 通过命令行参数启动 / Boot start by command line parameter

``` 
oscillo -c 'test-md5:md5 ~/TmpFiles/CL100006359_L01_2_1.fq.gz' 'gz-test: gz  ~/big.bin' -o summary-file

```

* 通过配置文件启动 / Boot start by config file

当命令很长或者很多时，可以使用配置文件启动
Whe the commands is too many, you can boot start by config file

```shell
oscillo --config </path/to/config-file.yml> [-g]
```

## 配置文件模板 / Config file



The command line in commands will be executed in order

```yml
# Demo
commands:
  -
    name: gzip
    cmd: gzip big-file
  
  -
    name: tar
    cmd: tar -zcf tmp.tar.gz big-file

output: gzip-and-tar-gz
```
