import psycopg2

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="billing_db",
        user="postgres",
        password="your password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Ensure the table schema is updated
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(15),
        email VARCHAR(100),
        amount FLOAT,
        quantity FLOAT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    # Function to insert customer data
    def insert_customer(name, phone, email, amount, quantity):
        insert_query = '''
        INSERT INTO customers (name, phone, email, amount, quantity)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        '''
        cursor.execute(insert_query, (name, phone, email, amount, quantity))
        conn.commit()

        customer_id = cursor.fetchone()[0]
        return customer_id

    while True:
        print("-" * 80)
        print("Customer Contact")
        contact = input("Enter customer phone number: ")
        print("-" * 80)
        name = input("Enter customer's name: ")
        print("-" * 80)
        email = input("Enter customer email: ")
        print("-" * 80)
        total = 0
        total_quantity = 0

        while True:
            print("Enter the amount and quantity")
            amount = float(input("Enter amount: "))
            quantity = float(input("Enter quantity: "))
            total += amount * quantity
            total_quantity += quantity

            repeat = input("Do you want to add more items? (Yes/No): ")
            if repeat.lower() == "no":
                break

        print("*" * 80)
        print("Name:", name)
        print("Amount to be paid:", total)
        print("Phone:", contact)
        print("Email:", email)
        print("*" * 80)

        # Insert the customer data into the database with total amount and quantity
        insert_customer(name, contact, email, total, total_quantity)

        print("******** Thank You For Shopping! Visit Again ********")

        repeat1 = input("Do you want to go to the next customer? (Yes/No): ")
        if repeat1.lower() == "no":
            break

    # Close the cursor and connection
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")

except Exception as e:
    print(f"Error: {e}")
