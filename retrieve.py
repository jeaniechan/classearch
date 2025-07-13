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
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses ORDER BY id;")
        results = cursor.fetchall()
        info = ""
        for row in results:
            info += row[0] + '\t' + '\t' + row[1] +  '\t' +  '\t' + row[2] + '\t' + '\t' + row[3] + '\n'
        
        
        return {
            'statusCode': 200,
            'body': info
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