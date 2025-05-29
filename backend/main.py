
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, articles, admin

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化 FastAPI 应用
app = FastAPI(
    title="个人博客 API",
    version="1.0.0",
    description="基于 FastAPI 的个人博客后端 API"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(admin.router)

@app.get("/")
def root():
    """根路径"""
    return {"message": "个人博客 API 服务正在运行"}

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
