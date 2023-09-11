FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install discord.py
RUN pip install python-dotenv

CMD ["python", "bot.py"]
