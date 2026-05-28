-- ============================================
-- 图书管理系统 - MySQL 数据库脚本
-- 适用于 Navicat 导入
-- ============================================

CREATE DATABASE IF NOT EXISTS `library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `library`;

-- ============================================
-- 删除表（按依赖顺序）
-- ============================================
DROP TABLE IF EXISTS `review`;
DROP TABLE IF EXISTS `reservation`;
DROP TABLE IF EXISTS `announcement`;
DROP TABLE IF EXISTS `borrow_record`;
DROP TABLE IF EXISTS `book`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `user`;

-- ============================================
-- 用户表
-- ============================================
CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `password_hash` VARCHAR(256) NOT NULL,
    `role` VARCHAR(16) NOT NULL DEFAULT 'user',
    `phone` VARCHAR(20) DEFAULT NULL,
    `avatar` VARCHAR(256) DEFAULT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 分类表
-- ============================================
CREATE TABLE `category` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    `description` TEXT DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 图书表
-- ============================================
CREATE TABLE `book` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(256) NOT NULL,
    `author` VARCHAR(128) NOT NULL,
    `isbn` VARCHAR(20) DEFAULT NULL,
    `publisher` VARCHAR(128) DEFAULT NULL,
    `publish_date` DATE DEFAULT NULL,
    `category_id` INT DEFAULT NULL,
    `total_copies` INT NOT NULL DEFAULT 1,
    `available_copies` INT NOT NULL DEFAULT 1,
    `cover_image` VARCHAR(256) DEFAULT NULL,
    `description` TEXT DEFAULT NULL,
    `location` VARCHAR(64) DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_isbn` (`isbn`),
    KEY `idx_category_id` (`category_id`),
    CONSTRAINT `fk_book_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 借阅记录表
-- ============================================
CREATE TABLE `borrow_record` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `borrow_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `due_date` DATETIME NOT NULL,
    `return_date` DATETIME DEFAULT NULL,
    `status` VARCHAR(16) NOT NULL DEFAULT 'borrowed',
    `fine` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_book_id` (`book_id`),
    KEY `idx_status` (`status`),
    CONSTRAINT `fk_borrow_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_borrow_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 预约表
-- ============================================
CREATE TABLE `reservation` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `reserve_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status` VARCHAR(16) NOT NULL DEFAULT 'pending',
    `notify_date` DATETIME DEFAULT NULL,
    `expire_date` DATETIME DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_reservation_user` (`user_id`),
    KEY `idx_reservation_book` (`book_id`),
    KEY `idx_reservation_status` (`status`),
    CONSTRAINT `fk_reservation_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_reservation_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 评论表
-- ============================================
CREATE TABLE `review` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `rating` INT NOT NULL DEFAULT 5,
    `content` TEXT DEFAULT NULL,
    `is_visible` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_review_user` (`user_id`),
    KEY `idx_review_book` (`book_id`),
    CONSTRAINT `fk_review_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_review_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 公告表
-- ============================================
CREATE TABLE `announcement` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(256) NOT NULL,
    `content` TEXT NOT NULL,
    `priority` VARCHAR(16) NOT NULL DEFAULT 'normal',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1,
    `publisher_id` INT DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_announcement_publisher` (`publisher_id`),
    CONSTRAINT `fk_announcement_publisher` FOREIGN KEY (`publisher_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 种子数据
-- ============================================

管理员账号 (密码: admin123)
INSERT INTO `user` (`username`, `email`, `password_hash`, `role`, `phone`, `is_active`) VALUES
('admin', 'admin@library.com', 'scrypt:32768:8:1$J5CeUn4fP2jepB4R$09012b13b021de99328724abf90bd03e03fc5d8fa92cf843c1c8e4a261455ffc98c89afaad01f526ea0ed34f069099ab99c6c662c0a6dacfe23c4308e48df3588', 'admin', '13800000000', 1);

-- 普通用户 (密码: 123456)
INSERT INTO `user` (`username`, `email`, `password_hash`, `role`, `phone`, `is_active`) VALUES
-- ('admin', 'admin@library.com', 'scrypt:32768:8:1$J5CeUn4fP2jepB4R$09012b13b021de99328724abf90bd03e03fc5d8fa92cf843c1c8e4a261455ffc98c89afaad01f526ea0ed34f069099ab99c6c662c0a6dacfe23c4308e48df3588', 'admin', '13800000000', 1),
('zhangsan', 'zhangsan@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000001', 1),
('lisi', 'lisi@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000002', 1),
('wangwu', 'wangwu@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000003', 1),
('zhaoliu', 'zhaoliu@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000004', 1),
('sunqi', 'sunqi@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000005', 1),
('zhouba', 'zhouba@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000006', 1),
('wujiu', 'wujiu@example.com', 'scrypt:32768:8:1$wdpbP8RZ1su1rd4j$02681420034cc99492b9c0294cd90235aeb73b9bec852bb6a6062d961f8898eb834456e17638108af4c657aa35243262e96fbd9fe41b0e74e7a9393ae2db8a86', 'user', '13800000007', 1);

