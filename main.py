import json
from google.cloud import bigquery

def get_game_data(request):
    headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '<>',  # Replace with your domain
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
        }

    # Handle preflight request for CORS (OPTIONS)
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    try:
        client = bigquery.Client()

        # Define your dataset and table
        PROJECT_ID = "<>"
        DATASET_ID = "categories"
        TABLE_ID = "Oddoneouttable"

        # Query the BigQuery table
        query = f"""
        SELECT string_field_0, string_field_1, string_field_2
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        """
        query_job = client.query(query)  # Run the query
        results = query_job.result()

        # Format results as a list of dictionaries
        game_data = []
        for row in results:
            game_data.append({
                "category": row["string_field_0"],
                "items": row["string_field_1"].split(","),
                "oddOneOut": row["string_field_2"]
            })

        # Prepare the response with game data
        response = {
            "gameData": game_data
        }
        return (json.dumps(response), 200, headers)
    except Exception as e:
        # Handle any exceptions that may occur
        error_message = {"error": str(e)}
        return (json.dumps(error_message), 500, headers)
