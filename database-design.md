# Personal OS - PostgreSQL Database Design

## 1. ER Diagram Description

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   users     │       │  projects   │       │    todos    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──┐   │ id (PK)     │◄──┐   │ id (PK)     │
│ email       │   │   │ user_id(FK) │───┘   │ user_id(FK) │───┐
│ ...         │   │   │ ...         │       │ project_id  │───┤
└─────────────┘   │   └─────────────┘       │ ...         │   │
                  │                         └─────────────┘   │
                  │                                           │
                  │   ┌─────────────┐       ┌─────────────┐   │
                  │   │learning_logs│       │calendar_    │   │
                  │   ├─────────────┤       │   events    │   │
                  │   │ id (PK)     │       ├─────────────┤   │
                  └───│ user_id(FK) │       │ id (PK)     │   │
                  │   │ ...         │       │ user_id(FK) │───┤
                  │   └─────────────┘       │ todo_id(FK) │───┘
                  │                         │ ...         │
                  │   ┌─────────────┐       └─────────────┘
                  │   │    tags     │
                  │   ├─────────────┤       ┌─────────────┐
                  │   │ id (PK)     │       │ attachments │
                  └───│ user_id(FK) │       ├─────────────┤
                      │ ...         │       │ id (PK)     │
                      └─────────────┘       │ user_id(FK) │───┐
                            │               │ ...         │   │
                            │               └─────────────┘   │
                      ┌─────┴─────┐                           │
              ┌───────┴───┐ ┌─────┴───────┐                   │
              │todo_tags  │ │learning_    │                   │
              │(Junction) │ │  log_tags   │                   │
              └───────────┘ └─────────────┘                   │
                                                              │
                  ┌─────────────┐       ┌─────────────┐       │
                  │user_settings│       │activity_logs│       │
                  ├─────────────┤       ├─────────────┤       │
                  │ id (PK)     │       │ id (PK)     │       │
                  │ user_id(FK) │───────│ user_id(FK) │───────┘
                  │ ...         │       │ ...         │
                  └─────────────┘       └─────────────┘
```

## 2. DDL Statements

### 2.1 Users Table

```sql
-- 用户表：系统核心实体，存储用户账户信息
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(500),
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- 注释
COMMENT ON TABLE users IS '用户账户表';
COMMENT ON COLUMN users.id IS '用户唯一标识';
COMMENT ON COLUMN users.email IS '登录邮箱，唯一';
COMMENT ON COLUMN users.hashed_password IS 'Bcrypt加密后的密码';
COMMENT ON COLUMN users.full_name IS '用户昵称';
COMMENT ON COLUMN users.avatar_url IS '头像URL';
COMMENT ON COLUMN users.timezone IS '用户时区，用于日历显示';
COMMENT ON COLUMN users.is_active IS '账户是否激活';
COMMENT ON COLUMN users.last_login_at IS '最后登录时间';
```

### 2.2 Projects Table

```sql
-- 项目表：管理长期复杂任务集合
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    tech_stack JSONB DEFAULT '[]',
    status VARCHAR(20) DEFAULT 'planning',
    cover_image VARCHAR(500),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_projects_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_projects_status 
        CHECK (status IN ('planning', 'ongoing', 'done', 'archived')),
    CONSTRAINT chk_projects_dates 
        CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);

-- 索引
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_user_status ON projects(user_id, status);
CREATE INDEX idx_projects_tech_stack ON projects USING GIN(tech_stack);

-- 注释
COMMENT ON TABLE projects IS '项目管理表';
COMMENT ON COLUMN projects.tech_stack IS '技术栈标签，JSONB数组格式 ["React", "FastAPI"]';
COMMENT ON COLUMN projects.status IS '项目状态：planning/ongoing/done/archived';
```

### 2.3 Todos Table

```sql
-- 待办事项表：日常任务管理核心
CREATE TABLE todos (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    project_id BIGINT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    priority SMALLINT DEFAULT 2,
    status VARCHAR(20) DEFAULT 'todo',
    category VARCHAR(20) DEFAULT 'work',
    is_completed BOOLEAN DEFAULT FALSE,
    position INTEGER DEFAULT 0,
    start_date TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_todos_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_todos_project FOREIGN KEY (project_id) 
        REFERENCES projects(id) ON DELETE SET NULL,
    CONSTRAINT chk_todos_priority 
        CHECK (priority BETWEEN 0 AND 2),
    CONSTRAINT chk_todos_status 
        CHECK (status IN ('todo', 'doing', 'done')),
    CONSTRAINT chk_todos_category 
        CHECK (category IN ('work', 'study', 'life', 'other'))
);

