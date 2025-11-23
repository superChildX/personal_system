# 数据库设计文档

> 个人成长管理系统 - MySQL数据库设计
> 
> **技术栈**: Python FastAPI + MySQL
> 
> **数据库配置**:
> - 账号: root
> - 密码: 123456
> - 数据库名: personal_growth_system

---

## 📊 数据库表设计

### 1. 用户表 (users)
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    github_username VARCHAR(100),
    linkedin_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

### 2. 个人档案表 (profiles)
```sql
CREATE TABLE profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    phone VARCHAR(20),
    bio TEXT,
    current_position VARCHAR(100),
    location VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 3. 教育背景表 (education)
```sql
CREATE TABLE education (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    school_name VARCHAR(200) NOT NULL,
    major VARCHAR(100),
    degree VARCHAR(50),
    gpa DECIMAL(3,2),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 4. 技能表 (skills)
```sql
CREATE TABLE skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50), -- 编程语言/框架/工具
    proficiency INT DEFAULT 3, -- 1-5星评分
    years_of_experience DECIMAL(3,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

### 5. 项目表 (projects)
```sql
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('planned', 'in_progress', 'completed', 'archived') DEFAULT 'in_progress',
    start_date DATE,
    end_date DATE,
    github_url VARCHAR(255),
    demo_url VARCHAR(255),
    tech_stack JSON, -- 存储技术栈数组
    highlights TEXT, -- 项目亮点
    summary TEXT, -- 开发总结
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_user_date (user_id, created_at)
);
```

### 6. 项目截图表 (project_images)
```sql
CREATE TABLE project_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(200),
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

---

### 7. 学习笔记表 (notes)
```sql
CREATE TABLE notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    category VARCHAR(50), -- 课程笔记/技术博客/代码片段
    tags JSON, -- 标签数组
    is_public BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FULLTEXT INDEX idx_content (title, content)
);
```

### 8. 代码片段表 (code_snippets)
```sql
CREATE TABLE code_snippets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(50), -- JavaScript/Python/Java等
    description TEXT,
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

### 9. 经历记录表 (experiences)
```sql
CREATE TABLE experiences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type ENUM('internship', 'competition', 'award', 'activity') NOT NULL,
    title VARCHAR(200) NOT NULL,
    organization VARCHAR(200),
    role VARCHAR(100),
    start_date DATE,
    end_date DATE,
    description TEXT,
    achievements TEXT, -- 成果与收获
    certificate_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_type (type)
);
```

---

### 10. Todo任务表 (tasks)
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    due_date DATETIME,
    completed_at DATETIME,
    category VARCHAR(50), -- 学习/工作/生活
    estimated_time INT, -- 预计时长（分钟）
    actual_time INT, -- 实际时长（分钟）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_due_date (due_date)
);
```

### 11. 番茄钟记录表 (pomodoro_sessions)
```sql
CREATE TABLE pomodoro_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    task_id INT,
    duration INT DEFAULT 25, -- 时长（分钟）
    session_type ENUM('focus', 'break') DEFAULT 'focus',
    start_time DATETIME,
    end_time DATETIME,
    is_completed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL,
    INDEX idx_user_date (user_id, start_time)
);
```

### 12. 日程安排表 (schedules)
```sql
CREATE TABLE schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    category VARCHAR(50), -- 会议/学习/生活/娱乐
    location VARCHAR(200),
    reminder_minutes INT, -- 提前提醒时间
    is_all_day BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_time (start_time, end_time)
);
```

---

### 13. 知识库-面试题表 (interview_questions)
```sql
CREATE TABLE interview_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question VARCHAR(500) NOT NULL,
    answer TEXT,
    category VARCHAR(50), -- JavaScript/算法/网络/操作系统等
    difficulty ENUM('easy', 'medium', 'hard'),
    tags JSON,
    is_mastered BOOLEAN DEFAULT FALSE,
    review_count INT DEFAULT 0,
    last_reviewed_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FULLTEXT INDEX idx_question (question, answer)
);
```

