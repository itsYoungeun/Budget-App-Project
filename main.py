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
        title = f"*************{self.name}*************"
        ledger_str = ""
        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}".rjust(30 - len(description))
            ledger_str += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + "\n" + ledger_str + total

def create_spend_chart(categories):
    # Calculate total spent across all categories
    total_spent = sum(
        sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        for category in categories
    )
    
    chart = "Percentage spent by category\n"
    
    # Calculate the percentage spent for each category
    percentages = []
    for category in categories:
        spent = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        percentage = (spent / total_spent) * 100 if total_spent > 0 else 0
        percentages.append(int(percentage))
    
    # Build the chart (100% to 0%)
    for i in range(100, -1, -10):
        chart += f"{i:3}|" + ''.join(' o ' if percentage >= i else ' ' for percentage in percentages) + "\n"
    
    # Build the horizontal line
    chart += "    -" + "---" * len(categories) + "\n"
    
    # Add category names vertically under the bars
    max_length = max(len(category.name) for category in categories)
    for i in range(max_length):
        chart += "    "  # Leading space for alignment
        for category in categories:
            chart += f" {category.name[i] if i < len(category.name) else ' '} "
        chart += "\n"
    
    return chart.strip()

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