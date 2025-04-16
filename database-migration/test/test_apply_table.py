from core.migration_registry import MigrationRegistry


def test_create_migration_table(db_config):

    migration_registry = MigrationRegistry(db_config)

    assert migration_registry.initialize() == "Applied"
