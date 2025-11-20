import pymongo
import psycopg2

# Database connections
postgres_database = psycopg2.connect(host="localhost", dbname="ProjectDB", user="postgres", password="admin", port="5432")

mongo_connection = pymongo.MongoClient("mongodb://localhost:27017/ProjectDB")
mongo_database = mongo_connection["NoSQL"]

# 1) Function to display the main menu
def main_menu():
    print("\nChoose what to do: ")
    print("1) Print a collection")
    print("2) Query data")
    print("3) Insert data")
    print("4) Update data")
    print("5) Delete data")
    print("0) Exit")
    return



# 2) Function for fetching database collections and attributes
def fetch_collections_and_attributes():
    # Find all collections and attributes in both databases
    postgres_cursor = postgres_database.cursor()
    postgres_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    postgres_collections = [row[0] for row in postgres_cursor.fetchall()]

    postgres_attributes = {}
    for table in postgres_collections:
        postgres_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table}';")
        postgres_attributes[table] = [row[0] for row in postgres_cursor.fetchall()]

    mongo_collections = mongo_database.list_collection_names()
    mongo_attributes = {}
    for collection in mongo_collections:
        doc = mongo_database[collection].find_one({}, {"_id": 0})
        mongo_attributes[collection] = list(doc.keys()) if doc else []

    return postgres_cursor, postgres_collections, postgres_attributes, mongo_collections, mongo_attributes



# 3) Function for printing data from both databases
def print_data_from_both_databases():
    try:
        # Find all collections in both databases
        postgres_cursor = postgres_database.cursor()
        postgres_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        postgres_collections = [row[0] for row in postgres_cursor.fetchall()]

        mongo_collections = mongo_database.list_collection_names()

        # Merge collections without duplicates
        all_collections = sorted(list(set(postgres_collections + mongo_collections)))

        # Display collections to the user
        print("\nAvailable collections:")
        for i, collection in enumerate(all_collections, start=1):
            print(f"{i}) {collection}")
        
        # User selects a collection
        try:
            selected_collection = int(input("\nChoose the collection: ")) - 1
        except ValueError:
            print("\nInvalid input. Please enter a number.")
            return
        
        if selected_collection < 0 or selected_collection >= len(all_collections):
            print("\nSelection out of range. Please try again.")
            return
        
        collection_name = all_collections[selected_collection]
        print(f"\nResults for collection: {collection_name}\n")

        # Connect results by id
        connecting_field = f"{collection_name[:-1]}_id"

        # Option 1: Selected collection only exists in PostgreSQL
        if collection_name in postgres_collections and collection_name not in mongo_collections:
            postgres_cursor.execute(f"SELECT * FROM {collection_name} ORDER BY {connecting_field} ASC;")
            results = postgres_cursor.fetchall()
            
            # Extract column names
            column_names = [desc[0] for desc in postgres_cursor.description]

            # Convert each row to a dictionary and print
            for row in results:
                dictionary = {column_names[i]: row[i] for i in range(len(column_names))}
                print(dictionary)
        
        # Option 2: Selected collection only exists in MongoDB
        elif collection_name in mongo_collections and collection_name not in postgres_collections:
            mongo_collection = mongo_database[collection_name]
            results = mongo_collection.find({}, {"_id": 0})
            for row in results:
                print(row)
        
        # Option 3: Selected collection exists in both databases
        elif collection_name in postgres_collections and collection_name in mongo_collections:
            
            postgres_cursor.execute(f"SELECT * FROM {collection_name};")
            # Create a list of dictionaries for easier merging of data
            columns = [col[0] for col in postgres_cursor.description]
            postgre_dictionary = [dict(zip(columns, row)) for row in postgres_cursor.fetchall()]

            # Fetch MongoDB data
            mongo_collection = mongo_database[collection_name]
            mongo_documents = list(mongo_collection.find({}, {"_id": 0}))
            # Search Mongo documents by connecting field
            mongo_connections = {doc.get(connecting_field): doc for doc in mongo_documents}

            # Merge the data
            merged_results = []

            for postgre_row in postgre_dictionary:
                key = postgre_row.get(connecting_field)
                mongo_data = mongo_connections.get(key, {})
                
                # Overwrite PostgreSQL data with MongoDB data in case of duplicates
                merged_row = {**postgre_row, **mongo_data}
                merged_results.append(merged_row)

            # Print merged results in order of connecting field (e.g., user_id)
            for row in sorted(merged_results, key=lambda x: x[connecting_field]):
                print(row)

    except Exception as e:
        print("\nAn error occurred while fetching collection: ", e)
        return
    
    return



