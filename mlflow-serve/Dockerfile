from continuumio/anaconda3

RUN pip3 install mlflow boto3

COPY deploy.sh .
RUN chmod +x deploy.sh

CMD ./deploy.sh