-- 索引
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_project_id ON todos(project_id);
CREATE INDEX idx_todos_user_due_date ON todos(user_id, due_date);
CREATE INDEX idx_todos_user_status ON todos(user_id, status);
CREATE INDEX idx_todos_user_category ON todos(user_id, category);

-- 注释
COMMENT ON TABLE todos IS '待办事项表';
COMMENT ON COLUMN todos.priority IS '优先级：0=P0(紧急), 1=P1(重要), 2=P2(普通)';
COMMENT ON COLUMN todos.status IS '任务状态：todo/doing/done，支持看板视图';
COMMENT ON COLUMN todos.category IS '分类：work/study/life/other，用于日历颜色区分';
COMMENT ON COLUMN todos.position IS '排序位置，支持拖拽排序';
COMMENT ON COLUMN todos.description IS '任务描述，支持Markdown';
```

### 2.4 Calendar Events Table

```sql
-- 日历事件表：独立于Todo的日历事件
CREATE TABLE calendar_events (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    todo_id BIGINT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(20) DEFAULT 'other',
    is_all_day BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    recurrence_rule VARCHAR(255),
    color VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_calendar_events_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_calendar_events_todo FOREIGN KEY (todo_id) 
        REFERENCES todos(id) ON DELETE SET NULL,
    CONSTRAINT chk_calendar_events_category 
        CHECK (category IN ('work', 'study', 'life', 'other')),
    CONSTRAINT chk_calendar_events_times 
        CHECK (end_time IS NULL OR end_time >= start_time)
);

-- 索引
CREATE INDEX idx_calendar_events_user_id ON calendar_events(user_id);
CREATE INDEX idx_calendar_events_user_time ON calendar_events(user_id, start_time, end_time);
CREATE INDEX idx_calendar_events_todo_id ON calendar_events(todo_id);

-- 注释
COMMENT ON TABLE calendar_events IS '日历事件表';
COMMENT ON COLUMN calendar_events.todo_id IS '关联的Todo，实现双向同步';
COMMENT ON COLUMN calendar_events.is_all_day IS '是否全天事件';
COMMENT ON COLUMN calendar_events.recurrence_rule IS '重复规则，iCal RRULE格式';
COMMENT ON COLUMN calendar_events.color IS '自定义颜色，覆盖category默认色';
```

### 2.5 Learning Logs Table

```sql
-- 学习日志表：记录知识碎片
CREATE TABLE learning_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200),
    content TEXT NOT NULL,
    content_type VARCHAR(20) DEFAULT 'note',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_learning_logs_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_learning_logs_type 
        CHECK (content_type IN ('note', 'code', 'book', 'idea', 'other'))
);

-- 索引
CREATE INDEX idx_learning_logs_user_id ON learning_logs(user_id);
CREATE INDEX idx_learning_logs_user_created ON learning_logs(user_id, created_at DESC);
CREATE INDEX idx_learning_logs_content ON learning_logs USING GIN(to_tsvector('english', content));

-- 注释
COMMENT ON TABLE learning_logs IS '学习日志表';
COMMENT ON COLUMN learning_logs.content IS '学习内容，支持Markdown';
COMMENT ON COLUMN learning_logs.content_type IS '内容类型：note/code/book/idea/other';
```

### 2.6 Tags Table

```sql
-- 标签表：统一的标签管理
CREATE TABLE tags (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20) DEFAULT '#6366f1',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_tags_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);

-- 注释
COMMENT ON TABLE tags IS '标签表';
COMMENT ON COLUMN tags.color IS '标签颜色，十六进制格式';
```

### 2.7 Junction Tables (Many-to-Many)

```sql
-- Todo与Tag的关联表
CREATE TABLE todo_tags (
    todo_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (todo_id, tag_id),
    CONSTRAINT fk_todo_tags_todo FOREIGN KEY (todo_id) 
        REFERENCES todos(id) ON DELETE CASCADE,
    CONSTRAINT fk_todo_tags_tag FOREIGN KEY (tag_id) 
        REFERENCES tags(id) ON DELETE CASCADE
);

-- 学习日志与Tag的关联表
CREATE TABLE learning_log_tags (
    learning_log_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (learning_log_id, tag_id),
    CONSTRAINT fk_learning_log_tags_log FOREIGN KEY (learning_log_id) 
        REFERENCES learning_logs(id) ON DELETE CASCADE,
    CONSTRAINT fk_learning_log_tags_tag FOREIGN KEY (tag_id) 
        REFERENCES tags(id) ON DELETE CASCADE
);

