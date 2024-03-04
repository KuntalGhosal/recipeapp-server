FROM python:3.10
WORKDIR /src
COPY . /src
# RUN pip install flask
# RUN pip install flask_restful
# Install project dependencies
COPY requirements.txt /
# RUN cat requirements.txt | xargs -n 1 pip install --no-cache-dir
RUN cat requirements.txt | cut -f1 -d"#" | sed '/^\s*$/d' | xargs -n 1 pip install --no-cache-dir
EXPOSE 8000
ENTRYPOINT ["python"]
