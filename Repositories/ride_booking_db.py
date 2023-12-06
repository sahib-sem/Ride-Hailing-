import aiosqlite
from Repositories.common_db import ensure_db_exists
from Repositories.user_db import get_name




async def save_ride_request(ride_data):
    user_id = ride_data.get('user_id')
    user_location = ride_data.get('user_location')

    async with aiosqlite.connect('../ride.db') as db:
        await ensure_db_exists()
        cur = await db.execute('INSERT INTO RideRequests (user_id, user_location, accepted_status) VALUES (?, ?, ?)', (user_id, user_location, 'pending',))
        await db.commit()

        return cur.lastrowid

async def get_ride_requests():
    async with aiosqlite.connect('../ride.db') as db:
        await ensure_db_exists()
        sql_query = 'SELECT * FROM RideRequests WHERE accepted_status = ?'
        
        cursor = await db.execute(sql_query, ('pending',))
        rows = await cursor.fetchall() 
        return rows

async def get_ride_history(user_id):
    async with aiosqlite.connect('../ride.db') as db:

        # status must be accepted
        await ensure_db_exists()
        sql_query = 'SELECT * FROM RideRequests WHERE user_id = ? AND accepted_status = ?'

        cursor = await db.execute(sql_query, (user_id, 'accepted',))
        rows = await cursor.fetchall()
        return rows

async def accept_ride_request(ride_id , driver_id):

    async with aiosqlite.connect('../ride.db') as db:

        await ensure_db_exists()
        sql_query = 'UPDATE RideRequests SET accepted_status = ?, driver_id = ? WHERE id = ?'

        await db.execute(sql_query, ('accepted', driver_id, ride_id,))
        await db.commit()





async def cancel_ride(ride_id):

    async with aiosqlite.connect('../ride.db') as db:

        await ensure_db_exists()
        sql_query = 'UPDATE RideRequests SET accepted_status = ? WHERE id = ?'
        
        await db.execute(sql_query, ('cancelled', ride_id,))
        await db.commit()