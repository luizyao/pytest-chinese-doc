<!-- TOC -->

- [1. `fixture`：作为形参使用](#1-fixture%e4%bd%9c%e4%b8%ba%e5%bd%a2%e5%8f%82%e4%bd%bf%e7%94%a8)
- [2. `fixture`：一个典型的依赖注入的实践](#2-fixture%e4%b8%80%e4%b8%aa%e5%85%b8%e5%9e%8b%e7%9a%84%e4%be%9d%e8%b5%96%e6%b3%a8%e5%85%a5%e7%9a%84%e5%ae%9e%e8%b7%b5)
- [3. `conftest.py`：共享`fixture`实例](#3-conftestpy%e5%85%b1%e4%ba%abfixture%e5%ae%9e%e4%be%8b)
- [4. 共享测试数据](#4-%e5%85%b1%e4%ba%ab%e6%b5%8b%e8%af%95%e6%95%b0%e6%8d%ae)
- [5. 作用域：在跨类的、模块的或整个测试会话的用例中，共享`fixture`实例](#5-%e4%bd%9c%e7%94%a8%e5%9f%9f%e5%9c%a8%e8%b7%a8%e7%b1%bb%e7%9a%84%e6%a8%a1%e5%9d%97%e7%9a%84%e6%88%96%e6%95%b4%e4%b8%aa%e6%b5%8b%e8%af%95%e4%bc%9a%e8%af%9d%e7%9a%84%e7%94%a8%e4%be%8b%e4%b8%ad%e5%85%b1%e4%ba%abfixture%e5%ae%9e%e4%be%8b)
  - [5.1. `package`作用域（实验性的）](#51-package%e4%bd%9c%e7%94%a8%e5%9f%9f%e5%ae%9e%e9%aa%8c%e6%80%a7%e7%9a%84)
- [6. `fixture`的实例化顺序](#6-fixture%e7%9a%84%e5%ae%9e%e4%be%8b%e5%8c%96%e9%a1%ba%e5%ba%8f)
- [7. `fixture`的清理操作](#7-fixture%e7%9a%84%e6%b8%85%e7%90%86%e6%93%8d%e4%bd%9c)
  - [7.1. 使用`yield`代替`return`](#71-%e4%bd%bf%e7%94%a8yield%e4%bb%a3%e6%9b%bfreturn)
  - [7.2. 使用`with`写法](#72-%e4%bd%bf%e7%94%a8with%e5%86%99%e6%b3%95)
  - [7.3. 使用contextlib.ExitStack](#73-%e4%bd%bf%e7%94%a8contextlibexitstack)
  - [7.4. 使用`addfinalizer`方法](#74-%e4%bd%bf%e7%94%a8addfinalizer%e6%96%b9%e6%b3%95)
- [8. `fixture`可以访问测试请求的上下文](#8-fixture%e5%8f%af%e4%bb%a5%e8%ae%bf%e9%97%ae%e6%b5%8b%e8%af%95%e8%af%b7%e6%b1%82%e7%9a%84%e4%b8%8a%e4%b8%8b%e6%96%87)

<!-- /TOC -->

`pytest fixture`的目的是提供一个固定的基线，使测试在此基础上可以可靠地、重复地执行；

对比`xUnit`经典的`setup/teardown`形式，`pytest fixture`在以下方面有了明显的改进：

- 每个`fixture`都拥有一个确定的名字，使其能够在函数、类、模块，甚至整个项目中去声明使用；
- `fixture`以模块化的方式实现。因为每一个`fixture`的名字都能触发一个**fixture函数**，而这个函数本身又能调用其它的`fixture`；
- `fixture`的管理从简单的单元测试扩展到复杂的功能测试，允许通过配置和组件化的选项参数化`fixture`和测试，或者跨功能、类、模块，甚至整个测试会话中复用`fixture`；

此外，`pytest`继续支持经典的`xUnit`风格的测试。你可以根据自己的喜好，混合使用两种风格，或者逐渐过渡到新的风格。你也可以从已有的`unittest.TestCase`或者`nose`项目中执行测试；


# 1. `fixture`：作为形参使用
测试函数可以接收`fixture`的名字作为入参，其实参是对应的`fixture`函数的返回值。通过`@pytest.fixture`装饰器可以注册一个`fixture`函数；

我们来看一个独立的测试模块，它包含一个`fixture`和一个使用它的测试方法：

```python
# src/chapter-4/test_smtpsimple.py

import pytest


@pytest.fixture
def smtp_connection():
    import smtplib

    return smtplib.SMTP("smtp.163.com", 25, timeout=5)


def test_ehlo(smtp_connection):
    response, _ = smtp_connection.ehlo()
    assert response == 250
    assert 0  # 为了展示，强制置为失败
```

这里，`test_ehlo`有一个形参`smtp_connection`，和上面定义的`fixture`函数同名；

我们执行这个测试模块：

```bash
$ pipenv run pytest -q src/chapter-4/test_smtpsimple.py 
F                                                                 [100%]
=============================== FAILURES ================================
_______________________________ test_ehlo _______________________________

smtp_connection = <smtplib.SMTP object at 0x105992d68>

    def test_ehlo(smtp_connection):
        response, _ = smtp_connection.ehlo()
        assert response == 250
>       assert 0  # 为了展示，强制置为失败
E       assert 0

src/chapter-4/test_smtpsimple.py:35: AssertionError
1 failed in 0.17s
```

`test_smtpsimple.py`的执行过程如下：

- `pytest`收集到测试用例`test_ehlo`，其有一个形参`smtp_connection`，`pytest`查找到一个同名的已经注册的`fixture smtp_connection()`；
- 执行`smtp_connection()`创建一个实例`smtp_connection = <smtplib.SMTP object at 0x105992d68>`作为`test_ehlo`的实参；
- 执行`test_ehlo(<smtplib.SMTP object at 0x105992d68>)`；

如果你不小心拼写出错，或者调用了一个未注册的`fixture`，你会得到一个`fixture not found`的错误，并告诉你目前所有可用的`fixture`：

```bash
$ pipenv run pytest -q src/chapter-4/test_smtpsimple.py 
E                                                                 [100%]
================================ ERRORS =================================
______________________ ERROR at setup of test_ehlo ______________________
file /Users/yaomeng/Private/Projects/pytest-chinese-doc/src/chapter-4/test_smtpsimple.py, line 32
  def test_ehlo(smtp_connectio):
E       fixture 'smtp_connectio' not found
>       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, smtp_connection, smtp_connection_package, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/Users/yaomeng/Private/Projects/pytest-chinese-doc/src/chapter-4/test_smtpsimple.py:32
1 error in 0.02s
```

> 注意：
> 
> 你也可以使用如下调用方式：
> 
>     pytest --fixtures [testpath]
> 
> 它会帮助你显示所有可用的 fixture；
> 
> 但是，对于`_`开头的`fixture`，需要加上`-v`选项；


# 2. `fixture`：一个典型的依赖注入的实践
`fixture`允许测试用例可以轻松的接收和处理特定的需要预初始化操作的应用对象，而不用过分关心**导入/设置/清理**的细节；它是一个典型的依赖注入的实践，其中，`fixture`扮演者注入者（`injector`）的角色，而测试用例扮演者消费者（`client`）的角色；

以上一章的例子来说明：`test_ehlo`测试用例需要一个`smtp_connection`的连接对象来做测试，它只关心这个连接是否有效和可达，却不关心它的创建过程。`smtp_connection`对`test_ehlo`来说，就是一个需要预初始化操作的应用对象，而这个预处理操作是在fixture中完成的；简而言之，`test_ehlo`说：“我需要一个`SMTP`连接对象。”，然后，`pytest`就给了它一个，就这么简单。

> 关于依赖注入的解释，可以看看Stackflow上这个问题的高票回答 [如何向一个5岁的孩子解释依赖注入？](https://stackoverflow.com/questions/1638919/how-to-explain-dependency-injection-to-a-5-year-old)：
> 
>> When you go and get things out of the refrigerator for yourself, you can cause problems. You might leave the door open, you might get something Mommy or Daddy doesn't want you to have. You might even be looking for something we don't even have or which has expired.
>>
>> What you should be doing is stating a need, "I need something to drink with lunch," and then we will make sure you have something when you sit down to eat.
>
> 更详细的资料可以看看维基百科 [Dependency injection](https://encyclopedia.thefreedictionary.com/Dependency+injection)；


# 3. `conftest.py`：共享`fixture`实例
如果你想在多个测试模块中共享同一个`fixture`实例，那么你可以把这个`fixture`函数移动到`conftest.py`文件中。并且，你不需要手动的导入它，`pytest`会自动发现，查找的顺序是：测试类、测试模块、`conftest.py`、最后是内置和第三方的插件；

你还可以利用`conftest.py`文件的这个特性[为每个目录实现一个本地化的插件](http://pytest.org/en/latest/writing_plugins.html#conftest-py-plugins)；


# 4. 共享测试数据
如果你想多个测试共享同样的测试数据文件，我们有两个好方法实现这个：

- 把这些数据加载到`fixture`中，测试中再使用这些`fixture`；
- 把这些数据文件放到`tests`文件夹中，一些第三方的插件能帮助你管理这方面的测试，例如：[pytest-datadir](https://pypi.org/project/pytest-datadir/)和[pytest-datafiles](https://pypi.org/project/pytest-datafiles/)；


# 5. 作用域：在跨类的、模块的或整个测试会话的用例中，共享`fixture`实例
需要使用到网络接入的`fixture`往往依赖于网络的连通性，并且创建过程一般都非常耗时；

我们来扩展一下上述示例（*src/chapter-4/test_smtpsimple.py*）：在`@pytest.fixture`装饰器中添加`scope='module'`参数，使每个**测试模块**只调用一次`smtp_connection fixture`（默认每个**测试用例**都会调用一次），这样模块中的每个测试用例将会共享同一个`fixture`实例；其中，`scope`参数可能的值都有：`function`（默认值）、`class`、`module`、`package`和`session`；

首先，我们把`smtp_connection()`提取到`conftest.py`文件中：

```python
# src/chapter-4/conftest.py


import pytest
import smtplib


@pytest.fixture(scope='module')
def smtp_connection():
  return smtplib.SMTP("smtp.163.com", 25, timeout=5)
```

然后，在相同的目录下，新建一个测试模块`test_module.py`，将`smtp_connection`作为形参传入每个测试用例，它们共享同一个`smtp_connection()`的返回值：

```python
# src/chapter-4/test_module.py


def test_ehlo(smtp_connection):
    response, _ = smtp_connection.ehlo()
    assert response == 250
    smtp_connection.extra_attr = 'test'
    assert 0  # 为了展示，强制置为失败


def test_noop(smtp_connection):
    response, _ = smtp_connection.noop()
    assert response == 250
    assert smtp_connection.extra_attr == 0  # 为了展示，强制置为失败
```

最后，让我们来执行这个测试模块：

```bash
pipenv run pytest -q src/chapter-4/test_module.py 
FF                                                                [100%]
=============================== FAILURES ================================
_______________________________ test_ehlo _______________________________

smtp_connection = <smtplib.SMTP object at 0x107193c50>

    def test_ehlo(smtp_connection):
        response, _ = smtp_connection.ehlo()
        assert response == 250
        smtp_connection.extra_attr = 'test'
>       assert 0  # 为了展示，强制置为失败
E       assert 0

src/chapter-4/test_module.py:27: AssertionError
_______________________________ test_noop _______________________________

smtp_connection = <smtplib.SMTP object at 0x107193c50>

    def test_noop(smtp_connection):
        response, _ = smtp_connection.noop()
        assert response == 250
>       assert smtp_connection.extra_attr == 0
E       AssertionError: assert 'test' == 0
E        +  where 'test' = <smtplib.SMTP object at 0x107193c50>.extra_attr

src/chapter-4/test_module.py:33: AssertionError
2 failed in 0.72s
```

我们可以看到，两个测试用例使用的`smtp_connection`实例都是`<smtplib.SMTP object at 0x107193c50>`，说明`smtp_connection` fixture 只被调用了一次；

同时，在前一个用例`test_ehlo`中修改`smtp_connection`实例（上述例子中，为`smtp_connection`添加`extra_attr`属性），也会反映到`test_noop`用例中， 但是不建议这么做；

如果你期望拥有一个`session`作用域的`smtp_connection`实例，那么你可以简单的将其声明为：

```python
@pytest.fixture(scope='session')
def smtp_connection():
  return smtplib.SMTP("smtp.163.com", 25, timeout=5)
```

> 注意：
> 
> `pytest`每次只缓存一个`fixture`实例，当使用参数化的`fixture`时，`pytest`可能会在声明的作用域内多次调用这个`fixture`；

## 5.1. `package`作用域（实验性的）
在 pytest 3.7 的版本中，正式引入了`package`作用域。

`package`作用域的`fixture`会作用于包内的每一个测试用例：

首先，我们在`src/chapter-4`目录下创建如下的组织：

```bash
chapter-4/
└── package_expr
    ├── __init__.py
    ├── test_module1.py
    └── test_module2.py
```

然后，在`src/chapter-4/conftest.py`中声明一个`package`作用域的`fixture`：

```python
@pytest.fixture(scope='package')
def smtp_connection_package():
    return smtplib.SMTP("smtp.163.com", 25, timeout=5)
```

接着，在`src/chapter-4/package_expr/test_module1.py`中添加如下测试用例：

```python
def test_ehlo_in_module1(smtp_connection_package):
    response, _ = smtp_connection_package.ehlo()
    assert response == 250
    assert 0  # 为了展示，强制置为失败


def test_noop_in_module1(smtp_connection_package):
    response, _ = smtp_connection_package.noop()
    assert response == 250
    assert 0  # 为了展示，强制置为失败
```

同样，在`src/chapter-4/package_expr/test_module2.py`中添加如下测试用例：

```python
def test_ehlo_in_module2(smtp_connection_package):
    response, _ = smtp_connection_package.ehlo()
    assert response == 250
    assert 0  # 为了展示，强制置为失败
```

最后，执行`pipenv run pytest -q src/chapter-4/package_expr/`：

```bash
$ pipenv run pytest -q src/chapter-4/package_expr/
FFF                                                               [100%]
=============================== FAILURES ================================
_________________________ test_ehlo_in_module1 __________________________

smtp_connection_package = <smtplib.SMTP object at 0x1028fec50>

    def test_ehlo_in_module1(smtp_connection_package):
        response, _ = smtp_connection_package.ehlo()
        assert response == 250
>       assert 0  # 为了展示，强制置为失败
E       assert 0

src/chapter-4/package_expr/test_module1.py:26: AssertionError
_________________________ test_noop_in_module1 __________________________

smtp_connection_package = <smtplib.SMTP object at 0x1028fec50>

    def test_noop_in_module1(smtp_connection_package):
        response, _ = smtp_connection_package.noop()
        assert response == 250
>       assert 0
E       assert 0

src/chapter-4/package_expr/test_module1.py:32: AssertionError
_________________________ test_ehlo_in_module2 __________________________

smtp_connection_package = <smtplib.SMTP object at 0x1028fec50>

    def test_ehlo_in_module2(smtp_connection_package):
        response, _ = smtp_connection_package.ehlo()
        assert response == 250
>       assert 0  # 为了展示，强制置为失败
E       assert 0

src/chapter-4/package_expr/test_module2.py:26: AssertionError
3 failed in 0.45s
```

我们可以看到，虽然这三个用例在不同的模块中，但是使用相同的`fixture`实例，都是`<smtplib.SMTP object at 0x1028fec50>`；

> 注意：
> 
> - `chapter-4/package_expr`可以不包含`__init__.py`文件，因为`pytest`发现测试用例的规则没有强制这一点；同样，`package_expr/`的命名也不需要符合`test_*`或者`*_test`的规则；
>
> - 这个功能标记为**实验性的**，如果在其实际应用中发现严重的`bug`，那么这个功能很可能被移除；


# 6. `fixture`的实例化顺序
多个`fixture`的实例化顺序，遵循以下原则：

- 高级别作用域的（例如：`session`）先于低级别的作用域的（例如：`class`或者`function`）
- 相同级别作用域的，遵循它们在**测试用例中被声明的顺序（也就是形参的顺序）**，或者`fixture`之间的相互调用关系
- 使能`autouse`的`fixture`，先于其同级别的其它`fixture`

我们来看一个具体的例子：

```python
# src/chapter-4/test_order.py

import pytest

order = []


@pytest.fixture(scope="session")
def s1():
    order.append("s1")


@pytest.fixture(scope="module")
def m1():
    order.append("m1")


@pytest.fixture
def f1(f3):
    order.append("f1")


@pytest.fixture
def f3():
    order.append("f3")


@pytest.fixture(autouse=True)
def a1():
    order.append("a1")


@pytest.fixture
def f2():
    order.append("f2")


def test_order(f1, m1, f2, s1):
    assert order == ["s1", "m1", "a1", "f3", "f1", "f2"]
```

- `s1`拥有最高级的作用域（`session`），即使在测试用例`test_order`中最后被声明，它也是第一个被实例化的（参照第一条原则）
- `m1`拥有仅次于`session`级别的作用域（`module`），所以它是第二个被实例化的（参照第一条原则）
- `f1 f2 f3 a1`同属于`function`级别的作用域：
  - 从`test_order(f1, m1, f2, s1)`形参的声明顺序中，可以看出，`f1`比`f2`先实例化（参照第二条原则）
  - `f1`的定义中又显式的调用了`f3`，所以`f3`比`f1`先实例化（参照第二条原则）
  - `a1`的定义中使能了`autouse`标记，所以它会在同级别的`fixture`之前实例化，这里也就是在`f3 f1 f2`之前实例化（参照第三条原则）
- 所以这个例子`fixture`实例化的顺序为：`s1 m1 a1 f3 f1 f2`

> 注意：
>
> - 除了`autouse`的`fixture`，需要测试用例显示声明使用，不声明的不会被实例化
>
> - 多个相同作用域的`autouse fixture`，其调用顺序遵循`fixture`函数名的顺序


# 7. `fixture`的清理操作
我们期望在`fixture`退出作用域之前，执行某些清理性操作（例如，关闭服务器的连接等）；

我们有以下几种形式，实现这个功能：

## 7.1. 使用`yield`代替`return`
将`fixture`函数中的`return`关键字替换成`yield`，则`yield`之后的代码，就是我们要的清理操作；

我们来声明一个包含清理操作的`smtp_connection fixture`：

```python
# src/chapter-4/conftest.py

@pytest.fixture()
def smtp_connection_yield():
    smtp_connection = smtplib.SMTP("smtp.163.com", 25, timeout=5)
    yield smtp_connection
    print("关闭SMTP连接")
    smtp_connection.close()
```

再添加一个使用它的测试用例：

```python
# src/chapter-4/test_smtpsimple.py

def test_ehlo_yield(smtp_connection_yield):
    response, _ = smtp_connection_yield.ehlo()
    assert response == 250
    assert 0  # 为了展示，强制置为失败
```

现在，我们来执行它：

```bash
λ pipenv run pytest -q -s --tb=no src/chapter-4/test_smtpsimple.py::test_ehlo_yield
F关闭SMTP连接

1 failed in 0.18s
```

我们可以看到在`test_ehlo_yield`执行完后，又执行了`yield`后面的代码；

## 7.2. 使用`with`写法
对于支持`with`写法的对象，我们也可以隐式的执行它的清理操作；

例如，上面的`smtp_connection_yield`也可以这样写：

```python
@pytest.fixture()
def smtp_connection_yield():
    with smtplib.SMTP("smtp.163.com", 25, timeout=5) as smtp_connection:
        yield smtp_connection
```

## 7.3. 使用[contextlib.ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack)

TODO：不是很能理解这个的实际功能，感觉限制很多：<https://docs.pytest.org/en/5.1.3/fixture.html#fixture-finalization-executing-teardown-code>

## 7.4. 使用`addfinalizer`方法
`fixture`函数能够接收一个`request`的参数，表示[测试请求的上下文](#8-fixture%e5%8f%af%e4%bb%a5%e8%ae%bf%e9%97%ae%e6%b5%8b%e8%af%95%e8%af%b7%e6%b1%82%e7%9a%84%e4%b8%8a%e4%b8%8b%e6%96%87)；我们可以使用`request.addfinalizer`方法为`fixture`添加一个清理函数;

例如，上面的`smtp_connection_yield`也可以这样写：

```python
@pytest.fixture()
def smtp_connection_fin(request):
    smtp_connection = smtplib.SMTP("smtp.163.com", 25, timeout=5)

    def fin():
        smtp_connection.close()

    request.addfinalizer(fin)
    return smtp_connection
```

> 注意：
>
> 在`yield`之前或者`addfinalizer`注册之前代码发生错误退出的，都不会再执行后续的清理操作


# 8. `fixture`可以访问测试请求的上下文
`fixture`函数可以接收一个`request`的参数，表示测试用例、类、模块，甚至测试会话的上下文环境；

我们可以扩展上面的`smtp_connection_yield fixture`，让其根据不同的测试模块使用不同的服务器：

```python
# src/chapter-4/conftest.py

@pytest.fixture(scope='module')
def smtp_connection_request(request):
    server, port = getattr(request.module, 'smtp_server', ("smtp.163.com", 25))
    with smtplib.SMTP(server, port, timeout=5) as smtp_connection:
        yield smtp_connection
        print("断开 %s：%d" % (server, port))
```

在测试模块中指定`smtp_server`：

```python
# src/chapter-4/test_request.py

smtp_server = ("mail.python.org", 587)


def test_163(smtp_connection_request):
    response, _ = smtp_connection_request.ehlo()
    assert response == 250
```

我们来看看效果：

```bash
λ pipenv run pytest -q -s src/chapter-4/test_request.py
.断开 mail.python.org：587

1 passed in 4.03s
```
