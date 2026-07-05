from app.agent.final_answer import FinalAnswerGenerator

generator = FinalAnswerGenerator()

sql_result = """
Customer | Revenue

ABC Ltd | 120000

XYZ Ltd | 115000
"""

rag_context = """
Employees travelling internationally
can claim hotel expenses up to ₹7000
per night after manager approval.
"""

answer = generator.generate(
    question="Who is the top customer and what is the hotel reimbursement policy?",
    sql_result=sql_result,
    rag_context=rag_context,
)

print(answer)
