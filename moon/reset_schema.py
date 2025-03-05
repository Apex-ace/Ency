from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

try:
    # Get database connection details
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_PORT = os.getenv('DB_PORT', '5432')

    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode='require'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    logger.info("Connected to database successfully")

    # Drop existing tables if they exist
    drop_tables = [
        'system_backup',
        'user_activity',
        'review',
        'notification_preference',
        'notification',
        'message',
        'group_booking',
        'booking',
        'event',
        'user'
    ]

    for table in drop_tables:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
            logger.info(f"Dropped table: {table}")
        except Exception as e:
            logger.error(f"Error dropping table {table}: {str(e)}")

    # Create tables
    schema_commands = [
        # Enable UUID extension
        "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";",
        
        # Create tables
        """
        CREATE TABLE IF NOT EXISTS "user" (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password VARCHAR(500) NOT NULL,
            role VARCHAR(20) NOT NULL,
            profile_picture VARCHAR(200),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS event (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(200) NOT NULL,
            price FLOAT NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            organizer_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            payment_qr VARCHAR(500),
            total_tickets INTEGER NOT NULL DEFAULT 0,
            remaining_tickets INTEGER NOT NULL DEFAULT 0,
            is_group_event BOOLEAN DEFAULT FALSE,
            min_group_size INTEGER DEFAULT 1,
            max_group_size INTEGER DEFAULT 1,
            group_discount_percentage FLOAT DEFAULT 0,
            category VARCHAR(50),
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS booking (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            event_id UUID REFERENCES event(id) ON DELETE CASCADE,
            booking_date TIMESTAMPTZ DEFAULT NOW(),
            payment_status VARCHAR(20) DEFAULT 'pending',
            payment_id VARCHAR(100) UNIQUE,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            mobile VARCHAR(20) NOT NULL,
            branch VARCHAR(50) NOT NULL,
            year VARCHAR(10) NOT NULL
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS group_booking (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            booking_id UUID REFERENCES booking(id) ON DELETE CASCADE,
            group_size INTEGER NOT NULL,
            group_members JSONB NOT NULL,
            discount_applied FLOAT DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS message (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            sender_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            receiver_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            event_id UUID REFERENCES event(id) ON DELETE SET NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            read BOOLEAN DEFAULT FALSE
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS notification (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            event_id UUID REFERENCES event(id) ON DELETE SET NULL,
            type VARCHAR(50) NOT NULL,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            sent BOOLEAN DEFAULT FALSE,
            error TEXT
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS notification_preference (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE UNIQUE,
            email_notifications BOOLEAN DEFAULT TRUE,
            sms_notifications BOOLEAN DEFAULT TRUE,
            event_updates BOOLEAN DEFAULT TRUE,
            event_reminders BOOLEAN DEFAULT TRUE,
            messages BOOLEAN DEFAULT TRUE,
            email VARCHAR(120),
            phone VARCHAR(20)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS review (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            event_id UUID REFERENCES event(id) ON DELETE CASCADE,
            rating INTEGER NOT NULL,
            review_text TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS user_activity (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            activity_type VARCHAR(50) NOT NULL,
            description TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            ip_address VARCHAR(50)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS system_backup (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            filename VARCHAR(200) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            created_by UUID REFERENCES "user"(id) ON DELETE SET NULL,
            size INTEGER,
            status VARCHAR(20) DEFAULT 'completed'
        );
        """,
        
        # Create indexes
        "CREATE INDEX IF NOT EXISTS idx_event_organizer ON event(organizer_id);",
        "CREATE INDEX IF NOT EXISTS idx_booking_user ON booking(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_booking_event ON booking(event_id);",
        "CREATE INDEX IF NOT EXISTS idx_message_sender ON message(sender_id);",
        "CREATE INDEX IF NOT EXISTS idx_message_receiver ON message(receiver_id);",
        "CREATE INDEX IF NOT EXISTS idx_notification_user ON notification(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_review_event ON review(event_id);",
        "CREATE INDEX IF NOT EXISTS idx_user_activity_user ON user_activity(user_id);"
    ]

    # Execute each SQL command
    for command in schema_commands:
        try:
            cursor.execute(command)
            logger.info("Executed SQL command successfully")
        except Exception as e:
            logger.error(f"Error executing SQL command: {str(e)}")
            raise

    print("Schema reset and setup completed successfully!")

except Exception as e:
    logger.error(f"Error in schema setup: {str(e)}")
    raise

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close() 