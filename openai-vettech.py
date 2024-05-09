import os
from openai import OpenAI
from dotenv import load_dotenv
import psycopg2

def main(conn, client):
    # Create a cursor object
    cur = conn.cursor()

    # Example query to retrieve data
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()

    # Close cursor and connection
    cur.close()
    conn.close()

    # Now use OpenAI's API to generate queries based on the retrieved data
    for row in rows:
        # Generate query using OpenAI API
        prompt = f"Retrieve data where column1 is '{row[0]}' and column2 is '{row[1]}'"
        response = client.chat.completions.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50  # Adjust as needed
        )
        generated_query = response.choices[0].text.strip()
        
        cur = conn.cursor()
        cur.execute(generated_query)
        result = cur.fetchall()
        
        # Process and display the results
        for res in result:
            print(res)

        # Close cursor and connection
        cur.close()
        conn.close()


def initDB():
    conn = psycopg2.connect(database="vettech",
                            host="caroleenchen",
                            user="openai",
                            password="db_pass",
                            port="db_port")
    return conn


def initAI():
    load_dotenv()
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    return client

if __name__ == "__main__":
    conn = initDB()
    client = initAI()
    main(conn, client)