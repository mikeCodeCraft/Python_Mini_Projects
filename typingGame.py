import tkinter as tk
import random
import time


# Word list
words = ["python", "keyboard", "function", "loop", 
         "variable", "class", "object", "exception", "list", "dictionary"]

class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Game")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Typing Speed Game",
                              font=("Helvetica", 18))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time: 60s",
                                    font=("Helvetica", 14), fg="red")
        self.timer_label.pack()

        self.word_label = tk.Label(root, text="",
                                   font=("Helvetica", 24), fg="blue")
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Helvetica", 16))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_word)

        self.feedback = tk.Label(root, text="", font=("Helvetica", 14))
        self.feedback.pack()

        self.stats = tk.Label(root, text="", font=("Helvetica", 12))
        self.stats.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Game",
                                      command=self.start_game)
        self.start_button.pack(pady=10)

        self.reset_game()

    def reset_game(self):
        self.shuffled_words = random.sample(words, len(words))
        self.current_index = 0
        self.correct_count = 0
        self.time_left = 60
        self.start_time = None
        self.entry.delete(0, tk.END)
        self.word_label.config(text="")
        self.feedback.config(text="")
        self.stats.config(text="")
        self.timer_label.config(text="Time: 60s")
        self.entry.config(state="disabled")

    def start_game(self):
        self.reset_game()
        self.start_time = time.time()
        self.entry.config(state="normal")
        self.entry.focus()
        self.update_timer()
        self.show_word()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def show_word(self):
        if self.current_index < len(self.shuffled_words):
            current_word = self.shuffled_words[self.current_index]
            self.word_label.config(text=current_word)
            self.entry.delete(0, tk.END)
        else:
            self.end_game()

    def check_word(self, event=None):
        typed_word = self.entry.get().strip()
        current_word = self.shuffled_words[self.current_index]

        if typed_word == current_word:
            self.feedback.config(text="✅ Correct!", fg="green")
            self.correct_count += 1
        else:
            self.feedback.config(text=f"❌ Incorrect! It was '{current_word}'", fg="red")

        self.current_index += 1
        self.show_word()

    def end_game(self):
        self.entry.config(state="disabled")
        self.word_label.config(text="Time's up!")
        total_time = time.time() - self.start_time
        speed = round((self.correct_count / total_time) * 60, 2)
        self.stats.config(text=f"Correct: {self.correct_count}/{self.current_index}\nTime: {round(total_time, 2)}s\nSpeed: {speed} WPM")
        
        
# credit = tk.Label(root, text="Created by mikeCodeCraft", font=("Arial", 10))
# credit.pack(pady=5)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    credit = tk.Label(root, text="mikeCodeCraft", 
                      font=("Arial", 28)) 
    credit.pack(pady=5)
    game = TypingGame(root)
    root.mainloop()
    
