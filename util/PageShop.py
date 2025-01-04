class PageShop:
    def __init__(self):
        self.list = []
        self.id_counter = 0

    def addRole(self, role, user, price):
        self.id_counter += 1
        self.list.append({"id": self.id_counter, "role": role, "user": user, "price": price})

    def get_items(self):
        return self.list

    def get_role_by_id(self, role_id):
        for item in self.list:
            if item["id"] == role_id:
                return item
        return None

class PageShopManager:
    def __init__(self, items_per_page):
        self.pages = []
        self.items_per_page = items_per_page
        self.current_page_index = 0

    def load_items(self, items):
        self.pages = []
        for i in range(0, len(items), self.items_per_page):
            self.pages.append(items[i:i + self.items_per_page])

    def get_current_page(self):
        if self.pages:
            return self.pages[self.current_page_index]
        return []

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1

    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1