# latr #

Lazy iterator chains

## Purpose ##

At its core, ```latr``` simply provides a cleaner syntax for composing functions that return iterators.  So, instead of writing this:

```python
f = five(four(three(two(one(xrange(100))))))
```

You can write this:

```python
f = latr(xrange(100)) >> one >> two >> three >> four >> five
```



## Installation ##

```shell
pip install latr
```

