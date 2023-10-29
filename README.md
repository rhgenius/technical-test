# To run the application
docker-compose up

# To stop the application
docker-compose down

This application will expose two APIs:

/: This API will return a simple "Hello, world!" message. However, it will be rate limited based on the source IP Address.
/rate_limit: This API can be used to get and set the rate limit. The GET method will return the current rate limit settings, while the POST method can be used to update the rate limit settings.
To modify the rate using the GET and POST methods, we can send the following requests:

# GET the health check link
curl http://localhost/flask-health-check

# GET the browser info
open this link in the browser http://localhost/info

# GET the current rate limit settings
curl http://localhost/rate_limit

# POST a new rate limit setting
curl -X POST http://localhost/rate_limit \
    -H "Content-Type: application/json" \
    -d '{
        "limit": 20
    }'
We can also test the rate limiting feature by sending multiple requests to the / API in a short period of time. If we exceed the rate limit, we will receive a 429 Too Many Requests response.

Elasticsearch: http://localhost:9200
Logstash: http://localhost:9600
Kibana: http://localhost:5601/api/status
