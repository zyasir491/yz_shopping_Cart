from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase# Product Categories
class ShopCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def inventory_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["inventory_agent"],
        )
    @agent
    def sales_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_agent"],
        )

    @agent
    def accounting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["accounting_agent"],
        )

    @agent
    def hr_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_agent"],
        )

    @task
    def inventory_task(self) -> Task:
        return Task(
            config=self.tasks_config["inventory_task"],
        )

    @task
    def sales_task(self) -> Task:
        return Task(
            config=self.tasks_config["sales_task"],
        )

    @task
    def account_task(self) -> Task:
        return Task(
            config=self.tasks_config["account_task"],
        )

    '''@task
    def hr_task(self) -> Task:
        return Task(
            config=self.tasks_config["hr_task"],
        )'''

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""


        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )


class ProductCategory:
    def __init__(self, name):
        self.name = name
    
class Laptops(ProductCategory):
    def __init__(self):
        super().__init__("Laptops")

class Mobiles(ProductCategory):
    def __init__(self):
        super().__init__("Mobiles")

# Shopping Cart System
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, name, category, price, stock):
        self.products.append({"name": name, "category": category, "price": price, "stock": stock})

    def check_stock(self, product_name, quantity):
        for product in self.products:
            if product["name"] == product_name and product["stock"] >= quantity:
                return True
        return False

class Sales:
    def __init__(self):
        self.sales_records = []

    def process_sale(self, product_name, quantity, inventory):
        for product in inventory.products:
            if product["name"] == product_name and product["stock"] >= quantity:
                total_price = product["price"] * quantity
                product["stock"] -= quantity
                self.sales_records.append({"product": product_name, "quantity": quantity, "total_price": total_price})
                return f"Sale processed: {quantity} x {product_name} for ${total_price}"
        return "Sale failed: Insufficient stock"

class Accounting:
    def __init__(self):
        self.reports = []

    def generate_report(self, sales):
        report = sales.sales_records
        self.reports.append(report)
        return report

class HR:
    def __init__(self):
        self.employees = []

    def add_employee(self, name, department, salary):
        self.employees.append({"name": name, "department": department, "salary": salary})

# CrewAI Agents
'''inventory_agent = Agent(role="Inventory Manager", goal="Manage stock and ensure product availability.", backstory="You are a senior Inventory manager. You know how to manage inventory for the product stocks")
sales_agent = Agent(role="Sales Manager", goal="Process sales transactions and track sales.", backstory="You are a senior sales agent. Your job is to manage sales of the products")
accounting_agent = Agent(role="Finance Manager", goal="Generate financial reports.", backstory="You are a senior accounting agent. you manage all accounting of the sales transactions, discounts, employee salary")
hr_agent = Agent(role="HR Manager", goal="Manage employee records.", backstory="you are a senior HR manager. Your job is to hire and monitor employees performance")

# CrewAI Tasks
inventory_task = Task(description="Check product stock levels and update inventory.", expected_output="proper management of inventory and stocks level", agent=inventory_agent)
sales_task = Task(description="Process a customer's purchase.",expected_output="proper sales management", agent=sales_agent)
account_task = Task(description="Generate monthly financial sales report.",expected_output="financial sales reports", agent=accounting_agent)
hr_task = Task(description="Monitor employee performance.", expected_output="employees performance record and attendance", agent=hr_agent)



crew = Crew(agents=[inventory_agent, sales_agent, accounting_agent, hr_agent], tasks=[task1, task2, task3, task4])
'''
if __name__ == '__main__':
    inventory = Inventory()
    sales = Sales()
    accounting = Accounting()
    hr = HR()
    
    inventory.add_product("MacBook Pro", "Laptops", 2000, 10)
    inventory.add_product("iPhone 13", "Mobiles", 999, 15)
    
    print(sales.process_sale("MacBook Pro", 2, inventory))
    print(accounting.generate_report(sales))
    hr.add_employee("Alice", "Sales", 50000)
    print(hr.employees)
    
    crew.kickoff()
