'''
1 datetime:处理时间和日期的标准库
    datetime是模块，还包含一个datetime类
    datetime类可获取指定时间日期
    timestamp 时间戳 1970.1.1 00：00

    datetime和timestamp转换：fromtiemstamp()方法
    str转换为datetime:datetime.strptime()
    反之              datetime.strftime()

    datetime加减
2 collections:集合模块
    namedtuple:定义坐标,可根据属性来引用
    deque: 实现高效的插入和删除操作的双向列表，适用于队列和栈
          list线性存储，数据量大时，插入删除效率极低
    deque.append()  pop()  appendleft()  popleft()
    defaultdict: Key值不存在，设置默认值
    OrderedDict:   Key是无序，对dict做迭代 !
    ChainMap:   实现参数的优先级查找，命令行-->环境变量-->默认参数
    Counter： 简单计数器
    统计字符出现个数

3 Base64: 二进制编码方法，用64个字符来表示任意二进制数据的方法
    应用场景：URL cookie 网页中传少量的二进制数据

4 struct: 解决bytes和其它二进制数据类型的转换
    struct.pack('>I', obj)
    位图文件.bmp 采用小端方式储存数据

5 Hashlib: 提供常用摘要（哈希）算法，MD5, SHA1等
    作用：原始数据是否被篡改

6 Hmac: 根据不同口令生成不同的哈希（原始msg,随机key,哈希算法）
    防止黑客通过彩虹表攻击

7 itertools: 操作迭代对象函数
    count(1):创建一个无限迭代器
    cycle('123'):传入一个序列无限重复下去
    repeat('f', 3):可指定重复次数
    chain('aaa','bbb')：把一组迭代对象串联起来
    groupby():相邻重复元素挑出来放在一起
        for key,group in itertools.groupby('AADDD')
            print(key, list(group))

 8 contextlib: 文件处理，上下文管理
    @contextmanager:省去__enter__和__exit__ 同with open实现原理
    用于：代码执行前后自动执行特定代码
        @contextmanager
        def tag(name):
            print('<%s>'%name)
            yield
            print('<%s>'%name)
        with tag('h1'):
            print('hello')
    @closing：把对象变为上下文对象
    













'''
# 1 datetime
from datetime import datetime, timedelta

now = datetime.now()
print(now) # 获取当前日期时间
dt = datetime(2019,8,8,12,12)
print(dt)

cday = datetime.strptime('2018-12-12 12:12:12', '%Y-%m-%d %H:%M:%S')
print(cday)

now = datetime.now()
print(now.strftime('%a %b %d %H:%M:%S'))

from datetime import datetime, timedelta
now = datetime.now()
n1 = now + timedelta(hours=10)
n2 = now - timedelta(days=1)
n3 = now + timedelta(days=2, hours=12)
print(now, n1, n2, n3)

# 假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息
# 如UTC+5:00，均是str，请编写一个函数将其转换为timestamp

import re 
from datetime import datetime, timedelta, timezone

def to_timestamp(dt_str, tz_str):
    time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(
                            tzinfo=timezone(timedelta(hours=int(tz_str[3:-3]))))
    return time.timestamp()
# 测试
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
print(t1)



# COLLECTIONS
from collections import namedtuple
Point = namedtuple('Point',['x', 'y'])
p = Point(1,4)
print(p.x, p.y)

from collections import deque
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)

from collections import OrderedDict
d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)
print(list(od.keys()))


# 实现一个FIFO的dict,当容量达到上限时，删除最早加的key
from collections import OrderedDict

class MyOrderedDict(OrderedDict):
    def __init__(self, capacity):
        super(MyOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containKey = 1 if key in self else 0
        if len(self) - containKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)


# 查找user和color两个参数
from collections import ChainMap
import os, argparse

# 构造缺省参数
defaults = {
    'color' : 'red',
    'user'  : 'guest'
}

# 构造命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args()
command_line_args = {k: v for k, v in vars(namespace).items() if v}

# 组合成ChainMap
combined = ChainMap(command_line_args, os.environ, defaults)

# 打印参数
print('color=%s' % combined['color'])
print('user=%s' % combined['user'])
# 测试：命令行输入： python __init__.py --u lee
#          user=admin color= green python __init__.py --u lee


from collections import Counter
c = Counter()
for ch in 'hellopython':
    c[ch] += 1
print(c)


# 3 BASE64
# 自定义去除=的base64解码函数
import base64

def safe_base64_decode(s):
    mod = int(len(s) / 4)
    if 0 != mod:
        s = s + b"=" * (4 - mod)
    return base64.b64decode(s)


import hashlib

md5 = hashlib.md5()
md5.update('md5iigfdgjghfhf'.encode('utf-8'))
md5.update('md5iigfdgjghf'.encode('utf-8'))
print(md5.hexdigest())

#  1 设计一个验证用户登录的函数，根据用户输入的口令是否正确，
#  返回True或False
db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}

def login(user, password):
    md = hashlib.md5()
    md.update(password.encode('utf-8'))
    return db[user] == md.hexdigest()




# 2 根据用户输入的登录名和口令模拟用户注册，计算更安全的MD5

import hashlib, random

db = {}

def register(username, password):
    db[username] = get_md5(password +username + 'the-Salt')


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.slat = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = get_md5(password + self.slat)

db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}



def login(username, password):
    user  = db[username]
    password = password + user.salt
    return user.password == get_md5(password)


# 将salt改为标准的hmac算法，验证用户口令
def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)

db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}
def login(username, password):
    user = db[username]
    return user.password == hmac_md5(user.key, password)

from functools import reduce
# 计算pi的值
def pi(N):
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
    odd = itertools.count(1, 2)

    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
    ns = itertools.takewhile(lambda x: x <= 2*N-1, odd)

    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
    c = itertools.cycle([1, -1])
    ns = map(lambda x: (4 / x) * next(c), ns)

    # step 4: 求和:
    sums = reduce(lambda x, y: x+y, ns)
    return sums


# 把对象变为上下文
from contextlib import contextmanager
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)

@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()

