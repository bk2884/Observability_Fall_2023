from flask import Response

def create_response(df):
    """Create a JSON response from a DataFrame."""
    return Response(df.to_json(orient="records"), mimetype='application/json')