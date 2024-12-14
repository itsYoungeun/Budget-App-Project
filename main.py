class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name}".center(30, "*")
        ledger_str = ""
        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}".rjust(30 - len(description))
            ledger_str += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + "\n" + ledger_str + total

def create_spend_chart(categories):
    # Calculate total spent and percentages
    total_spent = sum(sum(-entry['amount'] for entry in cat.ledger if entry['amount'] < 0) for cat in categories)
    percentages = [
        int((sum(-entry['amount'] for entry in cat.ledger if entry['amount'] < 0) / total_spent) * 100 // 10 * 10)
        for cat in categories
    ]

    # Build the header
    chart = "Percentage spent by category\n"

    # Add the percentage lines (100% to 0%)
    for i in range(100, -1, -10):
        chart += f"{i:3}|"  # Add percentage label with alignment
        for percentage in percentages:
            chart += " o " if percentage >= i else "   "
        chart += " \n"

    # Add the horizontal line
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Add the category names vertically
    category_names = [cat.name for cat in categories]
    max_length = max(len(name) for name in category_names)
    for i in range(max_length):
        chart += "    "  # Leading spaces
        for name in category_names:
            chart += f" {name[i] if i < len(name) else ' '} "
        chart += " \n"

    return chart.rstrip("\n")

# Example usage
food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
clothing.deposit(500, 'initial deposit')
clothing.withdraw(50, 'new clothes')

auto = Category('Auto')
auto.deposit(1000, 'initial deposit')
auto.withdraw(100, 'car maintenance')

food.transfer(50, clothing)
clothing.transfer(50, auto)

print(food)
print(clothing)
print(auto)
print(create_spend_chart([food, clothing, auto]))