-- 项目与Tag的关联表
CREATE TABLE project_tags (
    project_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (project_id, tag_id),
    CONSTRAINT fk_project_tags_project FOREIGN KEY (project_id) 
        REFERENCES projects(id) ON DELETE CASCADE,
    CONSTRAINT fk_project_tags_tag FOREIGN KEY (tag_id) 
        REFERENCES tags(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_todo_tags_tag_id ON todo_tags(tag_id);
CREATE INDEX idx_learning_log_tags_tag_id ON learning_log_tags(tag_id);
CREATE INDEX idx_project_tags_tag_id ON project_tags(tag_id);

-- 注释
COMMENT ON TABLE todo_tags IS 'Todo与标签的多对多关联表';
COMMENT ON TABLE learning_log_tags IS '学习日志与标签的多对多关联表';
COMMENT ON TABLE project_tags IS '项目与标签的多对多关联表';
```

### 2.8 Attachments Table

```sql
-- 附件表：统一管理文件上传
CREATE TABLE attachments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    entity_type VARCHAR(20) NOT NULL,
    entity_id BIGINT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_attachments_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_attachments_entity_type 
        CHECK (entity_type IN ('project', 'todo', 'learning_log', 'user'))
);

-- 索引
CREATE INDEX idx_attachments_user_id ON attachments(user_id);
CREATE INDEX idx_attachments_entity ON attachments(entity_type, entity_id);

-- 注释
COMMENT ON TABLE attachments IS '附件表，支持多实体关联';
COMMENT ON COLUMN attachments.entity_type IS '关联实体类型：project/todo/learning_log/user';
COMMENT ON COLUMN attachments.entity_id IS '关联实体ID';
```

### 2.9 User Settings Table

```sql
-- 用户设置表：存储个性化配置
CREATE TABLE user_settings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    theme VARCHAR(20) DEFAULT 'light',
    primary_color VARCHAR(20) DEFAULT 'indigo',
    default_view VARCHAR(20) DEFAULT 'list',
    calendar_start_day SMALLINT DEFAULT 1,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    settings_json JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user_settings_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_user_settings_theme 
        CHECK (theme IN ('light', 'dark', 'system')),
    CONSTRAINT chk_user_settings_view 
        CHECK (default_view IN ('list', 'kanban', 'calendar')),
    CONSTRAINT chk_user_settings_start_day 
        CHECK (calendar_start_day BETWEEN 0 AND 6)
);

-- 注释
COMMENT ON TABLE user_settings IS '用户设置表';
COMMENT ON COLUMN user_settings.theme IS '主题：light/dark/system';
COMMENT ON COLUMN user_settings.primary_color IS '主色调';
COMMENT ON COLUMN user_settings.default_view IS '默认视图：list/kanban/calendar';
COMMENT ON COLUMN user_settings.calendar_start_day IS '日历起始日：0=周日, 1=周一';
COMMENT ON COLUMN user_settings.settings_json IS '扩展设置，JSONB格式';
```

### 2.10 Activity Logs Table

```sql
-- 活动日志表：审计追踪
CREATE TABLE activity_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(20) NOT NULL,
    entity_id BIGINT,
    old_value JSONB,
    new_value JSONB,
    ip_address INET,
    user_agent VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_activity_logs_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at DESC);
CREATE INDEX idx_activity_logs_entity ON activity_logs(entity_type, entity_id);

-- 使用BRIN索引优化时序查询（适合大数据量）
CREATE INDEX idx_activity_logs_created_brin ON activity_logs USING BRIN(created_at);

-- 注释
COMMENT ON TABLE activity_logs IS '活动日志表，用于审计追踪';
COMMENT ON COLUMN activity_logs.action IS '操作类型：create/update/delete/login/logout';
COMMENT ON COLUMN activity_logs.old_value IS '修改前的值';
COMMENT ON COLUMN activity_logs.new_value IS '修改后的值';
```

## 3. Views

### 3.1 Project Progress View

```sql
-- 项目进度视图：计算项目完成率
CREATE VIEW v_project_progress AS
SELECT 
    p.id AS project_id,
    p.user_id,
    p.title,
    p.status,
    COUNT(t.id) AS total_todos,
    COUNT(t.id) FILTER (WHERE t.is_completed = TRUE) AS completed_todos,
    CASE 
        WHEN COUNT(t.id) = 0 THEN 0
        ELSE ROUND(COUNT(t.id) FILTER (WHERE t.is_completed = TRUE) * 100.0 / COUNT(t.id), 2)
    END AS progress_percentage