# 4) Function for selecting and querying data from both databases
def select_and_print_data_from_both_databases():
    try:
        # Fetch collections and attributes
        postgres_cursor, postgres_collections, postgres_attributes, mongo_collections, mongo_attributes = fetch_collections_and_attributes()

        QUERY = input("\nEnter your SELECT query in SQL format: ").strip()
        # Check that SQL query exists
        if QUERY == "":
            print("\nNo query entered.")
            return
        
        split_query = QUERY.replace(",", "").split(" ")
        if split_query[0].upper() != "SELECT" or "FROM" not in split_query:
            print("Expected format: SELECT <attributes> FROM <collection> [WHERE <condition>]")
            return
        
        # Find output attributes, collection name, and optional WHERE condition
        index_from = split_query.index("FROM")
        output_attributes = split_query[1:index_from]
        collection_name = split_query[index_from + 1]
        index_where = split_query.index("WHERE") if "WHERE" in split_query else None
        where_condition = None
        if index_where:
            field = split_query[index_where + 1]
            operator = split_query[index_where + 2]
            value = " ".join(split_query[index_where + 3:])
            if value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    value = value.strip("'")
            where_condition = (field, operator, value)
        
        
        # Detect which database to query from
        exists_in_postgres = collection_name in postgres_collections
        exists_in_mongo = collection_name in mongo_collections
        if not exists_in_postgres and not exists_in_mongo:
            print(f"\nCollection {collection_name} not found in either database.")
            return
        
        connecting_field = f"{collection_name[:-1]}_id"

        # Option 1: Query from MongoDB
        if exists_in_mongo and not exists_in_postgres:
            mongo_output_attributes = {attr: 1 for attr in output_attributes if attr in mongo_attributes[collection_name]}
            if where_condition:
                field, operator, value = where_condition
                if operator == "=":
                    filter_query = {field: value}
                elif operator == ">":
                    filter_query = {field: {"$gt": value}}
                elif operator == "<":
                    filter_query = {field: {"$lt": value}}
                results = mongo_database[collection_name].find(filter_query, mongo_output_attributes)
            else:
                results = mongo_database[collection_name].find({}, mongo_output_attributes)
            for row in results:
                print(row)
        
        # Option 2: Query from PostgreSQL
        elif exists_in_postgres and not exists_in_mongo:
            columns_str = ", ".join([attr for attr in output_attributes if attr in postgres_attributes[collection_name]])
            sql_query = f"SELECT {columns_str} FROM {collection_name}"
            if where_condition:
                field, operator, value = where_condition
                sql_query += f" WHERE {field} {operator} %s"
                postgres_cursor.execute(sql_query, (value,))
            else:
                postgres_cursor.execute(sql_query)
            
            results = postgres_cursor.fetchall()
            column_names = [desc[0] for desc in postgres_cursor.description]
            for row in results:
                dictionary = {column_names[i]: row[i] for i in range(len(column_names))}
                print(dictionary)
        
        # Option 3: Query from both databases
        else:
            # Determine which database contains the WHERE field
            field, operator, value = where_condition if where_condition else (None, None, None)
            field_in_mongo = field in mongo_attributes.get(collection_name, [])
            field_in_postgres = field in postgres_attributes.get(collection_name, [])
            if field and not (field_in_mongo or field_in_postgres):
                print(f"\nAttribute {field} not found in either database.")
                return

            # Fetch PostgreSQL data
            postgres_cursor.execute(f"SELECT * FROM {collection_name};")
            columns = [col[0] for col in postgres_cursor.description]
            postgre_dictionary = [dict(zip(columns, row)) for row in postgres_cursor.fetchall()]

            # Fetch MongoDB data
            mongo_documents = list(mongo_database[collection_name].find({}, {"_id": 0}))
            mongo_dictionary = {doc[connecting_field]: doc for doc in mongo_documents}

            # Merge results
            merged_results = []
            for postgre_row in postgre_dictionary:
                key = postgre_row.get(connecting_field)
                mongo_data = mongo_dictionary.get(key, {})
                merged_row = {**postgre_row, **mongo_data} # Overwrite in case of duplicates
                # Apply WHERE condition if exists
                if field:
                    row_value = merged_row.get(field)
                    if operator == "=" and row_value != value:
                        continue
                    elif operator == ">" and row_value <= value:
                        continue
                    elif operator == "<" and row_value >= value:
                        continue
                # Filter output columns
                filtered_row = {attr: merged_row.get(attr) for attr in output_attributes}
                merged_results.append(filtered_row)
            for row in merged_results:
                print(row)

    except Exception as e:
        print("\nAn error occurred while executing the query: ", e)
        return
    
    return



