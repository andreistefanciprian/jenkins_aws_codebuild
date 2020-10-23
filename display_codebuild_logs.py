# display codebuild logs
import boto3

client = boto3.client('logs')

log_group_name = 'cw-cb-group'
log_stream_id = 'deploy_static:2a5bb7db-26c6-41af-a0cd-6ae2ed172391'.split(':')[1]
log_stream = f'static/{log_stream_id}'
print(log_stream)
response = client.get_log_events(
    logGroupName=log_group_name,
    logStreamName=log_stream,
    startFromHead=True
)

for i in response['events']:
    log = i['message'].strip()
    print(log)