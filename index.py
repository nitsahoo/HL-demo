from flask import Flask , request, jsonify
import json


app = Flask(__name__)

#Global Declarations to store infomation
dataBase = {}

#################################
#
# End Points
#
#################################
@app.route('/api/iot/healthcheck')
def runHealthCheckApp():
    return 'ok'

@app.route('/api/device/<deviceName>/data',methods=['POST', 'GET'])
def handle_data(deviceName):
    if request.method == 'POST':
        getDeviceObject(deviceName)
        updateDataInObject(deviceName,request.data)
        return "Updated"
    else:
        responseList = getDeviceData(deviceName)
        return responseList

@app.route('/api/device/<deviceName>/filter',methods=['POST'])
def set_filter(deviceName):
    result = "ok"
    if request.method == 'POST':
        args = request.args
        if deviceName in dataBase:
            if "data_gt" in args:
                dataBase[str(deviceName)]['filter']['greaterThan'] = int(args["data_gt"])

            if "data_eq" in args:
                dataBase[str(deviceName)]['filter']['equal'] = int(args.get("data_eq"))

            if "data_lt" in args:
                dataBase[str(deviceName)]['filter']['lessThan'] = int(args["data_lt"])

        else:
            result = "Device not found."

    return result

@app.route('/api/getdb/<deviceName>',methods=['GET'])
def getDataBasebyDevice(deviceName):
    result = "Not Found"
    if deviceName in dataBase:
        result = json.dumps(dataBase[str(deviceName)], sort_keys=True, indent=4)
    return result

@app.route('/api/getdb/all',methods=['GET'])
def getDataBase():
    result = json.dumps(dataBase, sort_keys=True, indent=4)
    return result
#################################


#################################
#
# Service Class Logic
#
#################################
def getDeviceObject(deviceName):
    if deviceName not in dataBase:
        dataBase[str(deviceName)] = {}
        dataBase[str(deviceName)]['data'] = []
        dataBase[str(deviceName)]['filter'] = {}
        dataBase[str(deviceName)]['filter']['greaterThan'] = None
        dataBase[str(deviceName)]['filter']['equal'] = None
        dataBase[str(deviceName)]['filter']['lessThan'] = None


def updateDataInObject(deviceName,dataString):
    dataList = dataString.decode("utf-8").split(",")
    dataBase[deviceName]['data'].extend(dataList)

def getDeviceData(deviceName):
    finalData = []
    if deviceName in dataBase:
        if len(dataBase[deviceName]['data']):
            for eachPoint in dataBase[deviceName]['data']:
                currentPoint = eachPoint
                if dataBase[deviceName]['filter']['greaterThan'] is not None and int(currentPoint) <= dataBase[deviceName]['filter']['greaterThan']:
                    continue
                elif dataBase[deviceName]['filter']['equal'] is not None and int(currentPoint) != dataBase[deviceName]['filter']['equal']:
                    continue
                elif dataBase[deviceName]['filter']['lessThan'] is not None and int(currentPoint) >= dataBase[deviceName]['filter']['lessThan']:
                    continue
                finalData.append(currentPoint)
    return ", ".join(map(str, finalData)) if len(finalData) > 0 else ""

#################################

if __name__ == '__main__':
    app.run(host='0.0.0.0')