-- 图书分类
INSERT INTO `category` (`name`, `description`) VALUES
('计算机科学', '计算机编程、软件开发、人工智能等相关书籍'),
('文学小说', '中外文学名著、现代小说、散文诗歌'),
('历史地理', '历史研究、地理探索、人文社科'),
('科学技术', '自然科学、工程技术、医学健康'),
('经济管理', '经济学、管理学、市场营销、金融投资'),
('哲学心理', '哲学思想、心理学、心灵成长'),
('艺术设计', '绘画、设计、摄影、音乐、建筑'),
('教育学习', '教材教辅、语言学习、考试用书');

-- 图书数据（扩充至 24 本）
INSERT INTO `book` (`title`, `author`, `isbn`, `publisher`, `publish_date`, `category_id`, `total_copies`, `available_copies`, `location`, `description`) VALUES
-- 计算机科学 (category_id=1)
('Python编程：从入门到实践', 'Eric Matthes', '978-7-115-54608-1', '人民邮电出版社', '2020-10-01', 1, 5, 4, 'A-01-01', 'Python入门经典教程，涵盖基础语法、项目实践，适合零基础学习者。'),
('深入理解计算机系统', 'Randal E. Bryant', '978-7-111-54493-7', '机械工业出版社', '2016-11-01', 1, 3, 3, 'A-01-02', '从程序员视角深入理解计算机系统核心概念，CSAPP经典教材。'),
('算法导论（第三版）', 'Thomas H. Cormen', '978-7-111-40701-0', '机械工业出版社', '2013-01-01', 1, 2, 2, 'A-01-03', '计算机算法领域的经典权威教材，涵盖排序、图算法、动态规划等。'),
('JavaScript高级程序设计', 'Matt Frisbie', '978-7-115-53539-0', '人民邮电出版社', '2020-12-01', 1, 4, 4, 'A-01-04', '前端开发必读红宝书，深入讲解JavaScript核心概念与高级特性。'),
('数据库系统概念', 'Abraham Silberschatz', '978-7-111-61821-8', '机械工业出版社', '2019-08-01', 1, 3, 3, 'A-01-05', '数据库领域经典教材，涵盖关系模型、SQL、事务管理等核心内容。'),
-- 文学小说 (category_id=2)
('活着', '余华', '978-7-5302-2153-2', '北京十月文艺出版社', '2017-06-01', 2, 8, 7, 'B-02-01', '讲述了一个人一生的故事，展现生命的坚韧与苦难，余华代表作。'),
('百年孤独', '加西亚·马尔克斯', '978-7-5442-5399-4', '南海出版公司', '2011-06-01', 2, 4, 4, 'B-02-02', '魔幻现实主义文学的代表作，布恩迪亚家族七代人的传奇故事。'),
('三体', '刘慈欣', '978-7-5366-9293-0', '重庆出版社', '2008-01-01', 2, 6, 5, 'B-02-03', '中国科幻文学的里程碑之作，雨果奖获奖作品，三体三部曲第一部。'),
('围城', '钱钟书', '978-7-02-007002-2', '人民文学出版社', '1991-02-01', 2, 5, 5, 'B-02-04', '中国现代文学经典，以幽默犀利的笔触描绘知识分子的困境。'),
('挪威的森林', '村上春树', '978-7-5327-4292-9', '上海译文出版社', '2007-07-01', 2, 4, 4, 'B-02-05', '村上春树代表作，关于青春、爱情与死亡的动人故事。'),
-- 历史地理 (category_id=3)
('人类简史', '尤瓦尔·赫拉利', '978-7-5086-4735-7', '中信出版社', '2014-11-01', 3, 5, 5, 'C-03-01', '从认知革命到科学革命，以宏大视角审视人类历史发展。'),
('万历十五年', '黄仁宇', '978-7-101-11823-0', '中华书局', '2007-01-01', 3, 3, 3, 'C-03-02', '以万历十五年为切入点，剖析明朝政治制度与社会结构。'),
('枪炮、病菌与钢铁', '贾雷德·戴蒙德', '978-7-5086-4323-6', '中信出版社', '2016-07-01', 3, 3, 3, 'C-03-03', '探讨人类社会发展差异的根源，普利策奖获奖作品。'),
-- 科学技术 (category_id=4)
('时间简史', '史蒂芬·霍金', '978-7-5357-8779-8', '湖南科学技术出版社', '2010-04-01', 4, 3, 3, 'D-04-01', '探索宇宙起源、黑洞、时间本质的科普经典之作。'),
('自私的基因', '理查德·道金斯', '978-7-5086-9449-8', '中信出版社', '2018-11-01', 4, 2, 2, 'D-04-02', '从基因视角解释进化论，颠覆对生命与自然选择的认知。'),
-- 经济管理 (category_id=5)
('经济学原理：微观经济学分册', 'N. Gregory Mankiw', '978-7-301-25089-3', '北京大学出版社', '2015-05-01', 5, 4, 4, 'E-05-01', '全球最受欢迎的经济学入门教材，通俗易懂的经济学原理。'),
('从0到1', 'Peter Thiel', '978-7-5086-4971-9', '中信出版社', '2015-01-01', 5, 3, 3, 'E-05-02', '硅谷创投教父关于创业与创新的独特思考。'),
-- 哲学心理 (category_id=6)
('思考，快与慢', '丹尼尔·卡尼曼', '978-7-5086-3355-8', '中信出版社', '2012-07-01', 6, 3, 3, 'F-06-01', '诺贝尔经济学奖得主关于人类决策与判断的经典研究。'),
('被讨厌的勇气', '岸见一郎', '978-7-111-49548-2', '机械工业出版社', '2015-03-01', 6, 4, 4, 'F-06-02', '基于阿德勒心理学的自我启发之书，关于幸福与自由。'),
-- 艺术设计 (category_id=7)
('设计中的设计', '原研哉', '978-7-209-04106-5', '山东人民出版社', '2006-11-01', 7, 2, 2, 'G-07-01', '日本设计大师对设计本质的深度思考与探索。'),
('写给大家看的设计书', 'Robin Williams', '978-7-115-39440-8', '人民邮电出版社', '2016-01-01', 7, 3, 3, 'G-07-02', '设计入门经典，讲解亲密性、对齐、重复、对比四大原则。'),
-- 教育学习 (category_id=8)
('新概念英语2', 'L.G. Alexander', '978-7-5600-1347-3', '外语教学与研究出版社', '1997-10-01', 8, 10, 10, 'H-08-01', '经典英语学习教材，适合初中级学习者，实践与渐进。'),
('如何阅读一本书', 'Mortimer J. Adler', '978-7-100-04094-5', '商务印书馆', '2004-01-01', 8, 4, 4, 'H-08-02', '关于阅读方法与技巧的经典指南，提升阅读层次。');