# 5) Function for inserting data in both databases
def insert_data_in_both_databases():
    try:
        # Fetch collections and attributes
        postgres_cursor, postgres_collections, postgres_attributes, mongo_collections, mongo_attributes = fetch_collections_and_attributes()

        QUERY = input("\nEnter your INSERT query in SQL format: ").strip()
        # Check that SQL query exists
        if QUERY == "":
            print("\nNo query entered.")
            return
        
        split_query = QUERY.replace(",", "").split(" ")
        if split_query[0].upper() != "INSERT" or split_query[1].upper() != "INTO" or "VALUES" not in split_query:
            print("Expected format: INSERT INTO <collection> (<columns>) VALUES (<values>)")
            return
        
        collection_name = split_query[2]

        exists_in_postgres = collection_name in postgres_collections
        exists_in_mongo = collection_name in mongo_collections
        if not exists_in_postgres and not exists_in_mongo:
            print(f"\nCollection {collection_name} not found in either database.")
            return

        # Extract columns and values from the query
        columns_start = QUERY.index("(") + 1
        columns_end = QUERY.index(")")
        columns_str = QUERY[columns_start:columns_end]
        columns = [col.strip() for col in columns_str.split(",")]

        # print("Columns: ", columns)

        values_start = QUERY.index("VALUES") + 6
        values_str = QUERY[values_start:]
        values_start = values_str.index("(") + 1
        values_end = values_str.index(")")
        values = [v.strip().strip("'") for v in values_str[values_start:values_end].split(",")]

        # print("Values: ", values)

        # No empty values allowed
        for col, val in zip(columns, values):
            if val == "":
                print(f"\nEmpty value for column {col} is not allowed.")
                return

        # Convert numeric values
        for i in range(len(values)):
            if values[i].isdigit():
                values[i] = int(values[i])
            else:
                try:
                    values[i] = float(values[i])
                except ValueError:
                    pass
        
        if len(columns) != len(values):
            print("\nNumber of columns and values do not match.")
            return
        
        # Insert into MongoDB if exists
        if exists_in_mongo:
            document = {col: val for col, val in zip(columns, values) if col in mongo_attributes[collection_name]}
            if document:
                collection = mongo_database[collection_name]
                collection.insert_one(document)
                #print("Data inserted successfully into MongoDB.")
        
        # Insert into PostgreSQL if exists
        if exists_in_postgres:
            postgre_columns = [col for col in columns if col in postgres_attributes[collection_name]]
            postgre_values = [values[columns.index(col)] for col in postgre_columns]
            if postgre_columns:
                placeholders = ", ".join(["%s"] * len(postgre_columns))
                sql_query = f"INSERT INTO {collection_name} ({', '.join(postgre_columns)}) VALUES ({placeholders});"
                postgres_cursor.execute(sql_query, tuple(postgre_values))
                postgres_database.commit()
                #print("Data inserted successfully into PostgreSQL.")
        print("Data inserted successfully.")

    except Exception as e:
        print("\nAn error occurred while inserting data: ", e)
        return
    
    return



