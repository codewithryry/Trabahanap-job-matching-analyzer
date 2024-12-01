from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS applicant_job;")
print("Job table has been dropped.")
exit()
