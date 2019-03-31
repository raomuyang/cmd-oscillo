
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


### 通过命令行参数启动 / Boot start by command line parameter

命令行参数的格式是 `"<name>: <command [args]>"`：

* `name`: 命令行的别名/id (任意字符串)，当`--commands/-c`参数指定多个命令时，该值将作为命令的唯一标识，不可重复
* `command [args]`: 需要测试资源消耗的命令，比如 `gzip file.ext`

示例如下，监控gzip压缩一个文件时耗费的cpu、memory和时间：
 
``` 
oscillo -c 'gzip: gzip file.ext' -o output-file
```

* -c 代表将执行一个linux cmd 命令。参数后面可以跟以空格隔开的多个参数

* -o 结果输出文件:

命令执行完成后，会在当前目录下生成一个`<output-file>.log` 文件。文本结构是json 格式. 数据结构如下
```
{
  "test": {
            "elapsed": 0.022143125534057617,  //总执行时间
            "cpu": [], 
            "memory": []
          }
}

```
同时会产生一个`<output-file>.png`文件，`<output-file>`由`-o`参数指定，默认值为`metrix`

如果想对比多个命令对资源的消耗，可以使用 `-c/--commands` 选项指定多条命令, e.g.:

对比`gzip`和`tar`命令对资源的消耗：

```shell
oscillo -c 't1: gzip file.ext'  't2: tar czf target.tar.gz file1' -o output
```

在控制台上，`oscillo`会打印summary信息，其中包含命令的耗时、最大内存使用、最大cpu使用、退出码等，效果如下：

![demo](https://raw.githubusercontent.com/raomuyang/cmd-oscillo/master/demo/metrix.log.png)

![demo](https://raw.githubusercontent.com/raomuyang/cmd-oscillo/master/demo/compare-gzip.png)

### 通过配置文件启动 / Boot start by config file

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