-- 借阅记录（丰富示例数据）
INSERT INTO `borrow_record` (`user_id`, `book_id`, `borrow_date`, `due_date`, `return_date`, `status`, `fine`) VALUES
-- zhangsan 的借阅记录
(2, 1, '2026-04-01 10:00:00', '2026-05-01 10:00:00', '2026-04-20 14:30:00', 'returned', 0.00),
(2, 4, '2026-04-15 09:00:00', '2026-05-15 09:00:00', NULL, 'borrowed', 0.00),
(2, 7, '2026-03-10 08:00:00', '2026-04-10 08:00:00', '2026-04-25 16:00:00', 'returned', 7.50),
-- lisi 的借阅记录
(3, 6, '2026-03-20 11:00:00', '2026-04-20 11:00:00', NULL, 'overdue', 0.00),
(3, 9, '2026-04-10 15:00:00', '2026-05-10 15:00:00', '2026-05-05 10:00:00', 'returned', 0.00),
(3, 12, '2026-05-01 09:30:00', '2026-06-01 09:30:00', NULL, 'borrowed', 0.00),
-- wangwu 的借阅记录
(4, 11, '2026-04-20 08:30:00', '2026-05-20 08:30:00', NULL, 'borrowed', 0.00),
(4, 16, '2026-02-15 10:00:00', '2026-03-15 10:00:00', '2026-03-20 14:00:00', 'returned', 2.50),
-- zhaoliu 的借阅记录
(5, 8, '2026-04-25 13:00:00', '2026-05-25 13:00:00', NULL, 'borrowed', 0.00),
(5, 14, '2026-03-01 09:00:00', '2026-04-01 09:00:00', '2026-04-10 11:00:00', 'returned', 4.50),
-- sunqi 的借阅记录
(6, 18, '2026-05-05 10:00:00', '2026-06-05 10:00:00', NULL, 'borrowed', 0.00),
(6, 2, '2026-01-10 14:00:00', '2026-02-10 14:00:00', '2026-02-08 16:00:00', 'returned', 0.00),
-- zhouba 的借阅记录
(7, 20, '2026-04-28 11:00:00', '2026-05-28 11:00:00', NULL, 'borrowed', 0.00),
(7, 5, '2026-02-20 08:00:00', '2026-03-20 08:00:00', '2026-03-18 10:00:00', 'returned', 0.00),
-- wujiu 的借阅记录
(8, 22, '2026-05-08 15:00:00', '2026-06-08 15:00:00', NULL, 'borrowed', 0.00),
(8, 13, '2026-03-05 09:00:00', '2026-04-05 09:00:00', '2026-04-15 17:00:00', 'returned', 5.00);