# 6) Function for updating data in both databases
def update_data_in_both_databases():
    try:
        # Fetch collections and attributes
        postgres_cursor, postgres_collections, postgres_attributes, mongo_collections, mongo_attributes = fetch_collections_and_attributes()

        QUERY = input("\nEnter your UPDATE query in SQL format: ").strip()
        # Check that SQL query exists
        if QUERY == "":
            print("\nNo query entered.")
            return
        
        split_query = QUERY.replace(",", "").split(" ")
        if split_query[0].upper() != "UPDATE" or "SET" not in split_query:
            print("Expected format: UPDATE <collection> SET <attribute>=<value> [WHERE <condition>]")
            return
        
        collection_name = split_query[1]

        #Detect correct database
        exists_in_postgres = collection_name in postgres_collections
        exists_in_mongo = collection_name in mongo_collections
        if not exists_in_postgres and not exists_in_mongo:
            print(f"\nCollection {collection_name} not found in either database.")
            return

        # Locate SET and WHERE clauses
        set_index = split_query.index("SET")
        has_where = "WHERE" in split_query
        where_index = split_query.index("WHERE") if has_where else None

        if has_where:
            update_tokens = split_query[set_index + 1:where_index]
        else:
            update_tokens = split_query[set_index + 1:]
        
        update_field = update_tokens[0]
        update_value = " ".join(update_tokens[2:]) # Join values in case of spaces
        if update_value.isdigit():
            update_value = int(update_value)
        else:
            try:
                update_value = float(update_value)
            except ValueError:
                pass
        
        # Extract WHERE field and value
        if has_where:
            where_tokens = split_query[where_index + 1:]
            where_field = where_tokens[0]
            where_value = " ".join(where_tokens[2:])
            if where_value.isdigit():
                where_value = int(where_value)
        else:
            where_field = None
            where_value = None
        
        # Option 1: Update in MongoDB
        if exists_in_mongo and not exists_in_postgres:
            collection = mongo_database[collection_name]
            filter_query = {where_field: where_value} if where_field else {}
            collection.update_many(filter_query, {"$set": {update_field: update_value}})
            #print(f"MongoDB updated succesfully.")
            return

        # Option 2: Update in PostgreSQL
        if exists_in_postgres and not exists_in_mongo:
            if where_field:
                sql_query = f"UPDATE {collection_name} SET {update_field} = %s WHERE {where_field} = %s;"
                postgres_cursor.execute(sql_query, (update_value, where_value))
            else:
                sql_query = f"UPDATE {collection_name} SET {update_field} = %s;"
                postgres_cursor.execute(sql_query, (update_value,))
            postgres_database.commit()
            #print(f"PostgreSQL updated succesfully.")
            return
        
        # Option 3: Update in both databases
        if exists_in_postgres and exists_in_mongo:
            # Find which database contains the attribute to be updated
            if update_field in mongo_attributes[collection_name]:
                target = "mongo"
            elif update_field in postgres_attributes[collection_name]:
                target = "postgres"
            else:
                print(f"\nAttribute {update_field} not found in either database.")
                return

        # Update WHERE clause field must exist too
        if has_where:
            valid_where = (where_field in mongo_attributes[collection_name]) or (where_field in postgres_attributes[collection_name])
            if not valid_where:
                print(f"\nAttribute {where_field} not found in either database.")
                return
        
        # Execute update
        if target == "mongo":
            collection = mongo_database[collection_name]
            filter_query = {where_field: where_value} if has_where else {}
            collection.update_many(filter_query, {"$set": {update_field: update_value}})
            #print(f"MongoDB updated succesfully.")
        elif target == "postgres":
            if has_where:
                sql_query = f"UPDATE {collection_name} SET {update_field} = %s WHERE {where_field} = %s;"
                postgres_cursor.execute(sql_query, (update_value, where_value))
            else:
                sql_query = f"UPDATE {collection_name} SET {update_field} = %s;"
                postgres_cursor.execute(sql_query, (update_value,))
            postgres_database.commit()
            #print(f"PostgreSQL updated succesfully.")
        
        print("Data updated successfully.")

    except Exception as e:
        print("\nAn error occurred while updating data: ", e)
        return
    
    return



