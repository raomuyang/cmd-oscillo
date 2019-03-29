
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
oscillo -c 'test: echo "">1.txt&&md5 1.txt' -o 1.png

```

* -c 代表将执行一个linux cmd 命令

* -o 结果输出文件

* 会在当前目录下生成一个log 文件。文本结构是json 格式. 数据结构如下
```
{
  "test": {
            "elapsed": 0.022143125534057617,  //总执行时间
            "cpu": [], 
            "memory": []
          }
}

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

