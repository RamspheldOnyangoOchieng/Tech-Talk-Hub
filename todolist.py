import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime
import json
import os

class SimpleAwesomeTodo:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Awesome To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'accent': '#0f3460',
            'highlight': '#e94560',
            'text': '#ffffff',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#f44336'
        }
        
        # Sample tasks
        self.tasks = []
        self.load_tasks()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title with cool emoji
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="✨ AWESOME TO-DO LIST ✨",
            font=('Arial', 28, 'bold'),
            fg=self.colors['highlight'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Organize your tasks in style!",
            font=('Arial', 14),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        subtitle.pack(pady=5)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=30)
        
        # Left panel - Add task
        left_panel = tk.Frame(main_container, bg=self.colors['card'], relief='flat', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Add task form
        form_title = tk.Label(
            left_panel,
            text="➕ ADD NEW TASK",
            font=('Arial', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card'],
            pady=20
        )
        form_title.pack()
        
        # Task description
        tk.Label(
            left_panel,
            text="What do you need to do?",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=30, pady=(10, 5))
        
        self.task_entry = tk.Entry(
            left_panel,
            font=('Arial', 14),
            bg='white',
            fg='black',
            width=30,
            relief='flat'
        )
        self.task_entry.pack(padx=30, pady=(0, 20))
        self.task_entry.focus()
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority selection
        tk.Label(
            left_panel,
            text="Priority Level:",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=30, pady=(10, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(left_panel, bg=self.colors['card'])
        priority_frame.pack(padx=30, pady=(0, 20))
        
        priorities = [
            ("🔥 High", "High"),
            ("⚠️ Medium", "Medium"),
            ("📋 Low", "Low")
        ]
        
        for text, value in priorities:
            btn = tk.Radiobutton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value,
                font=('Arial', 11),
                bg=self.colors['card'],
                fg=self.colors['text'],
                selectcolor=self.colors['accent'],
                activebackground=self.colors['card'],
                activeforeground=self.colors['text']
            )
            btn.pack(side='left', padx=10)
        
        # Category selection
        tk.Label(
            left_panel,
            text="Category:",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=30, pady=(10, 5))
        
        self.category_var = tk.StringVar(value="General")
        categories = ["📚 School", "🏠 Home", "🎮 Fun", "⚽ Sports", "🎵 Music", "💻 Coding", "General"]
        
        category_menu = tk.OptionMenu(
            left_panel,
            self.category_var,
            *categories
        )
        category_menu.config(
            font=('Arial', 11),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text'],
            relief='flat'
        )
        category_menu.pack(padx=30, pady=(0, 30), fill='x')
        
        # Add Task Button
        add_button = tk.Button(
            left_panel,
            text="➕ ADD TASK",
            command=self.add_task,
            font=('Arial', 14, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2'
        )
        add_button.pack(pady=(0, 20))
        
        # Right panel - Task list
        right_panel = tk.Frame(main_container, bg=self.colors['card'], relief='flat', bd=2)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Task list header
        list_header = tk.Frame(right_panel, bg=self.colors['accent'], height=50)
        list_header.pack(fill='x')
        list_header.pack_propagate(False)
        
        tk.Label(
            list_header,
            text="📋 YOUR TASKS",
            font=('Arial', 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['accent']
        ).pack(pady=10)
        
        # Task list container with scrollbar
        list_container = tk.Frame(right_panel, bg=self.colors['card'])
        list_container.pack(fill='both', expand=True)
        
        # Canvas for scrollable area
        self.canvas = tk.Canvas(list_container, bg=self.colors['card'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Task list frame inside scrollable frame
        self.task_list_frame = tk.Frame(self.scrollable_frame, bg=self.colors['card'])
        self.task_list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Load existing tasks
        self.refresh_task_list()
        
        # Stats at bottom
        self.stats_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['bg'],
            pady=10
        )
        self.stats_label.pack()
        
        self.update_stats()
    
    def add_task(self):
        """Add a new task to the list"""
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Oops!", "Please enter a task description!")
            return
        
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': self.priority_var.get(),
            'category': self.category_var.get(),
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed_at': None
        }
        
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()
        self.save_tasks()
        
        # Show success message with flair
        success_window = tk.Toplevel(self.root)
        success_window.title("Success!")
        success_window.geometry("300x150")
        success_window.configure(bg=self.colors['success'])
        success_window.transient(self.root)
        
        tk.Label(
            success_window,
            text="🎉 Task Added!",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg=self.colors['success']
        ).pack(pady=30)
        
        tk.Label(
            success_window,
            text=f"'{description[:20]}...'",
            font=('Arial', 12),
            fg='white',
            bg=self.colors['success']
        ).pack()
        
        self.root.after(1500, success_window.destroy)
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing tasks
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            # Show empty state
            empty_label = tk.Label(
                self.task_list_frame,
                text="🎯 No tasks yet!\nAdd your first task above!",
                font=('Arial', 16),
                fg=self.colors['text'],
                bg=self.colors['card'],
                pady=50
            )
            empty_label.pack()
            return
        
        # Sort tasks: incomplete first, then by priority
        sorted_tasks = sorted(self.tasks, 
                            key=lambda x: (x['completed'], 
                                          {'High': 0, 'Medium': 1, 'Low': 2}[x['priority']]))
        
        for task in sorted_tasks:
            self.create_task_widget(task)
        
        self.update_stats()
    
    def create_task_widget(self, task):
        """Create a widget for a single task"""
        task_frame = tk.Frame(self.task_list_frame, bg=self.colors['card'], relief='flat', bd=1)
        task_frame.pack(fill='x', pady=5, padx=5)
        
        # Color based on priority
        priority_colors = {
            'High': self.colors['danger'],
            'Medium': self.colors['warning'],
            'Low': '#4CAF50'  # Green for low priority
        }
        
        bg_color = priority_colors.get(task['priority'], self.colors['card'])
        
        if task['completed']:
            bg_color = '#333333'  # Dark gray for completed tasks
        
        # Main task frame
        main_task_frame = tk.Frame(task_frame, bg=bg_color, relief='flat')
        main_task_frame.pack(fill='x', padx=2, pady=2)
        
        # Checkbox
        check_var = tk.BooleanVar(value=task['completed'])
        checkbox = tk.Checkbutton(
            main_task_frame,
            variable=check_var,
            command=lambda t=task, v=check_var: self.toggle_task(t, v),
            bg=bg_color,
            activebackground=bg_color,
            selectcolor=bg_color
        )
        checkbox.grid(row=0, column=0, padx=15, pady=10)
        
        # Task description
        desc_font = ('Arial', 12, 'overstrike' if task['completed'] else 'normal')
        desc_color = '#888888' if task['completed'] else self.colors['text']
        
        desc_label = tk.Label(
            main_task_frame,
            text=task['description'],
            font=desc_font,
            fg=desc_color,
            bg=bg_color,
            anchor='w'
        )
        desc_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Category and date
        info_frame = tk.Frame(main_task_frame, bg=bg_color)
        info_frame.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')
        
        tk.Label(
            info_frame,
            text=task['category'],
            font=('Arial', 9),
            fg=desc_color,
            bg=bg_color
        ).pack(side='left', padx=(0, 15))
        
        tk.Label(
            info_frame,
            text=f"📅 {task['created_at']}",
            font=('Arial', 9),
            fg=desc_color,
            bg=bg_color
        ).pack(side='left')
        
        # Priority indicator
        priority_frame = tk.Frame(main_task_frame, bg=bg_color)
        priority_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=10)
        
        priority_emoji = {
            'High': '🔥',
            'Medium': '⚠️',
            'Low': '📋'
        }
        
        tk.Label(
            priority_frame,
            text=priority_emoji.get(task['priority'], '📌'),
            font=('Arial', 16),
            bg=bg_color,
            fg=desc_color
        ).pack()
        
        tk.Label(
            priority_frame,
            text=task['priority'],
            font=('Arial', 10),
            bg=bg_color,
            fg=desc_color
        ).pack()
        
        # Action buttons frame
        actions_frame = tk.Frame(main_task_frame, bg=bg_color)
        actions_frame.grid(row=0, column=3, rowspan=2, padx=20, pady=10)
        
        # Edit button
        edit_btn = tk.Button(
            actions_frame,
            text="✏️",
            command=lambda t=task: self.edit_task(t),
            font=('Arial', 12),
            bg=self.colors['accent'],
            fg='white',
            relief='flat',
            padx=8,
            cursor='hand2'
        )
        edit_btn.pack(pady=2)
        
        # Delete button
        delete_btn = tk.Button(
            actions_frame,
            text="🗑️",
            command=lambda t=task: self.delete_task(t),
            font=('Arial', 12),
            bg=self.colors['danger'],
            fg='white',
            relief='flat',
            padx=8,
            cursor='hand2'
        )
        delete_btn.pack(pady=2)
    
    def toggle_task(self, task, check_var):
        """Toggle task completion status"""
        task['completed'] = check_var.get()
        if task['completed']:
            task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        else:
            task['completed_at'] = None
        
        self.save_tasks()
        self.refresh_task_list()
        
        # Celebration for completing all tasks
        if all(t['completed'] for t in self.tasks) and self.tasks:
            self.show_celebration()
    
    def edit_task(self, task):
        """Edit a task"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x300")
        edit_window.configure(bg=self.colors['card'])
        edit_window.transient(self.root)
        
        tk.Label(
            edit_window,
            text="✏️ EDIT TASK",
            font=('Arial', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=20)
        
        # Description
        tk.Label(
            edit_window,
            text="Description:",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=40, pady=(10, 5))
        
        desc_entry = tk.Entry(
            edit_window,
            font=('Arial', 14),
            width=30
        )
        desc_entry.pack(padx=40, pady=(0, 20))
        desc_entry.insert(0, task['description'])
        
        # Priority
        tk.Label(
            edit_window,
            text="Priority:",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=40, pady=(10, 5))
        
        priority_var = tk.StringVar(value=task['priority'])
        tk.Radiobutton(
            edit_window,
            text="🔥 High",
            variable=priority_var,
            value="High",
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=40)
        tk.Radiobutton(
            edit_window,
            text="⚠️ Medium",
            variable=priority_var,
            value="Medium",
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=40)
        tk.Radiobutton(
            edit_window,
            text="📋 Low",
            variable=priority_var,
            value="Low",
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=40, pady=(0, 20))
        
        def save_changes():
            task['description'] = desc_entry.get()
            task['priority'] = priority_var.get()
            self.save_tasks()
            self.refresh_task_list()
            edit_window.destroy()
            messagebox.showinfo("Updated!", "Task updated successfully!")
        
        tk.Button(
            edit_window,
            text="💾 SAVE CHANGES",
            command=save_changes,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def delete_task(self, task):
        """Delete a task with confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete task: '{task['description'][:30]}...'?", 
                              icon='warning'):
            self.tasks.remove(task)
            self.save_tasks()
            self.refresh_task_list()
            
            # Show deletion animation
            self.stats_label.config(text=f"🗑️ Deleted: {task['description'][:20]}...")
            self.root.after(1000, self.update_stats)
    
    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        
        if total == 0:
            self.stats_label.config(text="🎯 Add your first task!")
        else:
            progress = (completed / total) * 100
            self.stats_label.config(
                text=f"📊 Progress: {completed}/{total} tasks completed • {progress:.0f}%"
            )
    
    def show_celebration(self):
        """Show celebration when all tasks are completed"""
        celebration = tk.Toplevel(self.root)
        celebration.title("🎉 Congratulations!")
        celebration.geometry("400x300")
        celebration.configure(bg='gold')
        
        tk.Label(
            celebration,
            text="🎉🎊🎉",
            font=('Arial', 40),
            bg='gold'
        ).pack(pady=30)
        
        tk.Label(
            celebration,
            text="ALL TASKS COMPLETED!",
            font=('Arial', 20, 'bold'),
            bg='gold'
        ).pack(pady=10)
        
        tk.Label(
            celebration,
            text="You're awesome! 🏆",
            font=('Arial', 16),
            bg='gold'
        ).pack(pady=20)
        
        self.root.after(3000, celebration.destroy)
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists('tasks.json'):
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
        except:
            self.tasks = []

def main():
    """Main function to run the app"""
    root = tk.Tk()
    app = SimpleAwesomeTodo(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()