class Cart:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.goods = dict()

    def add_to_cart(self, service_name, service_price, chat_id):
        if self.chat_id == chat_id:
            self.goods[service_name] = service_price

    def remove_from_cart(self, service_name, chat_id):
        if self.goods and self.chat_id == chat_id:
            self.goods.pop(service_name)

    def total_price(self, chat_id):
        total = 0
        if self.chat_id == chat_id:
            for el in self.goods.keys():
                total += int(self.goods[el])

        return total

    def total_services(self, chat_id):
        list_services = []
        if self.chat_id == chat_id:
            for service in self.goods.keys():
                list_services.append(service)

        return list_services