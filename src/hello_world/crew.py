from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
# from tools.weather_tool import WeatherTool
from tools.weather_tool import WeatherTool
from crewai.tasks.task_output import TaskOutput

import panel as pn

chat_interface = pn.chat.ChatInterface()


def print_output(output: TaskOutput):
    message = output.raw
    chat_interface.send(message, user=output.agent, respond=False)


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class HelloWorld():
    """HelloWorld crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def weather_analyst(self) -> Agent:
       return Agent(
           config=self.agents_config['weather_analyst'],
           tools=[WeatherTool()],
           verbose=True,
       )

    @agent
    def weather_presenter(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_presenter'],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def gather_weather_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_weather_data'],
            # callback=print_output,
        )

    @task
    def present_weather_update(self) -> Task:
        return Task(
            config=self.tasks_config['present_weather_update'],
            callback=print_output,
            human_input=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyProject crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            # process=Process.sequential,
            verbose=True,
            # memory=False,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
