# FastAPI with DynamoDB deployed via AWS ECR to AWS Lambda 
- with JWT/OAuth2 authorizer
## Requirements
- serverless
- docker
- docker-compose
- aws cli

## Instructions
#### Create ECR
```console
aws ecr create-repository --repository-name kite-api --region eu-central-1
```

#### Login to ECR
```console
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <ecr_url>
```

#### Build the container
```console
docker-compose up --build --detach
```

#### Deploy the Lambda image
```console
docker push <image>
```

#### Push the docker image and update the image and hash attribute in functions.yml:
```console
IMAGE_FULL="<image_name>"; HASH=$(docker push $IMAGE_FULL | awk '/digest: / {print $3}'); IMAGE=$(echo "$IMAGE_FULL" | cut -d':' -f 1); sed -i "s|image.*|image: $IMAGE@$HASH|g" functions.yml
```

#### Deploy Lambda
```console
serverless deploy --stage prod
```

#### Test Unauthorized access
```console
curl https://*.amazonaws.com/spots/1000
```
Output:
```json
{"message":"Unauthorized"}
```

#### Test Authorized access
```console
curl  -H "Authorization: Bearer <your_oauth_token>" https://*.amazonaws.com/spots/1000
```
Output:
```json
{"alternative_name":"","longitude":"-9.1796","id":1006,"name":"Lagoa de Albufeira","country":"Portugal","latitude":"38.5088"}
```
