import json
import psycopg2
import os

def lambda_handler(event, context):
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        
        keyword = event['queryStringParameters']['search'].upper()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE UPPER(id) LIKE %s OR UPPER(name) LIKE %s OR UPPER(prereqs) LIKE %s OR UPPER(description) LIKE %s ORDER BY id", ("%"+keyword+"%", "%"+keyword+"%", "%"+keyword+"%", "%"+keyword+"%"))
        rows = cursor.fetchall()
        results = ""
        if rows == []:
            results = "No results found" 
        else:
            results = "ID \t \t Name \t \t Prerequisites \t \t Description \n"
            for row in rows:
               results += row[0] + '\t' +  '\t' + row[1] +   '\t' + '\t' + row[2] +  '\t' + '\t' + row[3] + '\n' 
        return {
            'statusCode': 200,
            'body': results
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()