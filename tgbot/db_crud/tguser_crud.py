from tgbot.db_crud.db_connection import DBConnection


class TgUserData:
    def __init__(self, db: DBConnection):
        self.db = db

    async def create_tg_user(self, tg_id: int, first_name: str, last_name: str, tg_username) -> None:
        insert_script = '''
                INSERT INTO tg_users(tg_id, first_name, last_name, tg_username) 
                VALUES($1, $2, $3, $4);'''
        await self.db.execute(insert_script, tg_id, first_name, last_name, tg_username)
    
    async def check_tg_user_exists(self, tg_id: int) -> bool:
        select_script = '''
            SELECT tg_id
            FROM tg_users
            WHERE tg_id = $1;'''
        tg_id_exists = await self.db.fetchval(select_script, tg_id)

        return tg_id_exists is not None

    async def delete_tg_user(self, tg_id: int) -> None:
        delete_script = '''
            DELETE FROM tg_users
            WHERE tg_id = $1;'''
        await self.db.execute(delete_script, tg_id)

    async def get_tg_username(self, tg_id: int) -> str:
        select_script = '''
            SELECT tg_username
            FROM tg_users
            WHERE tg_id = $1;'''
        username = await self.db.fetchval(select_script, tg_id)

        return username

    async def get_first_name(self, tg_id: int) -> str:
        select_script = '''
            SELECT first_name
            FROM tg_users
            WHERE tg_id = $1;'''
        first_name = await self.db.fetchval(select_script, tg_id)

        return first_name

    async def get_last_name(self, tg_id: int) -> str:
        select_script = '''
            SELECT last_name
            FROM tg_users
            WHERE tg_id = $1;'''
        last_name = await self.db.fetchval(select_script, tg_id)

        return last_name

    async def is_blocked(self, tg_id: int) -> bool:
        select_script = '''
            SELECT is_blocked
            FROM tg_users
            WHERE tg_id = $1;'''
        status = await self.db.fetchval(select_script, tg_id)

        return status

    async def update_tg_username(self, tg_id: int, new_username: str) -> None:
        update_script = '''
            UPDATE tg_users
            SET tg_username = $1
            WHERE tg_id = $2;'''
        await self.db.execute(update_script, new_username, tg_id)

    async def update_first_name(self, tg_id: int, new_first_name: str) -> None:
        update_script = '''
            UPDATE tg_users
            SET first_name = $1
            WHERE tg_id = $2;'''
        await self.db.execute(update_script, new_first_name, tg_id)

    async def update_last_name(self, tg_id: int, new_last_name: str) -> None:
        update_script = '''
            UPDATE tg_users
            SET last_name = $1
            WHERE tg_id = $2;'''
        await self.db.execute(update_script, new_last_name, tg_id)

    async def block(self, tg_id: int) -> None:
        update_script = '''
            UPDATE tg_users
            SET is_blocked = TRUE
            WHERE tg_id = $1;'''
        await self.db.execute(update_script, tg_id)

    async def unblock(self, tg_id: int) -> None:
        update_script = '''
            UPDATE tg_users
            SET is_blocked = FALSE
            WHERE tg_id = $1;'''
        await self.db.execute(update_script, tg_id)
    
    async def get_all_tg_users(self) -> list:
        select_script = '''
            SELECT tg_id
            FROM tg_users;'''
        users_id = await self.db.fetch(select_script)

        return [int(user_id['tg_id']) for user_id in users_id]
