from app.sql.agent import SQLAgent
from app.sql.formatter import SQLFormatter

agent = SQLAgent()

result = agent.run(
    "Top 10 customers by revenue."
)

formatted = SQLFormatter.format(result)

print(formatted)
