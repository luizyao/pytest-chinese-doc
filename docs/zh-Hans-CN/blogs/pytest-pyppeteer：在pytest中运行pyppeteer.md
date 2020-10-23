# pytest-pyppeteer

[pytest-pyppeteer](https://github.com/luizyao/pytest-pyppeteer)是我写的一个 pytest 插件，支持在 pytest 中运行[pyppeteer](https://github.com/pyppeteer/pyppeteer)，起因是为了解决工作中的一个测试需求，现在将其开源并做简单介绍。

# 背景

## 为什么不用 selenium？

主要的原因是 selenium 的配置比较繁琐，最常见的问题是需要保持 webdriver 和浏览器版本的一致性。

## pyppeteer 的简单介绍

pyppeteer 是 [puppeteer](https://github.com/puppeteer/puppeteer/)的非官方 python 版本，几乎实现了和其相同的 API，可以非常方便的去操作 Chrome 浏览器。

### pyppeteer 的局限性

目前最明显的问题是没有提供跨浏览器的解决方案，最新的 puppeteer 已经提供对 Firefox 的支持，但是 pyppeteer 可能还需要一些时间。

# 安装

!!! note

	推荐使用[pipenv](https://github.com/pypa/pipenv)管理虚拟环境，并替换为国内 pip 源。

```bash
$ pipenv install pytest-pyppeteer
```

!!! attention

	仅支持 python >= 3.7

# 快速开始

用下面这个测试用例来说明：断言电影《活着》的豆瓣评分大于 9.0。

```python
from dataclasses import dataclass

from pytest_pyppeteer.models import Browser


@dataclass(init=False)
class Elements:
    """收集所有使用到的页面元素，可以为 XPath 或者 CSS Selector。"""

    # 查询输入框
    query = "#inp-query"

    # 点击搜索
    apply = ".inp-btn > input:nth-child(1)"

    # 第一条结果
    first_result = (
        "#root > div > div > div > div > div:nth-child(1) > div.item-root a.cover-link"
    )

    # 评分
    rating = (
        "#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong"
    )


async def test_lifetimes(pyppeteer: Browser):
    page = await pyppeteer.new_page()
    await page.goto('https://movie.douban.com/')

    await page.type(Elements.query, "活着")
    await page.click(Elements.apply)

    await page.waitfor(Elements.first_result)
    await page.click(Elements.first_result)

    await page.waitfor(Elements.rating)
    rating = await page.get_value(Elements.rating)
    
    assert float(rating) >= 9.0
```

执行测试用例，看一下效果：

![断言电影《活着》的豆瓣评分大于 9.0](/img/pytest_pyppeteer_movie_lifetimes.gif)

这里我们无需指定浏览器的路径，pytest-pyppeteer 会在对应平台默认的安装路径下搜寻 Chrome 的可执行文件。

也可以通过 `--executable-path`命令行选项显示的指定 Chrome 的路径。

或者，在你的`conftest.py`文件中指定:

```python
@pytest.fixture(scope="session")
def executable_path(executable_path):
    if executable_path is None:
        return "path/to/Chrome/or/Chromium"
    return executable_path
```

其它支持的命令行选项，包括：

- `--headless`：使用浏览器的无头模式；

- `--args`：为浏览器指定其它参数。例如：指定代理服务器：

    ```bash
    $ pytest --args proxy-server "localhost:5555,direct://" --args proxy-bypass-list "192.0.0.1/8;10.0.0.1/8"
    ```

- `--window-size`：指定浏览器的大小，默认是 800*600；`--window-size 0 0`表示最大化浏览器；

# 同时操作多个浏览器

用下面这个测试用例来说明：断言书籍《活着》的豆瓣评分高于其电影的评分。

```python
import asyncio
from dataclasses import dataclass

from pytest_pyppeteer.models import Browser, Page


@dataclass(init=False)
class Elements:
    """公共对象库"""

    query = "#inp-query"
    apply = ".inp-btn > input:nth-child(1)"


@dataclass(init=False)
class BookElements(Elements):
    url = "https://book.douban.com/"

    first_result = '(//*[@class="item-root"]/a)[1]'
    rating = "#interest_sectl > div > div.rating_self.clearfix > strong"


@dataclass(init=False)
class MovieElements(Elements):
    url = "https://movie.douban.com/"

    first_result = (
        "#root > div > div > div > div > div:nth-child(1) > div.item-root a.cover-link"
    )
    rating = (
        "#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong"
    )


async def query_rating(pyppeteer: Browser, name: str, elements: Elements):
    """获取电影或者书籍的评分。"""

    page: Page = await pyppeteer.new_page()

    await page.goto(elements.url)

    await page.type(elements.query, name)
    await page.click(elements.apply)

    await page.waitfor(elements.first_result)
    await page.click(elements.first_result)

    await page.waitfor(elements.rating)
    rating = await page.get_value(elements.rating)

    return rating


async def test_multiple_pyppeteer(pyppeteer_factory):
    pyppeteer1 = await pyppeteer_factory()
    pyppeteer2 = await pyppeteer_factory()

    movie_rating, book_rating = await asyncio.gather(
        query_rating(pyppeteer1, "活着", MovieElements),
        query_rating(pyppeteer2, "活着", BookElements)
    )

    assert book_rating >= movie_rating
```

通过`pyppeteer_factory` 可以获取多个浏览器实例，分别执行不同的操作，再利用 python 标准库`asyncio`可以很方便的进行异步调用，节省时间。

执行测试用例，看一下效果：

![断言书籍《活着》的豆瓣评分高于其电影的评分](/img/pytest_pyppeteer_book_movie_lifetimes.gif)

# Github 仓库

更多功能可以访问：<https://github.com/luizyao/pytest-pyppeteer>，如果能帮助到你的话，可以给个 star，也欢迎提 issue 和 pr。

# pytest 中文文档(v6.1.1)

之前翻译过 pytest v5.1.3 的官方文档并开源，目前计划更新到 v6.1.1 版本。

项目更多进度可以访问：<https://github.com/luizyao/pytest-chinese-doc/tree/6.1.1>
