from crew import chain_crew, star_crew, hybrid_crew
from utils.db_tool import execute_query

print("\nChoose Topology")
print("1. Chain")
print("2. Star")
print("3. Hybrid")

choice = input("Choice: ")
question = input("\nAsk SQL Question: ")

if choice == "1":
    crew = chain_crew
elif choice == "2":
    crew = star_crew
else:
    crew = hybrid_crew

result = crew.kickoff(
    inputs={"user_question": question}
)

sql_query = str(result).strip()

print("\n========== GENERATED SQL ==========\n")
print(sql_query)

columns, rows = execute_query(sql_query)

print("\n========== DATABASE RESULT ==========\n")
print(columns)

for row in rows:
    print(row)