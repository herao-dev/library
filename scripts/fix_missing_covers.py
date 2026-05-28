#!/usr/bin/env python3
"""
修复缺失的图书封面 - 手动指定封面URL
"""
import os
import sys
import urllib.request
import ssl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.book import Book

ssl._create_default_https_context = ssl._create_unverified_context

# 手动指定缺失封面的URL
MISSING_COVERS = {
    '活着': 'https://img9.doubanio.com/view/subject/l/public/s29053580.jpg',
}


def download_image(url, save_path):
    """下载图片到本地"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
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
        covers_dir = os.path.join(app.root_path, '..', 'static', 'uploads', 'covers')
        os.makedirs(covers_dir, exist_ok=True)
        
        for title, cover_url in MISSING_COVERS.items():
            book = Book.query.filter_by(title=title).first()
            if not book:
                print(f"未找到图书: {title}")
                continue
            
            print(f"\n处理: {title}")
            print(f"  封面URL: {cover_url}")
            
            safe_title = "".join(c for c in book.title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')
            image_filename = f"book_{book.id}_{safe_title}.jpg"
            save_path = os.path.join(covers_dir, image_filename)
            
            if download_image(cover_url, save_path):
                relative_path = f"uploads/covers/{image_filename}"
                book.cover_image = relative_path
                db.session.commit()
                print(f"  成功保存: {relative_path}")
            else:
                print(f"  失败")
        
        print("\n处理完成!")


if __name__ == '__main__':
    main()
