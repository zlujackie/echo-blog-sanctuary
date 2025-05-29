
"""
数据库初始化脚本
创建初始管理员用户和示例数据
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Article
from auth import get_password_hash
from datetime import datetime

def init_database():
    """初始化数据库"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 创建管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("创建管理员用户...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("管理员用户创建成功！用户名: admin, 密码: admin123")
        
        # 创建示例文章
        if db.query(Article).count() == 0:
            print("创建示例文章...")
            sample_articles = [
                {
                    "title": "探索现代前端开发的最新趋势",
                    "content": """
                    <h2>前端开发的演进</h2>
                    <p>现代前端开发正在经历快速的变化。从传统的 jQuery 到现在的 React、Vue 和 Angular，技术栈变得越来越丰富。</p>
                    
                    <h2>主要趋势</h2>
                    <ul>
                        <li>组件化开发</li>
                        <li>TypeScript 的普及</li>
                        <li>服务端渲染（SSR）</li>
                        <li>微前端架构</li>
                    </ul>
                    
                    <p>这些趋势正在重新定义我们构建 Web 应用的方式。</p>
                    """,
                    "excerpt": "探讨现代前端开发的主要趋势和技术演进",
                    "category": "技术",
                    "status": "已发布",
                    "author_id": admin_user.id
                },
                {
                    "title": "人工智能时代的思考",
                    "content": """
                    <h2>AI 的影响</h2>
                    <p>人工智能正在改变我们的生活和工作方式。作为开发者，我们需要思考如何在这个时代保持竞争力。</p>
                    
                    <h2>关键思考</h2>
                    <p>学习与 AI 协作，而不是被 AI 替代，是我们需要掌握的重要技能。</p>
                    """,
                    "excerpt": "在人工智能时代，开发者应该如何思考和应对",
                    "category": "思考",
                    "status": "草稿",
                    "author_id": admin_user.id
                },
                {
                    "title": "代码之美：编程中的艺术哲学",
                    "content": """
                    <h2>什么是优美的代码？</h2>
                    <p>优美的代码不仅仅是能够运行的代码，更是易读、易维护、具有良好设计的代码。</p>
                    
                    <h2>编程哲学</h2>
                    <p>编程是一门艺术，好的程序员不仅是技术专家，更是艺术家。</p>
                    """,
                    "excerpt": "探讨编程中的美学和哲学思考",
                    "category": "编程",
                    "status": "已发布",
                    "author_id": admin_user.id
                }
            ]
            
            for article_data in sample_articles:
                article = Article(**article_data)
                if article_data["status"] == "已发布":
                    article.published_at = datetime.utcnow()
                db.add(article)
            
            db.commit()
            print("示例文章创建成功！")
        
        print("数据库初始化完成！")
    
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
