from typing import List
from tgbot.db_crud.db_connection import DBConnection


class AdminData:
    def __init__(self, db: DBConnection):
        self.db = db

    async def get_admin_id_by_tg_id(self, tg_id: int) -> int:
        select_script = '''
            SELECT admin_id 
            FROM admin
            WHERE tg_id = $1;'''

        admin_id = await self.db.fetchval(select_script, tg_id)
        return admin_id

    async def create_admin(self, tg_id: int) -> None:
        insert_script = '''
            INSERT INTO admin(tg_id) 
            VALUES($1);'''
        await self.db.execute(insert_script, tg_id)

    async def delete_admin(self, admin_id: int) -> None:
        delete_script = '''
            DELETE FROM admin
            WHERE admin_id = $1;'''
        await self.db.execute(delete_script, admin_id)
    
    async def get_all_admins_id(self) -> List[int]:
        select_script = '''
            SELECT admin_id 
            FROM admin;'''

        admins_id = await self.db.fetch(select_script)
        return [int(_id['admin_id']) for _id in admins_id]
    
    async def get_tg_id_by_admin_id(self, admin_id: int) -> int:
        select_script = '''
            SELECT tg_id 
            FROM admin
            WHERE admin_id = $1;'''

        tg_id = await self.db.fetchval(select_script, admin_id)
        return tg_id
    
    
