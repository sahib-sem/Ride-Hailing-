import aiosqlite
from Repositories.common_db import ensure_db_exists, drop_tables



async def check_user_exists(user_id : int):
    async with aiosqlite.connect('../ride.db') as db:
        await ensure_db_exists()

        sql_query = 'SELECT id FROM Users WHERE id = ?'
        
        cursor = await db.execute(sql_query, (user_id,))
        row = await cursor.fetchone() 

        if row:
            return True

        else:
            return False
    


async def register_user(user_data):

    name = user_data.get('name' , 'unknown')
    user_id = user_data.get('id')
    phone_number = user_data.get('user_phone_number', 'unknown')
    role = user_data.get('role')


    async with aiosqlite.connect('../ride.db') as db:

        await ensure_db_exists()
        await db.execute('INSERT INTO Users (id, name, phone_number, role) VALUES (?, ?, ?, ?)', (user_id, name, phone_number ,role,))
        await db.commit()
    
# unregister_user
async def unregister_user(user_id : int):
    async with aiosqlite.connect('../ride.db') as db:
        await db.execute('DELETE FROM Users WHERE id = ?', (user_id,))
        await db.commit()

async def get_user_role(user_id : int):
    async with aiosqlite.connect('../ride.db') as db:
        sql_query = 'SELECT role FROM Users WHERE id = ?'
        
        cursor = await db.execute(sql_query, (user_id,))
        row = await cursor.fetchone() 
        if row:
            return row[0]

        else:
            return None

async def update_user_name(user_id : int, name : str):
    async with aiosqlite.connect('../ride.db') as db:
        await db.execute('UPDATE Users SET name = ? WHERE id = ?', (name, user_id,))
        await db.commit()

async def update_user_phone_number(user_id : int, phone_number : str):
    async with aiosqlite.connect('../ride.db') as db:
        await db.execute('UPDATE Users SET phone_number = ? WHERE id = ?', (phone_number, user_id,))
        await db.commit()

async def get_name(user_id):
    async with aiosqlite.connect('../ride.db') as db:
        sql_query = 'SELECT name FROM Users WHERE id = ?'
        
        cursor = await db.execute(sql_query, (user_id,))
        row = await cursor.fetchone() 
        if row:
            return row[0]

        else:
            return None