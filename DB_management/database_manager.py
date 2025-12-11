# database_manager.py
import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='D:\Programming\Project\Starting\Mental_Health_Prediction\mental_health_app\instance\mental_health.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        try:
            # Check if database exists
            if not os.path.exists(self.db_path):
                print(f"❌ Database file '{self.db_path}' not found!")
                print("🔍 Searching for database files...")
                self._find_database_files()
                return False
            
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"✅ Connected to database: {os.path.abspath(self.db_path)}")
            print(f"📏 Database size: {os.path.getsize(self.db_path)} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def _find_database_files(self):
        """Find database files in current directory and subdirectories"""
        import glob
        db_files = glob.glob('**/*.db', recursive=True)
        db_files.extend(glob.glob('**/*.sqlite', recursive=True))
        db_files.extend(glob.glob('**/*.sqlite3', recursive=True))
        
        if db_files:
            print("📁 Found database files:")
            for db_file in db_files:
                size = os.path.getsize(db_file)
                print(f"   📍 {db_file} ({size} bytes)")
        else:
            print("   No database files found!")
    
    def show_tables(self):
        """Show all tables in the database"""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            
            print("\n🗂️ DATABASE TABLES:")
            print("=" * 50)
            for table in tables:
                table_name = table[0]
                # Count rows in each table
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = self.cursor.fetchone()[0]
                print(f"📊 {table_name}: {count} rows")
            print("=" * 50)
            return [table[0] for table in tables]
            
        except Exception as e:
            print(f"❌ Error showing tables: {e}")
            return []
    
    def show_table_schema(self, table_name):
        """Show the schema (column structure) of a table"""
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = self.cursor.fetchall()
            
            print(f"\n📐 TABLE SCHEMA: {table_name}")
            print("=" * 80)
            print("CID | Name                | Type    | NotNull | Default | PK")
            print("-" * 80)
            for col in columns:
                cid, name, type_, notnull, default, pk = col
                print(f"{cid:3} | {name:19} | {type_:7} | {notnull:7} | {str(default or ''):7} | {pk}")
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Error showing table schema: {e}")
    
    def show_table_content(self, table_name):
        """Show ALL content of a specific table with ALL columns"""
        try:
            # Get table schema first
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = self.cursor.fetchall()
            column_names = [column[1] for column in columns]
            
            print(f"\n📋 TABLE: {table_name}")
            print("SCHEMA:", column_names)
            print("=" * 100)
            
            # Print column headers
            header = " | ".join(f"{col:15}" for col in column_names)
            print(header)
            print("-" * 100)
            
            # Get all data
            self.cursor.execute(f"SELECT * FROM {table_name};")
            rows = self.cursor.fetchall()
            
            if not rows:
                print("   (No data found)")
                return
            
            for row in rows:
                formatted_row = []
                for value in row:
                    if value is None:
                        formatted_row.append("NULL".ljust(15))
                    elif isinstance(value, str):
                        # Show full string, no truncation for passwords
                        formatted_row.append(str(value).ljust(15))
                    else:
                        formatted_row.append(str(value).ljust(15))
                print(" | ".join(formatted_row))
            
            print(f"📊 Total rows: {len(rows)}")
            print("=" * 100)
            
        except Exception as e:
            print(f"❌ Error showing table content: {e}")
    
    def show_all_users_with_passwords(self):
        """Show ALL user data including passwords"""
        try:
            print("\n🔓 ALL USER DATA (INCLUDING PASSWORDS):")
            print("=" * 120)
            
            self.cursor.execute("SELECT * FROM user ORDER BY id;")
            users = self.cursor.fetchall()
            
            if not users:
                print("   (No users found)")
                return
            
            # Get column names
            self.cursor.execute("PRAGMA table_info(user);")
            columns = self.cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # Print headers
            header = " | ".join(f"{col:20}" for col in column_names)
            print(header)
            print("-" * 120)
            
            for user in users:
                formatted_user = []
                for value in user:
                    if value is None:
                        formatted_user.append("NULL".ljust(20))
                    else:
                        formatted_user.append(str(value).ljust(20))
                print(" | ".join(formatted_user))
            
            print(f"👥 Total users: {len(users)}")
            print("=" * 120)
            
        except Exception as e:
            print(f"❌ Error showing user data: {e}")
    
    def show_all_predictions(self):
        """Show ALL prediction data with ALL columns"""
        try:
            print("\n📈 ALL PREDICTION DATA:")
            print("=" * 150)
            
            self.cursor.execute("SELECT * FROM prediction ORDER BY id;")
            predictions = self.cursor.fetchall()
            
            if not predictions:
                print("   (No predictions found)")
                return
            
            # Get column names
            self.cursor.execute("PRAGMA table_info(prediction);")
            columns = self.cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # Print headers
            header = " | ".join(f"{col:15}" for col in column_names)
            print(header)
            print("-" * 150)
            
            for pred in predictions:
                formatted_pred = []
                for value in pred:
                    if value is None:
                        formatted_pred.append("NULL".ljust(15))
                    else:
                        formatted_pred.append(str(value).ljust(15))
                print(" | ".join(formatted_pred))
            
            print(f"📊 Total predictions: {len(predictions)}")
            print("=" * 150)
            
        except Exception as e:
            print(f"❌ Error showing prediction data: {e}")
    
    def show_detailed_join_data(self):
        """Show joined data with user info and predictions"""
        try:
            print("\n🔗 JOINED USER & PREDICTION DATA:")
            print("=" * 120)
            
            self.cursor.execute("""
                SELECT u.id as user_id, u.username, u.email, u.name, 
                       p.id as prediction_id, p.mental_health_score, p.created_at as prediction_date
                FROM user u
                LEFT JOIN prediction p ON u.id = p.user_id
                ORDER BY u.id, p.created_at DESC;
            """)
            
            results = self.cursor.fetchall()
            
            if not results:
                print("   (No data found)")
                return
            
            print("UserID | Username    | Email              | Name          | PredID | Score | Prediction Date")
            print("-" * 120)
            
            for row in results:
                user_id, username, email, name, pred_id, score, pred_date = row
                pred_info = f"{pred_id}" if pred_id else "None"
                score_info = f"{score}" if score else "None"
                date_info = pred_date if pred_date else "None"
                
                print(f"{user_id:6} | {username:10} | {email:17} | {name:12} | {pred_info:6} | {score_info:5} | {date_info}")
            
            print("=" * 120)
            
        except Exception as e:
            print(f"❌ Error showing joined data: {e}")
    
    def delete_all_data(self):
        """Delete all data from all tables (with confirmation)"""
        try:
            print("\n🚨 DANGER ZONE: DELETE ALL DATA")
            print("=" * 50)
            
            # Show current counts
            tables = self.show_tables()
            
            confirmation = input("\n❌ Are you sure you want to delete ALL data? This cannot be undone! (yes/NO): ")
            if confirmation.lower() != 'yes':
                print("✅ Operation cancelled.")
                return
            
            # Delete data from all tables (in correct order due to foreign keys)
            tables_to_clear = ['prediction', 'user']  # prediction first due to foreign key
            
            for table in tables_to_clear:
                if table in tables:
                    self.cursor.execute(f"DELETE FROM {table};")
                    print(f"✅ Deleted all data from {table}")
            
            # Reset auto-increment counters
            self.cursor.execute("DELETE FROM sqlite_sequence;")
            
            self.connection.commit()
            print("✅ All data deleted successfully!")
            print("✅ Auto-increment counters reset!")
            
        except Exception as e:
            print(f"❌ Error deleting data: {e}")
            self.connection.rollback()
    
    def delete_specific_record(self):
        """Delete a specific record by ID"""
        try:
            tables = self.show_tables()
            if not tables:
                print("❌ No tables found!")
                return
            
            print("\n🗑️ DELETE SPECIFIC RECORD")
            print("=" * 40)
            
            table_name = input("Enter table name: ").strip()
            if table_name not in tables:
                print(f"❌ Table '{table_name}' not found!")
                return
            
            # Show current data in the table
            self.show_table_content(table_name)
            
            record_id = input(f"Enter {table_name} ID to delete: ").strip()
            
            # Check if record exists
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?;", (record_id,))
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                print(f"❌ Record with ID {record_id} not found in {table_name}!")
                return
            
            # Show the specific record being deleted
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?;", (record_id,))
            record = self.cursor.fetchone()
            
            print(f"\n📝 Record to delete:")
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in self.cursor.fetchall()]
            for col_name, value in zip(columns, record):
                print(f"   {col_name}: {value}")
            
            confirmation = input(f"\n❌ Delete this {table_name} record? (yes/NO): ")
            if confirmation.lower() != 'yes':
                print("✅ Operation cancelled.")
                return
            
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?;", (record_id,))
            self.connection.commit()
            
            print(f"✅ Record ID {record_id} deleted from {table_name}!")
            
        except Exception as e:
            print(f"❌ Error deleting record: {e}")
            self.connection.rollback()
    
    def run_custom_query(self):
        """Run a custom SQL query"""
        try:
            print("\n🔧 CUSTOM SQL QUERY")
            print("=" * 50)
            print("Available tables:", self.show_tables())
            
            query = input("\nEnter your SQL query: ").strip()
            
            if not query:
                print("❌ No query entered!")
                return
            
            # Check if it's a SELECT query (read-only)
            if query.strip().upper().startswith('SELECT'):
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                
                if results:
                    # Get column names
                    columns = [desc[0] for desc in self.cursor.description]
                    print(f"\n📊 Query Results ({len(results)} rows):")
                    print(" | ".join(columns))
                    print("-" * 80)
                    
                    for row in results:
                        print(" | ".join(str(val) for val in row))
                else:
                    print("✅ Query executed successfully (0 rows returned)")
                    
            else:
                # For non-SELECT queries, ask for confirmation
                print(f"\n⚠️  This query will modify data: {query}")
                confirmation = input("Are you sure? (yes/NO): ")
                if confirmation.lower() == 'yes':
                    self.cursor.execute(query)
                    self.connection.commit()
                    print("✅ Query executed successfully!")
                else:
                    print("✅ Operation cancelled.")
                    
        except Exception as e:
            print(f"❌ Query error: {e}")
    
    def export_to_csv(self):
        """Export all tables to CSV files"""
        try:
            import csv
            
            tables = self.show_tables()
            if not tables:
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = f"database_export_{timestamp}"
            os.makedirs(export_dir, exist_ok=True)
            
            print(f"\n💾 Exporting data to '{export_dir}' folder...")
            
            for table in tables:
                self.cursor.execute(f"SELECT * FROM {table};")
                rows = self.cursor.fetchall()
                
                # Get column names
                self.cursor.execute(f"PRAGMA table_info({table});")
                columns = [column[1] for column in self.cursor.fetchall()]
                
                filename = os.path.join(export_dir, f"{table}.csv")
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)
                    writer.writerows(rows)
                
                print(f"✅ Exported {table} ({len(rows)} rows) to {filename}")
            
            print(f"📁 All data exported to: {export_dir}")
            
        except Exception as e:
            print(f"❌ Export error: {e}")
    
    def show_database_info(self):
        """Show database information"""
        try:
            print("\n📊 DATABASE INFORMATION:")
            print("=" * 50)
            print(f"📍 Database path: {os.path.abspath(self.db_path)}")
            print(f"📏 File size: {os.path.getsize(self.db_path)} bytes")
            print(f"📅 Last modified: {datetime.fromtimestamp(os.path.getmtime(self.db_path))}")
            
            # Get database version
            self.cursor.execute("SELECT sqlite_version();")
            version = self.cursor.fetchone()[0]
            print(f"🔧 SQLite version: {version}")
            
            # Get table info
            tables = self.show_tables()
            print(f"🗂️ Number of tables: {len(tables)}")
            
        except Exception as e:
            print(f"❌ Error getting database info: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed.")

