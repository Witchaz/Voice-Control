from flask import Flask,request,make_response
import gspread
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# def next_available_row(worksheet):
#     str_list = list(filter(None, worksheet.col_values(1)))
#     return str(len(str_list)+1)

def response(text):

    build_ans = {"fulfillmentText":text}
    response = json.dumps(build_ans,indent=4)
    return response

# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# cerds = ServiceAccountCredentials.from_json_keyfile_name("esp32sheet-398506-0390a8d4fe49.json", scope)
# client = gspread.authorize(cerds)

# sheet = client.open("esp32-Log").worksheet('LOG') 


app = Flask(__name__)

n = 0


@app.route('/main')
def c():
    return "main page"

@app.route('/test',methods = ['GET','POST'])
def test_run():
    if request.method == "GET":
        return "GET mehtod "
    else :
        return response("เชื่อมต่อกับเซิฟเวอร์สำเร็จแล้ว")


# @app.route('/set_data')
# def hello_world():
#     global n

#     n = request.args.get('u', default = '*', type = str)
#     row = next_available_row(sheet)
#     now = datetime.datetime.now().isoformat(timespec='minutes')  
#     value = n.split()
#     sheet.update_cell(row,1,now)
#     sheet.update_cell(row,2,value[0])
#     sheet.update_cell(row,3,value[1])
#     sheet.update_cell(row,4,value[2])
#     return f'{n}'

@app.route('/show')
def a():
    return f'{n}'