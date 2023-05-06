# ChineseWailingWall[学业冲突，暂停维护至六月中旬]
CN数字时代哭墙————李文亮微博
Chinese Wailing Wall ——MicroBlog of Li Wenliang
直连：http://wailingwall.top

20221128初试，中间因网络故障遗漏约1h
20221129优化代码，遇临时网络故障可自动重试(其实就是try)，以及中断重启脚本无需手动删除重复的头部
20221205中间多处由于挂载脚本的树莓派多次Read-only错误而丢失
20221206爬虫脚本挂载至云服务器
20221207在脚本中应用多线程以防在获取response时出现未知卡死(由于毕竟是小概率事件，暂不设异常线程回收)