def main():
    """Main menu function"""
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        return
    
    while True:
        print("\n" + "=" * 60)
        print("🗃️  MENTAL HEALTH DATABASE MANAGER - ALL COLUMNS VISIBLE")
        print("=" * 60)
        print("1. 📋 Show all tables")
        print("2. 🔓 Show ALL user data (with passwords)")
        print("3. 📈 Show ALL prediction data")
        print("4. 📊 Show specific table content (ALL columns)")
        print("5. 📐 Show table schema/structure")
        print("6. 🔗 Show joined user-prediction data")
        print("7. 🗑️  Delete ALL data (DANGEROUS!)")
        print("8. ❌ Delete specific record")
        print("9. 🔧 Run custom SQL query")
        print("10. 💾 Export all data to CSV")
        print("11. ℹ️  Database information")
        print("12. 🚪 Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-12): ").strip()
        
        if choice == '1':
            db_manager.show_tables()
        
        elif choice == '2':
            db_manager.show_all_users_with_passwords()
        
        elif choice == '3':
            db_manager.show_all_predictions()
        
        elif choice == '4':
            tables = db_manager.show_tables()
            if tables:
                table_name = input("Enter table name: ").strip()
                if table_name in tables:
                    db_manager.show_table_content(table_name)
                else:
                    print(f"❌ Table '{table_name}' not found!")
        
        elif choice == '5':
            tables = db_manager.show_tables()
            if tables:
                table_name = input("Enter table name: ").strip()
                if table_name in tables:
                    db_manager.show_table_schema(table_name)
                else:
                    print(f"❌ Table '{table_name}' not found!")
        
        elif choice == '6':
            db_manager.show_detailed_join_data()
        
        elif choice == '7':
            db_manager.delete_all_data()
        
        elif choice == '8':
            db_manager.delete_specific_record()
        
        elif choice == '9':
            db_manager.run_custom_query()
        
        elif choice == '10':
            db_manager.export_to_csv()
        
        elif choice == '11':
            db_manager.show_database_info()
        
        elif choice == '12':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-12.")
        
        input("\nPress Enter to continue...")
    
    db_manager.close()

if __name__ == "__main__":
    main()