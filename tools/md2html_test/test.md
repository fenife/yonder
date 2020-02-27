
## 概述
我们知道，Python语法简单，但运行速度相对C、java等语言还是比较慢的；在CPU密集型程序中，
为了提高运行速度，有时候需要我们写Python的C扩展；
本文给出一个简单的Python调用C扩展的demo示例。

## 依赖
Python3
virtualenv    

## 流程
### 准备目录及环境
在个人工作目录下新建一个目录存放源文件，比如我的工作目录为：`/icode/learn/cpy/`，

进入工作目录：
cd /icode/learn/cpy/

新建目录：
mkdir demo

进入该目录，后续所有操作都在该目录进行：
cd demo

新起一个独立的Python运行环境：
virtualenv venv --python=python3

新建的Python环境放在当前的`venv`目录下，进入该环境：
source venv/bin/activate

### C源码

新建一个文件`demo.c`，写入以下C代码（代码中各API的含义后面再分析）：

```c

#include "Python.h"

static PyObject *py_hello(PyObject *self, PyObject *args) {
    /* print hello */
    printf("hello\n");

    /* return None */
    return Py_BuildValue("");
}

/* Module method table */
static PyMethodDef DemoMethods[] = {
  {"hello", py_hello,   METH_VARARGS, "hello"},
  { NULL,   NULL,       0,            NULL}
};

/* Module structure */
static struct PyModuleDef demomodule = {
  PyModuleDef_HEAD_INIT,

  "demo",           /* name of module */
  "A demo module",  /* Doc string (may be NULL) */
  -1,               /* Size of per-interpreter state or -1 */
  DemoMethods       /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_demo(void) {
  return PyModule_Create(&demomodule);
}
```

### 编译

1. 新建`setup.py`以构建函数库，代码如下：

```python
from distutils.core import setup, Extension
    
demomodule = Extension('demo',
                       sources = ['demo.c'])
    
setup (name = 'demo',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [demomodule])
```

2. 编译，生成共享库
```bash
(venv)$ python setup.py build
running build
running build_ext
building 'demo' extension
creating build
creating build/temp.linux-x86_64-3.6
x86_64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -g 
    -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time 
    -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m 
    -I/icode/learn/cpy/demo/venv/include/python3.6m -c demo.c 
    -o build/temp.linux-x86_64-3.6/demo.o
creating build/lib.linux-x86_64-3.6
x86_64-linux-gnu-gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions 
    -Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-Bsymbolic-functions -Wl,-z,relro 
    -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time 
    -D_FORTIFY_SOURCE=2 build/temp.linux-x86_64-3.6/demo.o 
    -o build/lib.linux-x86_64-3.6/demo.cpython-36m-x86_64-linux-gnu.so
```

可见，生成的共享库文件`demo.cpython-36m-x86_64-linux-gnu.so`被放在子目录`build/lib.system`下。
​    
### 安装

编译好后，但是该子目录`build`不在环境变量`PYTHONPATH`中，所以还不能在Python代码中导入该共享库（模块），
可以手动添加该子目录到`PYTHONPATH`中，但如果每次新建C扩展都要修改`PYTHONPATH`，就太麻烦了。所以Python提供了命令，把新生成的共享库文件安装到Python环境的`site-packages`下，相当于安装第三方的包，这样就可以直接在Python代码中导入。
有两种安装方式：

#### 执行`setup.py`安装

执行`python setup.py install`即可。

如果后续想要从`site-packages`中删除上面安装的包文件，可以先用下面的命令把包路径记录到文件中：

```bash
(venv)$ python setup.py install --record files.txt
running install
running build
running build_ext
running install_lib
copying build/lib.linux-x86_64-3.6/demo.cpython-36m-x86_64-linux-gnu.so -> 
    /icode/learn/cpy/demo/venv/lib/python3.6/site-packages
running install_egg_info
Writing /icode/learn/cpy/demo/venv/lib/python3.6/site-packages/demo-1.0.egg-info
writing list of installed files to 'files.txt'
```

看下`files.txt`中的内容是什么：
```bash
(venv)$ cat files.txt 
/icode/learn/cpy/demo/venv/lib/python3.6/site-packages/demo.cpython-36m-x86_64-linux-gnu.so
/icode/learn/cpy/demo/venv/lib/python3.6/site-packages/demo-1.0.egg-info
```

可以看到，上面记录的就是安装包的绝对路径

这种方式如何删除包？可执行下面的命令：

```bash
xargs rm -rf < files.txt
```

#### 用pip安装

可直接在当前目录下执行：

```bash
(venv)$ pip install .
Looking in indexes: https://mirrors.aliyun.com/pypi/simple
Processing /icode/learn/cpy/demo
Building wheels for collected packages: demo
  Building wheel for demo (setup.py) ... done
  Created wheel for demo: filename=demo-1.0-cp36-cp36m-linux_x86_64.whl 
    size=12892 sha256=add10d...
  Stored in directory: /tmp/pip-ephem-wheel-cache-ed29mpkc/wheels/2f/a0/71/b24...
Successfully built demo
Installing collected packages: demo
Successfully installed demo-1.0
```

看是否安装成功了：

```bash
(venv)$ ls venv/lib/python3.6/site-packages/demo*
venv/lib/python3.6/site-packages/demo.cpython-36m-x86_64-linux-gnu.so

venv/lib/python3.6/site-packages/demo-1.0.dist-info:
INSTALLER  METADATA  RECORD  top_level.txt  WHEEL

(venv)$ pip list | grep demo
demo       1.0   
```

从上面的结果看，确实已经安装好了。

可直接通过`pip`卸载该包？

```bash
(venv)$ pip uninstall demo
Uninstalling demo-1.0:
  Would remove:
    /icode/learn/cpy/demo/venv/lib/python3.6/site-packages/demo-1.0.dist-info/*
    /icode/learn/cpy/demo/venv/lib/python3.6/site-packages/demo.cpython-36m-x86_64-linux-gnu.so
Proceed (y/n)? y
  Successfully uninstalled demo-1.0
```

### Python中调用

新建`pydemo.py`测试，调用上面生成的`demo.*.so`包，代码如下：
```python
#!/usr/bin/env python

from __future__ import print_function
import demo

def main():
    s = demo.hello()
    print('c return:', s)

if __name__ == "__main__":
    main()
```

然后执行该代码：
```bash
(venv)$ python pydemo.py
hello
c return: None
```

可以看到：Python代码中成功调用了C语言中的函数。

## 分析
    看完上面的例子后，我们来分析下写Python的C扩展的步骤，及用到的API


## 参考：
1. [Building C and C++ Extensions](https://docs.python.org/3.7/extending/building.html)

2. [Create a C++ extension for Python](<https://docs.microsoft.com/en-us/visualstudio/python/working-with-c-cpp-python-in-visual-studio?view=vs-2019>)
