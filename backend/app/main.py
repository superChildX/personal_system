"""
FastAPI应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .database import engine, Base
from . import models  # 导入所有模型以便创建表

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="个人成长管理系统API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时的操作"""
    print("🚀 启动个人成长管理系统...")
    print(f"📚 项目名称: {settings.PROJECT_NAME}")
    print(f"📦 版本: {settings.VERSION}")
    print(f"📡 API地址: {settings.API_V1_STR}")
    print(f"📖 API文档: {settings.API_V1_STR}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的操作"""
    print("👋 关闭个人成长管理系统...")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to Personal Growth System API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "系统运行正常"}


# 导入并注册API路由
from .api.v1 import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)
