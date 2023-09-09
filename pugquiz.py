import discord
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Replace this with your bot token
PREFIX = '!pugquiz'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

bot = discord.Client(intents=intents)

# Define questions and answers
questions = [
    {
        'question': 'What is the name of the PUG Cult Leader?',
        'options': ['A. Ronaldo', 'B. Dr. VonWinkle', 'C. Rupert', 'D. ValaShibbs'],
        'correct_answer': 'C'
    },
    # Add more questions here
]

# Keep track of user scores
current_question = 0
user_score = 0
quiz_in_progress = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    global current_question, user_score, quiz_in_progress

    if message.author == bot.user:
        return

    if message.content.startswith(f'{PREFIX} start'):
        print("starting_quiz")
        if not quiz_in_progress:
            await start_quiz(message)
        else:
            await message.channel.send("A quiz is already in progress!")

    elif quiz_in_progress:
        question_data = questions[current_question]
        if message.content.lower() == question_data['correct_answer'].lower():
            user_score += 1
        current_question += 1
        if current_question < len(questions):
            await next_question(message)
        else:
            await end_quiz(message)

async def start_quiz(message):
    global current_question, user_score, quiz_in_progress
    current_question = 0
    user_score = 0
    quiz_in_progress = True

    random.shuffle(questions)
    await next_question(message)

async def next_question(message):
    global current_question
    if current_question < len(questions):
        question_data = questions[current_question]
        await message.channel.send(f'Question {current_question + 1}: {question_data["question"]}')
        for option in question_data['options']:
            await message.channel.send(option)
    else:
        await end_quiz(message)

async def end_quiz(message):
    global quiz_in_progress
    quiz_in_progress = False
    
    total_questions = len(questions)
    percentage = (user_score / total_questions) * 100
    await message.channel.send(f'Quiz ended. You scored {user_score}/{total_questions} ({percentage:.2f}%)')

bot.run(TOKEN)
