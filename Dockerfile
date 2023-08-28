FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements_image.txt /prod/requirements_image.txt
RUN pip install -r requirements.txt


# Then only, install taxifare!
COPY mlops/ /prod/mlops/
COPY setup.py /prod/setup.py
COPY API/ /prod/API/
copy code_for_API/ /prod/code_for_API/
RUN pip install .

CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
