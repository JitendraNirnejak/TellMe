# Librarys
from flask import request
from flask import jsonify

import psycopg2 as pg2

# Importing the Application Modules
from app import app
from data import aadharData


# Connecting to database
conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")


# Views

# GetOTP - Return Success Message if aadhar ID is valid and unregistered
@app.route('/api/getOTP', methods=['GET', 'POST'])
def getOTP():
    res={}
    if request.method == 'POST':
        # Receiving Aadhar ID
        aadharID = request.get_json()['aadharID']
        
        if len(aadharID)==12 and aadharID in aadharData:
            # Creating cursor
            cur = conn.cursor()
            # Executing Query
            try:
                cur.execute("SELECT aadhar_id FROM user_all WHERE aadhar_id = %s",[aadharID])
            except:
                conn.rollback()
                res["status"]="failed"
                res['message']="Something went wrong"
                return jsonify(res)

            # Fetching Data
            data = cur.fetchall()

            if len(data)>0:
                res["status"]="failed"
                res['message']="Aadhar ID is already registered"
            else:
                # Generating Response
                res["status"]="success"

            # Commiting the Changes
            conn.commit()

            # Closing the cursor
            cur.close()
        else:
            res["status"]="failed"
            res['message']="Incorrect Aadhar ID"
    else:
        res["status"]="failed"
        res["message"]="Invalid Request Method"

    return jsonify(res)

# verifyOTP - Return Success Message if OTP sent by the user is correct
@app.route('/api/verifyOTP', methods=['GET', 'POST'])
def verifyOTP():
    if request.method == 'POST':
        data = request.get_json()
        res = {}
    
        aadharID = data["aadharID"]
        OTP = data["OTP"]

        if OTP=='123456':
            res["status"] = "success"
        else:
            res["status"] = "failed"
            res["message"] = "Incorrect OTP"
    else:
        res["status"]="failed"
        res["message"]="Invalid Request Method"
    return jsonify(res)

# Register - Register the User and send Success Message
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        res = {}
        aadharID = data['aadharID']
        password = data['password']

        contactNo = aadharData[aadharID]['contact_no']
        name = aadharData[aadharID]['name']

        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("INSERT INTO user_all VALUES(%s,%s,%s,%s,%s)",[aadharID, password, name, contactNo,'REGISTERED'])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        res["status"]="success"

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

    else:
        res["status"]="failed"
        res["message"]="Invalid Request Method"

    return jsonify(res)

# Login - Get Credentioals and Return User Information
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    res={}
    data = request.get_json()
    
    aadharID = data['aadharID']
    password_candidate = data['password']

    # Creating cursor
    cur = conn.cursor()
    # Executing Query
    try:
        cur.execute("SELECT password,user_status,name FROM user_all WHERE aadhar_id = %s",[aadharID])
    except:
        conn.rollback()
        res["status"]="failed"
        res['message']="Something went wrong"
        return jsonify(res)

    # Generate Response
    data = cur.fetchone()

    # Commiting the Changes
    conn.commit()

    # Closing the cursor
    cur.close()

    res={}

    if data:
        # Compare Passwords
        if password_candidate == data[0]:
            res["status"] = "success"
            res["aadharID"] = aadharID
            res["name"] = data[2]
            res["userStatus"] = data[1]
        else:
            res["status"] = "failed"
            res["message"] = "Invalid Login"
        # Close connection
    else:
            res["status"] = "failed",
            res["message"] = "Aadhar not Registered"
    return jsonify(res)

# CheckNotification - Check If user has any new notification
@app.route('/api/checkNotification', methods=['GET', 'POST'])
def checkNotification():
    data = request.get_json()

    aadharID = data['aadharID']
    
    if True:
    	res = {
    		"status" : "success",
    		"type" : "success",	# success, warning or danger
    		"body" : "message body",
    		"link" : "http://google.com"
    	}
    	return jsonify(res)
    else:
    	res = {
    		"status" : "failed",
    		"message" : "No New Notification"
    	}
    	return jsonify(res)