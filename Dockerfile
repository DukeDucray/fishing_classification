FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements_image.txt /prod/requirements_image.txt
RUN pip install -r requirements_image.txt


# Install API file
COPY setup_API.py /prod/setup.py
COPY API/ /prod/API/
COPY code_for_API/ /prod/code_for_API/
RUN pip install .

CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
