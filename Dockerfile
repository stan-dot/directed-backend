FROM python:3.9.15

#set home dir in docker
WORKDIR /usr/scr/app

#copy requirements.txt to docker
COPY requirements.txt ./

#install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy everything
COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]