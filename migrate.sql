-- ============================================
-- 图书管理系统 - 数据库迁移脚本（修复版）
-- 为已有数据库添加新字段和新表
-- ============================================

USE `library`;

-- 1. 为 borrow_record 表添加 fine 字段（仅当不存在时）
SET @sql_fine = (
    SELECT IF(
        COUNT(*) = 0,
        'ALTER TABLE `borrow_record` ADD COLUMN `fine` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 AFTER `status`',
        'SELECT ''fine column already exists, skipping...'''
    )
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = 'library'
      AND TABLE_NAME = 'borrow_record'
      AND COLUMN_NAME = 'fine'
);
PREPARE stmt FROM @sql_fine;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. 创建预约表
CREATE TABLE IF NOT EXISTS `reservation` (
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

-- 3. 创建评论表
CREATE TABLE IF NOT EXISTS `review` (
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

-- 4. 创建公告表
CREATE TABLE IF NOT EXISTS `announcement` (
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

-- 5. 插入种子数据
INSERT IGNORE INTO `reservation` (`user_id`, `book_id`, `reserve_date`, `status`) VALUES
(3, 3, '2026-05-10 10:00:00', 'pending'),
(5, 15, '2026-05-08 14:00:00', 'pending'),
(6, 10, '2026-04-20 09:00:00', 'fulfilled'),
(7, 17, '2026-05-12 11:00:00', 'pending'),
(4, 19, '2026-04-15 16:00:00', 'cancelled');

INSERT IGNORE INTO `review` (`user_id`, `book_id`, `rating`, `content`, `is_visible`, `created_at`) VALUES
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
(7, 20, 5, '原研哉的设计哲学令人耳目一新，"空"的概念很有启发性。', 1, '2026-05-03 10:00:00'),
(7, 5, 4, '数据库领域的圣经级教材，内容全面但有些章节偏理论。', 1, '2026-03-20 14:00:00'),
(8, 22, 5, '经典英语教材，循序渐进，适合自学。配套练习很有帮助。', 1, '2026-05-10 09:00:00'),
(8, 13, 5, '戴蒙德的宏大叙事令人叹服，地理决定论的视角很有说服力。', 1, '2026-04-16 11:00:00'),
(2, 12, 4, '黄仁宇的大历史观很有特色，对明朝制度的分析入木三分。', 1, '2026-04-28 15:00:00'),
(3, 17, 4, 'Peter Thiel的创业思维很有启发性，"从0到1"的理念值得深思。', 1, '2026-05-07 10:00:00');

INSERT IGNORE INTO `announcement` (`title`, `content`, `priority`, `is_published`, `publisher_id`, `created_at`) VALUES
('图书馆五一假期开放安排', '各位读者：五一劳动节期间（5月1日至5月5日），图书馆开放时间调整为9:00-17:00，5月6日起恢复正常开放时间。祝大家节日快乐！', 'important', 1, 1, '2026-04-28 09:00:00'),
('新书上架通知', '图书馆近期新购入一批图书，涵盖计算机科学、文学小说、经济管理等多个类别，共计50余册，欢迎广大读者前来借阅。', 'normal', 1, 1, '2026-05-05 10:00:00'),
('关于逾期图书归还的紧急通知', '请以下读者尽快归还逾期图书：lisi（《三体》）、wangwu（《经济学原理》）。逾期将按每日0.50元收取罚金，请相互转告。', 'urgent', 1, 1, '2026-05-10 08:00:00'),
('图书馆借阅规则更新', '为更好地服务读者，图书馆对借阅规则进行了优化：每位读者最多可同时借阅5本图书，借阅期限为30天，可续借一次（15天）。预约功能已上线，库存不足时可预约排队。', 'normal', 1, 1, '2026-05-12 14:00:00'),
('读者评论功能上线', '图书馆新增图书评论与评分功能，欢迎各位读者在归还图书后发表您的阅读感受和评价，帮助其他读者选择好书！', 'normal', 1, 1, '2026-05-15 09:00:00');