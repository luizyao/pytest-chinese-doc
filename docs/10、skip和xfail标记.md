- [1. 跳过测试用例的执行](#1-跳过测试用例的执行)
  - [1.1. `@pytest.mark.skip`装饰器](#11-pytestmarkskip装饰器)
  - [1.2. `pytest.skip`方法](#12-pytestskip方法)
  - [1.3. `@pytest.mark.skipif`装饰器](#13-pytestmarkskipif装饰器)
  - [1.4. `pytest.importorskip`方法](#14-pytestimportorskip方法)
  - [1.5. 跳过测试类](#15-跳过测试类)
  - [1.6. 跳过测试模块](#16-跳过测试模块)
  - [1.7. 跳过指定文件或目录](#17-跳过指定文件或目录)
  - [1.8. 总结](#18-总结)
- [2. 标记用例为预期失败的](#2-标记用例为预期失败的)
  - [2.1. 去使能`xfail`标记](#21-去使能xfail标记)
- [3. 结合`pytest.param`方法](#3-结合pytestparam方法)

实际工作中，测试用例的执行可能会依赖于一些外部条件，例如：只能运行在某个特定的操作系统（`Windows`），或者我们本身期望它们测试失败，例如：被某个已知的`Bug`所阻塞；如果我们能为这些用例提前打上标记，那么`pytest`就相应地预处理它们，并提供一个更加准确的测试报告；

在这种场景下，常用的标记有：

- `skip`：只有当某些条件得到满足时，才执行测试用例，否则跳过整个测试用例的执行；例如，在非`Windows`平台上跳过只支持`Windows`系统的用例；
- `xfail`：因为一个确切的原因，我们知道这个用例会失败；例如，对某个未实现的功能的测试，或者阻塞于某个已知`Bug`的测试；

`pytest`默认不显示`skip`和`xfail`用例的详细信息，我们可以通过`-r`选项来自定义这种行为；

通常，我们使用一个字母作为一种类型的代表，具体的规则如下：

```bash
(f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed, (p)assed, (P)assed with output, (a)ll except passed(p/P), or (A)ll
```

例如，显示结果为`XFAIL`、`XPASS`和`SKIPPED`的用例：

```bash
pytest -rxXs
```

更多细节可以参考：[2、使用和调用 -- 总结报告](2、使用和调用.md#7-总结报告)


## 1. 跳过测试用例的执行

### 1.1. `@pytest.mark.skip`装饰器
跳过执行某个用例最简单的方式就是使用`@pytest.mark.skip`装饰器，并且可以设置一个可选参数`reason`，表明跳过的原因；

```python
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...
```

### 1.2. `pytest.skip`方法
如果我们想在测试执行期间（也可以在`SetUp/TearDown`期间）强制跳过后续的步骤，可以考虑`pytest.skip()`方法，它同样可以设置一个参数`msg`，表明跳过的原因；

```python
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

另外，我们还可以为其设置一个布尔型的参数`allow_module_level`（默认是`False`），表明是否允许在模块中调用这个方法，如果置为`True`，则跳过模块中剩余的部分；

例如，在`Windows`平台下，不测试这个模块：

```python
import sys
import pytest

if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)
```

> 注意：
>
> 当在用例中设置`allow_module_level`参数时，并不会生效；
>
> ```python
> def test_one():
>     pytest.skip("跳出", allow_module_level=True)
> 
> 
> def test_two():
>     assert 1
> ```
>
> 也就是说，在上述示例中，并不会跳过`test_two`用例；

### 1.3. `@pytest.mark.skipif`装饰器
如果我们想有条件的跳过某些测试用例的执行，可以使用`@pytest.mark.skipif`装饰器；

例如，当`python`的版本小于`3.6`时，跳过用例：

```python
import sys


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_function():
    ...
```

我们也可以在两个模块之间共享`pytest.mark.skipif`标记；

例如，我们在`test_module.py`中定义了`minversion`，表明当`python`的最低支持版本：

```python
# src/chapter-10/test_module.py

import sys

import pytest

minversion = pytest.mark.skipif(sys.version_info < (3, 8),
                                reason='请使用 python 3.8 或者更高的版本。')


@minversion
def test_one():
    assert True
```

并且，在`test_other_module.py`中引入了`minversion`：

```python
# src/chapter-10/test_other_module.py

from test_module import minversion


@minversion
def test_two():
    assert True
```

现在，我们来执行这两个用例（当前虚拟环境的`python`版本为`3.7.3`）：

```bash
λ pytest -rs -k 'module' src/chapter-10/
================================ test session starts ================================= 
platform win32 -- Python 3.7.3, pytest-5.1.3, py-1.8.0, pluggy-0.13.0
rootdir: D:\Personal Files\Projects\pytest-chinese-doc
collected 2 items

src\chapter-10\test_module.py s                                                 [ 50%] 
src\chapter-10\test_other_module.py s                                           [100%]

============================== short test summary info =============================== 
SKIPPED [1] src\chapter-10\test_module.py:29: 请使用 python 3.8 或者更高的版本。
SKIPPED [1] src\chapter-10\test_other_module.py:26: 请使用 python 3.8 或者更高的版本。
================================= 2 skipped in 0.03s =================================
```

可以看到，`minversion`在两个测试模块中都生效了；

因此，在大型的测试项目中，可以在一个文件中定义所有的执行条件，需要时再引入到模块中；

另外，需要注意的是，当一个用例指定了多个`skipif`条件时，只需满足其中一个，就可以跳过这个用例的执行；

> 注意：不存在`pytest.skipif()`的方法；

### 1.4. `pytest.importorskip`方法
当引入某个模块失败时，我们同样可以跳过后续部分的执行；

```python
docutils = pytest.importorskip("docutils")
```

我们也可以为其指定一个最低满足要求的版本，判断的依据是检查引入模块的`__version__ `属性：

```python
docutils = pytest.importorskip("docutils", minversion="0.3") 
```

我们还可以再为其指定一个`reason`参数，表明跳过的原因；

> 我们注意到`pytest.importorskip`和`pytest.skip(allow_module_level=True)`都可以在模块的引入阶段跳过剩余部分；实际上，在源码中它们抛出的都是同样的异常：
> 
> ```python
> # pytest.skip(allow_module_level=True)
> 
> raise Skipped(msg=msg, allow_module_level=allow_module_level)
> ```
> 
> ```python
> # pytest.importorskip()
> 
> raise Skipped(reason, allow_module_level=True) from None
> ```
> 
> 只是`importorskip`额外增加了`minversion`参数：
> 
> ```python
> # _pytest/outcomes.py
>  
> if minversion is None:
>         return mod
>     verattr = getattr(mod, "__version__", None)
>     if minversion is not None:
>         if verattr is None or Version(verattr) < Version(minversion):
>             raise Skipped(
>                 "module %r has __version__ %r, required is: %r"
>                 % (modname, verattr, minversion),
>                 allow_module_level=True,
>             )
> ```
> 
> 从中我们也证实了，它实际检查的是模块的`__version__`属性；
>
> 所以，对于一般场景下，使用下面的方法可以实现同样的效果：
> 
> ```python
> try:
>     import docutils
> except ImportError:
>     pytest.skip("could not import 'docutils': No module named 'docutils'",
>                 allow_module_level=True)
> ```

### 1.5. 跳过测试类
在类上应用`@pytest.mark.skip`或`@pytest.mark.skipif`：

```python
# src/chapter-10/test_skip_class.py

import pytest


@pytest.mark.skip("作用于类中的每一个用例，所以 pytest 共收集到两个 SKIPPED 的用例。")
class TestMyClass():
    def test_one(self):
        assert True

    def test_two(self):
        assert True
```

### 1.6. 跳过测试模块
在模块中定义`pytestmark`变量（推荐）：

```python
# src/chapter-10/test_skip_module.py

import pytest

pytestmark = pytest.mark.skip('作用于模块中的每一个用例，所以 pytest 共收集到两个 SKIPPED 的用例。')


def test_one():
    assert True


def test_two():
    assert True
```

或者，在模块中调用`pytest.skip`方法，并设置`allow_module_level=True`：

```python
# src/chapter-10/test_skip_module.py

import pytest

pytest.skip('在用例收集阶段就已经跳出了，所以不会收集到任何用例。', allow_module_level=True)


def test_one():
    assert True


def test_two():
    assert True
```

### 1.7. 跳过指定文件或目录
通过在`conftest.py`中配置`collect_ignore_glob`项，可以在用例的收集阶段跳过指定的文件和目录；

例如，跳过当前测试目录中文件名匹配`test_*.py`规则的文件和`config`的子文件夹`sub`中的文件：

```python
collect_ignore_glob = ['test*.py', 'config/sub']
```

更多细节可以参考：<https://docs.pytest.org/en/5.1.3/example/pythoncollection.html#customizing-test-collection>

### 1.8. 总结
|            | `pytest.mark.skip`                | `pytest.mark.skipif`                | `pytest.skip`                          | `pytest.importorskip`                | `conftest.py`         |
| ---------- | --------------------------------- | ----------------------------------- | -------------------------------------- | ------------------------------------ | --------------------- |
| 用例       | `@pytest.mark.skip()`             | `@pytest.mark.skipif()`             | `pytest.skip(msg='')`                  | /                                    | /                     |
| 类         | `@pytest.mark.skip()`             | `@pytest.mark.skipif()`             | /                                      | /                                    | /                     |
| 模块       | `pytestmark = pytest.mark.skip()` | `pytestmark = pytest.mark.skipif()` | `pytest.skip(allow_module_level=True)` | `pytestmark = pytest.importorskip()` | /                     |
| 文件或目录 | /                                 | /                                   | /                                      | /                                    | `collect_ignore_glob` |


## 2. 标记用例为预期失败的
我们可以使用`@pytest.mark.xfail`标记用例，表示期望这个用例执行失败；

用例会正常执行，只是失败时不再显示堆栈信息，最终的结果有两个：用例执行失败时（`XFAIL`：符合预期的失败）、用例执行成功时（`XPASS`：不符合预期的成功）

另外，我们也可以通过`pytest.xfail`方法在用例执行过程中直接标记用例结果为`XFAIL`，并跳过剩余的部分：

```python
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")
```

同样可以为`pytest.xfail`指定一个`reason`参数，表明原因；

下面我们来重点看一下`@pytest.mark.xfail`的用法：

- `condition`位置参数，默认值为`None`
  
    和`@pytest.mark.skipif`一样，它也可以接收一个`python`表达式，表明只有满足条件时才标记用例；

    例如，只在`pytest 3.6`版本以上标记用例：

    ```python
    @pytest.mark.xfail(sys.version_info >= (3, 6), reason="python3.6 api changes")
    def test_function():
        ...
    ```

- `reason`关键字参数，默认值为`None`

    可以指定一个字符串，表明标记用例的原因；

- `strict`关键字参数，默认值为`False`
  
    当`strict=False`时，如果用例执行失败，结果标记为`XFAIL`，表示符合预期的失败；如果用例执行成功，结果标记为`XPASS`，表示不符合预期的成功；

    当`strict=True`时，如果用例执行成功，结果将标记为`FAILED`，而不再是`XPASS`了；

    我们也可以在`pytest.ini`文件中配置：

    ```ini
    [pytest]
    xfail_strict=true
    ```

- `raises`关键字参数，默认值为`None`

    可以指定为一个异常类或者多个异常类的元组，表明我们期望用例上报指定的异常；
    
    如果用例的失败不是因为所期望的异常导致的，`pytest`将会把测试结果标记为`FAILED`;

- `run`关键字参数，默认值为`True`:
  
    当`run=False`时，`pytest`不会再执行测试用例，直接将结果标记为`XFAIL`；

我们以下表来总结不同参数组合对测试结果的影响（其中`xfail = pytest.mark.xfail`）：

|                                    | `@xfail()` | `@xfail(strict=True)` | `@xfail(raises=IndexError)` | `@xfail(strict=True, raises=IndexError)` | `@xfail(..., run=False)` |
| ---------------------------------- | ---------- | --------------------- | --------------------------- | ---------------------------------------- | ------------------------ |
| 用例测试成功                       | `XPASS`    | `FAILED`              | `XPASS`                     | `FAILED`                                 | `XFAIL`                  |
| 用例测试失败，上报`AssertionError` | `XFAIL`    | `XFAIL`               | `FAILED`                    | `FAILED`                                 | `XFAIL`                  |
| 用例上报`IndexError`               | `XFAIL`    | `XFAIL`               | `XFAIL`                     | `XFAIL`                                  | `XFAIL`                  |

### 2.1. 去使能`xfail`标记
我们可以通过命令行选项`pytest --runxfail`来去使能`xfail`标记，使这些用例变成正常执行的用例，仿佛没有被标记过一样：

同样，`pytest.xfail()`方法也将会失效；


## 3. 结合`pytest.param`方法
`pytest.param`方法可用于为`@pytest.mark.parametrize`或者参数化的`fixture`指定一个具体的实参，它有一个关键字参数`marks`，可以接收一个或一组标记，用于标记这轮测试的用例；

我们以下面的例子来说明：

```python
# src/chapter-10/test_params.py

import pytest
import sys


@pytest.mark.parametrize(
    ('n', 'expected'),
    [(2, 1),
     pytest.param(2, 1, marks=pytest.mark.xfail(), id='XPASS'),
     pytest.param(0, 1, marks=pytest.mark.xfail(raises=ZeroDivisionError), id='XFAIL'),
     pytest.param(1, 2, marks=pytest.mark.skip(reason='无效的参数，跳过执行')),
     pytest.param(1, 2, marks=pytest.mark.skipif(sys.version_info <= (3, 8), reason='请使用3.8及以上版本的python。'))])
def test_params(n, expected):
    assert 2 / n == expected
```

执行：

```bash
λ pytest -rA src/chapter-10/test_params.py
================================ test session starts ================================= 
platform win32 -- Python 3.7.3, pytest-5.1.3, py-1.8.0, pluggy-0.13.0
rootdir: D:\Personal Files\Projects\pytest-chinese-doc
collected 5 items

src\chapter-10\test_params.py .Xxss                                             [100%]

======================================= PASSES ======================================= 
============================== short test summary info =============================== 
PASSED src/chapter-10/test_params.py::test_params[2-1]
SKIPPED [1] src\chapter-10\test_params.py:26: 无效的参数，跳过执行
SKIPPED [1] src\chapter-10\test_params.py:26: 请使用3.8及以上版本的python。
XFAIL src/chapter-10/test_params.py::test_params[XFAIL]
XPASS src/chapter-10/test_params.py::test_params[XPASS]
================= 1 passed, 2 skipped, 1 xfailed, 1 xpassed in 0.08s =================
```

关于参数化的`fixture`的细节可以参考：[4、fixtures：明确的、模块化的和可扩展的 -- 在参数化的fixture中标记用例](4、fixtures：明确的、模块化的和可扩展的.md#11-在参数化的fixture中标记用例)