### 14. 技术资源收藏表 (resources)
```sql
CREATE TABLE resources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500),
    type ENUM('article', 'video', 'course', 'tool', 'documentation'),
    description TEXT,
    tags JSON,
    rating INT, -- 1-5星
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 15. LeetCode刷题记录表 (leetcode_problems)
```sql
CREATE TABLE leetcode_problems (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    problem_id INT NOT NULL, -- LeetCode题目ID
    title VARCHAR(200) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard'),
    category VARCHAR(50), -- 数组/链表/动态规划等
    solution TEXT, -- 解题思路
    code TEXT, -- 代码实现
    time_complexity VARCHAR(50),
    space_complexity VARCHAR(50),
    is_solved BOOLEAN DEFAULT FALSE,
    attempts INT DEFAULT 1,
    last_attempted_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_difficulty (difficulty)
);
```

---

### 16. 每日记录表 (daily_records)
```sql
CREATE TABLE daily_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    record_date DATE NOT NULL,
    study_hours DECIMAL(4,1), -- 学习时长
    sleep_hours DECIMAL(3,1), -- 睡眠时长
    exercise_done BOOLEAN DEFAULT FALSE, -- 是否运动
    mood_rating INT, -- 心情指数 1-5
    tasks_completed INT DEFAULT 0, -- 完成任务数
    tasks_total INT DEFAULT 0, -- 总任务数
    summary TEXT, -- 今日总结
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, record_date),
    INDEX idx_date (record_date)
);
```

### 17. 每日任务明细表 (daily_tasks)
```sql
CREATE TABLE daily_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    daily_record_id INT NOT NULL,
    task_description VARCHAR(200) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (daily_record_id) REFERENCES daily_records(id) ON DELETE CASCADE
);
```

---

### 18. 灵感笔记表 (ideas)
```sql
CREATE TABLE ideas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200),
    content TEXT NOT NULL,
    type ENUM('quick_note', 'project_idea', 'book_review', 'movie_review'),
    priority ENUM('low', 'medium', 'high'),
    feasibility VARCHAR(50), -- 可行性评估
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 19. 读书/电影记录表 (media_records)
```sql
CREATE TABLE media_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type ENUM('book', 'movie', 'course'),
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    rating INT, -- 1-5星
    status ENUM('want', 'reading', 'finished') DEFAULT 'want',
    review TEXT,
    notes TEXT,
    tags JSON,
    finished_at DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

### 20. OKR目标表 (goals)
```sql
CREATE TABLE goals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type ENUM('okr', 'habit'),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    quarter VARCHAR(10), -- 2024Q4
    start_date DATE,
    end_date DATE,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 21. 关键结果表 (key_results)
```sql
CREATE TABLE key_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    goal_id INT NOT NULL,
    description VARCHAR(300) NOT NULL,
    target_value DECIMAL(10,2), -- 目标值
    current_value DECIMAL(10,2) DEFAULT 0, -- 当前值
    unit VARCHAR(20), -- 单位：个/次/小时
    progress INT DEFAULT 0, -- 进度百分比
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
);
```

### 22. 习惯打卡表 (habit_logs)
```sql
CREATE TABLE habit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    goal_id INT NOT NULL,
    log_date DATE NOT NULL,
    is_completed BOOLEAN DEFAULT TRUE,
    note VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE,
    UNIQUE KEY unique_habit_date (goal_id, log_date)
);
```

### 23. 月度复盘表 (monthly_reviews)
```sql
CREATE TABLE monthly_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    summary TEXT,
    achievements TEXT, -- 本月成果
    problems TEXT, -- 遇到的问题
    improvements TEXT, -- 改进计划
    study_hours DECIMAL(6,1),
    tasks_completed INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_month (user_id, year, month)
);
```

---

### 24. 社交网络-联系人表 (contacts)
```sql
CREATE TABLE contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category ENUM('mentor', 'classmate', 'colleague', 'friend'),
    position VARCHAR(100),
    company VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    wechat VARCHAR(50),
    github VARCHAR(100),
    linkedin VARCHAR(255),
    notes TEXT,
    last_contact_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 25. 会议记录表 (meetings)
```sql
CREATE TABLE meetings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    meeting_date DATETIME,
    location VARCHAR(200),
    attendees JSON, -- 参与人员数组
    agenda TEXT, -- 会议议程
    minutes TEXT, -- 会议纪要
    action_items TEXT, -- 行动项
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

### 26. 标签表 (tags)
```sql
CREATE TABLE tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20),
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_tag (user_id, name)
);
```

### 27. 附件表 (attachments)
```sql
CREATE TABLE attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- projects/notes/experiences等
    entity_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT, -- 字节
    file_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_entity (entity_type, entity_id)
);
```

---

## 🔧 数据库初始化脚本

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS personal_growth_system 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE personal_growth_system;

-- 按照上述顺序创建所有表...
```

---

## 📝 表关系说明

### 核心关系：
- **users** 是核心表，其他所有表通过 `user_id` 关联
- **projects** ←→ **project_images** (一对多)
- **goals** ←→ **key_results** (一对多)
- **goals** ←→ **habit_logs** (一对多)
- **daily_records** ←→ **daily_tasks** (一对多)
- **tasks** ←→ **pomodoro_sessions** (一对多)

### 索引策略：
- 外键字段都建立了索引
- 常用查询字段（status, date等）建立了索引
- 全文搜索字段使用 FULLTEXT 索引

---

## 🚀 FastAPI 连接配置

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/personal_growth_system?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
