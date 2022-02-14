FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
COPY /assets/. .

# install dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./main.py"]