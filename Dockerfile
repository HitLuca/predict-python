FROM python:3.6-stretch

# Add requirements file used by pip install
ADD ./requirements.txt /predict-python/
WORKDIR /predict-python

# Run pip install to install all python dependenies
RUN pip3 install --no-cache-dir -r requirements.txt

# Add all the project files
ADD . /predict-python

EXPOSE 8000
