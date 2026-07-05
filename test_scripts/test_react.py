from pprint import pprint

from app.agent.react import ReactAgent

agent = ReactAgent()

question = input("Question: ")

result = agent.ask(question)

print()

print(result)
