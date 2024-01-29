FROM python:3.11.6

# Set the working directory in the container
WORKDIR /usr/src/app

# Lazy way to trigger new build because Railway limitations
ADD "https://api.github.com/repos/WeebSoftware/NaviBot/commits?per_page=1" latest_commit
RUN curl -sLO "https://github.com/WeebSoftware/NaviBot/archive/main.zip" && unzip main.zip

WORKDIR /usr/src/app/NaviBot-main 

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot 
CMD ["python", "./navi/main.py"]
