from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Watson configurations from environment variables
MODEL = os.getenv('MODEL')
WATSONX_URL = os.getenv('WATSONX_URL')
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

# Validate required environment variables
if not all([MODEL, WATSONX_URL, WATSONX_APIKEY, WATSONX_PROJECT_ID]):
	raise ValueError("Missing required Watson environment variables in .env file")

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ayaz():
	"""Ayaz crew for handling various workflow tasks through a supervisor-based approach"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def get_watson_config(self):
		"""Returns Watson configuration for agents"""
		return {
			'llm_model': MODEL,
			'watsonx_url': WATSONX_URL,
			'watsonx_apikey': WATSONX_APIKEY,
			'watsonx_project_id': WATSONX_PROJECT_ID
		}

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def supervisor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['supervisor_agent'],
			verbose=True,
			**self.get_watson_config()
		)

	@agent
	def email_processor(self) -> Agent:
		return Agent(
			config=self.agents_config['email_processor'],
			verbose=True,
			**self.get_watson_config()
		)

	@agent
	def calendar_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['calendar_manager'],
			verbose=True,
			**self.get_watson_config()
		)

	@agent
	def document_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['document_manager'],
			verbose=True,
			**self.get_watson_config()
		)

	@agent
	def spreadsheet_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['spreadsheet_manager'],
			verbose=True,
			**self.get_watson_config()
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def orchestrate_workflow(self) -> Task:
		return Task(
			config=self.tasks_config['orchestrate_workflow'],
		)

	@task
	def process_email(self) -> Task:
		return Task(
			config=self.tasks_config['process_email'],
		)

	@task
	def schedule_meeting(self) -> Task:
		return Task(
			config=self.tasks_config['schedule_meeting'],
		)

	@task
	def generate_document(self) -> Task:
		return Task(
			config=self.tasks_config['generate_document'],
		)

	@task
	def update_spreadsheet(self) -> Task:
		return Task(
			config=self.tasks_config['update_spreadsheet'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Ayaz crew with a supervisor-based workflow"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			planning=True,
			verbose=True,
			**self.get_watson_config()
		)
