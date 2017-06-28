""" Import required libraries """
import json
import requests

URL = "https://api.bitbucket.org/2.0/repositories/{team}/{repo_name}"


def handler(event, context):
    """ Create a new repository. """
    response = {
        "statusCode": 200,
        "body": {}
    }

    try:
        body = json.loads(event["body"])
    except Exception:
        body = {}

    required_params = [
        "user", "pass", "team", "repo_name"
    ]

    try:
        for param in required_params:
            if param not in body:
                raise Exception("Missing params: {param}".format(
                    param=param))
    except:
        response["body"] = {
            "type": "error",
            "error": {
                "message": "Missing parameter."
            }
        }
        return response

    headers = {"Content-Type": "application/json"}

    if "data" not in body:
        body["data"] = {
            "scm": "git",
            "is_private": "true",
            "fork_policy": "no_public_forks"
        }

    try:
        result = requests.post(
            URL.format(team=body["team"], repo_name=body["repo_name"]),
            auth=(body["user"], body["pass"]),
            data=json.dumps(body["data"]),
            headers=headers)

        if result.status_code == 200:
            result = json.loads(result.text)
    except requests.exceptions.HTTPError as err:
        response["body"] = {
            "type": "error",
            "error": {
                "message": "Failed to connect."
            }
        }
    except Exception as err:
        response["body"] = {
            "type": "error",
            "error": {
                "message": str(err)
            }
        }
    else:
        response["body"] = {
            "type": "success",
            "data": result
        }

    return response
