# SQL Chatbot

A conversational AI that lets you query databases using natural language. Ask questions in plain English and get SQL results instantly.

## Features

- **Natural Language to SQL**: Convert plain English questions to SQL queries
- **Multi-Database Support**: Works with SQLite, PostgreSQL, MySQL
- **Conversational Memory**: Maintains context across multiple queries
- **Query Explanation**: Explains what each generated query does
- **Error Handling**: Graceful handling of invalid queries

## Demo

```
You: How many customers made purchases last month?

Bot: Let me query that for you...

Generated SQL:
SELECT COUNT(DISTINCT customer_id)
FROM orders
WHERE order_date >= DATE('now', '-1 month')

Result: 247 customers made purchases last month.
```

## Tech Stack

- **Framework**: LangChain
- **LLM**: OpenAI GPT / Ollama
- **Database**: SQLAlchemy (supports multiple backends)
- **Frontend**: Streamlit
- **Language**: Python

## Architecture

```
Natural Language Query
        │
        ▼
┌─────────────────┐
│  LLM (GPT-4)    │
│  SQL Generation │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQL Validator  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Database       │
│  Execution      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response       │
│  Formatting     │
└─────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Jeswin-arul-samuel/SQL_chatbot.git
cd SQL_chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

## Environment Variables

```
OPENAI_API_KEY=your_openai_key
DATABASE_URL=sqlite:///your_database.db
```

## Usage

```bash
# Run with Streamlit
streamlit run app.py

# Or run in terminal
python main.py
```

## Supported Query Types

- **Aggregations**: COUNT, SUM, AVG, MIN, MAX
- **Filtering**: WHERE clauses with multiple conditions
- **Joins**: Multi-table queries
- **Grouping**: GROUP BY with HAVING
- **Sorting**: ORDER BY with limits
- **Time-based**: Date range queries

## Example Queries

| Natural Language | Generated SQL |
|-----------------|---------------|
| "Show me top 5 customers by revenue" | `SELECT customer_name, SUM(amount) as revenue FROM orders GROUP BY customer_id ORDER BY revenue DESC LIMIT 5` |
| "What products are out of stock?" | `SELECT * FROM products WHERE stock_quantity = 0` |
| "Average order value this year" | `SELECT AVG(total) FROM orders WHERE YEAR(order_date) = YEAR(CURRENT_DATE)` |

## Safety Features

- Read-only mode available (prevents INSERT, UPDATE, DELETE)
- Query validation before execution
- Parameterized queries to prevent SQL injection

## License

MIT

## Author

**Jeswin Arul Samuel**
- [LinkedIn](https://www.linkedin.com/in/jeswinarul)
- [Portfolio](https://portfolio-jeswin.vercel.app)
