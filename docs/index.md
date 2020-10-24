# pytest-chinese-doc

[pytest（v6.1.1）](https://docs.pytest.org/en/6.1.1/contents.html)的中文文档，不仅仅是单纯的翻译，也包含我的一些理解和实践，希望有更多的人使用这款优秀的测试框架。


## 环境

- `pytest`版本：6.1.1
- `python`版本：3.8.4


## 使用

- 克隆此仓库；

    - `docs`目录中包含所有的文章，以[markdown](https://daringfireball.net/projects/markdown/)格式编写，集成[admonition](https://python-markdown.github.io/extensions/admonition/)扩展，使用[mkdocs](https://github.com/mkdocs/mkdocs)工具支撑在线文档。
    
    - `src`目录中包含所有示例的源码，以章节划分。
  
- 进入项目根目录，执行命令`pipenv install`安装虚拟环境，使用的是[豆瓣的镜像](https://pypi.doubanio.com/simple/)。

## 其它获取途径

- 关注微信公众号【小鹿的先森】，回复【pytest】：

    ![wechat](img/wechat.jpg)

- 博客园：<https://www.cnblogs.com/luizyao/p/11771740.html>

## 主要新加及修订的内容（v5.1.3 -> v6.1.1）

- `--pdb`加载[ipython](https://ipython.org/)环境作为诊断器：[查看](zh-Hans-CN/二、使用和调用/#_13)

- `--durations-min`默认值从`0.01`秒修改成`0.005`秒：[查看](zh-Hans-CN/二、使用和调用/#_14)

- `--junit_family`命令行选项的默认值改成`xunit2`：[查看](zh-Hans-CN/二、使用和调用/#xml)

- 移除了对`--resultlog`命令行选项的支持：[查看](https://docs.pytest.org/en/stable/deprecations.html#result-log-result-log)

