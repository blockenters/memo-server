from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class MemoListResource(Resource) :

    @jwt_required()
    def post(self) :
        
        data = request.get_json()

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into memo
                    (userId, title, date, content)
                    values
                    ( %s, %s, %s, %s);'''
            record = (user_id,
                      data['title'],
                      data['date'],
                      data['content'])
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
        
        return {'result' : 'success'}, 200
    

    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        # 쿼리스트링 (쿼리 파라미터)를 통해서
        # 데이터를 받아온다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try : 
            connection = get_connection()

            query = '''select id, title, date, content
                    from memo
                    where userId = %s
                    order by date
                    limit 0, 25;'''
            
            record = (user_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500

        i = 0
        for row in result_list :
            result_list[i]['date'] = row['date'].isoformat()
            i = i + 1            


        return {'result' : 'success',
                'items' : result_list,
                'count' : len(result_list)}



