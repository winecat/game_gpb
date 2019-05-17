notice:
1.copy 【conf.ini.sample】配置，改成 【conf.ini】文件，配置相应目录(这是重点！！！)
2.生成服务端协议，只需执行 gen_server.bat
3.协议文档里， 协议的新加，尽量从最底下追加，别从中间插入内容，以免造成协议号混乱
4. 协议message的定义
.41.服务端-->客户端 sc_XXXXX
.42.客户端-->服务端 cs_XXXXX
.43.其他的message，因为不用生成协议映射，不需要以cs|sc为前缀
.44.共用的message可以追加到protomacro.proto文件里，而引用的proto则需要在文件头加入 import "protomacro.proto"; 以引入相应的文件结构
5.如果只是单个协议文档使用的message，不需要追加到protomacro.proto里，以提高文件生成效率
6.protobuf的使用详情参考http://blog.csdn.net/yi_ya/article/details/40404231
                        
                                        
                                                    -- mars