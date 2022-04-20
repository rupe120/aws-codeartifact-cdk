#!/usr/bin/env python3
import os
import aws_cdk as cdk

from codeartifact.codeartifact_stack import CodeartifactStack

ENVIRONMENT = os.getenv("ENVIRONMENT")

app = cdk.App()

# Read the App Config
app_config = app.node.try_get_context("appConfig")

# Determine current environment
app_config["current_environment"] = {}
if "Environments" in app_config:
    current_env_tmp = ([env for env in app_config["Environments"] if env["Name"] == ENVIRONMENT])
    if len(current_env_tmp) > 0:
        app_config["current_environment"] = current_env_tmp[0]

stack_name = app_config["AppName"]
if "Name" in app_config["current_environment"]:
    stack_name += "-" + app_config["current_environment"]["Name"]

CodeartifactStack(app, stack_name, app_config)

# Apply App Tags
app_tags = cdk.Tags.of(app)
for tag_key in app_config["Tags"]:
    cdk.Tags.of(app).add(tag_key,app_config["Tags"][tag_key])


app.synth()
