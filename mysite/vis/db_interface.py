from django.db import connections
import MySQLdb

def my_custom_sql(self):
	cursor = connections['my_db_alias'].cursor()

    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])

    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

    return row