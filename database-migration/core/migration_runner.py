from typing import Dict, List
from .migration_scanner import MigrationScanner
from .migration_registry import MigrationRegistry
import time

class MigrationRunner:

    def __init__(self, migration_dir, db_config) -> None:
        self.migration_dir = migration_dir
        self.MR = MigrationRegistry(db_config)


    def get_applied_migrations(self) -> dict:
            conn = self.MR._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""SELECT version,checksum
                               FROM schema_migrations
                               ORDER BY version
                               """
                               )

                return {row[0]: row[1] for row in cursor.fetchall()}

            finally:
                cursor.close()
                conn.close()

    #Let's Filter Out Migrations that already have been applied, along the way checking previously applied migrations haven't been alterd by checking there checksum
    def get_migrations_to_apply(self) -> List[Dict[str,any]]:

        scanner = MigrationScanner(self.migration_dir)

        #Already returned sorted by version number
        migration_files = scanner.discover_migrations()

        if not migration_files:
            raise ValueError("No migration files found")

        applied_migrations = self.get_applied_migrations()


        apply_migrations = []

        for migration in migration_files:
            version,checksum = migration["version"], migration['checksum']

            if version in applied_migrations:

                if checksum != applied_migrations[version]:
                     raise ValueError(f'Applied Migration {version} has been changed')

            else:
                 apply_migrations.append(migration)

        return apply_migrations


    def run_migrations(self) -> None:

        to_apply = self.get_migrations_to_apply()

        if not to_apply:
            raise ValueError("No migrations to apply")

        conn = self.MR._get_connection()
        conn.autocommit = False

        try:
            cursor = conn.cursor()

            for migration in to_apply:

                print(f"Applying migration {migration['version']}...")

                try:
                    with open(migration["filepath"], 'r') as file:
                        sql_statements = file.read()


                    start = time.time()
                    cursor.execute(sql_statements)
                    end = time.time()

                    conn.commit()
                    self.MR.record_migration(migration,(end - start),"Applied")

                except Exception as e:
                    conn.rollback()
                    print(f'Error {e} when applying migration {migration['version']}')
                    raise
        finally:
            cursor.close()
            conn.close()
