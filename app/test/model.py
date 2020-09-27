# @Time    : 2020/9/23 下午9:22

__author__ = 'xhb'


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

"""
1.插入数据（单条、批量、每次插入1000条）
2.删除，根据不同条件,truncate 表操作
3.查询：
   a. 查询结果排序取第一条
   b. 分组查询取第一条
   c. 多表连接查询
4.更新操作

高级操作：

"""
Base = declarative_base()


class Book(Base):
    """
        一些属性定义重复性比较大，元类可以解决这个问题
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column('author', String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))


class Drift(Base):
    __tablename__ = 'drift'

    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    _pending = Column('pending', SmallInteger, default=1)


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)


def save(table, data, num=2):
    """
    table 是表的映射类
    data: 是存入表中数据
    num 是多少条数据存入一次数据库
    """
    count = 0
    for i, d in enumerate(data):
        t = table()
        for k, v in d.items():
            if hasattr(t, k) and k!='id':
                setattr(t, k, v)
        print(dict(t.__dict__))
        session.add(t)

        if (i+1) % num == 0:
            session.commit()
            count += 1
    session.commit()
    count += 1
    print('提交次数：', count)


def save_books():
    data = [
        {
            'title': '书本1',
            'author': '',
            'binding': '',
            'publisher': '',
            'price': '',
            'pages': '',
            'pubdate': '',
            'isbn': 12,
            'summary': '',
            'image': '',
        }, {
            'title': '书本2',
            'author': '',
            'binding': '',
            'publisher': '',
            'price': '',
            'pages': '',
            'pubdate': '',
            'isbn': 13,
            'summary': '',
            'image': '',
        }, {
            'title': '书本3',
            'author': '',
            'binding': '',
            'publisher': '',
            'price': '',
            'pages': '',
            'pubdate': '',
            'isbn': 14,
            'summary': '',
            'image': '',
        }
    ]
    save(Book, data)


if __name__ == '__main__':
    engine = create_engine("sqlite:///kk.db",
                           echo=True
                           )

    # 建表
    # Base.metadata.create_all(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    save_books()


