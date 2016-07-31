# SQLite Migrations
This project is using raw SQL migrations, rather than a more complex SQLAlchemy-compatible migration tool such as Alembic.


----


## Running migrations

```
$ sqlite3 local.db
sqlite> BEGIN;
sqlite> .read sql/xxxx.sql
sqlite> -- Verify that migration succeeded
sqlite> -- If it did not succeed, ROLLBACK;
sqlite> -- Otherwise, COMMIT;
sqlite> COMMIT;
```
