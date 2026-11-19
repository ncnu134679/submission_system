# 投稿審查系統

## 一、系統介紹

本系統是一個投稿審查系統，分為作者與編輯兩種角色。

作者可以新增、編輯、刪除及送出投稿；編輯可以查看待審查的稿件，並決定通過或退回。

## 二、使用技術

- 前端：HTML、JavaScript
- 後端：Python、FastAPI
- 資料庫：PostgreSQL
- 資料庫連線：psycopg

## 三、系統架構

本系統分成前端、後端及資料庫三個部分。

### 1. 前端（HTML + JavaScript）

- 使用 HTML 製作網頁畫面。
- 使用 JavaScript 的 `fetch()` 呼叫後端 API。
- 將使用者輸入的資料傳送給 FastAPI。
- 接收後端回傳的資料，並更新網頁畫面。

### 2. 後端（FastAPI）

- 使用 FastAPI 撰寫系統功能。
- 在 `main.py` 定義 API 路由。
- 接收前端傳送的請求及資料。
- 處理新增、查詢、修改及刪除稿件等功能。
- 將處理結果回傳給前端。

### 3. 資料庫（PostgreSQL）

- 使用 PostgreSQL 儲存系統資料。
- 透過 `db.py` 建立資料庫連線。
- 儲存使用者及投稿稿件等資料。

## 四、前後端如何連接

前端 HTML 透過 JavaScript 的 `fetch()` 呼叫 FastAPI 中定義的 API。

例如，作者新增投稿時：

1. 作者在 HTML 表單填寫類別、標題及文章內容。
2. JavaScript 使用 `fetch()` 將表單資料傳送至 FastAPI。
3. FastAPI 接收資料，並執行新增投稿的 SQL 指令。
4. PostgreSQL 將投稿資料儲存至資料庫。
5. FastAPI 將執行結果回傳給前端。
6. JavaScript 接收結果，顯示新增成功訊息。

## 五、HTTP 方法

| HTTP 方法 | 用途 | 系統中的功能 |
|---|---|---|
| GET | 查詢資料 | 查看投稿清單、查看稿件內容 |
| POST | 新增資料 | 新增投稿 |
| PUT | 修改資料 | 編輯投稿、送出投稿、通過或退回 |
| DELETE | 刪除資料 | 刪除編輯中的投稿 |

## 六、資料庫資料表設計

本系統使用 PostgreSQL，主要使用兩個資料表。

### 1. users（使用者資料表）

| 欄位名稱 | 用途 |
|---|---|
| id | 使用者編號 |
| username | 使用者名稱 |

### 2. manuscripts（投稿資料表）

| 欄位名稱 | 用途 |
|---|---|
| id | 稿件編號 |
| author_id | 作者編號，對應 users.id |
| category | 投稿類別 |
| title | 稿件標題 |
| content | 文章內容 |
| status | 稿件審查狀態 |

### 3. 資料表關聯

`manuscripts.author_id` 對應 `users.id`，用來判斷每篇稿件所屬的作者。

## 七、系統功能

### 1. 作者功能

- 查看自己的投稿稿件清單（類別、標題、審查狀態）。
- 新增投稿（類別、標題、文章內容）。
- 查看單篇稿件詳細內容。
- 編輯投稿。
- 刪除編輯中的稿件。
- 送出投稿進入審查。

### 2. 編輯功能

- 查看待審查的投稿清單（作者、類別、標題）。
- 查看投稿詳細內容。
- 通過投稿。
- 退回投稿，讓作者重新編輯。

## 八、稿件狀態流程

| 操作 | 狀態變化 |
|---|---|
| 新增投稿 | 編輯中 |
| 作者送出投稿 | 編輯中 → 審查中 |
| 編輯通過投稿 | 審查中 → 已通過 |
| 編輯退回投稿 | 審查中 → 編輯中 |

## 九、系統操作方式

### 1. 安裝套件

在終端機輸入：

```bash
pip install -r requirements.txt
```

### 2. 設定資料庫

- 安裝並啟動 PostgreSQL。
- 建立 `submission_system` 資料庫。
- 設定 `.env` 中的資料庫連線資訊。

### 3. 啟動系統

在專案資料夾中開啟終端機，輸入：

```bash
uvicorn main:app --reload
```

### 4. 開啟系統

啟動成功後，在瀏覽器輸入：

```text
http://127.0.0.1:8000
```

也可以透過以下網址查看 API 文件：

```text
http://127.0.0.1:8000/docs
```

## 十、專案檔案結構

```text
submission_system/
│
├── main.py
├── db.py
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── author.html
    ├── add_manuscript.html
    ├── edit_manuscript.html
    ├── editor.html
    └── editor_manuscript.html
```

