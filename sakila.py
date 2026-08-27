import os
from mcp.server.fastmcp import FastMCP
import mysql.connector

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

cnx = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

mcp = FastMCP("sakila")


@mcp.tool()
async def get_sales_by_store():
    """Returns the number of sales for each sakila store"""
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT store, manager, total_sales FROM sales_by_store")
    results = cursor.fetchall()
    cursor.close()
    
    if not results:
        return "No sales data found"
    
    output = []
    for row in results:
        output.append(f"Store {row['store']}: {row['manager']} - ${row['total_sales']}")
    return "\n-----\n".join(output)


def main():
    try:
        mcp.run(transport="stdio")
    finally:
        cnx.close()


if __name__ == "__main__":
    main()
