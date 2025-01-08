import boto3
import os


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
        print(f"Amplify app created with App ID: {app_id}")

        # Step 2: Create Branch and Set BuildSpec
        print(f"Creating branch '{branch_name}'...")
        branch_response = amplify_client.create_branch(
            appId=app_id,
            branchName=branch_name,
            environmentVariables=env_vars,
        )
        print(f"Branch '{branch_name}' created.")

        # Step 3: Update BuildSpec for the Branch
        build_spec = f"""
version: 1.0
frontend:
  phases:
    preBuild:
      commands:
        - npm ci --cache .npm --prefer-offline
    build:
      commands:
        - npm run sources && npm run build 
  artifacts:
    baseDirectory: {build_directory}
    files:
      - '**/*'
  cache:
    paths:
      - .npm/**/*

image: {build_image}
        """
        print("Updating build spec...")
        amplify_client.update_branch(
            appId=app_id,
            branchName=branch_name,
            buildSpec=build_spec
        )
        print("Build spec updated successfully.")

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
    BRANCH_NAME = os.getenv('branch_name', 'main')

    # Custom Build Image and Build Directory
    BUILD_IMAGE = 'public.ecr.aws/docker/library/node:20-bookworm'
    BUILD_DIRECTORY = 'build'

    # Environment Variables
    ENV_VARS = {
        'EVIDENCE_SOURCE__brighthive_dev_redshift__user': redshift_username,
        'EVIDENCE_SOURCE__brighthive_dev_redshift__password': redshift_password
    }

    app_name = 'custom_app2'

    deploy_amplify_app(app_name, REPO_URL, BRANCH_NAME, BUILD_IMAGE, BUILD_DIRECTORY, ENV_VARS)
