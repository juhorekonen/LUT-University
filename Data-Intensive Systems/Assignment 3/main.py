import pymongo

# Database connection
mongo_connection = pymongo.MongoClient("mongodb://localhost:27017/ProjectDB")
europeDB = mongo_connection["Europe"]
north_americaDB = mongo_connection["NorthAmerica"]
asiaDB = mongo_connection["Asia"]

# Function to display the main menu
def main_menu():
    print("\nChoose what to do: ")
    print("1) Choose a database")
    print("2) Print all data from a table")
    print("3) Query data")
    print("4) Update data")
    print("0) Exit")
    return

# Function for printing any table from the selected database
def print_data_from_database(db):
    collections = db.list_collection_names()
    i = 1
    for c in collections:
        print(str(i) + ") " + c)
        i += 1
    
    selected_table = input("Choose the collection: ")
    collection = db[collections[int(selected_table)-1]]
    result = collection.find({}, {"_id": 0})
    for row in result:
        print(row)
    return

# Function to query data from the selected database
def query_handler(selection):

    # Find the correct database
    if selection == "1":
        database = europeDB
    elif selection == "2":
        database = north_americaDB
    elif selection == "3":
        database = asiaDB
    else:
        print("Invalid database selection.")
        return
    
    QUERY = input("Enter your query in SQL format: ").strip()
    # Check that SQL query exists
    if QUERY == "":
        print("No query entered.")
        return
    
    split_query = QUERY.replace(",", "").split(" ")

    index_where = 0
    index_from = 0
    i = 0
    for word in split_query:
        if word.lower() == "from":
            index_from = i
            i += 1
        if word.lower() == "where":
            index_where = i
        i += 1

    output_attributes = split_query[1:index_from]
    collection = split_query[index_from + 1]
    if index_where != 0:
        where_conditions = split_query[index_where:]
    else:
        where_conditions = None
    mongo_output = {"_id": 0}
    for item in output_attributes:
        mongo_output.update({str(item): 1})

    mongo_collection = database[collection]

    if where_conditions != None:
        # Handle the operator
        operator = where_conditions[1]
        if operator == "=" and where_conditions[2].isdigit():
            mongo_condition = {where_conditions[0]: int(where_conditions[2])}
        elif operator == "=":
            mongo_condition = {where_conditions[0]: str(where_conditions[2])}
        elif operator == ">":
            mongo_condition = {where_conditions[0]: {"$gt": int(where_conditions[2])}}
        elif operator == "<":
            mongo_condition = {where_conditions[0]: {"$lt": int(where_conditions[2])}}
        result = mongo_collection.find(mongo_condition, mongo_output)
    else:
        result = mongo_collection.find({}, mongo_output)
    for row in result:
        print(row)
    return

# Function to update data in the selected database
def update_handler(selection):

    # Find the correct database
    if selection == "1":
        database = europeDB
    elif selection == "2":
        database = north_americaDB
    elif selection == "3":
        database = asiaDB
    else:
        print("Invalid database selection.")
        return
    
    QUERY = input("Enter UPDATE query in SQL format: ").strip()
    # Check that SQL query exists
    if QUERY == "":
        print("No query entered.")
        return
    
    "Split query into tokens"
    split_query = QUERY.replace(",", "").split(" ")

    "Query must start with UPDATE"
    if split_query[0].lower() != "update":
        print("Invalid query format.")
        return
    
    collection_name = split_query[1]
    collection = database[collection_name]

    "Locate SET and optional WHERE clauses"
    set_index = [word.lower() for word in split_query].index("set")

    if "where" in [word.lower() for word in split_query]:
        where_index = [word.lower() for word in split_query].index("where")
        has_where = True
    else:
        where_index = None
        has_where = False
    
    "Find the update fields and values"
    if has_where:
        update_fields = split_query[set_index + 1:where_index]
    else:
        update_fields = split_query[set_index + 1:]
    
    updated_field = update_fields[0]
    updated_value = ' '.join(update_fields[2:])

    if updated_value.isdigit():
        updated_value = int(updated_value)
    
    updated_query = {"$set": {updated_field: updated_value}}

    # Handle WHERE clause if it exists
    if has_where:
        where_tokens = split_query[where_index + 1:]
        where_field = where_tokens[0]
        where_value = ' '.join(where_tokens[2:])
        if where_value.isdigit():
            where_value = int(where_value)
        
        filter_query = {where_field: where_value}
    else:
        filter_query = {}
    
    # Execute the update
    result = collection.update_one(filter_query, updated_query)

    if result.modified_count > 0:
        print("\nUpdate successful!")
    else:
        print("\nNo updates performed.")
    return

#Console program
def main():
    print("Welcome to the Database Manager")
    choice = -1
    selected_db = -1
    while choice != "0":
        main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nSelect the database:")
            selected_db = input("1) Europe\n2) North America\n3) Asia\nEnter your choice: ")
            if selected_db == "1":
                print("\nEuropean database selected.")
            elif selected_db == "2":
                print("\nNorth American database selected.")
            elif selected_db == "3":
                print("\nAsian database selected.")
        elif choice == "2":
            if selected_db == "1":
                print_data_from_database(europeDB)
            elif selected_db == "2":
                print_data_from_database(north_americaDB)
            elif selected_db == "3":
                print_data_from_database(asiaDB)
            else:
                print("No database selected. Please select a database first.")

        elif choice == "3":
            query_handler(selected_db)

        elif choice == "4":
            update_handler(selected_db)

        elif choice == "0":
            print("Exiting the program.\n")

        else:
            print("Invalid choice, please try again.")

    return

main()
