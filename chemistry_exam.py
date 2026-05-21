#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chemistry Exam Program
A console-based exam application for chemistry students with multiple choice questions,
scoring system, and final results.
"""

class ChemistryExam:
    """Class to manage chemistry exam with multiple choice questions."""
    
    def __init__(self):
        """Initialize the exam with questions and answers."""
        self.questions = [
            {
                "question": "1. Какъв е атомния номер на кислорода?",
                "options": ["A) 6", "B) 7", "C) 8", "D) 9"],
                "correct": "C"
            },
            {
                "question": "2. Колко електрона има водородният атом?",
                "options": ["A) 0", "B) 1", "C) 2", "D) 3"],
                "correct": "B"
            },
            {
                "question": "3. Какво е молекулното тегло на H2O?",
                "options": ["A) 16 g/mol", "B) 18 g/mol", "C) 20 g/mol", "D) 22 g/mol"],
                "correct": "B"
            },
            {
                "question": "4. Кой е химичният символ за натрия?",
                "options": ["A) Na", "B) N", "C) Ni", "D) Ne"],
                "correct": "A"
            },
            {
                "question": "5. Кола е обвързаност е най-силна?",
                "options": ["A) Йонна", "B) Ковалентна", "C) Водородна", "D) Ван дер Ваалсова"],
                "correct": "B"
            },
            {
                "question": "6. Какъв е pH на чиста вода при 25°C?",
                "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
                "correct": "C"
            },
            {
                "question": "7. Колко протона има въглеродния атом?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "C"
            },
            {
                "question": "8. Кой газ е необходим за дишането?",
                "options": ["A) Азот", "B) Кислород", "C) Въглероден диоксид", "D) Хелий"],
                "correct": "B"
            },
            {
                "question": "9. Какво е съединението NaCl?",
                "options": ["A) Кислина", "B) Основа", "C) Сол", "D) Оксид"],
                "correct": "C"
            },
            {
                "question": "10. Колко валентни електрона има кислородът?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "C"
            }
        ]
        self.score = 0
        self.answers = []
    
    def display_welcome(self):
        """Display welcome message."""
        print("\n" + "="*60)
        print("🧪 ИЗПИТ ПО ХИМИЯ - Chemistry Exam 🧪".center(60))
        print("="*60)
        print("\nДобре дошъл! Отговори на всички въпроси.")
        print("Welcome! Answer all questions.")
        print("\nПолучаваш 1 точка за всеки верен отговор.")
        print("You get 1 point for each correct answer.\n")
        print("="*60 + "\n")
    
    def display_question(self, question_num, question_data):
        """Display a single question with options."""
        print(f"\n{question_data['question']}")
        for option in question_data['options']:
            print(f"  {option}")
    
    def get_answer(self):
        """Get user answer and validate it."""
        while True:
            answer = input("\nТвоят отговор (A/B/C/D): ").upper().strip()
            if answer in ['A', 'B', 'C', 'D']:
                return answer
            else:
                print("❌ Невалиден отговор! Моля, въведи A, B, C или D.")
                print("Invalid answer! Please enter A, B, C or D.")
    
    def run_exam(self):
        """Run the exam."""
        self.display_welcome()
        
        for i, question_data in enumerate(self.questions, 1):
            self.display_question(i, question_data)
            answer = self.get_answer()
            self.answers.append({
                "question_num": i,
                "user_answer": answer,
                "correct_answer": question_data['correct'],
                "question_text": question_data['question']
            })
            
            if answer == question_data['correct']:
                self.score += 1
                print("✅ Верен отговор!")
            else:
                print(f"❌ Грешен отговор! Верния отговор е: {question_data['correct']}")
    
    def display_results(self):
        """Display exam results."""
        total_questions = len(self.questions)
        percentage = (self.score / total_questions) * 100
        
        print("\n" + "="*60)
        print("📊 РЕЗУЛТАТИ - RESULTS 📊".center(60))
        print("="*60)
        print(f"\nЩе получи: {self.score}/{total_questions} точки")
        print(f"You got: {self.score}/{total_questions} points")
        print(f"Процент: {percentage:.1f}%")
        print(f"Percentage: {percentage:.1f}%")
        
        # Grade assignment
        if percentage >= 90:
            grade = "A - Отличен (Excellent)"
        elif percentage >= 80:
            grade = "B - Добър (Good)"
        elif percentage >= 70:
            grade = "C - Среден (Average)"
        elif percentage >= 60:
            grade = "D - Задоволителен (Satisfactory)"
        else:
            grade = "F - Недостатъчен (Insufficient)"
        
        print(f"\nОценка: {grade}")
        print(f"Grade: {grade}")
        print("\n" + "="*60)
    
    def display_detailed_results(self):
        """Display detailed results for each question."""
        print("\n" + "="*60)
        print("📝 ДЕТАЙЛНИ РЕЗУЛТАТИ - DETAILED RESULTS 📝".center(60))
        print("="*60 + "\n")
        
        for answer in self.answers:
            status = "✅" if answer['user_answer'] == answer['correct_answer'] else "❌"
            print(f"{status} Въпрос {answer['question_num']}: {answer['question_text']}")
            print(f"   Твоят отговор: {answer['user_answer']}")
            print(f"   Верен отговор: {answer['correct_answer']}\n")
    
    def start(self):
        """Start the exam process."""
        try:
            self.run_exam()
            self.display_results()
            
            # Ask if user wants detailed results
            while True:
                show_details = input("\nИскаш ли да видиш детайлните резултати? (Да/Не): ").lower().strip()
                if show_details in ['да', 'yes', 'y']:
                    self.display_detailed_results()
                    break
                elif show_details in ['не', 'no', 'n']:
                    print("\nСпасибо за участието! Thank you for participating!")
                    break
                else:
                    print("Моля, въведи 'Да' или 'Не'. Please enter 'Yes' or 'No'.")
        
        except KeyboardInterrupt:
            print("\n\n❌ Изпитът беше прекъснат. The exam was interrupted.")
        except Exception as e:
            print(f"\n❌ Възникна грешка: {e}")
            print(f"An error occurred: {e}")


def main():
    """Main function."""
    exam = ChemistryExam()
    exam.start()


if __name__ == "__main__":
    main()