-- 预约记录
INSERT INTO `reservation` (`user_id`, `book_id`, `reserve_date`, `status`) VALUES
(3, 3, '2026-05-10 10:00:00', 'pending'),
(5, 15, '2026-05-08 14:00:00', 'pending'),
(6, 10, '2026-04-20 09:00:00', 'fulfilled'),
(7, 17, '2026-05-12 11:00:00', 'pending'),
(4, 19, '2026-04-15 16:00:00', 'cancelled');

-- 评论数据
INSERT INTO `review` (`user_id`, `book_id`, `rating`, `content`, `is_visible`, `created_at`) VALUES
(2, 1, 5, '非常棒的Python入门书，讲解清晰，项目实战很有帮助！', 1, '2026-04-25 10:00:00'),
(2, 7, 5, '余华的文字有一种直击人心的力量，读完后久久不能平静。', 1, '2026-04-26 14:00:00'),
(3, 6, 4, '想象力惊人，硬科幻的典范。有些物理概念需要反复阅读才能理解。', 1, '2026-04-10 09:00:00'),
(3, 9, 5, '霍金用通俗的语言讲述了宇宙的奥秘，科普读物的巅峰之作。', 1, '2026-05-06 11:00:00'),
(4, 11, 4, '视角宏大，对人类历史的梳理非常清晰，值得反复阅读。', 1, '2026-05-02 15:00:00'),
(4, 16, 5, '经济学入门必读，曼昆的讲解深入浅出，案例丰富。', 1, '2026-03-22 10:00:00'),
(5, 8, 5, '中国科幻的骄傲！黑暗森林法则令人深思，期待后续两部。', 1, '2026-05-01 08:00:00'),
(5, 14, 4, '虽然有些内容已经过时，但作为科普经典仍然值得一读。', 1, '2026-04-12 16:00:00'),
(6, 18, 5, '卡尼曼的研究改变了我们对决策的理解，系统1和系统2的概念非常实用。', 1, '2026-05-06 13:00:00'),
(6, 2, 4, 'CSAPP是每个程序员都应该读的书，对理解底层原理帮助极大。', 1, '2026-02-10 09:00:00'),
(7, 20, 5, '原研哉的设计哲学令人耳目一新，\"空\"的概念很有启发性。', 1, '2026-05-03 10:00:00'),
(7, 5, 4, '数据库领域的圣经级教材，内容全面但有些章节偏理论。', 1, '2026-03-20 14:00:00'),
(8, 22, 5, '经典英语教材，循序渐进，适合自学。配套练习很有帮助。', 1, '2026-05-10 09:00:00'),
(8, 13, 5, '戴蒙德的宏大叙事令人叹服，地理决定论的视角很有说服力。', 1, '2026-04-16 11:00:00'),
(2, 12, 4, '黄仁宇的大历史观很有特色，对明朝制度的分析入木三分。', 1, '2026-04-28 15:00:00'),
(3, 17, 4, 'Peter Thiel的创业思维很有启发性，\"从0到1\"的理念值得深思。', 1, '2026-05-07 10:00:00');

-- 公告数据
INSERT INTO `announcement` (`title`, `content`, `priority`, `is_published`, `publisher_id`, `created_at`) VALUES
('图书馆五一假期开放安排', '各位读者：五一劳动节期间（5月1日至5月5日），图书馆开放时间调整为9:00-17:00，5月6日起恢复正常开放时间。祝大家节日快乐！', 'important', 1, 1, '2026-04-28 09:00:00'),
('新书上架通知', '图书馆近期新购入一批图书，涵盖计算机科学、文学小说、经济管理等多个类别，共计50余册，欢迎广大读者前来借阅。', 'normal', 1, 1, '2026-05-05 10:00:00'),
('关于逾期图书归还的紧急通知', '请以下读者尽快归还逾期图书：lisi（《三体》）、wangwu（《经济学原理》）。逾期将按每日0.50元收取罚金，请相互转告。', 'urgent', 1, 1, '2026-05-10 08:00:00'),
('图书馆借阅规则更新', '为更好地服务读者，图书馆对借阅规则进行了优化：每位读者最多可同时借阅5本图书，借阅期限为30天，可续借一次（15天）。预约功能已上线，库存不足时可预约排队。', 'normal', 1, 1, '2026-05-12 14:00:00'),
('读者评论功能上线', '图书馆新增图书评论与评分功能，欢迎各位读者在归还图书后发表您的阅读感受和评价，帮助其他读者选择好书！', 'normal', 1, 1, '2026-05-15 09:00:00');