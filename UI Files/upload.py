import boto3

def main():
    # this will create dynamodb resource object and
    # here dynamodb is resource name
    client = boto3.resource('dynamodb')

    # this will search for dynamoDB table 
    # your table name may be different
    table = client.Table("yelp-restaurants")
    print(table.table_status)

    table.put_item(Item= {"id": "w3wKbjuNCZnYoPOr-FCk5w", "name": "New Moon", "category": "chinese", "rating": 4.0, "review_count": 170, "coordinates": {"latitude": "40.742569", "longitude": "-73.977856"}, "address": "547 2nd Ave, New York, NY 10016", "phone": "(212) 779-2828", "zip_code": "10016"})

main()