#!/usr/bin/env python3
"""
批量获取图书封面图片并更新数据库
使用豆瓣图书搜索API获取封面图片URL
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
import ssl

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.book import Book

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 图书封面映射（书名 -> 豆瓣搜索关键词）
BOOK_COVER_MAP = {
    'Python编程：从入门到实践': 'Python编程从入门到实践',
    '深入理解计算机系统': '深入理解计算机系统',
    '算法导论（第三版）': '算法导论',
    'JavaScript高级程序设计': 'JavaScript高级程序设计',
    '数据库系统概念': '数据库系统概念',
    '活着': '活着 余华',
    '百年孤独': '百年孤独',
    '三体': '三体',
    '围城': '围城 钱钟书',
    '挪威的森林': '挪威的森林',
    '人类简史': '人类简史',
    '万历十五年': '万历十五年',
    '枪炮、病菌与钢铁': '枪炮病菌与钢铁',
    '时间简史': '时间简史',
    '自私的基因': '自私的基因',
    '经济学原理：微观经济学分册': '经济学原理 曼昆',
    '从0到1': '从0到1',
    '思考，快与慢': '思考快与慢',
    '被讨厌的勇气': '被讨厌的勇气',
    '设计中的设计': '设计中的设计',
    '写给大家看的设计书': '写给大家看的设计书',
    '新概念英语2': '新概念英语2',
    '如何阅读一本书': '如何阅读一本书',
}


def search_douban_book(query):
    """搜索豆瓣图书，返回封面图片URL"""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f'https://book.douban.com/j/subject_suggest?q={encoded_query}'
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://book.douban.com/'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data and len(data) > 0:
                # 返回第一个结果的封面图片URL
                first_result = data[0]
                cover_url = first_result.get('pic', '')
                if cover_url:
                    # 将缩略图URL转换为高清图URL
                    cover_url = cover_url.replace('/s/', '/l/')
                    return cover_url
            return None
    except Exception as e:
        print(f"  搜索失败: {e}")
        return None


def download_image(url, save_path):
    """下载图片到本地"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://book.douban.com/'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(save_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False


def main():
    app = create_app()
    
    with app.app_context():
        # 创建封面图片保存目录
        covers_dir = os.path.join(app.root_path, '..', 'static', 'uploads', 'covers')
        os.makedirs(covers_dir, exist_ok=True)
        
        # 获取所有图书
        books = Book.query.all()
        print(f"共找到 {len(books)} 本图书")
        print("-" * 60)
        
        success_count = 0
        skip_count = 0
        fail_count = 0
        
        for book in books:
            print(f"\n处理: {book.title}")
            
            # 检查是否已有封面
            if book.cover_image and book.cover_image.strip():
                print(f"  已有封面，跳过")
                skip_count += 1
                continue
            
            # 获取搜索关键词
            search_query = BOOK_COVER_MAP.get(book.title, book.title)
            print(f"  搜索关键词: {search_query}")
            
            # 搜索豆瓣图书
            cover_url = search_douban_book(search_query)
            
            if not cover_url:
                print(f"  未找到封面图片")
                fail_count += 1
                continue
            
            print(f"  找到封面: {cover_url}")
            
            # 下载图片
            safe_title = "".join(c for c in book.title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')
            image_filename = f"book_{book.id}_{safe_title}.jpg"
            save_path = os.path.join(covers_dir, image_filename)
            
            if download_image(cover_url, save_path):
                # 更新数据库
                relative_path = f"uploads/covers/{image_filename}"
                book.cover_image = relative_path
                db.session.commit()
                print(f"  成功保存: {relative_path}")
                success_count += 1
            else:
                fail_count += 1
            
            # 添加延迟，避免请求过快
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print(f"处理完成!")
        print(f"  成功: {success_count}")
        print(f"  跳过(已有封面): {skip_count}")
        print(f"  失败: {fail_count}")


if __name__ == '__main__':
    main()
