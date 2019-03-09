
# oscillo

Record the system load at the execution of the command line and display it graphically

![demo](https://raw.githubusercontent.com/raomuyang/cmd-oscillo/master/demo/metrix.log.png)

## Usage

```shell
pip install oscillo

oscillo -c </path/to/config-file.yml> [-g]
```

## Config file

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
