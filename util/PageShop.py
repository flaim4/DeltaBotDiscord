from util.db import Data

class PageShop:
    def __init__(self):
        super().__init__()
        self.list = []

    def get_role_by_role_id(self, role_id, server_id):
        self.cur.execute("SELECT id, role_id, user_id, price FROM Role WHERE server_id = ? AND role_id = ?", (server_id, role_id))
        row = self.cur.fetchone()
        return {"id": row[0], "role_id": row[1], "user_id": row[2], "price": row[3]} if row else None

    def add_role(self, role_id, user_id, price, server_id):
        self.cur.execute("SELECT MAX(id) FROM Role")
        max_id = self.cur.fetchone()[0]

        new_id = max_id + 1 if max_id is not None else 1

        self.cur.execute("""INSERT INTO Role (id, server_id, user_id, role_id, price) VALUES (?, ?, ?, ?, ?)""", (new_id, server_id, user_id, role_id, price))
        Data.commit()

    def get_items(self, server_id):
        self.cur.execute("SELECT id, role_id, user_id, price FROM Role WHERE server_id = ?", (server_id,))
        rows = self.cur.fetchall()
        return [{"id": row[0], "role": row[1], "user": row[2], "price": row[3]} for row in rows]

    def get_role_by_id(self, role_id, server_id):
        self.cur.execute("SELECT id, role_id, user_id, price FROM Role WHERE server_id = ? AND id = ?", (server_id, role_id))
        row = self.cur.fetchone()
        return {"id": row[0], "role": row[1], "user": row[2], "price": row[3]} if row else None


    def remove_role_by_id(self, role_id, server_id):
        self.cur.execute(
            "SELECT id, role_id, user_id, price FROM Role WHERE server_id = ? AND id = ?",
            (server_id, role_id)
        )
        row = self.cur.fetchone()

        if row:
            self.cur.execute(
                "DELETE FROM Role WHERE server_id = ? AND id = ?",
                (server_id, role_id)
            )
            Data.commit()
            return {"id": row[0], "role": row[1], "user": row[2], "price": row[3]}
        return None

class PageShopManager:
    def __init__(self, items_per_page, page_shop, server_id):
        self.items_per_page = items_per_page
        self.page_shop = page_shop
        self.server_id = server_id
        self.pages = []
        self.current_page_index = 0
        self.load_pages()

    def load_pages(self):
        items = self.page_shop.get_items(self.server_id)
        self.pages = [
            items[i:i + self.items_per_page]
            for i in range(0, len(items), self.items_per_page)
        ]

    def get_current_page(self):
        if self.pages:
            return self.pages[self.current_page_index]
        return []

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            return True

    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            return True
