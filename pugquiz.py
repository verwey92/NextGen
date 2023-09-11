import random

from discord.ext import commands


class PugQuiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        # Define questions and answers
        self.questions = [
            {
                "question": "What is the name of the PUG Cult Leader?",
                "options": [
                    "A. Ronaldo",
                    "B. Dr. VonWinkle",
                    "C. Rupert",
                    "D. ValaShibbs",
                ],
                "correct_answer": "C",
            },
            # Add more questions here
        ]
        # Keep track of user scores
        self.current_question = 0
        self.user_score = 0
        self.quiz_in_progress = False

    @commands.Cog.listener()
    async def on_message(self, message):
        # global self.current_question, self.user_score, self.quiz_in_progress

        if message.author == self.bot.user:
            return

        if message.content.startswith("! start"):
            print("starting_quiz")
            if not self.quiz_in_progress:
                await self.start_quiz(message)
            else:
                await message.channel.send("A quiz is already in progress!")

        elif self.quiz_in_progress:
            question_data = self.questions[self.current_question]
            if message.content.lower() == question_data["correct_answer"].lower():
                self.user_score += 1
            self.current_question += 1
            if self.current_question < len(self.questions):
                await self.next_question(message)
            else:
                await self.end_quiz(message)

    async def start_quiz(self, message):
        # global current_question, user_score, quiz_in_progress
        self.current_question = 0
        self.user_score = 0
        self.quiz_in_progress = True

        random.shuffle(self.questions)
        await self.next_question(message)

    async def next_question(self, message):
        # global current_question
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            await message.channel.send(
                f'Question {self.current_question + 1}: {question_data["question"]}'
            )
            for option in question_data["options"]:
                await message.channel.send(option)
        else:
            await self.end_quiz(message)

    async def end_quiz(self, message):
        # global quiz_in_progress
        self.quiz_in_progress = False

        total_questions = len(self.questions)
        percentage = (self.user_score / total_questions) * 100
        await message.channel.send(
            f"Quiz ended. You scored {self.user_score}/{total_questions} ({percentage:.2f}%)"
        )
