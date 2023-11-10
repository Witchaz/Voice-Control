from flask import Flask,request,jsonify
import gspread
import datetime,json,ast
from oauth2client.service_account import ServiceAccountCredentials



scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("esp32sheet-398506-0390a8d4fe49.json", scope)
client = gspread.authorize(cerds)

sheet = client.open("esp32-Log").worksheet('LOG')


def findBoardID(worksheet,boardID):
    if boardID == None:
        return None
    return  worksheet.find(boardID).row

def createPayLoad():
    d_str = sheet.cell(2, 5).value
    res = {"digitalValue": d_str}
    ast.literal_eval(str(res))
    return res



def response(text):
    res = {"fulfillmentMessages": [{"text": {"text": [text]}}]}
    return res

def fecth_data():
    boardID = sheet.cell(2,1).value #Board ID
    humidity = float(sheet.cell(2,3).value) #Humidity
    temperature = float(sheet.cell(2,4).value) #Temperature

    return f"รหัสบอร์ด {boardID} ความชื้น {humidity:.2f} อุณหภูมิ {temperature:.2f}"

def update_pinValue(pin, status):
    d_str = sheet.cell(2, 5).value
  
    d = json.loads(d_str)
    value = None
    value = {i for i in d if d[i]== pin}
    if value != None:
        if status == 'True':
            status = True
        else:
            status = False

        d[pin] = status

        updated_json = json.dumps(d)
        sheet.update_cell(2, 5, updated_json)
        return True
    return False

app = Flask(__name__)

@app.route('/webhook',methods = ['POST'])
def test_run():
    
    message = request.get_json()
    intent = message["queryResult"]["intent"]["displayName"]

    if intent == "order.Test":
        return jsonify(response("ทดสอบสำเร็จ"))
    elif intent == "order.getStatus":
        return jsonify(response(fecth_data()))
    elif intent == "order.setPin":
        pin = str(int(message["queryResult"]["parameters"]["pin"]))
        status = str(message["queryResult"]["parameters"]["status"])
        if (update_pinValue(pin,status)):
            return jsonify(response("ปรับค่าใน pin เรียบร้อย"))
        return jsonify(response("ไม่พบ pin ที่ต้องการ"))
    else:
        return jsonify(response("ไม่พบบริบทที่ส่งเข้ามา"))
        


@app.route('/',methods = ['GET'])
def set_data():
    
    boardID = request.args.get("id")
    humidity = request.args.get("hum")
    temp = request.args.get("temp")
    row = findBoardID(sheet,boardID)
    if row == None:
        return "not found"
    now = datetime.datetime.now().isoformat(timespec='minutes')

    sheet.update_cell(row,2,now)
    sheet.update_cell(row,3,humidity)
    sheet.update_cell(row,4,temp)

    return createPayLoad