FROM projects p
LEFT JOIN todos t ON t.project_id = p.id
GROUP BY p.id, p.user_id, p.title, p.status;

COMMENT ON VIEW v_project_progress IS '项目进度视图，包含完成率计算';
```

### 3.2 Today's Tasks View

```sql
-- 今日任务视图
CREATE VIEW v_today_tasks AS
SELECT 
    t.*,
    p.title AS project_title
FROM todos t
LEFT JOIN projects p ON t.project_id = p.id
WHERE t.is_completed = FALSE
  AND (
      t.due_date::DATE = CURRENT_DATE
      OR t.start_date::DATE = CURRENT_DATE
  );

COMMENT ON VIEW v_today_tasks IS '今日待办任务视图';
```

### 3.3 Overdue Tasks View

```sql
-- 逾期任务视图
CREATE VIEW v_overdue_tasks AS
SELECT 
    t.*,
    p.title AS project_title,
    CURRENT_DATE - t.due_date::DATE AS overdue_days
FROM todos t
LEFT JOIN projects p ON t.project_id = p.id
WHERE t.is_completed = FALSE
  AND t.due_date < CURRENT_TIMESTAMP;

COMMENT ON VIEW v_overdue_tasks IS '逾期任务视图';
```

## 4. Functions & Triggers

### 4.1 Auto Update Timestamp

```sql
-- 自动更新 updated_at 字段的函数
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有需要的表创建触发器
CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_todos_updated_at
    BEFORE UPDATE ON todos
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_calendar_events_updated_at
    BEFORE UPDATE ON calendar_events
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_learning_logs_updated_at
    BEFORE UPDATE ON learning_logs
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_user_settings_updated_at
    BEFORE UPDATE ON user_settings
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
```

### 4.2 Auto Set Completed Timestamp

```sql
-- Todo完成时自动设置completed_at
CREATE OR REPLACE FUNCTION fn_todo_completed()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_completed = TRUE AND OLD.is_completed = FALSE THEN
        NEW.completed_at = CURRENT_TIMESTAMP;
        NEW.status = 'done';
    ELSIF NEW.is_completed = FALSE AND OLD.is_completed = TRUE THEN
        NEW.completed_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_todo_completed
    BEFORE UPDATE ON todos
    FOR EACH ROW EXECUTE FUNCTION fn_todo_completed();
```

### 4.3 Sync Todo to Calendar Event

```sql
-- Todo设置时间后自动同步到日历
CREATE OR REPLACE FUNCTION fn_sync_todo_to_calendar()
RETURNS TRIGGER AS $$
BEGIN
    -- 当Todo有due_date时，创建或更新对应的日历事件
    IF NEW.due_date IS NOT NULL THEN
        INSERT INTO calendar_events (user_id, todo_id, title, category, start_time, is_all_day)
        VALUES (NEW.user_id, NEW.id, NEW.title, NEW.category, NEW.due_date, TRUE)
        ON CONFLICT (todo_id) WHERE todo_id IS NOT NULL
        DO UPDATE SET 
            title = EXCLUDED.title,
            category = EXCLUDED.category,
            start_time = EXCLUDED.start_time,
            updated_at = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 注意：需要先创建部分唯一索引
CREATE UNIQUE INDEX idx_calendar_events_todo_unique 
    ON calendar_events(todo_id) WHERE todo_id IS NOT NULL;

CREATE TRIGGER trg_sync_todo_to_calendar
    AFTER INSERT OR UPDATE OF due_date, title, category ON todos
    FOR EACH ROW EXECUTE FUNCTION fn_sync_todo_to_calendar();
```

## 5. Sample Queries

### 5.1 Get User Dashboard Data

```sql
-- 获取用户仪表盘数据
WITH user_stats AS (
    SELECT 
        u.id AS user_id,
        (SELECT COUNT(*) FROM todos WHERE user_id = u.id AND is_completed = FALSE) AS pending_todos,
        (SELECT COUNT(*) FROM todos WHERE user_id = u.id AND due_date < NOW() AND is_completed = FALSE) AS overdue_todos,
        (SELECT COUNT(*) FROM projects WHERE user_id = u.id AND status = 'ongoing') AS active_projects,
        (SELECT COUNT(*) FROM learning_logs WHERE user_id = u.id AND created_at >= CURRENT_DATE - INTERVAL '7 days') AS weekly_logs
    FROM users u
    WHERE u.id = :user_id
)
SELECT * FROM user_stats;
```

### 5.2 Get Todos with Tags

```sql
-- 获取带标签的Todo列表
SELECT 
    t.*,
    p.title AS project_title,
    COALESCE(
        json_agg(
            json_build_object('id', tg.id, 'name', tg.name, 'color', tg.color)
        ) FILTER (WHERE tg.id IS NOT NULL),
        '[]'
    ) AS tags
