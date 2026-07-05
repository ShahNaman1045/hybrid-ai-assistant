from app.agent.reasoning import ReasoningEngine

engine = ReasoningEngine()

questions = [
    "Top 10 customers by revenue.",
    "What is the travel reimbursement policy?",
    "Which vendors are eligible for 60-day payment and what is their pending balance?"
]

for question in questions:
    decision = engine.decide(question)

    print("=" * 70)
    print(question)
    print("Decision:", decision.value)
