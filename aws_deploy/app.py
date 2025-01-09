import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

# add url to amplify table 
def add_amplify_url(table_name, url, uuid):
    """
    Adds amplify default domain to amplifyUrls dynamodb table.

    :param table_name: Name of the DynamoDB table.
    :param url: amplify app default domain
    :param uuid: workspace/<workspace-id>/project/<project-id>, for now its the amplify_app_id
    :return: None
    """
    # Initialize a DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Reference the table
    table = dynamodb.Table(table_name)
    item = {
        'workspace_project_UUID': uuid,
        'url': url
    }

    try:
        # Put the item into the table
        table.put_item(Item=item)
        print("Item added successfully.")

    except NoCredentialsError:
        print("AWS credentials not found.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")


def deploy_amplify_app(app_name, repo_url, branch_name, build_image, build_directory, env_vars):
    session = boto3.Session(profile_name='brighthive-dev')
    amplify_client = session.client('amplify')

    try:
        # Step 1: Create Amplify App
        print("Creating Amplify app...")
        app_response = amplify_client.create_app(
            name=app_name,
            repository=repo_url,
            platform='WEB',
            environmentVariables=env_vars,
            accessToken=gh_access_token
        )
        app_id = app_response['app']['appId']
        app_url = app_response['app']['defaultDomain']
        print(f"Amplify app created with App ID: {app_id}")
      
        # add it to dynamodb
        full_url = 'https://' + branch_name + app_url
        # we should use the uuid instaed of the app_id here
        add_amplify_url('amplifyUrls', full_url, app_id)

        # Step 2: Create Branch and Set BuildSpec
        print(f"Creating branch '{branch_name}'...")
        branch_response = amplify_client.create_branch(
            appId=app_id,
            branchName=branch_name,
            environmentVariables=env_vars
        )
        print(f"Branch '{branch_name}' created.")

        amplify_client.start_job(
            appId=app_id,
            branchName=branch_name,
            jobType='RELEASE'
        )
        print("Deployment initiated. Check the Amplify console for status.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
if __name__ == "__main__":
    # GitHub Repository URL and Branch
    gh_access_token = os.getenv('gh_token')
    redshift_username = os.getenv('redshift_username')
    redshift_password = os.getenv('redshift_password')
    REPO_URL = os.getenv('repo_url', 'https://github.com/brighthive-workspaces/evidence-dev-test')
    BRANCH_NAME = os.getenv('branch_name', 'deploy-script')

    # Custom Build Image and Build Directory
    BUILD_IMAGE = 'public.ecr.aws/docker/library/node:20-bookworm'
    BUILD_DIRECTORY = 'build'

    # Environment Variables
    ENV_VARS = {
        'EVIDENCE_SOURCE__brighthive_dev_redshift__user': redshift_username,
        'EVIDENCE_SOURCE__brighthive_dev_redshift__password': redshift_password,
        '_CUSTOM_IMAGE': 'public.ecr.aws/docker/library/node:20-bookworm'
    }

    APP_NMAE = 'evidence_deploy_script_1'

    deploy_amplify_app(APP_NMAE, REPO_URL, BRANCH_NAME, BUILD_IMAGE, BUILD_DIRECTORY, ENV_VARS)
