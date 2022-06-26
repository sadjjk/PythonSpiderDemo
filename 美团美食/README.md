#### 爬取目标

根据美团美食爬取对应推荐餐厅列表

- 输入

  网址:https://(城市缩写).meituan.com/meishi/

  如:https://hz.meituan.com/meishi/

  这里的城市缩写由美团定义 后续代码中已申明各城市对应的缩写

- 输出

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lnnx0199j20w10u077s.jpg)

#### 目标分析

该页面需要强制登陆后才可登陆

因此一定是需要Cookies验证

目标接口:https://hz.meituan.com/meishi/api/poi/getPoiList

GET请求 请求参数

其中`user`为当前登陆用户id

`uuid`为唯一标识 可从Cookies中获取

`_token`为加密结果

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lnsa5b65j22f80akte8.jpg)

经过一番探索和查询

加密方式为请求参数转二级制再进base64加密 再重复一遍 得到最终加密结果

#### 爬取过程

这里原本想使用无脑扣JS的方法 扣到转二进制时最后发现难以进行下去 故查询相关资料

发现Python复现更加优雅简洁 因此主要用Python实现加密过程

##### 1.搜索请求参数关键词

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lo2q57h4j22uc0psdrv.jpg)

搜索请求参数关键词`_token`  左侧出现所有与该关键词有关的js文件 挨个查看

发现`index.js`文件中出现`_token`定义  打点调试进入该段函数

##### 2.分析加密过程

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lofbr9aij21980o0tfw.jpg)

输入`jv`  中间变量`jx` 、`iP` 输出`jw`(即最终加密结果) 查询各个变量值

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lp775b9gj21s20gutbs.jpg)

`iP` 字典 基本为常量

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lpm5gqqmj216o0f8mzb.jpg)

`jv`即不含`_token`的其他参数

`jx`即将各个参数解析成字典 再通过`iJ`函数生成sign值 赋值给`iP`

```javascript
iP.sign = iJ(jx);
```

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lph1f2swj20oi07o0uc.jpg)

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3lpibj3sdj22em02a75f.jpg)

`jd` 即`jx`字典按key排序后 再&拼接  

最后通过`iI`函数返回最终的sign值 

```javascript
var iI = function(jc) {
                    jc = cD.deflate(JSON.stringify(jc));
                    jc = iD(jc);
                    return jc
                };
```

其中`cD.deflate`这段的js比较难扣 难以复现 可以先跳过这段加密逻辑

最终将生成的sign值 赋值给`iP`

再对`iP`字典进行一次`iI`函数加密 加密后的结果为最终的`_token`

##### 3.Python复现核心加密逻辑

`iI`函数 用Python的复现逻辑如下

```
def decode_sign(token_string):
    # base编码
    encode1 = str(token_string).encode()
    # 参数 压缩成 特殊的编码 ->
    compress = zlib.compress(encode1)  # 二进制压缩
    b_encode = base64.b64encode(compress)
    # 转变 str
    e_sign = str(b_encode, encoding='utf-8')
    return e_sign
```

##### 4.最后封装 发起请求

#### 爬虫源码

[Github](https://github.com/sadjjk/PythonSpiderDemo/blob/master/%E7%BE%8E%E5%9B%A2%E7%BE%8E%E9%A3%9F/meituan.py)

#### 总结

美团美食的核心加密逻辑的js比较复杂 难以扣出来复现

在实际探索过程中 发现`iI`函数变成了二进制 

但没有相关的经验 就很难反应出是二进制压缩

因此 **熟能生巧**