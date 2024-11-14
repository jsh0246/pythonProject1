import psycopg2

# CREATE TABLE IF NOT EXISTS players (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(50),
#     age INTEGER
# )

class DBService:

    def __init__(self):
        self.conn, self.cursor = self.create_connection()

    # Connection
    def create_connection(self):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="password",
                host="localhost",
                port="5432"
            )

            cursor = conn.cursor()
            print(f"Database connected successfully.")

            return conn, cursor
        except Exception as e:
            print(f"Error connecting to database : {e}")

    # Create
    def create(self, name, age):
        # self.cursor.execute("SELECT setval('players_id_seq', COALESCE((SELECT MAX(id) FROM players), 1))")
        self.cursor.execute("INSERT INTO players (name, age) VALUES (%s, %s)", (name, age))
        self.conn.commit()

    # Read
    def read(self):
        self.cursor.execute("SELECT * FROM players ORDER BY id asc")
        return self.cursor.fetchall()

    # Update
    def update(self, id, name=None, age=None):
        if name is not None:
            self.cursor.execute("UPDATE players SET name = %s WHERE id = %s", (name, id))
        if age is not None:
            self.cursor.execute("UPDATE players SET age = %s WHERE id = %s", (age, id))
        self.conn.commit()
        print(f"Player with ID {id} updated successfully.")

    # Delete
    def delete(self, id):
        self.cursor.execute("DELETE FROM players WHERE id = %s", (id,))
        self.conn.commit()
        print(f"Player with ID {id} deleted successfully.")

    # Close connection
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

    # Method to truncate the players table
    def truncate_table(self):
        try:
            # Truncate the players table and reset the ID sequence
            self.cursor.execute("TRUNCATE TABLE players RESTART IDENTITY")
            self.conn.commit()
            print("Table truncated successfully, and ID sequence reset.")
        except Exception as e:
            print(f"Error truncating table: {e}")


if __name__ == "__main__":
    service = DBService()