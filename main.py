
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from db import getDB

app = FastAPI()


# ==============================
# 網頁路由
# ==============================

# 首頁
@app.get("/")
def home():
    return FileResponse("templates/index.html")


# 顯示作者投稿頁面
@app.get("/author-page")
def author_page():
    return FileResponse("templates/author.html")


# 顯示新增投稿頁面
@app.get("/add-manuscript-page")
def add_manuscript_page():
    return FileResponse("templates/add_manuscript.html")


# 顯示編輯投稿頁面
@app.get("/edit-manuscript-page")
def edit_manuscript_page():
    return FileResponse("templates/edit_manuscript.html")


# 顯示編輯端投稿清單
@app.get("/editor-page")
def editor_page():
    return FileResponse("templates/editor.html")


# 顯示編輯端投稿內容
@app.get("/editor-manuscript-page")
def editor_manuscript_page():
    return FileResponse("templates/editor_manuscript.html")


# ==============================
# 資料庫測試
# ==============================

@app.get("/test-db")
def test_db():
    conn = getDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


# ==============================
# 作者功能
# ==============================

# 查看作者的投稿清單
@app.get("/author/{author_id}/manuscripts")
def get_author_manuscripts(author_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, category, title, status, editor_feedback
        FROM manuscripts
        WHERE author_id = %s
        ORDER BY id DESC
    """, (author_id,))

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


# 查看單篇投稿（僅限編輯中）
@app.get("/author/{author_id}/manuscripts/{manuscript_id}")
def get_manuscript(author_id: int, manuscript_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, category, title, content, status, editor_feedback
        FROM manuscripts
        WHERE id = %s
        AND author_id = %s
        AND status = '編輯中'
    """, (manuscript_id, author_id))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is None:
        return {"message": "找不到稿件或目前無法編輯"}

    return result


# 新增投稿
@app.post("/author/{author_id}/manuscripts")
def create_manuscript(
    author_id: int,
    category: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO manuscripts
        (author_id, category, title, content)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (author_id, category, title, content))

    result = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿新增成功",
        "id": result["id"],
        "status": "編輯中"
    }


# 修改投稿
@app.put("/author/{author_id}/manuscripts/{manuscript_id}")
def update_manuscript(
    author_id: int,
    manuscript_id: int,
    category: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE manuscripts
        SET category = %s,
            title = %s,
            content = %s
        WHERE id = %s
        AND author_id = %s
        AND status = '編輯中'
        RETURNING id
    """, (category, title, content, manuscript_id, author_id))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "找不到稿件或目前無法修改"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿修改成功",
        "id": manuscript_id
    }


# 刪除投稿
@app.delete("/author/{author_id}/manuscripts/{manuscript_id}")
def delete_manuscript(author_id: int, manuscript_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM manuscripts
        WHERE id = %s
        AND author_id = %s
        AND status = '編輯中'
        RETURNING id
    """, (manuscript_id, author_id))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "找不到稿件或目前無法刪除"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿刪除成功",
        "id": manuscript_id
    }


# 送出投稿
@app.put("/author/{author_id}/manuscripts/{manuscript_id}/submit")
def submit_manuscript(author_id: int, manuscript_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE manuscripts
        SET status = '審查中'
        WHERE id = %s
        AND author_id = %s
        AND status = '編輯中'
        RETURNING id
    """, (manuscript_id, author_id))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "找不到稿件或目前無法送出"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿送出成功",
        "id": manuscript_id,
        "status": "審查中"
    }


# ==============================
# 編輯功能
# ==============================

# 查看待審查投稿清單
@app.get("/editor/manuscripts")
def get_editor_manuscripts():

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            manuscripts.id,
            users.username AS author,
            manuscripts.category,
            manuscripts.title
        FROM manuscripts
        JOIN users
        ON manuscripts.author_id = users.id
        WHERE manuscripts.status = '審查中'
        ORDER BY manuscripts.id DESC
    """)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


# 查看單篇投稿內容
@app.get("/editor/manuscripts/{manuscript_id}")
def get_editor_manuscript(manuscript_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            manuscripts.id,
            users.username AS author,
            manuscripts.category,
            manuscripts.title,
            manuscripts.content,
            manuscripts.status
        FROM manuscripts
        JOIN users
        ON manuscripts.author_id = users.id
        WHERE manuscripts.id = %s
        AND manuscripts.status = '審查中'
    """, (manuscript_id,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is None:
        return {"message": "找不到稿件或目前無法審查"}

    return result


# 通過投稿
@app.put("/editor/manuscripts/{manuscript_id}/approve")
def approve_manuscript(manuscript_id: int):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE manuscripts
        SET status = '已通過'
        WHERE id = %s
        AND status = '審查中'
        RETURNING id
    """, (manuscript_id,))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "找不到稿件或目前無法通過"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "稿件已通過",
        "id": manuscript_id,
        "status": "已通過"
    }


# 不通過投稿，並儲存編輯建議
@app.put("/editor/manuscripts/{manuscript_id}/return")
def return_manuscript(
    manuscript_id: int,
    editor_feedback: str = Form(...)
):

    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE manuscripts
        SET status = '編輯中',
            editor_feedback = %s
        WHERE id = %s
        AND status = '審查中'
        RETURNING id
    """, (editor_feedback, manuscript_id))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "稿件不存在或目前無法退回"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "稿件已退回",
        "id": manuscript_id,
        "status": "編輯中",
        "editor_feedback": editor_feedback
    }
