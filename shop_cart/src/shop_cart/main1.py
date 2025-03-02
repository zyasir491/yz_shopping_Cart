from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task  #!/usr/bin/env python
from crewai.flow import Flow, listen, start
from shop_cart.crews.poem_crew.poem_crew import PoemCrew
from shop_cart.crews.shopCart_crew.shop import ShopCrew, ProductCategory, Inventory, Sales, Accounting, HR, Crew

class ShopFlow(Flow):

    @start()
    def run_dev_crew(self):
        output = ShopCrew().crew().kickoff(
            inputs={
                "my_shop":"Buy a laptop from shop"
            }
        )
        return output.raw
    


def kickoff():
    dev_flow = ShopFlow()
    result = dev_flow.kickoff()
    print(result)