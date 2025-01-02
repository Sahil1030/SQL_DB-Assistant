# SQL Query AI Agent

## Overview
This repository contains a Python-based application leveraging large language models (LLMs) to interact with SQL databases. The application allows users to input natural language queries, which are then processed into SQL queries, executed on a database, and returned with results. The app is implemented using **Streamlit** for the user interface, **LangChain Community Toolkits** for SQL database interaction, and integrates with Groq API for LLMs.

---

## Features
- **Natural Language to SQL**: Translates user queries into SQL commands.
- **Database Interaction**: Connects to SQLite databases and dynamically creates databases from CSV files.
- **LLM Integration**: Uses `ChatGroq` for language model-based reasoning.
- **Customizable Queries**: Predefined instructions ensure safe and efficient SQL execution.

---

## Prerequisites
- Python 3.8+
- Required Python libraries:
  - `streamlit`
  - `dotenv`
  - `langchain-community`
  - `pandas`
  - `sqlalchemy`
  - `langchain-groq`
  - `langchain-openai`

Install dependencies using pip:
```bash
pip install -r requirements.txt
```

---

## Environment Setup
1. Create a `.env` file in the root directory.
2. Add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
3. Ensure the `salaries_2023.csv` file is available in the root directory.

---

## Usage
1. Run the application:
   ```bash
   streamlit run db_agent.py
   ```
2. Enter your natural language query in the input box.
3. Click on the **Run Query** button to execute the query.

---

## Application Flow
1. **CSV to SQLite Database**:
   - Reads `salaries_2023.csv`.
   - Converts it into an SQLite database `salary.db`.
2. **Query Translation**:
   - Accepts user input.
   - Uses `ChatGroq` model for natural language understanding.
   - Generates and executes SQL queries.
3. **Safe Execution**:
   - Predefined instructions prevent unsafe operations like `DROP`, `DELETE`, etc.

---

## Example Query
Input:
```plaintext
How many employees are in ABS 85 Administrative Division and what is their average salary?
```
Output:
```markdown
Final Answer: There are 30 employees in ABS 85 Administrative Division with an average salary of $70,000.

SQL Query:
```sql
SELECT COUNT(*), AVG(salary) FROM salary_2023 WHERE division = 'ABS 85 Administrative';
```
```

---

## File Structure
```
.
|-- db_agent.py          # Main application file
|-- salaries_2023.csv    # Input data file
|-- .env                 # Environment variables
|-- requirements.txt     # Python dependencies
```

---

## Future Enhancements
- Support for multiple database types (PostgreSQL, MySQL).
- Expanded LLM capabilities with other APIs.
- Enhanced UI for detailed data visualization.

---

## Contributors
- [Sahil Soni]  
- [email: sahilsoni1030@gmail.com ]

