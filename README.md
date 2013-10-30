pub
===

路径管理使用了两个文件

urls.py
pub_app.py

这里服务器的配置文件需要做一下的改变：
1. ex_var.py文件 - 改变两个位置，以后再也不用改变了
2. 然后是配置setting里面的东西了

pub_nginx.conf
pub_uwsgi.ini
这两个文件是nginx和uwsgi的配置文件

如果是测试的话，运行run_app.py比较合适

所有改变的文件有：
    run_app.py
    secret.py
    ex_var.py