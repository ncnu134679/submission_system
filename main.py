
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from db import getDB

app = FastAPI()


@app.get("/")
def home():
    return {"message": "投稿審查系統"}

@app.get("/author-page")
def author_page():
    return FileResponse("templates/author.html")

@app.get("/add-manuscript-page")
def add_manuscript_page():
    return FileResponse("templates/add_manuscript.html")

@app.get("/edit-manuscript-page")
def edit_manuscript_page():
    return FileResponse("templates/edit_manuscript.html")

@app.get("/editor-page")
def editor_page():
    return FileResponse("templates/editor.html")

@app.get("/editor-manuscript-page")
def editor_manuscript_page():
    return FileResponse("templates/editor_manuscript.html")


# 資料庫測試
@app.get("/test-db")
def test_db():
    conn = getDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


# 作者投稿清單
@app.get("/author/{author_id}/manuscripts")
def get_manuscripts(author_id: int):
    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, category, title, status
        FROM manuscripts
        WHERE author_id = %s
        ORDER BY id DESC
    """, (author_id,))

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


# 作者單篇稿件資料
@app.get("/author/{author_id}/manuscripts/{manuscript_id}")
def get_author_manuscript(author_id: int, manuscript_id: int):
    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, category, title, content, status
        FROM manuscripts
        WHERE id = %s
        AND author_id = %s
        AND status = '編輯中'
    """, (manuscript_id, author_id))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is None:
        return {"message": "找不到稿件，或稿件目前無法編輯"}

    return result


# 作者：新增投稿
@app.post("/author/{author_id}/manuscripts")
def add_manuscript(
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

    manuscript_id = cur.fetchone()["id"]

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿新增成功",
        "id": manuscript_id,
        "status": "編輯中"
    }


# 作者：修改投稿
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
        return {"message": "找不到稿件，或稿件目前無法編輯"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿修改成功",
        "id": result["id"]
    }


# 作者刪除
@app.delete("/author/{author_id}/manuscripts/{manuscript_id}")
def delete_manuscript(
    author_id: int,
    manuscript_id: int
):
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
        return {"message": "找不到稿件，或稿件目前無法刪除"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "稿件刪除成功",
        "id": result["id"]
    }


# 作者送出
@app.put("/author/{author_id}/manuscripts/{manuscript_id}/submit")
def submit_manuscript(
    author_id: int,
    manuscript_id: int
):
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
        return {"message": "找不到稿件，或稿件目前無法送出"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "投稿送出成功",
        "id": result["id"],
        "status": "審查中"
    }


# 編輯查看清單
@app.get("/editor/manuscripts")
def get_pending_manuscripts():
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


# 編輯查看內容
@app.get("/editor/manuscripts/{manuscript_id}")
def get_manuscript_content(manuscript_id: int):
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
        return {"message": "找不到稿件，或稿件目前不是審查中"}

    return result


# 編輯審核通過
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
        return {"message": "找不到稿件，或稿件目前無法通過"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "稿件審查通過",
        "id": result["id"],
        "status": "已通過"
    }


# 編輯退回投稿
@app.put("/editor/manuscripts/{manuscript_id}/return")
def return_manuscript(manuscript_id: int):
    conn = getDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE manuscripts
        SET status = '編輯中'
        WHERE id = %s
        AND status = '審查中'
        RETURNING id
    """, (manuscript_id,))

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return {"message": "找不到稿件，或稿件目前無法退回"}

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "稿件已退回",
        "id": result["id"],
        "status": "編輯中"
    }
