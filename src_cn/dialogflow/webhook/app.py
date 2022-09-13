# pip install flask
# pip install sqlalchemy

# 载入相关套件
from flask import Flask, request, jsonify, make_response
from sqlalchemy import create_engine

# 宣告 Flask 物件
app = Flask(__name__)

def language_response(req):
    # 取得意图 set-language
    intent = req.get('queryResult').get('intent')['displayName']
    # 取得 entity
    entity1 =  req.get('queryResult').get('parameters')["language-programming"]
    if entity1:
        response = entity1 + ' 是一个很棒的程式语言.'
    else:
        response = '哇, 厉害! ' + entity1 + ' 学多久了?'
    return response

@app.route('/webhook', methods=['POST'])
def hotel_booking():
    # 取得请求
    req = request.get_json(force=True)
    # 取得意图 set-language
    intent = req.get('queryResult').get('intent')['displayName']
    # 取得 entity
    entityCity = req.get('queryResult').get('parameters')["geo-city"].lower()
    entityDate = req.get('queryResult').get('parameters')["date-time"].lower()
    entityDate = entityDate[:10].replace('/', '-')
    
    # 开启资料库连线
    engine = create_engine('sqlite:///test.db', convert_unicode=True)
    con = engine.connect()

    if intent == 'booking':
        # 根据城市、日期查询
        sql_cmd = f"select room_count from  hotels "
        sql_cmd += f"where city = '{entityCity}' and order_date = '{entityDate}'" 
        result = con.execute(sql_cmd)
        list1 = result.fetchall()
        
        # 增修记录
        if len(list1) > 0: # 订房数加 1
            sql_cmd = f"update hotels set 'room_count' = {list1[-1][-1]+1} "
            sql_cmd += f"where city = '{entityCity}' and order_date = '{entityDate}'" 
            result = con.execute(sql_cmd)
        else: # 新增一笔记录   
            sql_cmd = "insert into hotels('city', 'order_date', 'room_count')" 
            sql_cmd += f" values ('{entityCity}', '{entityDate}', 1)" 
            result = con.execute(sql_cmd)
        
        # 回应
        response = f'{entityCity}, {entityDate} OK.'
        return make_response(jsonify({ 'fulfillmentText': response }))
    elif intent == 'set-language':
        response = language_response(req)
        return make_response(jsonify({ 'fulfillmentText': response }))
    else:
        return make_response(jsonify({ 'fulfillmentText': 'sorry i am not sure' }))

@app.route('/', methods = ['GET'])
def test():
    return make_response(jsonify({ 'message': 'welcome' }))
    
if __name__ == '__main__':
    app.run(debug=True)
    