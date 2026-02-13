import random
import math

class Questioning:
    def __init__(self, question):
        self.correct_answer = 0
        self.question = question
    
    def get_answer(self):
        print(self.question)
        while True:
            user = input("Give your answer: ").strip()
            try:
                user_answer = int(user)
                return user_answer
            except ValueError:
                try:
                    user_answer = float(user)
                    return user_answer
                except ValueError:
                    print("Invalid number. Please enter an integer or float (e.g., 3 or 3.14).")
    
class Quiz:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.questions_list = []


    def get_number_of_questions(self):
        while True:
            user_input = input("How many questions would you like? (1-25): ").strip()
            try:
                num_questions = int(user_input)
                if 1 <= num_questions <= 25:
                    return num_questions
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Please enter a valid integer.")
    
    def enable_retake(self):
        while True:
            user_input = input("Would you like to take the quiz again?, if u dont then u wont get a prize (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                return True
            elif user_input in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")
    

    def logarithmic_questions(self):
        y = random.randint(1, 5)
        x = 10 ** y
        question = f'Solve log10(x)={y} for x'
        question_obj = Questioning(question)
        question_obj.correct_answer = x
        return question_obj
    
    def generate_intergral_question(self):
        a = random.randint(1, 5)
        b = random.randint(-3, 3)
        c = random.randint(-5, 5)

        lower_bound = random.randint(0, 2)
        upper_bound = random.randint(lower_bound + 1, 5)

        def antideriv(x):
            return (a/3) * (x**3) + (b/2)* (x**2) +  c * x
        
        answer = antideriv(upper_bound) - antideriv(lower_bound)
        answer = round(answer, 4)

        question = f'Find ∫({a}x^2 + {b}x + {c}) dx from {lower_bound} to {upper_bound}'

        answering_obj = Questioning(question)
        answering_obj.correct_answer = answer
        return answering_obj
    
    def generate_quadtratic_question(self):
        a = random.randint(1, 3)        
        b = random.randint(-10, 10)        
        c = random.randint(-10, 10)

        discriminant = b**2 - 4*a*c

        while discriminant <= 0: 
               b = random.randint(-10, 10)        
               c = random.randint(-10, 10)  
               discriminant = b**2 - 4*a*c  

        sqrt_disc = math.sqrt(discriminant)      
        root1 = (-b - sqrt_disc) / (2 * a)      
        root2 = (-b + sqrt_disc) / (2 * a)

        if root1 > root2:            
            root1, root2 = root2, root1
            root1 = round(root1, 4)        
            root2 = round(root2, 4)

        question = f"Solve for x: {a}x^2 + {b}x + {c} = 0"
        
        questioning_obj = Questioning(question)
        questioning_obj.root1 = root1
        questioning_obj.root2 = root2
        return questioning_obj
    
    def run_quiz(self):
     print("=" * 50)
     print("Helloooo and welcome to the my personally made mathematics quiz and first project")
     print("=" * 50)
    
     while True:
        self.score = 0
        self.total_questions = 0
        
        num_questions = self.get_number_of_questions()
        
        question_types = [
            self.logarithmic_questions,
            self.generate_intergral_question,
            self.generate_quadtratic_question
        ]
        
        questions = [question_types[i % len(question_types)]() for i in range(num_questions)]
        
        for q_obj in questions:
            self.total_questions += 1
            user_answer = q_obj.get_answer()
            
            if hasattr(q_obj, 'root1'):  
                print(f"Correct answers: {q_obj.root1} and {q_obj.root2}")
                print("For quadratic questions, please provide the smaller root.")
                if abs(user_answer - q_obj.root1) < 0.01:
                    print(" Correct!")
                    self.score += 1
                else:
                    print(f" Wrong. The answer was {q_obj.root1}")
            elif hasattr(q_obj, 'correct_answer'):
                if abs(user_answer - q_obj.correct_answer) < 0.01:
                    print(" Correct!")
                    self.score += 1
                else:
                    print(f" Incorrect. The answer was {q_obj.correct_answer}")
            print()

        print("=" * 50)
        print(f"Quiz complete, your score: {self.score}/{self.total_questions}")
        print(f"Percentage: {(self.score/self.total_questions)*100:.1f}%")
        print("=" * 50)
        
        if not self.enable_retake():
            print("Thank you for partcipating in my verry first project")
            break


quiz = Quiz()
quiz.run_quiz()