from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey


client = Cloudant("1f8813d0-2ec5-4eb6-9c88-b82316fead0e-bluemix", "726e3de24d6e12ad54f735e5034421fec49ae7ed72b1cdb12d01ca8660db8fd9", url="https://1f8813d0-2ec5-4eb6-9c88-b82316fead0e-bluemix:726e3de24d6e12ad54f735e5034421fec49ae7ed72b1cdb12d01ca8660db8fd9@1f8813d0-2ec5-4eb6-9c88-b82316fead0e-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()


database_name = "sample"

my_database = client.create_database(database_name)

if my_database.exists():
   print(f"'{database_name}' successfully created.")


record={"Device":"Laptop","Name":"Dell"}

new_document = my_database.create_document(record)

if new_document.exists():
    print(f"Document successfully created.")

#To get data from database
result_collection = Result(my_database.all_docs,include_docs=True)

print(f"Retrieved minimal document:\n{result_collection[0]}\n")
