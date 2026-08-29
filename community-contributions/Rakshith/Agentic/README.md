# CrewAI Autonomous SQL Querying System

A multi-agent SQL querying system built using **CrewAI**, **Gemini LLM**, and **SQLite** that converts natural language questions into executable SQL queries using autonomous AI agents.

## Project Overview

This project demonstrates how multiple AI agents can collaborate to process a user's natural language query, generate a safe SQL query, execute it on a relational database, and return the matching records.

Instead of using a single LLM for the entire task, the workflow is divided among specialized CrewAI agents.

## Features

- Convert natural language questions into SQL queries.
- Multi-agent architecture using CrewAI.
- SQLite employee database for query execution.
- SQL validation to allow only safe `SELECT` statements.
- Supports three workflow topologies:
  - Chain
  - Star
  - Hybrid

## Architecture

```text
User Query
     │
     ▼
Planner Agent
     │
     ├───────────────┐
     ▼               ▼
Schema Agent     Context Agent
     │               │
     └──────┬────────┘
            ▼
     SQL Generator Agent
            │
            ▼
     Validator Agent
            │
            ▼
      SQLite Database
            │
            ▼
      Query Results
```

## Agents

### Planner Agent
- Understands the user's natural language query.
- Identifies intent and required information.

### Schema Agent
- Reads the SQLite database schema.
- Determines the required tables and columns.

### Context Agent
- Extracts filters such as department, city, salary, and experience.

### SQL Generator Agent
- Generates a valid SQLite SQL query.

### Validator Agent
- Ensures only safe `SELECT` queries are executed.
- Blocks `DELETE`, `DROP`, `UPDATE`, `ALTER`, and `INSERT` statements.

### Execution Agent
- Executes the validated SQL query on the SQLite database.
- Returns matching records.

## Project Structure

```text
Crewai_sql_project/
│
├── app.py
├── crew.py
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── planner.py
│   ├── schema_agent.py
│   ├── context_agent.py
│   ├── sql_agent.py
│   ├── validator_agent.py
│   └── execution_agent.py
│
├── tasks/
│   └── tasks.py
│
├── utils/
│   └── db_tool.py
│
├── database/
│   ├── create_db.py
│   ├── test_db.py
│   └── employee.db
│
└── README.md
```

## Technologies Used

- Python
- CrewAI
- Google Gemini API
- SQLite
- python-dotenv

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Crewai_sql_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 4. Create the SQLite database

```bash
python database/create_db.py
```

### 5. Run the application

```bash
python app.py
```

## Example Usage

**Input**

```text
Show Engineering employees in Bengaluru earning above 90000
```

**Generated SQL**

```sql
SELECT employee_id, name, department_id, city, salary
FROM Employees
WHERE city = 'Bengaluru'
AND salary > 90000;
```

**Output**

```text
(1, 'Aarav', 'Bengaluru', 120000)
(2, 'Diya', 'Bengaluru', 95000)
(11, 'Harsha', 'Bengaluru', 110000)
(14, 'Keerthi', 'Bengaluru', 98000)
(17, 'Abhishek', 'Bengaluru', 150000)
```

## Workflow Topologies

### Chain Topology

Agents execute sequentially.

```text
Planner → Schema → Context → SQL Generator → Validator → Database
```

### Star Topology

Planner coordinates specialist agents before SQL generation.

```text
        Planner
      /    |    \
 Schema  Context Validator
      \    |    /
    SQL Generator
         │
      Database
```

### Hybrid Topology

Combines sequential planning with specialized agent collaboration.

```text
Planner
   │
Schema + Context
   │
SQL Generator
   │
Validator
   │
Database
```

## Safety Features

- Executes only `SELECT` statements.
- Prevents destructive SQL operations such as:
  - `DELETE`
  - `DROP`
  - `UPDATE`
  - `ALTER`
  - `INSERT`

## Future Improvements

- Streamlit web interface.
- Support for multiple databases (MySQL/PostgreSQL).
- Query history and logging.
- Role-based access control.
- Advanced SQL optimization.

## Author

**Rakshith**

CrewAI Autonomous SQL Querying System — Engineering Project.