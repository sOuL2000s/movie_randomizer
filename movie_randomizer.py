import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import random

# Define main application class
class MovieRandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Randomizer")
        self.root.geometry("800x600")
        
        # Placeholder for movie data
        self.movies = pd.DataFrame()
        
        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # File Selection Section
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        load_button = tk.Button(file_frame, text="Load Movie File", command=self.load_file)
        load_button.pack()

        # Search and Filter Section
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        tk.Label(filter_frame, text="Search Movie:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(filter_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = tk.Button(filter_frame, text="Search", command=self.search_movie)
        search_button.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Filter Genre:").pack(side=tk.LEFT, padx=5)
        self.genre_entry = tk.Entry(filter_frame, width=20)
        self.genre_entry.pack(side=tk.LEFT, padx=5)
        
        # Sorting Section
        sort_frame = tk.Frame(self.root)
        sort_frame.pack(pady=10)
        sort_label = tk.Label(sort_frame, text="Sort by:")
        sort_label.pack(side=tk.LEFT, padx=5)
        self.sort_options = ttk.Combobox(sort_frame, values=["Title", "Year", "IMDb Rating"], width=10)
        self.sort_options.pack(side=tk.LEFT, padx=5)
        sort_button = tk.Button(sort_frame, text="Sort", command=self.sort_movies)
        sort_button.pack(side=tk.LEFT, padx=5)

        # Randomize Section
        random_frame = tk.Frame(self.root)
        random_frame.pack(pady=10)
        random_button = tk.Button(random_frame, text="Random Movie", command=self.random_movie)
        random_button.pack()

        # Results Section
        self.result_text = tk.Text(self.root, height=10, width=80, state="disabled")
        self.result_text.pack(pady=10)

    def load_file(self):
        filepath = filedialog.askopenfilename(title="Select a Movie Dataset", filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                self.movies = pd.read_csv(filepath)
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def search_movie(self):
        query = self.search_entry.get().lower()
        if self.movies.empty:
            messagebox.showwarning("Warning", "Please load a movie file first.")
            return
        results = self.movies[self.movies["Title"].str.lower().str.contains(query, na=False)]
        self.display_results(results, f"Results for '{query}':")

    def sort_movies(self):
        sort_by = self.sort_options.get()
        if self.movies.empty:
            messagebox.showwarning("Warning", "Please load a movie file first.")
            return
        if sort_by not in ["Title", "Year", "IMDb Rating"]:
            messagebox.showwarning("Warning", "Invalid sort option selected.")
            return
        sorted_movies = self.movies.sort_values(by=sort_by)
        self.display_results(sorted_movies, f"Movies sorted by {sort_by}:")

    def random_movie(self):
        if self.movies.empty:
            messagebox.showwarning("Warning", "Please load a movie file first.")
            return
        random_movie = self.movies.sample()
        self.display_results(random_movie, "Randomly selected movie:")

    def display_results(self, results, header):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, header + "\n")
        for idx, row in results.iterrows():
            self.result_text.insert(tk.END, f"{row['Title']} ({row['Year']}) - Rating: {row['IMDb Rating']}\n")
        self.result_text.config(state="disabled")

# Create main window
root = tk.Tk()
app = MovieRandomizerApp(root)
root.mainloop()
