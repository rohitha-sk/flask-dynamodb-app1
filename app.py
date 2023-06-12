from flask import Flask, request, render_template, redirect
import boto3

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/create-table",methods=['POST'])
def create_table():
    table_name = request.form["tableName"]
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'regNo',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'stud_name',
                'KeyType': 'RANGE'  #Sort key
            },
          
        ],
        AttributeDefinitions=[
             {
                'AttributeName': 'regNo',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'stud_name',
                'AttributeType': 'S'
            },
            ],
	    ProvisionedThroughput={
            
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
            )
    
    print("Table status:", table.table_status)
    
    return "Data writtten successfully!"
    
@app.route("/put-via-form",methods=['POST'])
def put_item():
    dynamodb =boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('student-table')
    
    # item={
    #     'regNo':'001',
    #     'stud_name':'Jone',
    #     'age':26
    # }
    
    data=request.form.to_dict()
    table.put_item(Item=data)
    return "Successfully Updated!"
    
@app.route("/update-table",methods=['PUT'])
def update_item():
    dynamodb =boto3.resource('dynamodb',region_name='us-east-1')
      # Get the record ID from the request.
    regNo = request.form['regNo']
     # Get the new values for the record.
    new_values = request.form.to_dict()
    
      # Update the record in DynamoDB.
    dynamodb.update_item(
        TableName='student-table',
        Key={'regNo': regNo},
        UpdateExpression='SET #new_values = :new_values',
        ExpressionAttributeNames={
            '#new_values': {
               
                'age': 'age',
            }
        },
        ExpressionAttributeValues={
            ':new_values': new_values,
        }
    )
    
    
if __name__ == '__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')