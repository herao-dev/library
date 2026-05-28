import click
from datetime import datetime, timedelta
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.book import Book
from app.models.borrow import BorrowRecord


@click.command('seed')
def seed_command():
    click.echo('开始填充种子数据...')

    if User.query.filter_by(username='admin').first():
        click.echo('种子数据已存在，跳过填充。')
        return

    admin = User(
        username='admin',
        email='admin@library.com',
        role='admin',
        phone='13800000000',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    user1 = User(username='zhangsan', email='zhangsan@example.com', role='user', phone='13800000001')
    user1.set_password('123456')
    db.session.add(user1)

    user2 = User(username='lisi', email='lisi@example.com', role='user', phone='13800000002')
    user2.set_password('123456')
    db.session.add(user2)

    user3 = User(username='wangwu', email='wangwu@example.com', role='user', phone='13800000003')
    user3.set_password('123456')
    db.session.add(user3)

    db.session.flush()

    categories_data = [
        ('计算机科学', '计算机编程、软件开发、人工智能等相关书籍'),
        ('文学小说', '中外文学名著、现代小说、散文诗歌'),
        ('历史地理', '历史研究、地理探索、人文社科'),
        ('科学技术', '自然科学、工程技术、医学健康'),
        ('经济管理', '经济学、管理学、市场营销、金融投资'),
        ('哲学心理', '哲学思想、心理学、心灵成长'),
        ('艺术设计', '绘画、设计、摄影、音乐、建筑'),
        ('教育学习', '教材教辅、语言学习、考试用书'),
    ]
    categories = []
    for name, desc in categories_data:
        cat = Category(name=name, description=desc)
        db.session.add(cat)
        categories.append(cat)

    db.session.flush()

    books_data = [
        ('Python编程：从入门到实践', 'Eric Matthes', '978-7-115-54608-1', '人民邮电出版社', '2020-10-01', 0, 5, 5, 'A-01-01', 'Python入门经典教程，涵盖基础语法、项目实践'),
        ('深入理解计算机系统', 'Randal E. Bryant', '978-7-111-54493-7', '机械工业出版社', '2016-11-01', 0, 3, 3, 'A-01-02', '从程序员视角深入理解计算机系统核心概念'),
        ('算法导论（第三版）', 'Thomas H. Cormen', '978-7-111-40701-0', '机械工业出版社', '2013-01-01', 0, 2, 2, 'A-01-03', '计算机算法领域的经典权威教材'),
        ('活着', '余华', '978-7-5302-2153-2', '北京十月文艺出版社', '2017-06-01', 1, 8, 8, 'B-02-01', '讲述了一个人一生的故事，展现生命的坚韧与苦难'),
        ('百年孤独', '加西亚·马尔克斯', '978-7-5442-5399-4', '南海出版公司', '2011-06-01', 1, 4, 4, 'B-02-02', '魔幻现实主义文学的代表作，拉丁美洲的史诗'),
        ('三体', '刘慈欣', '978-7-5366-9293-0', '重庆出版社', '2008-01-01', 1, 6, 6, 'B-02-03', '中国科幻文学的里程碑之作，雨果奖获奖作品'),
        ('人类简史', '尤瓦尔·赫拉利', '978-7-5086-4735-7', '中信出版社', '2014-11-01', 2, 5, 5, 'C-03-01', '从认知革命到科学革命，人类历史的宏大叙事'),
        ('万历十五年', '黄仁宇', '978-7-101-11823-0', '中华书局', '2007-01-01', 2, 3, 3, 'C-03-02', '以万历十五年为切入点，剖析明朝政治制度'),
        ('时间简史', '史蒂芬·霍金', '978-7-5357-8779-8', '湖南科学技术出版社', '2010-04-01', 3, 3, 3, 'D-04-01', '探索宇宙起源、黑洞、时间本质的科普经典'),
        ('自私的基因', '理查德·道金斯', '978-7-5086-9449-8', '中信出版社', '2018-11-01', 3, 2, 2, 'D-04-02', '从基因视角解释进化论，颠覆对生命的认知'),
        ('经济学原理：微观经济学分册', 'N. Gregory Mankiw', '978-7-301-25089-3', '北京大学出版社', '2015-05-01', 4, 4, 4, 'E-05-01', '全球最受欢迎的经济学入门教材'),
        ('思考，快与慢', '丹尼尔·卡尼曼', '978-7-5086-3355-8', '中信出版社', '2012-07-01', 5, 3, 3, 'F-06-01', '诺贝尔经济学奖得主关于人类决策与判断的研究'),
        ('设计中的设计', '原研哉', '978-7-209-04106-5', '山东人民出版社', '2006-11-01', 6, 2, 2, 'G-07-01', '日本设计大师对设计本质的深度思考'),
        ('新概念英语2', 'L.G. Alexander', '978-7-5600-1347-3', '外语教学与研究出版社', '1997-10-01', 7, 10, 10, 'H-08-01', '经典英语学习教材，适合初中级学习者'),
    ]

    books = []
    for title, author, isbn, publisher, pub_date, cat_idx, total, avail, loc, desc in books_data:
        book = Book(
            title=title, author=author, isbn=isbn, publisher=publisher,
            publish_date=datetime.strptime(pub_date, '%Y-%m-%d').date() if pub_date else None,
            category_id=categories[cat_idx].id,
            total_copies=total, available_copies=avail,
            location=loc, description=desc
        )
        db.session.add(book)
        books.append(book)

    db.session.flush()

    now = datetime.utcnow()
    records_data = [
        (user1, books[0], now - timedelta(days=45), now - timedelta(days=15), now - timedelta(days=25), 'returned'),
        (user1, books[3], now - timedelta(days=31), now - timedelta(days=1), None, 'borrowed'),
        (user2, books[5], now - timedelta(days=57), now - timedelta(days=27), None, 'overdue'),
        (user2, books[8], now - timedelta(days=36), now - timedelta(days=6), now - timedelta(days=11), 'returned'),
        (user3, books[10], now - timedelta(days=26), now + timedelta(days=4), None, 'borrowed'),
    ]

    for user, book, borrow_date, due_date, return_date, status in records_data:
        record = BorrowRecord(
            user_id=user.id, book_id=book.id,
            borrow_date=borrow_date, due_date=due_date,
            return_date=return_date, status=status
        )
        db.session.add(record)

    db.session.commit()
    click.echo('种子数据填充完成！')
    click.echo('  管理员: admin / admin123')
    click.echo('  用户: zhangsan / 123456')
    click.echo('  用户: lisi / 123456')
    click.echo('  用户: wangwu / 123456')