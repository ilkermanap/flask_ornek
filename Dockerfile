FROM python:3.9
COPY template.py ./
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
# Bundle app source
COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
