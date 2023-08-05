
from main import app,initialize_database,create_trigger_log_file
 
if __name__ == "__main__":
    initialize_database()
    create_trigger_log_file()
    app.run(debug=True)
