import sqlite3
import psycopg2
import mysql.connector

class MigrationRegistry:
    def __init__(self,db_config: dict) -> None:
        self.db_config = db_config
        self.db_type = db_config.get('type', 'postgresql')

    def initialize(self) -> None:

        conn = self._get_connection()
        cursor = conn.cursor()

        if self.db_type == 'postgresql':
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS
                    schema_migrations (
                           id SERIAL PRIMARY KEY,
                           version VARCHAR(50) NOT NULL,
                           description VARCHAR(200),
                           filename VARCHAR(255) NOT NULL,
                           checksum VARCHAR(64) NOT NULL,
                           executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                           execution_time INTEGER,
                           status VARCHAR(20) NOT NULL,
                           applied_by VARCHAR(100),
                           UNIQUE(version)
                        );
                    """)

        conn.commit()
        cursor.close()
        conn.close()

    def _get_connection(self):
        if self.db_type == 'postgresql':
            return psycopg2.connect(**self.db_config)

        elif self.db_type == 'mysql':
            return mysql.connector.connect(**self.db_config)
