from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Get Gemini configurations
MODEL = os.getenv('MODEL')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Validate required environment variables
if not all([MODEL, GOOGLE_API_KEY]):
	raise ValueError("Missing required Gemini environment variables in .env file")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
	model=MODEL,
	google_api_key=GOOGLE_API_KEY,
	temperature=0.7,
	convert_system_message_to_human=True
)

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

	def get_llm_config(self):
		"""Returns LLM configuration for agents"""
		return {
			'llm': llm,
			'verbose': True
		}

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def supervisor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['supervisor_agent'],
			verbose=True,
			allow_delegation=True,  # Enable delegation to other agents
			max_iterations=10,      # Allow multiple iterations for complex workflows
			**self.get_llm_config(),
			planning=True
		)

	@agent
	def email_processor(self) -> Agent:
		return Agent(
			config=self.agents_config['email_processor'],
			verbose=True,
			**self.get_llm_config()
		)

	@agent
	def calendar_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['calendar_manager'],
			verbose=True,
			**self.get_llm_config()
		)

	@agent
	def document_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['document_manager'],
			verbose=True,
			**self.get_llm_config()
		)

	@agent
	def spreadsheet_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['spreadsheet_manager'],
			verbose=True,
			**self.get_llm_config()
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
			**self.get_llm_config()
		)
