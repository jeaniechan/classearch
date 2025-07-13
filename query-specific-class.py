import json
import psycopg2
import os

def lambda_handler(event, context):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        
        course = event['queryStringParameters']['course'].upper()
        
        show_prereqs = event['queryStringParameters']['prereqs']
        
        show_advanced = event['queryStringParameters']['advanced']
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE UPPER(id) = %s OR UPPER(name) = %s", (course, course))
        rows = cursor.fetchall()
        if rows == []:
            results = "The course you are searching for does not exist."
        else:
            results = "ID \t \t Name \t \t Prerequisites \t \t Description \n"
            results += rows[0][0] + '\t' + '\t' + rows[0][1] + '\t' + '\t' + rows[0][2] + '\t' + '\t' + rows[0][3] + '\n'
            if show_prereqs.lower() == "true":
                results += "Prerequisites: \n" 
                prereqs = str(rows[0][2])
                prereqs = tuple(list(prereqs.split(", ")))
                cursor.execute("SELECT * FROM courses WHERE id IN %s ORDER BY id", (prereqs,))
                prereqs_query = cursor.fetchall()
                if prereqs_query == []:
                    results += "none \n"
                else:
                    for p in prereqs_query:
                        results += p[0] + '\t' + '\t' + p[1] + '\t' + '\t' + p[2] + '\t' + '\t' + p[3] + '\n'
            if show_advanced.lower() == "true":
                results += "Further courses: \n"
                cursor.execute("SELECT * FROM courses WHERE prereqs LIKE %s ORDER BY id", (("%"+course+"%"),))
                further_query = cursor.fetchall() 
                if further_query == []:
                    results += "none \n"
                else:
                    for f in further_query:
                        results += f[0] + '\t' + '\t' + f[1] + '\t' + '\t' + f[2] + '\t' + '\t' + f[3] + '\n'
                
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