import aiosqlite




async def ensure_db_exists():
    async with aiosqlite.connect('../ride.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, phone_number Text, role Text)')
        await db.execute('CREATE TABLE IF NOT EXISTS RideRequests (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, user_location TEXT, accepted_status TEXT, driver_id INTEGER)')
        await db.commit()
        

        

async def drop_tables():
    async with aiosqlite.connect('../ride.db') as db:
        sql_drop = 'DROP TABLE IF EXISTS Users'
        
        await db.execute(sql_drop)

        await db.commit()

