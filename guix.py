import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading

class ForensicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensic Tool")

        self.image_path_label = tk.Label(root, text="Image Path:")
        self.image_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.image_path_entry = tk.Entry(root, width=50)
        self.image_path_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.output_dir_label = tk.Label(root, text="Output Directory:")
        self.output_dir_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.output_dir_entry = tk.Entry(root, width=50)
        self.output_dir_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.browse_image_button = tk.Button(root, text="Browse", command=self.browse_image)
        self.browse_image_button.grid(row=0, column=3, padx=5, pady=5)

        self.browse_output_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.browse_output_button.grid(row=1, column=3, padx=5, pady=5)

        self.extract_button = tk.Button(root, text="Extract Data", command=self.extract_data)
        self.extract_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.output_text = tk.Text(root, height=20, width=70)
        self.output_text.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
        self.output_text.config(state="disabled")

    def browse_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Disk Image Files","*.*")])
        if image_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, image_path)

    def browse_output(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, output_dir)

    def update_output(self, output):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state="disabled")

    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            messagebox.showerror("Error", error.decode())
            return ""
        return output.decode()

    def extract_data(self):
        image_path = self.image_path_entry.get()
        output_dir = self.output_dir_entry.get()

        if not image_path or not output_dir:
            messagebox.showwarning("Warning", "Please provide both image path and output directory.")
            return

        command = f"python forensic.py {image_path} {output_dir}"
        
        t = threading.Thread(target=self.execute_extraction, args=(command,))
        t.start()

    def execute_extraction(self, command):
        output = self.run_command(command)
        self.update_output(output)


if __name__ == "__main__":
    root = tk.Tk()
    app = ForensicApp(root)
    root.mainloop()
