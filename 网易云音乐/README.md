#### 爬取目标

根据网易云音乐id爬取对应的音频文件

- 输入

  网址:https://music.163.com/#/song?id=歌曲id
  如:https://music.163.com/#/song?id=1956514098

- 输出

  ![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhbklqibj221h0u0gsg.jpg)

#### 目标分析

简单搜索音乐后缀 发现该音频文件来自某一接口请求返回内容

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhhmnw49j22bo0q2n6t.jpg)

该接口:https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=

POST请求 请求参数

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhi4nsl4j21wm070tbk.jpg)

`params`和`encSecKey`均为加密结果

大致分析加密过程

`params`为两层AES加密

`encSecKey`为RSA加密

这里不过多介绍AES与RSA加密基本原理

因为爬虫不用过多关注加密原理 会应用即可

#### 爬取过程

这里采用**无脑扣JS**的方法 可以说是最简单粗暴的 将整段加密js过程扣出来 js编辑后直接输出上述两个参数

当然也有更有优雅的方法 用Python复写JS加密过程 但对Python和JS要有一定掌握

##### 1. 根据音频后缀名搜索对应接口

   ![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhs45ivdj22y40ow494.jpg)

   获取接口请求地址和请求参数 

   ![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhi4nsl4j21wm070tbk.jpg)

##### 2.搜索请求参数关键词

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dhwkj20mj22ja0u0nck.jpg)

搜索请求参数关键词`encSecKey`  左侧出现所有与该关键词有关的js文件 挨个查看

发现第一个js文件中出现`params`和`encSecKey`  基本锁定加密过程出自这段部分

```javascript
var bKB5G = window.asrsea(JSON.stringify(i9b), buV3x(["流泪", "强"]), buV3x(Rg5l.md), buV3x(["爱心", "女孩", "惊恐", "大笑"]));
e9f.data = j9a.cr0x({
                params: bKB5G.encText,
                encSecKey: bKB5G.encSecKey
            })
```

加密主函数来自`asrsea` 有以下参数

- `i9b` 字典

  `{ids: '[1956514098]', level: 'standard', encodeType: 'aac', csrf_token: ''}`

  ids中的id即当前歌曲id

  ![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3di9v2vkqj217g0h6dle.jpg)

- `buV3x(["流泪", "强"])` 常量 010001

- `buV3x(Rg5l.md)` 常量

- `buV3x(["爱心", "女孩", "惊恐", "大笑"])` 常量

  ![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3dikks4jbj20zc0cugo0.jpg)

加密的主要参数`i9b`这个字典 字典中有歌曲的id 其余参数均为常量

##### 3.搜索关键词`asrsea`

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3diorj0lbj21580tsq7n.jpg)

在当前文件中搜索关键词`asrsea` 发现核心加密逻辑

`asrsea`即函数`d` 其中`d`函数有4个参数 即`asrsea`对应的4个参数

`d`函数中又使用了`a、b、c`等函数 输出`h`(字典) 字典中有`encText、encSecKey`

即请求接口对应的参数  `params`和`encSecKey`

##### 4.扣JS源码 安装`CryptoJS`

将上述`a、b、c、d`等函数 复制粘贴至新建的js文件中

在底层增加打印`d`函数

```javascript
在d函数底部补充return h 便于结果打印

console.log(d("{\"ids\":\"[1956514098]\",\"level\":\"standard\",\"encodeType\":\"aac\",\"csrf_token\":\"\"}", "010001", '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7', "0CoJUm6Qyw8W8jud"))
```

`node js文件`开始本地调试

代码中使用到了`CryptoJS`库 需进行本地安装

```
npm install crypto-js
```

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3diyqmg21j22ak0m0wk2.jpg)

安装过程中出现几个`WARN` 可忽略不计 不影响后续使用

在js文件中引入新安装的`CryptoJS`

```
const CryptoJS = require('./node_modules/crypto-js')
```

出于强迫症 这个几个`WARN`也有办法解决

```shell
npm WARN saveError ENOENT: no such file or directory, open '/Users/sadjjk/Desktop/PythonSpiderDemo/网易云音乐/package.json'
npm notice created a lockfile as package-lock.json. You should commit this file.

前两句提示没有package.json文件 初始化即可
npm init -y 

后面几句 修改初始化后在当前目录生成的package.json文件
1.将description修改为
"description": "npm-insall-package"
2.底部补充
"private": true
```

##### 5.缺啥补啥 继续无脑扣js

安装好`CryptoJS`后继续node调试

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3djbefnrxj21tc0lwq8g.jpg)

提示`reverseStr`函数未定义

在chrome浏览器当前js文件中 搜索复制该函数

**大概会提示10多次函数或常量未定义 缺啥补啥**

最后成功输出结果

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h3djfn47qij22an0u0tgm.jpg)

##### 6.封装函数 发起请求

```python
import requests
import execjs

def get_music_file_url(music_id):
    with open('./163music.js', 'r') as f:
        jscode = f.read()

    d = "{\"ids\":\"[" + str(music_id) + "]\",\"level\":\"standard\",\"encodeType\":\"aac\",\"csrf_token\":\"\"}"
    ctx = execjs.compile(jscode).call('d', d)
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    response = requests.post(url, data=ctx, headers=headers).json()
    return response['data'][0]["url"]
if __name__ == '__main__':
    print(get_music_file_url(1956514098))

```

#### 爬虫源码

[Github](https://github.com/sadjjk/PythonSpiderDemo/blob/master/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90/163music.py)

#### 总结

网易云音乐加密过程比较复杂 

但在爬取过程中使用无脑扣JS的方法 还是比较简单

无需关注加密过程 `Ctrl C+V`即可