from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from dynamo_client import dynamodb

app = FastAPI(title='Kite spots API', openapi_prefix='/prod')


@app.get('/')
async def read_root():
    return {'Kite spots API': 'Welcome!'}


@app.get('/spots/{id}')
async def read_spot(id: int):
    table = dynamodb.Table('kite_spots')

    try:
        response = table.get_item(Key=dict(id=id))
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if 'Item' in response:
        return response['Item']

    return ''


handler = Mangum(app)
