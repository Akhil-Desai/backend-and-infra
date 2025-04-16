import sqlite3
import psycopg2
import mysql.connector
from typing import Dict

class MigrationRegistry:
    def __init__(self,db_config) -> None:
        self.db_config = db_config
        self.db_type = db_config.get('type', 'postgresql')

    def initialize(self) -> str:

        conn = self._get_connection()
        cursor = conn.cursor()

        ret = ""

        if self.db_type == 'postgresql':
            try:
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
                ret = "Applied"
            except psycopg2.error as e:
                print("Error", e)
                raise

        conn.commit()
        cursor.close()
        conn.close()

        return ret


    def record_migration(self, migration: Dict[str,any], execution_time: str, status: str, applied_by='system') -> None:
        """
        Record our migration to the migration registry if successfull, called in MigrationRunner
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        if self.db_type == 'postgresql':
            try:
                cursor.execute("""
                                INSERT INTO schema_migrations
                                (version,description, filename,checksum,execution_time,status,applied_by)
                                VALUES(%s, %s, %s, %s, %s, %s, %s)
                                """,(
                                    migration['version'],
                                    migration['description'],
                                    migration['filename'],
                                    migration['checksum'],
                                    execution_time,
                                    status,
                                    applied_by,
                                ))
                conn.commit()
            finally:
                cursor.close()
                conn.close()


    def _get_connection(self):
        if self.db_type == 'postgresql':
            db_config_no_type = {k:v for k,v in self.db_config.items() if k != "type"}
            return psycopg2.connect(**db_config_no_type)

        elif self.db_type == 'mysql':
            return mysql.connector.connect(**self.db_config)
