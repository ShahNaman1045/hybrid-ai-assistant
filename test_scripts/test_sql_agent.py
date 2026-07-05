from pprint import pprint

from app.sql.agent import SQLAgent

agent = SQLAgent()

question = "Top 10 customers by revenue."

result = agent.run(question)

pprint(result)
