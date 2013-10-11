# coding: utf-8

这个包定义了models相关的东西，比如db，engine，和表格的类

这个models包需要单独配置
需要配置的文件是：
database.py - 通常配置来自于 ex_var.py文件

如何创建数据库：
- 创建全部的数据库表格
1. 配置好database.py
2. 运行 __init__.py

- 每个文件单独创建
1. 配置好database.py
2. 运行单独的文件，有外键关系的表格需要有创建的先后顺序  # 目前是不行的，我没有添加代码，可以手动添加engine，模仿__init__.py