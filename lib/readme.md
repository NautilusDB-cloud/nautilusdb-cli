
1. run qa server directly
go to the parent dir and python qa_main.py to start the qa server.
run qa_server/web_qa_cli.py to create/delete collection, add doc and ask question.

Set env variables:
ENV_STORE=fs or snow
OPENAI_API_KEY=xx

If ENV_STORE == snow, set snowflake env variables
ENV_SF_ACCOUNT=xx
ENV_SF_PASSWD=xx
ENV_SF_USER=xx

2. run qa server in a container
add the above env variables into the env.list file, then run:
docker run -d --env-file env.list --name qa1 -p 0.0.0.0:8080:8080 junius/cloudann-qademo-arm64

3. example cli ops
python qa_server/web_qa_cli.py --collection clqa1 --op create_cl

python qa_server/web_qa_cli.py --collection clqa1 --op add_doc --file example/pages/openai.com_blog_gpt-4-api-general-availability.txt

python qa_server/web_qa_cli.py --collection clqa1 --op ask --question 'what is the newest embeddings model?'
