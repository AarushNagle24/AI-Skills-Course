import secrets
import sqlite3
import string
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).with_name("ai_skills_courses.db")
SEEDED_CREATION_KEYS = [
    ("A7xQ9L2#mP4zR8$", "generic"),
    ("B4nT6K1@vS8pL3!", "generic"),
    ("C9rM2V5&hQ7wN6?", "generic"),
    ("D5pR8#vL2qM9sT!", "generic"),
    ("E2mN7@kQ4zP8rW$", "generic"),
    ("F9tL3&xA6cR2vH?", "generic"),
    ("G4wC8!nP5yK1qZ#", "generic"),
    ("H6zV2$eT9mB4xL@", "generic"),
    ("J8qP3#rN6vC1sY!", "generic"),
    ("K2mW9@tH5xD7pR$", "generic"),
    ("L7cA4&zQ8nF2vT?", "generic"),
    ("N3yR6!pK9mE5xB#", "generic"),
    ("P5vT1$sL8qG4nW@", "generic"),
    ("M4rK9A2!dQ7xP5$", "marketing_advertising"),
    ("Ad8V2#kL9pQ4zR!", "marketing_advertising"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company_name TEXT NOT NULL,
                company_type TEXT NOT NULL,
                description TEXT NOT NULL,
                join_code TEXT NOT NULL UNIQUE,
                admin_user_id INTEGER NOT NULL,
                content_template TEXT NOT NULL DEFAULT 'generic',
                created_at TEXT NOT NULL,
                FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS course_creation_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_value TEXT NOT NULL UNIQUE,
                used INTEGER NOT NULL DEFAULT 0,
                used_by_user_id INTEGER,
                used_for_course_id INTEGER,
                content_template TEXT NOT NULL DEFAULT 'generic',
                created_at TEXT NOT NULL,
                used_at TEXT,
                FOREIGN KEY (used_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
                FOREIGN KEY (used_for_course_id) REFERENCES courses(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(user_id, course_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                reading_viewed INTEGER NOT NULL DEFAULT 0,
                quiz_completed INTEGER NOT NULL DEFAULT 0,
                quiz_score INTEGER NOT NULL DEFAULT 0,
                progress_percent INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, course_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS contact_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company_name TEXT NOT NULL,
                work_email TEXT NOT NULL,
                company_type TEXT NOT NULL,
                employee_count TEXT NOT NULL,
                requested_skills TEXT NOT NULL,
                additional_notes TEXT,
                created_at TEXT NOT NULL
            );
            """
        )
        ensure_column(conn, "courses", "content_template", "TEXT NOT NULL DEFAULT 'generic'")
        ensure_column(conn, "course_creation_keys", "content_template", "TEXT NOT NULL DEFAULT 'generic'")
        for key_value, content_template in SEEDED_CREATION_KEYS:
            conn.execute(
                """
                INSERT OR IGNORE INTO course_creation_keys (key_value, used, content_template, created_at)
                VALUES (?, 0, ?, ?)
                """,
                (key_value, content_template, utc_now()),
            )
            conn.execute(
                """
                UPDATE course_creation_keys
                SET content_template = ?
                WHERE key_value = ? AND used = 0
                """,
                (content_template, key_value),
            )


def ensure_column(conn: sqlite3.Connection, table_name: str, column_name: str, definition: str) -> None:
    columns = [row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
    if column_name not in columns:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def create_user(username: str, password_hash: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash, utc_now()),
        )
        return int(cursor.lastrowid)


def get_user_by_username(username: str):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def get_user_by_id(user_id: int):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def change_user_password(user_id: int, password_hash: str) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))


def create_contact_request(
    name: str,
    company_name: str,
    work_email: str,
    company_type: str,
    employee_count: str,
    requested_skills: str,
    additional_notes: str,
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO contact_requests (
                name, company_name, work_email, company_type, employee_count,
                requested_skills, additional_notes, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                company_name,
                work_email,
                company_type,
                employee_count,
                requested_skills,
                additional_notes,
                utc_now(),
            ),
        )
        return int(cursor.lastrowid)


def validate_creation_key(key_value: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM course_creation_keys WHERE key_value = ? AND used = 0",
            (key_value,),
        ).fetchone()
        return row is not None


def generate_join_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    with get_connection() as conn:
        while True:
            code = "".join(secrets.choice(alphabet) for _ in range(6))
            exists = conn.execute("SELECT 1 FROM courses WHERE join_code = ?", (code,)).fetchone()
            if not exists:
                return code


def create_course_from_key(
    key_value: str,
    admin_user_id: int,
    title: str,
    company_name: str,
    company_type: str,
    description: str,
) -> int:
    join_code = generate_join_code()
    with get_connection() as conn:
        key_row = conn.execute(
            "SELECT * FROM course_creation_keys WHERE key_value = ? AND used = 0",
            (key_value,),
        ).fetchone()
        if not key_row:
            raise ValueError("This creation key is invalid or has already been used")

        cursor = conn.execute(
            """
            INSERT INTO courses (
                title, company_name, company_type, description, join_code,
                admin_user_id, content_template, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                company_name,
                company_type,
                description,
                join_code,
                admin_user_id,
                key_row["content_template"],
                utc_now(),
            ),
        )
        course_id = int(cursor.lastrowid)
        conn.execute(
            """
            UPDATE course_creation_keys
            SET used = 1, used_by_user_id = ?, used_for_course_id = ?, used_at = ?
            WHERE id = ?
            """,
            (admin_user_id, course_id, utc_now(), key_row["id"]),
        )
        return course_id


def get_course_by_join_code(join_code: str):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM courses WHERE join_code = ?", (join_code,)).fetchone()


def ensure_progress_row(conn: sqlite3.Connection, user_id: int, course_id: int) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO progress (
            user_id, course_id, reading_viewed, quiz_completed,
            quiz_score, progress_percent, updated_at
        )
        VALUES (?, ?, 0, 0, 0, 0, ?)
        """,
        (user_id, course_id, utc_now()),
    )


def enroll_user_in_course(user_id: int, join_code: str):
    clean_code = join_code.strip().upper()
    if len(clean_code) != 6:
        return "invalid", "Course code must be exactly 6 characters"
    with get_connection() as conn:
        course = conn.execute("SELECT * FROM courses WHERE join_code = ?", (clean_code,)).fetchone()
        if not course:
            return "invalid", "No course was found for that code"

        existing = conn.execute(
            "SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?",
            (user_id, course["id"]),
        ).fetchone()
        if existing:
            return "already", "You are already enrolled in this course"

        conn.execute(
            "INSERT INTO enrollments (user_id, course_id, created_at) VALUES (?, ?, ?)",
            (user_id, course["id"], utc_now()),
        )
        ensure_progress_row(conn, user_id, course["id"])
        return "success", f"You joined {course['title']}"


def leave_course(user_id: int, course_id: int) -> bool:
    with get_connection() as conn:
        enrollment = conn.execute(
            "SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?",
            (user_id, course_id),
        ).fetchone()
        if not enrollment:
            return False

        conn.execute(
            "DELETE FROM enrollments WHERE user_id = ? AND course_id = ?",
            (user_id, course_id),
        )
        conn.execute(
            "DELETE FROM progress WHERE user_id = ? AND course_id = ?",
            (user_id, course_id),
        )
        return True


def get_enrolled_courses(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                c.*,
                COALESCE(p.progress_percent, 0) AS progress_percent
            FROM enrollments e
            JOIN courses c ON c.id = e.course_id
            LEFT JOIN progress p ON p.user_id = e.user_id AND p.course_id = e.course_id
            WHERE e.user_id = ?
            ORDER BY e.created_at DESC
            """,
            (user_id,),
        ).fetchall()


def get_admin_courses(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                c.*,
                COUNT(e.id) AS employee_count,
                CAST(COALESCE(ROUND(AVG(p.progress_percent)), 0) AS INTEGER) AS average_progress
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN progress p ON p.user_id = e.user_id AND p.course_id = c.id
            WHERE c.admin_user_id = ?
            GROUP BY c.id
            ORDER BY c.created_at DESC
            """,
            (user_id,),
        ).fetchall()


def get_course_for_learning(user_id: int, course_id: int):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT c.*
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id AND e.user_id = ?
            WHERE c.id = ?
              AND (e.user_id IS NOT NULL OR c.admin_user_id = ?)
            """,
            (user_id, course_id, user_id),
        ).fetchone()


def get_progress(user_id: int, course_id: int):
    with get_connection() as conn:
        ensure_progress_row(conn, user_id, course_id)
        return conn.execute(
            "SELECT * FROM progress WHERE user_id = ? AND course_id = ?",
            (user_id, course_id),
        ).fetchone()


def mark_reading_viewed(user_id: int, course_id: int) -> None:
    with get_connection() as conn:
        ensure_progress_row(conn, user_id, course_id)
        conn.execute(
            """
            UPDATE progress
            SET reading_viewed = 1,
                updated_at = ?
            WHERE user_id = ? AND course_id = ?
            """,
            (utc_now(), user_id, course_id),
        )


def mark_quiz_completed(user_id: int, course_id: int, score: int) -> None:
    with get_connection() as conn:
        ensure_progress_row(conn, user_id, course_id)
        conn.execute(
            """
            UPDATE progress
            SET reading_viewed = 1,
                quiz_completed = 1,
                quiz_score = ?,
                progress_percent = 100,
                updated_at = ?
            WHERE user_id = ? AND course_id = ?
            """,
            (score, utc_now(), user_id, course_id),
        )


def mark_course_step_completed(user_id: int, course_id: int, completed_steps: int, score: int) -> None:
    completed_steps = max(0, min(5, completed_steps))
    progress_percent = completed_steps * 20
    quiz_completed = 1 if completed_steps >= 5 else 0
    with get_connection() as conn:
        ensure_progress_row(conn, user_id, course_id)
        conn.execute(
            """
            UPDATE progress
            SET reading_viewed = 1,
                quiz_completed = CASE
                    WHEN ? = 1 THEN 1
                    ELSE quiz_completed
                END,
                quiz_score = ?,
                progress_percent = CASE
                    WHEN progress_percent < ? THEN ?
                    ELSE progress_percent
                END,
                updated_at = ?
            WHERE user_id = ? AND course_id = ?
            """,
            (
                quiz_completed,
                score,
                progress_percent,
                progress_percent,
                utc_now(),
                user_id,
                course_id,
            ),
        )


def get_admin_course(admin_user_id: int, course_id: int):
    with get_connection() as conn:
        course = conn.execute(
            """
            SELECT
                c.*,
                CAST(COALESCE(ROUND(AVG(p.progress_percent)), 0) AS INTEGER) AS average_progress
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN progress p ON p.user_id = e.user_id AND p.course_id = c.id
            WHERE c.id = ? AND c.admin_user_id = ?
            GROUP BY c.id
            """,
            (course_id, admin_user_id),
        ).fetchone()
        employees = conn.execute(
            """
            SELECT
                u.id AS user_id,
                u.username,
                COALESCE(p.progress_percent, 0) AS progress_percent,
                COALESCE(p.quiz_completed, 0) AS quiz_completed
            FROM enrollments e
            JOIN users u ON u.id = e.user_id
            LEFT JOIN progress p ON p.user_id = e.user_id AND p.course_id = e.course_id
            WHERE e.course_id = ?
            ORDER BY u.username
            """,
            (course_id,),
        ).fetchall()
        return course, employees


def remove_employee_from_course(admin_user_id: int, course_id: int, employee_user_id: int) -> bool:
    with get_connection() as conn:
        course = conn.execute(
            "SELECT id FROM courses WHERE id = ? AND admin_user_id = ?",
            (course_id, admin_user_id),
        ).fetchone()
        if not course:
            return False

        conn.execute(
            "DELETE FROM enrollments WHERE user_id = ? AND course_id = ?",
            (employee_user_id, course_id),
        )
        conn.execute(
            "DELETE FROM progress WHERE user_id = ? AND course_id = ?",
            (employee_user_id, course_id),
        )
        return True


def delete_admin_course(admin_user_id: int, course_id: int) -> bool:
    with get_connection() as conn:
        course = conn.execute(
            "SELECT id FROM courses WHERE id = ? AND admin_user_id = ?",
            (course_id, admin_user_id),
        ).fetchone()
        if not course:
            return False

        conn.execute(
            "DELETE FROM progress WHERE course_id = ?",
            (course_id,),
        )
        conn.execute(
            "DELETE FROM enrollments WHERE course_id = ?",
            (course_id,),
        )
        conn.execute(
            "DELETE FROM courses WHERE id = ? AND admin_user_id = ?",
            (course_id, admin_user_id),
        )
        return True


def regenerate_join_code(admin_user_id: int, course_id: int) -> str:
    new_code = generate_join_code()
    with get_connection() as conn:
        course = conn.execute(
            "SELECT id FROM courses WHERE id = ? AND admin_user_id = ?",
            (course_id, admin_user_id),
        ).fetchone()
        if not course:
            raise ValueError("Course not found")
        conn.execute("UPDATE courses SET join_code = ? WHERE id = ?", (new_code, course_id))
        return new_code


def update_course_details(admin_user_id: int, course_id: int, title: str, description: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE courses
            SET title = ?, description = ?
            WHERE id = ? AND admin_user_id = ?
            """,
            (title, description, course_id, admin_user_id),
        )
