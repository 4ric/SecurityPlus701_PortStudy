import tkinter as tk
from tkinter import messagebox
import random

class NetworkProtocolQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Protocol Quiz")
        self.ports = self.load_file('Ports.txt')
        self.acronyms = self.load_file('Protocol_Acronym.txt')
        self.descriptions = self.load_file('Protocol_Desc.txt')
        self.protocols = self.load_file('TCP_UDP.txt')

        if not (len(self.ports) == len(self.acronyms) == len(self.descriptions) == len(self.protocols)):
            messagebox.showerror("Error", "The files do not have the same number of lines.")
            self.root.quit()
            return
        
        self.data = self.prepare_data(self.ports, self.acronyms, self.descriptions, self.protocols)
        self.correct_counts = {i: 0 for i in range(len(self.data))}
        self.ignored_questions = set()
        self.previous_question_indices = []
        
        self.current_question = None
        self.create_widgets()
        self.ask_question()

    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    def prepare_data(self, ports, acronyms, descriptions, protocols):
        data = []
        for i in range(len(ports)):
            port_info = {
                'ports': ports[i].strip(),
                'acronym': acronyms[i].strip(),
                'description': descriptions[i].strip(),
                'protocols': protocols[i].strip()
            }
            data.append(port_info)
        return data

    def ask_question(self):
        available_indices = [i for i, count in self.correct_counts.items() if i not in self.ignored_questions]
        if not available_indices:
            messagebox.showinfo("Quiz Completed", "All questions have been ignored or answered.")
            self.root.quit()
            return

        if len(self.previous_question_indices) > 1:
            available_indices = [i for i in available_indices if i not in self.previous_question_indices[-3:]]

        if not available_indices:
            messagebox.showinfo("Quiz Completed", "All questions have been ignored or answered.")
            self.root.quit()
            return

        self.current_index = random.choice(available_indices)
        self.previous_question_indices.append(self.current_index)
        
        if len(self.previous_question_indices) > 5:
            self.previous_question_indices.pop(0)

        self.current_question = self.data[self.current_index]
        self.question_type = random.choice(["port", "protocol"])
        
        if self.question_type == "port":
            question_text = f"What protocol runs on port {self.current_question['ports']}?"
        else:
            question_text = f"What is the port number for {self.current_question['acronym']}?"
        
        self.question_label.config(text=question_text)
        self.answer_entry.delete(0, tk.END)
        self.protocol_entry.delete(0, tk.END)
        self.ignore_var.set(False)

    def capitalize_input(self, event):
        current_text = event.widget.get().upper()
        event.widget.delete(0, tk.END)
        event.widget.insert(0, current_text)

    def check_answer(self):
        user_input_answer = self.answer_entry.get().strip().upper()
        user_input_protocol = self.protocol_entry.get().strip().upper().replace(" ", "")

        correct_acronym_answer = correct_ports_answer = False
        correct_protocol_answer = False
        
        if self.question_type == "port":
            correct_acronym = self.current_question['acronym'].upper()
            correct_protocol = self.current_question['protocols'].upper().replace(" ", "")
            
            correct_acronym_answer = set(user_input_answer.split(',')) == set(correct_acronym.split(','))
            correct_protocol_answer = set(user_input_protocol.split(',')) == set(correct_protocol.split(','))
        else:
            correct_ports = self.current_question['ports']
            correct_protocol = self.current_question['protocols'].upper().replace(" ", "")
            
            correct_ports_answer = set(user_input_answer.split(',')) == set(correct_ports.split(','))
            correct_protocol_answer = set(user_input_protocol.split(',')) == set(correct_protocol.split(','))

        if (self.question_type == "port" and correct_acronym_answer and correct_protocol_answer) or \
           (self.question_type == "protocol" and correct_ports_answer and correct_protocol_answer):
            self.correct_counts[self.current_index] += 1
            result = "Correct"
        else:
            self.correct_counts[self.current_index] = 0
            result = "Incorrect"
        
        if self.ignore_var.get():
            self.ignored_questions.add(self.current_index)
        
        result_text = f"{result}: {self.current_question['ports']} - {self.current_question['description']} - {self.current_question['acronym']} - {self.current_question['protocols']}"
        messagebox.showinfo("Result", result_text)
        self.ask_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="Question", font=("Helvetica", 12))
        self.question_label.pack(pady=20)

        self.answer_label = tk.Label(self.root, text="Your Answer:")
        self.answer_label.pack()
        
        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<KeyRelease>", self.capitalize_input)

        self.protocol_label = tk.Label(self.root, text="TCP or UDP:")
        self.protocol_label.pack()
        
        self.protocol_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.protocol_entry.pack(pady=10)
        self.protocol_entry.bind("<KeyRelease>", self.capitalize_input)

        self.ignore_var = tk.BooleanVar()
        self.ignore_check = tk.Checkbutton(self.root, text="Ignore this question", variable=self.ignore_var)
        self.ignore_check.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer, font=("Helvetica", 12))
        self.submit_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkProtocolQuizApp(root)
    root.mainloop()