# 7) Function for deleting data in both databases
def delete_data_in_both_databases():
    try:
        # Fetch collections and attributes
        postgres_cursor, postgres_collections, postgres_attributes, mongo_collections, mongo_attributes = fetch_collections_and_attributes()

        QUERY = input("\nEnter your DELETE query in SQL format: ").strip()
        # Check that SQL query exists
        if QUERY == "":
            print("\nNo query entered.")
            return
        
        split_query = QUERY.replace(",", "").split(" ")
        if split_query[0].upper() != "DELETE" or "FROM" not in split_query or "WHERE" not in split_query:
            print("Expected format: DELETE FROM <collection> [WHERE <condition>]")
            return
        
        collection_name = split_query[2]

        #Detect correct database
        exists_in_postgres = collection_name in postgres_collections
        exists_in_mongo = collection_name in mongo_collections
        if not exists_in_postgres and not exists_in_mongo:
            print(f"\nCollection {collection_name} not found in either database.")
            return

        # Locate WHERE clause
        has_where = "WHERE" in split_query
        where_index = split_query.index("WHERE") if has_where else None
        
        # Extract WHERE field and value
        where_field = split_query[where_index + 1]
        where_value = " ".join(split_query[where_index + 3:])
        if where_value.isdigit():
            where_value = int(where_value)
        else:
            try:
                where_value = float(where_value)
            except ValueError:
                pass
        
        # print("Where field: ", where_field)
        # print("Where value: ", where_value)

        # Determine connecting field
        connecting_field = f"{collection_name[:-1]}_id"

        # Detect which database contains the WHERE attribute
        field_in_mongo = has_where and (where_field in mongo_attributes.get(collection_name, []))
        field_in_postgres = has_where and (where_field in postgres_attributes.get(collection_name, []))
        if has_where and not (field_in_mongo or field_in_postgres):
            print(f"\nAttribute {where_field} not found in either database.")
            return

        # Option 1: WHERE clause exists in both databases
        if field_in_mongo and field_in_postgres:
            # PostgreSQL
            postgres_cursor.execute(f"DELETE FROM {collection_name} WHERE {where_field} = %s;", (where_value,))
            postgres_database.commit()

            #MongoDB
            collection = mongo_database[collection_name]
            collection.delete_many({where_field: where_value})
            # print(f"Data deleted successfully from both databases.")
        
        # Option 2: WHERE clause exists only in one database
        elif field_in_mongo or field_in_postgres:
            # Determine which database to delete from
            target = "mongo" if field_in_mongo else "postgres"
            id_to_delete = []

            if target == "mongo":
                collection = mongo_database[collection_name]
                documents = collection.find({where_field: where_value}, {connecting_field: 1, "_id": 0})
                id_to_delete = [doc[connecting_field] for doc in documents]
            else:
                postgres_cursor.execute(f"SELECT {connecting_field} FROM {collection_name} WHERE {where_field} = %s;", (where_value,))
                id_to_delete = [row[0] for row in postgres_cursor.fetchall()]

            if not id_to_delete:
                print("\nNo matching records found to delete.")
                return

            # Delete from both databases using the connecting field
            if exists_in_mongo:
                collection = mongo_database[collection_name]
                collection.delete_many({connecting_field: {"$in": id_to_delete}})
                # print(f"Data deleted successfully from MongoDB.")
            
            if exists_in_postgres:
                postgres_cursor.execute(f"DELETE FROM {collection_name} WHERE {connecting_field} = ANY(%s);", (id_to_delete,))
                postgres_database.commit()
                # print(f"Data deleted successfully from PostgreSQL.")
            
            print(f"Data deleted successfully.")
        
    except Exception as e:
        print("\nAn error occurred while deleting data: ", e)
        return
    
    return
    



# 8) Main function
def main():

    print("Welcome to the Database Management System!")
    while True:
        main_menu()

        choice = input("Enter your choice: ").strip()
        if not choice.isdigit():
            print("\nInvalid choice. Please try again.")
            continue
        
        if choice == '1':
            print_data_from_both_databases()

        elif choice == '2':
            select_and_print_data_from_both_databases()

        elif choice == '3':
            insert_data_in_both_databases()

        elif choice == '4':
            update_data_in_both_databases()

        elif choice == '5':
            delete_data_in_both_databases()

        elif choice == '0':
            print("\nDisconnecting for server and exiting the program.\n")
            postgres_database.cursor().close()
            postgres_database.close()
            mongo_connection.close()
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
