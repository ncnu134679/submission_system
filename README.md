
# 投稿審查系統

## 一、專案介紹

本專案使用 FastAPI 與 PostgreSQL 開發投稿審查系統，提供作者投稿管理及編輯審查功能。

系統分為兩種角色：
- 作者
- 編輯

## 二、使用技術

- Python
- FastAPI
- PostgreSQL
- HTML
- CSS
- JavaScript

## 三、系統功能

### 1. 作者功能

- 查看自己的投稿稿件清單。
- 查看投稿類別、文章標題及審查狀態。
- 新增投稿，填寫投稿類別、文章標題及文章內容。
- 編輯尚未送出的投稿。
- 刪除尚未送出的投稿。
- 送出投稿，將稿件狀態改為「審查中」。
- 查看編輯退回的建議，依照建議修改文章。

### 2. 編輯功能

- 查看待審查投稿清單。
- 查看作者、投稿類別及文章標題。
- 查看單篇投稿的完整內容。
- 通過投稿，將稿件狀態改為「已通過」。
- 退回投稿，填寫退回建議，將稿件狀態改回「編輯中」。

## 四、投稿狀態流程

| 狀態 | 說明 |
|---|---|
| 編輯中 | 作者新增或修改投稿的狀態 |
| 審查中 | 作者送出投稿，等待編輯審查 |
| 已通過 | 編輯審查通過 |

狀態轉換：

1. 作者新增投稿：編輯中
2. 作者送出投稿：編輯中 → 審查中
3. 編輯通過投稿：審查中 → 已通過
4. 編輯退回投稿：審查中 → 編輯中

## 五、資料庫

資料庫名稱：`submission_system`

### users 使用者資料表

| 欄位 | 說明 |
|---|---|
| id | 使用者編號 |
| username | 使用者名稱 |
| password | 密碼 |
| role | 使用者角色 |

### manuscripts 投稿資料表

| 欄位 | 說明 |
|---|---|
| id | 投稿編號 |
| author_id | 作者編號 |
| category | 投稿類別 |
| title | 文章標題 |
| content | 文章內容 |
| status | 投稿狀態 |
| editor_feedback | 編輯退回建議 |

## 六、專案架構

```text
submission_system/
│
├── main.py
├── db.py
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── index.html
    ├── author.html
    ├── add_manuscript.html
    ├── edit_manuscript.html
    ├── editor.html
    └── editor_manuscript.html
```

## 七、環境安裝與執行

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 設定資料庫

請先安裝並啟動 PostgreSQL，建立資料庫：

```sql
CREATE DATABASE submission_system;
```

接著在專案根目錄建立 `.env`，設定資料庫連線資訊：

```env
DATABASE_URL=postgresql://postgres:你的密碼@localhost:5432/submission_system
```

請依照自己的 PostgreSQL 帳號及密碼修改連線資訊。

### 3. 啟動系統

在專案根目錄執行：

```bash
uvicorn main:app --reload
```

### 4. 開啟系統

在瀏覽器輸入：

```text
http://127.0.0.1:8000
```

即可進入投稿審查系統首頁。