FROM todos t
LEFT JOIN projects p ON t.project_id = p.id
LEFT JOIN todo_tags tt ON t.id = tt.todo_id
LEFT JOIN tags tg ON tt.tag_id = tg.id
WHERE t.user_id = :user_id
GROUP BY t.id, p.title
ORDER BY t.position, t.created_at DESC;
```

### 5.3 Get Calendar Events for Date Range

```sql
-- 获取日期范围内的日历事件（包含Todo同步的事件）
SELECT 
    ce.*,
    t.is_completed AS todo_completed,
    t.priority AS todo_priority
FROM calendar_events ce
LEFT JOIN todos t ON ce.todo_id = t.id
WHERE ce.user_id = :user_id
  AND ce.start_time >= :start_date
  AND (ce.end_time <= :end_date OR ce.end_time IS NULL)
ORDER BY ce.start_time;
```

### 5.4 Get Learning Timeline with Tags

```sql
-- 获取学习时间轴（带标签过滤）
SELECT 
    ll.*,
    COALESCE(
        json_agg(
            json_build_object('id', t.id, 'name', t.name, 'color', t.color)
        ) FILTER (WHERE t.id IS NOT NULL),
        '[]'
    ) AS tags
FROM learning_logs ll
LEFT JOIN learning_log_tags llt ON ll.id = llt.learning_log_id
LEFT JOIN tags t ON llt.tag_id = t.id
WHERE ll.user_id = :user_id
  AND (:tag_id IS NULL OR t.id = :tag_id)
GROUP BY ll.id
ORDER BY ll.created_at DESC
LIMIT :limit OFFSET :offset;
```

### 5.5 Kanban Board Query

```sql
-- 看板视图数据查询
SELECT 
    t.status,
    json_agg(
        json_build_object(
            'id', t.id,
            'title', t.title,
            'priority', t.priority,
            'due_date', t.due_date,
            'project_title', p.title
        ) ORDER BY t.position
    ) AS tasks
FROM todos t
LEFT JOIN projects p ON t.project_id = p.id
WHERE t.user_id = :user_id
  AND (:project_id IS NULL OR t.project_id = :project_id)
GROUP BY t.status;
```

## 6. Design Notes

### 6.1 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| BIGSERIAL for PKs | 预留大数据量空间，避免Integer溢出 |
| TIMESTAMPTZ | 带时区时间戳，支持多时区用户 |
| JSONB for tech_stack | 灵活存储数组数据，支持GIN索引查询 |
| Polymorphic attachments | 使用entity_type+entity_id实现多态关联，避免多个外键 |
| Separate tags table | 统一标签管理，支持跨实体复用 |
| Calendar events table | 独立于Todo，支持纯日历事件和重复事件 |
| Activity logs | 审计追踪，使用BRIN索引优化时序查询 |

### 6.2 Index Strategy

- 所有外键列都有索引
- 常用查询条件的复合索引（user_id + status, user_id + due_date）
- JSONB字段使用GIN索引
- 全文搜索使用GIN索引 + to_tsvector
- 时序数据使用BRIN索引（activity_logs）

### 6.3 Data Integrity

- 所有表都有 ON DELETE CASCADE 或 SET NULL
- CHECK约束确保枚举值有效
- 日期范围约束（end_date >= start_date）
- 触发器自动维护 updated_at 和 completed_at

## 7. Performance Recommendations

1. **分区策略**：当 `activity_logs` 数据量超过100万行时，考虑按月分区
2. **物化视图**：如果 `v_project_progress` 查询频繁，可改为物化视图并定时刷新
3. **连接池**：使用 PgBouncer 管理连接池
4. **定期维护**：设置 VACUUM 和 ANALYZE 定时任务

```sql
-- 示例：按月分区 activity_logs
CREATE TABLE activity_logs_partitioned (
    LIKE activity_logs INCLUDING ALL
) PARTITION BY RANGE (created_at);

CREATE TABLE activity_logs_2025_01 PARTITION OF activity_logs_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```
