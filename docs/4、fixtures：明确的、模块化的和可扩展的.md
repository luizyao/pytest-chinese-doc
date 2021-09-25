- [1. `fixture`：作为形参使用](#1-fixture作为形参使用)
- [2. `fixture`：一个典型的依赖注入的实践](#2-fixture一个典型的依赖注入的实践)
- [3. `conftest.py`：共享`fixture`实例](#3-conftestpy共享fixture实例)
- [4. 共享测试数据](#4-共享测试数据)
- [5. 作用域：在跨类的、模块的或整个测试会话的用例中，共享`fixture`实例](#5-作用域在跨类的模块的或整个测试会话的用例中共享fixture实例)
  - [5.1. `package`作用域（实验性的）](#51-package作用域实验性的)
- [6. `fixture`的实例化顺序](#6-fixture的实例化顺序)
- [7. `fixture`的清理操作](#7-fixture的清理操作)
  - [7.1. 使用`yield`代替`return`](#71-使用yield代替return)
  - [7.2. 使用`with`写法](#72-使用with写法)
  - [7.3. 使用`addfinalizer`方法](#73-使用addfinalizer方法)
- [8. `fixture`可以访问测试请求的上下文](#8-fixture可以访问测试请求的上下文)
- [9. `fixture`返回工厂函数](#9-fixture返回工厂函数)
- [10. `fixture`的参数化](#10-fixture的参数化)
- [11. 在参数化的`fixture`中标记用例](#11-在参数化的fixture中标记用例)
- [12. 模块化：`fixture`使用其它的`fixture`](#12-模块化fixture使用其它的fixture)
- [13. 高效的利用`fixture`实例](#13-高效的利用fixture实例)
- [14. 在类、模块和项目级别上使用`fixture`实例](#14-在类模块和项目级别上使用fixture实例)
- [15. 自动使用`fixture`](#15-自动使用fixture)
- [16. 在不同的层级上覆写`fixture`](#16-在不同的层级上覆写fixture)
  - [16.1. 在文件夹（`conftest.py`）层级覆写`fixture`](#161-在文件夹conftestpy层级覆写fixture)
  - [16.2. 在模块层级覆写`fixture`](#162-在模块层级覆写fixture)
  - [16.3. 在用例参数中覆写`fixture`](#163-在用例参数中覆写fixture)
  - [16.4. 参数化的`fixture`覆写非参数化的`fixture`，反之亦然](#164-参数化的fixture覆写非参数化的fixture反之亦然)

`pytest fixtures`的目的是提供一个固定的基线，使测试可以在此基础上可靠地、重复地执行；对比`xUnit`经典的`setup/teardown`形式，它在以下方面有了明显的改进：

- `fixture`拥有一个**明确的名称**，通过声明使其能够在函数、类、模块，甚至整个测试会话中被激活使用；
- `fixture`以一种**模块化的方式实现**。因为每一个`fixture`的名字都能触发一个*fixture函数*，而这个函数本身又能调用其它的`fixture`；
- `fixture`的管理**从简单的单元测试扩展到复杂的功能测试**，允许通过配置和组件选项参数化`fixture`和测试用例，或者跨功能、类、模块，甚至整个测试会话复用`fixture`；

此外，`pytest`继续支持经典的`xUnit`风格的测试。你可以根据自己的喜好，混合使用两种风格，或者逐渐过渡到新的风格。你也可以从已有的`unittest.TestCase`或者`nose`项目中执行测试；


## 1. `fixture`：作为形参使用
测试用例可以接收`fixture`的名字作为入参，其实参是对应的`fixture`函数的返回值。通过`@pytest.fixture`装饰器可以注册一个`fixture`；

我们来看一个简单的测试模块，它包含一个`fixture`和一个使用它的测试用例：

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

执行：

```bash
$ pytest -q src/chapter-4/test_smtpsimple.py 
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

执行的过程如下：

- `pytest`收集到测试用例`test_ehlo`，其有一个形参`smtp_connection`，`pytest`查找到一个同名的已经注册的`fixture`；
- 执行`smtp_connection()`创建一个`smtp_connection`实例`<smtplib.SMTP object at 0x105992d68>`作为`test_ehlo`的实参；
- 执行`test_ehlo(<smtplib.SMTP object at 0x105992d68>)`；

如果你不小心拼写出错，或者调用了一个未注册的`fixture`，你会得到一个`fixture <...> not found`的错误，并告诉你目前所有可用的`fixture`，如下：

```bash
$ pytest -q src/chapter-4/test_smtpsimple.py 
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
> ```bash
> pytest --fixtures [testpath]
> ```
> 
> 它会帮助你显示所有可用的 fixture；
> 
> 但是，对于`_`开头的`fixture`，需要加上`-v`选项；


## 2. `fixture`：一个典型的依赖注入的实践
`fixture`允许测试用例可以轻松的接收和处理特定的需要预初始化操作的应用对象，而不用过分关心**导入/设置/清理**的细节；这是一个典型的依赖注入的实践，其中，`fixture`扮演者注入者（`injector`）的角色，而测试用例扮演者消费者（`client`）的角色；

以上一章的例子来说明：`test_ehlo`测试用例需要一个`smtp_connection`的连接对象来做测试，它只关心这个连接是否有效和可达，并不关心它的创建过程。`smtp_connection`对`test_ehlo`来说，就是一个需要预初始化操作的应用对象，而这个预处理操作是在fixture中完成的；简而言之，`test_ehlo`说：“我需要一个`SMTP`连接对象。”，然后，`pytest`就给了它一个，就这么简单。

> 关于依赖注入的解释，可以看看Stackflow上这个问题的高票回答[*如何向一个5岁的孩子解释依赖注入？*](https://stackoverflow.com/questions/1638919/how-to-explain-dependency-injection-to-a-5-year-old)：
> 
>> When you go and get things out of the refrigerator for yourself, you can cause problems. You might leave the door open, you might get something Mommy or Daddy doesn't want you to have. You might even be looking for something we don't even have or which has expired.
>>
>> What you should be doing is stating a need, "I need something to drink with lunch," and then we will make sure you have something when you sit down to eat.
>
> 更详细的资料可以看看维基百科[*Dependency injection*](https://encyclopedia.thefreedictionary.com/Dependency+injection)；


## 3. `conftest.py`：共享`fixture`实例
如果你想在多个测试模块中共享同一个`fixture`实例，那么你可以把这个`fixture`移动到`conftest.py`文件中。在测试模块中你不需要手动的导入它，`pytest`会自动发现，`fixture`的查找的顺序是：测试类、测试模块、`conftest.py`、最后是内置和第三方的插件；

你还可以利用`conftest.py`文件的这个特性[*为每个目录实现一个本地化的插件*](https://docs.pytest.org/en/5.1.3/writing_plugins.html#conftest-py-plugins)；


## 4. 共享测试数据
如果你想多个测试共享同样的测试数据文件，我们有两个好方法实现这个：

- 把这些数据加载到`fixture`中，测试中再使用这些`fixture`；
- 把这些数据文件放到`tests`文件夹中，一些第三方的插件能帮助你管理这方面的测试，例如：[*pytest-datadir*](https://pypi.org/project/pytest-datadir/)和[*pytest-datafiles*](https://pypi.org/project/pytest-datafiles/)；


## 5. 作用域：在跨类的、模块的或整个测试会话的用例中，共享`fixture`实例
需要使用到网络接入的`fixture`往往依赖于网络的连通性，并且创建过程一般都非常耗时；

我们来扩展一下上述示例（*src/chapter-4/test_smtpsimple.py*）：在`@pytest.fixture`装饰器中添加`scope='module'`参数，使每个**测试模块**只调用一次`smtp_connection`（默认每个用例都会调用一次），这样模块中的所有测试用例将会共享同一个`fixture`实例；其中，`scope`参数可能的值都有：`function`（默认值）、`class`、`module`、`package`和`session`；

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
pytest -q src/chapter-4/test_module.py 
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

可以看到：

- 两个测试用例使用的`smtp_connection`实例都是`<smtplib.SMTP object at 0x107193c50>`，说明`smtp_connection`只被调用了一次；
- 在前一个用例`test_ehlo`中修改`smtp_connection`实例（上述例子中，为`smtp_connection`添加`extra_attr`属性），也会反映到`test_noop`用例中；

如果你期望拥有一个会话级别作用域的`fixture`，可以简单的将其声明为：

```python
@pytest.fixture(scope='session')
def smtp_connection():
  return smtplib.SMTP("smtp.163.com", 25, timeout=5)
```

> 注意：
> 
> `pytest`每次只缓存一个`fixture`实例，当使用参数化的`fixture`时，`pytest`可能会在声明的作用域内多次调用这个`fixture`；

### 5.1. `package`作用域（实验性的）
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

最后，执行`src/chapter-4/package_expr`下所有的测试用例：

```bash
$ pytest -q src/chapter-4/package_expr/
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

可以看到：

- 虽然这三个用例在不同的模块中，但是使用相同的`fixture`实例，即`<smtplib.SMTP object at 0x1028fec50>`；

> 注意：
> 
> - `chapter-4/package_expr`可以不包含`__init__.py`文件，因为`pytest`发现测试用例的规则没有强制这一点；同样，`package_expr/`的命名也不需要符合`test_*`或者`*_test`的规则；
>
> - 这个功能标记为**实验性的**，如果在其实际应用中发现严重的`bug`，那么这个功能很可能被移除；


## 6. `fixture`的实例化顺序
多个`fixture`的实例化顺序，遵循以下原则：

- 高级别作用域的（例如：`session`）先于低级别的作用域的（例如：`class`或者`function`）实例化；
- 相同级别作用域的，其实例化顺序遵循它们在**测试用例中被声明的顺序（也就是形参的顺序）**，或者`fixture`之间的相互调用关系；
- 使能`autouse`的`fixture`，先于其同级别的其它`fixture`实例化；

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
> - 除了`autouse`的`fixture`，需要测试用例显示声明（形参），不声明的不会被实例化；
>
> - 多个相同作用域的`autouse fixture`，其实例化顺序遵循`fixture`函数名的排序；


## 7. `fixture`的清理操作
我们期望在`fixture`退出作用域之前，执行某些清理性操作（例如，关闭服务器的连接等）；

我们有以下几种形式，实现这个功能：

### 7.1. 使用`yield`代替`return`
将`fixture`函数中的`return`关键字替换成`yield`，则`yield`之后的代码，就是我们要的清理操作；

我们来声明一个包含清理操作的`smtp_connection`：

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
λ pytest -q -s --tb=no src/chapter-4/test_smtpsimple.py::test_ehlo_yield
F关闭SMTP连接

1 failed in 0.18s
```

我们可以看到在`test_ehlo_yield`执行完后，又执行了`yield`后面的代码；

### 7.2. 使用`with`写法
对于支持`with`写法的对象，我们也可以隐式的执行它的清理操作；

例如，上面的`smtp_connection_yield`也可以这样写：

```python
@pytest.fixture()
def smtp_connection_yield():
    with smtplib.SMTP("smtp.163.com", 25, timeout=5) as smtp_connection:
        yield smtp_connection
```

### 7.3. 使用`addfinalizer`方法
`fixture`函数能够接收一个`request`的参数，表示[*测试请求的上下文*](#8-fixture可以访问测试请求的上下文)；我们可以使用`request.addfinalizer`方法为`fixture`添加清理函数;

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


## 8. `fixture`可以访问测试请求的上下文
`fixture`函数可以接收一个`request`的参数，表示测试用例、类、模块，甚至测试会话的上下文环境；

我们可以扩展上面的`smtp_connection_yield`，让其根据不同的测试模块使用不同的服务器：

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
λ pytest -q -s src/chapter-4/test_request.py
.断开 mail.python.org：587

1 passed in 4.03s
```


## 9. `fixture`返回工厂函数
如果你需要在一个测试用例中，多次使用同一个`fixture`实例，相对于直接返回数据，更好的方法是返回一个产生数据的工厂函数；

并且，对于工厂函数产生的数据，也可以在`fixture`中对其管理：

```python
@pytest.fixture
def make_customer_record():

    # 记录生产的数据
    created_records = []

    # 工厂
    def _make_customer_record(name):
        record = models.Customer(name=name, orders=[])
        created_records.append(record)
        return record

    yield _make_customer_record

    # 销毁数据
    for record in created_records:
        record.destroy()


def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
``` 


## 10. `fixture`的参数化
如果你需要在一系列的测试用例的执行中，每轮执行都使用同一个`fixture`，但是有不同的依赖场景，那么可以考虑对`fixture`进行参数化；这种方式适用于对多场景的功能模块进行详尽的测试；

在之前的章节[*fixture可以访问测试请求的上下文*](#8-fixture可以访问测试请求的上下文)中，我们在测试模块中指定不同`smtp_server`，得到不同的`smtp_connection`实例；

现在，我们可以通过指定`params`关键字参数创建两个`fixture`实例，每个实例供一轮测试使用，所有的测试用例执行两遍；在`fixture`的声明函数中，可以使用`request.param`获取当前使用的入参；

```python
# src/chapter-4/test_request.py

@pytest.fixture(scope='module', params=['smtp.163.com', "mail.python.org"])
def smtp_connection_params(request):
    server = request.param
    with smtplib.SMTP(server, 587, timeout=5) as smtp_connection:
        yield smtp_connection
```

在测试用例中使用这个`fixture`：

```python
# src/chapter-4/test_params.py

def test_parames(smtp_connection_params):
    response, _ = smtp_connection_params.ehlo()
    assert response == 250
```

执行：

```bash
$ pytest -q -s src/chapter-4/test_params.py 
.断开 smtp.163.com：25
.断开 smtp.126.com：25

2 passed in 0.26s
```
  
可以看到：

- 这个测试用例使用不同的`SMTP`服务器，执行了两次；

在参数化的`fixture`中，`pytest`为每个`fixture`实例自动指定一个测试`ID`，例如：上述示例中的`test_parames[smtp.163.com]`和`test_parames[smtp.126.com]`；

使用`-k`选项执行一个指定的用例：

```bash
$ pytest -q -s -k 163 src/chapter-4/test_params.py 
.断开 smtp.163.com：25

1 passed, 1 deselected in 0.16s
```

使用`--collect-only`可以显示这些测试`ID`，而不执行用例：

```bash
$ pytest -q -s --collect-only src/chapter-4/test_params.py 
src/chapter-4/test_params.py::test_parames[smtp.163.com]
src/chapter-4/test_params.py::test_parames[smtp.126.com]

no tests ran in 0.01s
```

同时，也可以使用`ids`关键字参数，自定义测试`ID`：

```python
# src/chapter-4/test_ids.py

@pytest.fixture(params=[0, 1], ids=['spam', 'ham'])
def a(request):
    return request.param


def test_a(a):
    pass
```

执行`--collect-only`：

```bash
$ pytest -q -s --collect-only src/chapter-4/test_ids.py::test_a 
src/chapter-4/test_ids.py::test_a[spam]
src/chapter-4/test_ids.py::test_a[ham]

no tests ran in 0.01s
```

我们看到，测试`ID`为我们指定的值；

数字、字符串、布尔值和`None`在测试`ID`中使用的是它们的字符串表示形式：

```python
# src/chapter-4/test_ids.py

def idfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    elif fixture_value == 1:
        return False
    elif fixture_value == 2:
        return None
    else:
        return fixture_value


@pytest.fixture(params=[0, 1, 2, 3], ids=idfn)
def b(request):
    return request.param


def test_b(b):
    pass
```

执行`--collect-only`：

```bash
$ pytest -q -s --collect-only src/chapter-4/test_ids.py::test_b 
src/chapter-4/test_ids.py::test_b[eggs]
src/chapter-4/test_ids.py::test_b[False]
src/chapter-4/test_ids.py::test_b[2]
src/chapter-4/test_ids.py::test_b[3]

no tests ran in 0.01s
```

可以看到：

- `ids`可以接收一个函数，用于生成测试`ID`；
- 测试`ID`指定为`None`时，使用的是`params`原先对应的值；

> 注意：
>
> 当测试`params`中包含元组、字典或者对象时，测试`ID`使用的是`fixture`函数名+`param`的下标：

> ```python
> # src/chapter-4/test_ids.py
>
> class C:
>     pass
>
>
> @pytest.fixture(params=[(1, 2), {'d': 1}, C()])
> def c(request):
>     return request.param
>
>
> def test_c(c):
>     pass
> ```
> 
> 执行`--collect-only`：
>
> ```bash
> $ pytest -q -s --collect-only src/chapter-4/test_ids.py::test_c
> src/chapter-4/test_ids.py::test_c[c0]
> src/chapter-4/test_ids.py::test_c[c1]
> src/chapter-4/test_ids.py::test_c[c2]
>
> no tests ran in 0.01s
> ```
>
> 可以看到，测试`ID`为`fixture`的函数名（`c`）加上对应`param`的下标（从`0`开始）；
>
> 如果你不想这样，可以使用`str()`方法或者复写`__str__()`方法；


## 11. 在参数化的`fixture`中标记用例
在`fixture`的`params`参数中，可以使用`pytest.param`标记这一轮的所有用例，其用法和在`pytest.mark.parametrize`中的用法一样；

```python
# src/chapter-4/test_fixture_marks.py

import pytest


@pytest.fixture(params=[('3+5', 8),
                        pytest.param(('6*9', 42),
                                     marks=pytest.mark.xfail,
                                     id='failed')])
def data_set(request):
    return request.param


def test_data(data_set):
    assert eval(data_set[0]) == data_set[1]
```

我们使用`pytest.param(('6*9', 42), marks=pytest.mark.xfail, id='failed')`的形式指定一个`request.param`入参，其中`marks`表示当用例使用这个入参时，为这个用例打上`xfail`标记；并且，我们还使用`id`为此时的用例指定了一个测试`ID`；

```bash
$ pytest -v src/chapter-4/test_fixture_marks.py::test_data
============================ test session starts ============================
platform darwin -- Python 3.7.3, pytest-5.1.3, py-1.8.0, pluggy-0.13.0 -- /Users/yaomeng/.local/share/virtualenvs/pytest-chinese-doc-EK3zIUmM/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/yaomeng/Private/Projects/pytest-chinese-doc
collected 2 items                                                           

src/chapter-4/test_fixture_marks.py::test_data[data_set0] PASSED      [ 50%]
src/chapter-4/test_fixture_marks.py::test_data[failed] XFAIL          [100%]

======================= 1 passed, 1 xfailed in 0.08s ========================
```

可以看到：

- 用例结果是`XFAIL`，而不是`FAILED`；
- 测试`ID`是我们指定的`failed`，而不是`data_set1`；


我们也可以使用`pytest.mark.parametrize`实现相同的效果：

```python
# src/chapter-4/test_fixture_marks.py

@pytest.mark.parametrize(
    'test_input, expected',
    [('3+5', 8),
     pytest.param('6*9', 42, marks=pytest.mark.xfail, id='failed')])
def test_data2(test_input, expected):
    assert eval(test_input) == expected
```

执行：

```bash
pytest -v src/chapter-4/test_fixture_marks.py::test_data2
============================ test session starts ============================
platform darwin -- Python 3.7.3, pytest-5.1.3, py-1.8.0, pluggy-0.13.0 -- /Users/yaomeng/.local/share/virtualenvs/pytest-chinese-doc-EK3zIUmM/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/yaomeng/Private/Projects/pytest-chinese-doc
collected 2 items                                                           

src/chapter-4/test_fixture_marks.py::test_data2[3+5-8] PASSED         [ 50%]
src/chapter-4/test_fixture_marks.py::test_data2[failed] XFAIL         [100%]

======================= 1 passed, 1 xfailed in 0.07s ========================
```


## 12. 模块化：`fixture`使用其它的`fixture`
你不仅仅可以在测试用例上使用`fixture`，还可以在`fixture`的声明函数中使用其它的`fixture`；这有助于模块化的设计你的`fixture`，可以在多个项目中重复使用框架级别的`fixture`；

一个简单的例子，我们可以扩展之前`src/chapter-4/test_params.py`的例子，实例一个`app`对象：

```python
# src/chapter-4/test_appsetup.py

import pytest


class App:
    def __init__(self, smtp_connection):
        self.smtp_connection = smtp_connection


@pytest.fixture(scope='module')
def app(smtp_connection_params):
    return App(smtp_connection_params)


def test_smtp_connection_exists(app):
    assert app.smtp_connection
```

我们创建一个`fixture app`并调用之前在`conftest.py`中定义的`smtp_connection_params`，返回一个`App`的实例；

执行：

```bash
$ pytest -v src/chapter-4/test_appsetup.py 
============================ test session starts ============================
platform darwin -- Python 3.7.3, pytest-5.1.3, py-1.8.0, pluggy-0.13.0 -- /Users/yaomeng/.local/share/virtualenvs/pytest-chinese-doc-EK3zIUmM/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/yaomeng/Private/Projects/pytest-chinese-doc
collected 2 items                                                           

src/chapter-4/test_appsetup.py::test_smtp_connection_exists[smtp.163.com] PASSED [ 50%]
src/chapter-4/test_appsetup.py::test_smtp_connection_exists[smtp.126.com] PASSED [100%]

============================= 2 passed in 1.25s =============================
```

因为`app`使用了参数化的`smtp_connection_params`，所以测试用例`test_smtp_connection_exists`会使用不同的`App`实例执行两次，并且，`app`并不需要关心`smtp_connection_params`的实现细节；

`app`的作用域是**模块**级别的，它又调用了`smtp_connection_params`，也是**模块**级别的，如果`smtp_connection_params`是**会话**级别的作用域，这个例子还是一样可以正常工作的；这是因为低级别的作用域可以调用高级别的作用域，但是高级别的作用域调用低级别的作用域会返回一个`ScopeMismatch`的异常；


## 13. 高效的利用`fixture`实例
在测试期间，`pytest`只激活最少个数的`fixture`实例；如果你拥有一个参数化的`fixture`，所有使用它的用例会在创建的第一个`fixture`实例并销毁后，才会去使用第二个实例；

下面这个例子，使用了两个参数化的`fixture`，其中一个是模块级别的作用域，另一个是用例级别的作用域，并且使用`print`方法打印出它们的`setup/teardown`流程：

```python
# src/chapter-4/test_minfixture.py

import pytest


@pytest.fixture(scope="module", params=["mod1", "mod2"])
def modarg(request):
    param = request.param
    print("  SETUP modarg", param)
    yield param
    print("  TEARDOWN modarg", param)


@pytest.fixture(scope="function", params=[1, 2])
def otherarg(request):
    param = request.param
    print("  SETUP otherarg", param)
    yield param
    print("  TEARDOWN otherarg", param)


def test_0(otherarg):
    print("  RUN test0 with otherarg", otherarg)


def test_1(modarg):
    print("  RUN test1 with modarg", modarg)


def test_2(otherarg, modarg):
    print("  RUN test2 with otherarg {} and modarg {}".format(otherarg, modarg))
```

执行：

```bash
$ pytest -q -s src/chapter-4/test_minfixture.py 
  SETUP otherarg 1
  RUN test0 with otherarg 1
.  TEARDOWN otherarg 1
  SETUP otherarg 2
  RUN test0 with otherarg 2
.  TEARDOWN otherarg 2
  SETUP modarg mod1
  RUN test1 with modarg mod1
.  SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod1
.  TEARDOWN otherarg 1
  SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod1
.  TEARDOWN otherarg 2
  TEARDOWN modarg mod1
  SETUP modarg mod2
  RUN test1 with modarg mod2
.  SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod2
.  TEARDOWN otherarg 1
  SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod2
.  TEARDOWN otherarg 2
  TEARDOWN modarg mod2

8 passed in 0.02s
```

可以看出:

- `mod1`的`TEARDOWN`操作完成后，才开始`mod2`的`SETUP`操作；
- 用例`test_0`独立完成测试；
- 用例`test_1`和`test_2`都使用到了模块级别的`modarg`，同时`test_2`也使用到了用例级别的`otherarg`。它们执行的顺序是，`test_1`先使用`mod1`，接着`test_2`使用`mod1`和`otherarg 1/otherarg 2`，然后`test_1`使用`mod2`，最后`test_2`使用`mod2`和`otherarg 1/otherarg 2`；也就是说`test_1`和`test_2`共用相同的`modarg`实例，最少化的保留`fixture`的实例个数；


## 14. 在类、模块和项目级别上使用`fixture`实例
有时，我们并不需要在测试用例中直接使用`fixture`实例；例如，我们需要一个空的目录作为当前用例的工作目录，但是我们并不关心如何创建这个空目录；这里我们可以使用标准的[*tempfile*](https://docs.python.org/3/library/tempfile.html)模块来实现这个功能；

```python
# src/chapter-4/conftest.py

import pytest
import tempfile
import os


@pytest.fixture()
def cleandir():
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
```

在测试中使用`usefixtures`标记声明使用它：

```python
# src/chapter-4/test_setenv.py

import os
import pytest


@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
```

得益于`usefixtures`标记，测试类`TestDirectoryInit`中所有的测试用例都可以使用`cleandir`，这和在每个测试用例中指定`cleandir`参数是一样的；

执行：

```bash
$ pytest -q -s src/chapter-4/test_setenv.py 
..
2 passed in 0.02s
```

你可以使用如下方式指定多个`fixture`：

```python
@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
    ...
```

你也可以使用如下方式为测试模块指定`fixture`：

```python
pytestmark = pytest.mark.usefixtures("cleandir")
```

> 注意：参数的名字**必须**是`pytestmark`;

你也可以使用如下方式为整个项目指定`fixture`：

```ini
# src/chapter-4/pytest.ini

[pytest]
usefixtures = cleandir
```

> 注意：
>
> `usefixtures`标记不适用于`fixture`声明函数；例如：
>
> ```python
> @pytest.mark.usefixtures("my_other_fixture")
> @pytest.fixture
> def my_fixture_that_sadly_wont_use_my_other_fixture():
>   ...
> ```
>
> 这并不会返回任何的错误或告警，具体讨论可以参考[*#3664*](https://github.com/pytest-dev/pytest/issues/3664)


## 15. 自动使用`fixture`
有时候，你想在测试用例中自动使用`fixture`，而不是作为参数使用或者`usefixtures`标记；设想，我们有一个数据库相关的`fixture`，包含`begin/rollback/commit`的体系结构，现在我们希望通过`begin/rollback`包裹每个测试用例；

下面，通过列表实现一个虚拟的例子：

```python
# src/chapter-4/test_db_transact.py

import pytest


class DB:
    def __init__(self):
        self.intransaction = []

    def begin(self, name):
        self.intransaction.append(name)

    def rollback(self):
        self.intransaction.pop()


@pytest.fixture(scope="module")
def db():
    return DB()


class TestClass:
    @pytest.fixture(autouse=True)
    def transact(self, request, db):
        db.begin(request.function.__name__)
        yield
        db.rollback()

    def test_method1(self, db):
        assert db.intransaction == ["test_method1"]

    def test_method2(self, db):
        assert db.intransaction == ["test_method2"]
```

**类级别作用域**的`transact`函数中声明了`autouse=True`，所以`TestClass`中的所有用例，可以自动调用`transact`而不用显式的声明或标记；

执行：

```bash
$ pytest -q -s src/chapter-4/test_db_transact.py 
..
2 passed in 0.01s
```

`autouse=True`的`fixture`在其它级别作用域中的工作流程：

- `autouse fixture`遵循`scope`关键字的定义：如果其含有`scope='session'`，则不管它在哪里定义的，都将只执行一次；`scope='class'`表示每个测试类执行一次；
- 如果在测试模块中定义`autouse fixture`，那么这个测试模块所有的用例自动使用它；
- 如果在`conftest.py`中定义`autouse fixture`，那么它的相同文件夹和子文件夹中的所有测试模块中的用例都将自动使用它；
- 如果在插件中定义`autouse fixture`，那么所有安装这个插件的项目中的所有用例都将自动使用它；

上述的示例中，我们期望只有`TestClass`的用例自动调用`fixture transact`，这样我们就不希望`transact`一直处于**激活**的状态，所以更标准的做法是，将`transact`声明在`conftest.py`中，而不是使用`autouse=True`：

```python
@pytest.fixture
def transact(request, db):
    db.begin()
    yield
    db.rollback()
```

并且，在`TestClass`上声明：

```python
@pytest.mark.usefixtures("transact")
class TestClass:
    def test_method1(self):
        ...
```

其它类或者用例也想使用的话，同样需要显式的声明`usefixtures`；


## 16. 在不同的层级上覆写`fixture`
在大型的测试中，你可能需要在本地覆盖项目级别的`fixture`，以增加可读性和便于维护；

### 16.1. 在文件夹（`conftest.py`）层级覆写`fixture`
假设我们有如下的测试项目：

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture
        def username():
            return 'username'

    test_something.py
        # content of tests/test_something.py
        def test_username(username):
            assert username == 'username'

    subfolder/
        __init__.py

        conftest.py
            # content of tests/subfolder/conftest.py
            import pytest

            @pytest.fixture
            def username(username):
                return 'overridden-' + username

        test_something.py
            # content of tests/subfolder/test_something.py
            def test_username(username):
                assert username == 'overridden-username'
```

可以看到：

- 子文件夹`conftest.py`中的`fixture`覆盖了上层文件夹中同名的`fixture`；
- 子文件夹`conftest.py`中的`fixture`可以轻松的访问上层文件夹中同名的`fixture`；

### 16.2. 在模块层级覆写`fixture`
假设我们有如下的测试项目：

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture
        def username():
            return 'username'

    test_something.py
        # content of tests/test_something.py
        import pytest

        @pytest.fixture
        def username(username):
            return 'overridden-' + username

        def test_username(username):
            assert username == 'overridden-username'

    test_something_else.py
        # content of tests/test_something_else.py
        import pytest

        @pytest.fixture
        def username(username):
            return 'overridden-else-' + username

        def test_username(username):
            assert username == 'overridden-else-username'
```

可以看到：

- 模块中的`fixture`覆盖了`conftest.py`中同名的`fixture`；
- 模块中的`fixture`可以轻松的访问`conftest.py`中同名的`fixture`；

### 16.3. 在用例参数中覆写`fixture`
假设我们有如下的测试项目：

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture
        def username():
            return 'username'

        @pytest.fixture
        def other_username(username):
            return 'other-' + username

    test_something.py
        # content of tests/test_something.py
        import pytest

        @pytest.mark.parametrize('username', ['directly-overridden-username'])
        def test_username(username):
            assert username == 'directly-overridden-username'

        @pytest.mark.parametrize('username', ['directly-overridden-username-other'])
        def test_username_other(other_username):
            assert other_username == 'other-directly-overridden-username-other'
```

可以看到：

- `fixture`的值被用例的参数所覆盖；
- 尽管用例`test_username_other`没有使用`username`，但是`other_username`使用到了`username`，所以也同样受到了影响；

### 16.4. 参数化的`fixture`覆写非参数化的`fixture`，反之亦然

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture(params=['one', 'two', 'three'])
        def parametrized_username(request):
            return request.param

        @pytest.fixture
        def non_parametrized_username(request):
            return 'username'

    test_something.py
        # content of tests/test_something.py
        import pytest

        @pytest.fixture
        def parametrized_username():
            return 'overridden-username'

        @pytest.fixture(params=['one', 'two', 'three'])
        def non_parametrized_username(request):
            return request.param

        def test_username(parametrized_username):
            assert parametrized_username == 'overridden-username'

        def test_parametrized_username(non_parametrized_username):
            assert non_parametrized_username in ['one', 'two', 'three']

    test_something_else.py
        # content of tests/test_something_else.py
        def test_username(parametrized_username):
            assert parametrized_username in ['one', 'two', 'three']

        def test_username(non_parametrized_username):
            assert non_parametrized_username == 'username'
```

可以看出：

- 参数化的`fixture`和非参数化的`fixture`同样可以相互覆盖；
- 在模块层级上的覆盖不会影响其它模块；
