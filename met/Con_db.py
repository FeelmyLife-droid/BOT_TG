import aiosqlite


class Con_DB:
    def __init__(self, path_to_db='data/test.sql'):
        self.path_to_db = path_to_db

    @property
    async def connection(self):
        return await aiosqlite.connect(self.path_to_db)

    async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        connection = await self.connection
        cursor = await connection.cursor()
        data = None
        await connection.execute(sql, parameters)

        if commit:
            await connection.commit()
        if fetchone:
            data = await cursor.fetchone()
        if fetchall:
            data = await cursor.fetchall()

        await connection.close()

        return data

    async def create_table_users(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS firms(
            ИНН TEXT NOT NULL) 
        '''
        await self.execute(sql, commit=True)

    async def add_firms(self, inn: str):
        sql = '''
        INSERT INTO firms(ИНН) VALUES(?)
        '''
        parameters = (inn,)
        await self.execute(sql, parameters=parameters, commit=True)

    async def select_all_firms(self):
        await self.create_table_users()
        sql = '''
        SELECT * FROM firms
        '''
        return await self.execute(sql, fetchall=True)

    @staticmethod
    async def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    async def check_in(self, inn: str):
        result = await self.execute('SELECT * FROM firms WHERE ИНН = ?', (inn,), fetchall=True)
        print(result)
        return bool(len(result))

    async def select_firm(self, **kwargs):
        sql = '''
        SELECT * FROM firms WHERE
        '''
        sql, parameters = await self.format_args(sql, kwargs)
        return await self.execute(sql, parameters, fetchone=True)

    async def count_firms(self):
        return await self.execute("SELECT COUNT (*) FROM firms;", fetchone=True)

    async def delete_firms(self):
        await self.execute("DELETE FROM firms", commit=True)
