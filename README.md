# pytest-chinese-doc
`pytest`[官方文档（5.1.3版本）](https://docs.pytest.org/en/5.1.3/contents.html)的中文翻译，但不仅仅是简单的翻译：

- 更多的例子，尽量做到每一知识点都有例子；
- 更多的拓展阅读，部分章节添加了作者学习时，所查阅的资料；

所以这也是作者自身学习`pytest`的历程，希望能有更多的人了解这款优秀的测试框架；


# 环境
- `pytest`版本：5.1.3
- `python`版本：3.7.3
- `pipenv`版本：2018.11.26


# 使用
- `git clone git@github.com:luizyao/pytest-chinese-doc.git`仓库：

  `docs/`目录下包含所有的文章，以[markdown](https://daringfireball.net/projects/markdown/)格式编写；

  `src/`目录下包含所有的示例源码，以章节划分；

- 进入项目的根目录下，执行`pipenv install`，创建仓库的虚拟环境


# 目录

- [1、安装和入门](docs/1、安装和入门.md)
- [2、使用和调用](docs/2、使用和调用.md)
- [3、编写断言](docs/3、编写断言.md)
- [4、fixtures：明确的、模块化的和可扩展的](docs/4、fixtures：明确的、模块化的和可扩展的.md)
- [5、猴子补丁](docs/5、猴子补丁.md)
- [6、临时目录和文件](docs/6、临时目录和文件.md)
- [7、捕获标准输出和标准错误输出](docs/7、捕获标准输出和标准错误输出.md)
- [8、捕获告警信息](docs/8、捕获告警信息.md)

# TODO
- [ ] 阅读`pytest`源码
- [ ] 基于`pytest`，实践一个WEB自动化框架 


# LICENSE
[MIT LICENSE](LICENSE)
