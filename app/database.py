import aiosqlite as sq
import pandas as pd

from config import DB_NAME


async def create_db():
    async with sq.connect(DB_NAME) as db:
        print("Database created!")

        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            users_count INTEGER,
            photo TEXT,
            document TEXT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS registers (
            register_id INTEGER PRIMARY KEY,
            full_name TEXT,
            date_age INTEGER,
            rider_exp TEXT,
            skate TEXT,
            helmet TEXT,
            defender TEXT,
            parents_name TEXT,
            parents_contact TEXT,
            event_id INTEGER,
            email TEXT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS accepted (
                    register_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    date_age INTEGER,
                    rider_exp TEXT,
                    skate TEXT,
                    helmet TEXT,
                    defender TEXT,
                    parents_name TEXT,
                    parents_contact TEXT,
                    event_id INTEGER,
                    email TEXT
                )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS rejected (
                            register_id INTEGER PRIMARY KEY,
                            full_name TEXT,
                            date_age INTEGER,
                            rider_exp TEXT,
                            skate TEXT,
                            helmet TEXT,
                            defender TEXT,
                            parents_name TEXT,
                            parents_contact TEXT,
                            event_id INTEGER,
                            reason TEXT,
                            email TEXT
                        )""")


        # await db.execute("ALTER TABLE events ADD COLUMN document TEXT")

        await db.commit()


async def insert_user(user_id, username):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (user_id, username))
        await db.commit()


async def get_all_users():
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, username FROM users") as cursor:
            return await cursor.fetchall()


async def insert_event(name, description, users_count, photo, document):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO events(name, description, users_count, photo, document) VALUES (?, ?, ?, ?, ?)",
                         (name, description, users_count, photo, document))
        await db.commit()


async def get_event_id(name, description, users_count, photo, document):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT event_id FROM events WHERE name = ? AND description = ? AND users_count = ? AND photo = ? AND document = ?",
                              (name, description, users_count, photo, document)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_all_events():
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM events") as cursor:
            return await cursor.fetchall()


async def get_event(event_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)) as cursor:
            return await cursor.fetchone()


async def delete_event(event_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
        await db.commit()


async def update_event_name(event_id, new_name):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE events SET name = ? WHERE event_id = ?", (new_name, event_id))
        await db.commit()


async def update_event_description(event_id, new_description):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE events SET description = ? WHERE event_id = ?", (new_description, event_id))
        await db.commit()


async def update_event_users_count(event_id, new_users_count):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE events SET users_count = ? WHERE event_id = ?", (new_users_count, event_id))
        await db.commit()


async def update_event_photo(event_id, new_photo):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE events SET photo = ? WHERE event_id = ?", (new_photo, event_id))
        await db.commit()


async def update_event_document(event_id, new_document):
    async with sq.connect(DB_NAME) as db:
        await db.execute("UPDATE events SET document = ? WHERE event_id = ?", (new_document, event_id))
        await db.commit()


async def insert_register(full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO registers(full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email))
        await db.commit()


async def get_register_id(full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT register_id FROM registers WHERE full_name = ? AND date_age = ? AND rider_exp = ? AND skate = ? AND helmet = ? AND defender = ? AND parents_name = ? AND parents_contact = ? AND event_id = ? AND email = ?",
                              (full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_register(register_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM registers WHERE register_id = ?", (register_id,)) as cursor:
            return await cursor.fetchone()


async def delete_register(event_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute("DELETE FROM registers WHERE event_id = ?", (event_id,))
        await db.commit()


async def insert_accepted(register_id, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT INTO accepted VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (register_id, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email))
        await db.commit()


async def get_accepted_count(event_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM accepted WHERE event_id = ?", (event_id,)) as cursor:
            return (await cursor.fetchone())[0]


async def get_accepted(accepted_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM accepted WHERE register_id = ?", (accepted_id,)) as cursor:
            return await cursor.fetchone()


async def delete_accepted(event_id):
    async with sq.connect(DB_NAME) as db:
        await db.execute("DELETE FROM accepted WHERE event_id = ?", (event_id,))
        await db.commit()


async def insert_rejected(register_id, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, reason, email):
    async with sq.connect(DB_NAME) as db:
        await db.execute("INSERT INTO rejected VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (register_id, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, reason, email))
        await db.commit()


async def get_rejected(reject_id):
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM rejected WHERE register_id = ?", (reject_id,)) as cursor:
            return await cursor.fetchone()


async def get_rejected_count():
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM rejected") as cursor:
            return (await cursor.fetchone())[0]


async def get_all_rejected():
    async with sq.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM rejected") as cursor:
            return await cursor.fetchall()


async def save_to_excel(event_id, event_name):
    async with sq.connect(DB_NAME) as db:
        query = f"SELECT * FROM accepted WHERE event_id = ?"
        async with db.execute(query, (event_id,)) as cursor:
            # Получаем данные из курсора
            rows = await cursor.fetchall()
            # Получаем названия колонок
            column_names = [description[0] for description in cursor.description]

        # Создаем DataFrame из полученных данных
        df = pd.DataFrame(rows, columns=column_names)

        # Запись данных в Excel файл
        df.to_excel(f'{event_name}.xlsx', index=False)

        return f'{event_name}.xlsx'


