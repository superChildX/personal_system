"""
数据库初始化脚本
创建所有表结构
"""
from app.database import engine, Base
from app import models  # 导入所有模型


def init_database():
    """初始化数据库，创建所有表"""
    print("🔧 开始初始化数据库...")
    print(f"📊 数据库连接: {engine.url}")
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功！")
        print(f"✅ 共创建 {len(Base.metadata.tables)} 张表:")
        
        for table_name in Base.metadata.tables.keys():
            print(f"   📋 {table_name}")
        
        print("\n🎉 数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        raise


def drop_all_tables():
    """删除所有表（慎用！）"""
    print("⚠️  警告: 即将删除所有表...")
    confirm = input("确认删除所有表？输入 'yes' 继续: ")
    
    if confirm.lower() == 'yes':
        try:
            Base.metadata.drop_all(bind=engine)
            print("✅ 所有表已删除")
        except Exception as e:
            print(f"❌ 删除表失败: {e}")
            raise
    else:
        print("❌ 操作已取消")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
    else:
        init_database()
