#operating system 

import tkinter as tk
from tkinter import ttk, messagebox

class SchedulerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Scheduling Simulator - Pro Version")
        self.root.geometry("1100x900") 
        self.root.configure(bg="#1e1e2e")

        self.processes = []
        self.colors = ["#ff5555", "#50fa7b", "#8be9fd", "#bd93f9", "#ff79c6", "#f1fa8c"]

        self.setup_ui()
        

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="CPU SCHEDULING SIMULATOR", font=("Helvetica", 22, "bold"), fg="#bd93f9", bg="#1e1e2e").pack(pady=10)

        # --- INPUT SECTION ---
        input_frame = tk.Frame(self.root, bg="#282a36", padx=15, pady=15, highlightbackground="#44475a", highlightthickness=2)
        input_frame.pack(fill="x", padx=30)

        label_style = {"fg": "#f8f8f2", "bg": "#282a36", "font": ("Arial", 11, "bold")}
        
        # Static Inputs
        tk.Label(input_frame, text="Arrival:", **label_style).grid(row=0, column=0)
        self.arrival_entry = tk.Entry(input_frame, width=6, font=("Arial", 12))
        self.arrival_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Burst:", **label_style).grid(row=0, column=2)
        self.burst_entry = tk.Entry(input_frame, width=6, font=("Arial", 12))
        self.burst_entry.grid(row=0, column=3, padx=5)

        # Algorithm Selection
        self.algo_var = tk.StringVar(value="FCFS")
        algo_menu = ttk.Combobox(input_frame, textvariable=self.algo_var, values=["FCFS", "SJF (Non-Preemptive)", "Priority (Non-Preemptive)", "Round Robin"], font=("Arial", 10), width=22, state="readonly")
        algo_menu.grid(row=0, column=4, padx=15)
        algo_menu.bind("<<ComboboxSelected>>", self.toggle_extra_inputs)

        # Dynamic Priority Container
        self.prio_frame = tk.Frame(input_frame, bg="#282a36")
        tk.Label(self.prio_frame, text="Priority:", **label_style).pack(side="left")
        self.priority_entry = tk.Entry(self.prio_frame, width=6, font=("Arial", 12))
        self.priority_entry.insert(0, "1")
        self.priority_entry.pack(side="left", padx=5)

        # Dynamic Quantum Container
        self.quantum_frame = tk.Frame(input_frame, bg="#282a36")
        tk.Label(self.quantum_frame, text="Quantum:", **label_style).pack(side="left")
        self.quantum_entry = tk.Entry(self.quantum_frame, width=4, font=("Arial", 12))
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side="left", padx=5)

        # Add Button
        tk.Button(input_frame, text="ADD +", command=self.add_process, bg="#50fa7b", font=("Arial", 10, "bold"), padx=15).grid(row=0, column=7, padx=10)

        # Initialize visibility
        self.toggle_extra_inputs()

        # --- TABLES & CHARTS ---
        tk.Label(self.root, text="CURRENT INPUT DATA", font=("Helvetica", 12, "bold"), fg="#f8f8f2", bg="#1e1e2e").pack(pady=(15, 0))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#282a36", foreground="white", fieldbackground="#282a36", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#44475a", foreground="white")

        self.input_tree = ttk.Treeview(self.root, columns=("ID", "AT", "BT", "Priority"), show="headings", height=5)
        for col in ("ID", "AT", "BT", "Priority"):
            self.input_tree.heading(col, text=col)
            self.input_tree.column(col, anchor="center")
        self.input_tree.pack(pady=5, padx=30, fill="x")

        tk.Label(self.root, text="SIMULATION RESULTS", font=("Helvetica", 12, "bold"), fg="#8be9fd", bg="#1e1e2e").pack(pady=(15, 0))
        self.result_tree = ttk.Treeview(self.root, columns=("ID", "AT", "BT", "CT", "TAT", "WT"), show="headings", height=5)
        for col in ("ID", "AT", "BT", "CT", "TAT", "WT"):
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, anchor="center", width=100)
        self.result_tree.pack(pady=5, padx=30, fill="x")

        tk.Label(self.root, text="GANTT CHART", font=("Helvetica", 12, "bold"), fg="#ffb86c", bg="#1e1e2e").pack(pady=(15, 0))
        self.canvas = tk.Canvas(self.root, height=120, bg="#282a36", highlightthickness=1, highlightbackground="#6272a4")
        self.canvas.pack(fill="x", padx=30, pady=5)

        # Footer / Controls
        avg_ctrl_frame = tk.Frame(self.root, bg="#1e1e2e")
        avg_ctrl_frame.pack(pady=10, fill="x", padx=30)
        self.avg_tat_lbl = tk.Label(avg_ctrl_frame, text="Avg TAT: --", font=("Arial", 12, "bold"), fg="#f8f8f2", bg="#1e1e2e")
        self.avg_tat_lbl.pack(side="left", padx=20)
        self.avg_wt_lbl = tk.Label(avg_ctrl_frame, text="Avg WT: --", font=("Arial", 12, "bold"), fg="#f8f8f2", bg="#1e1e2e")
        self.avg_wt_lbl.pack(side="left", padx=20)
        tk.Button(avg_ctrl_frame, text="RESET ALL", command=self.reset_all, bg="#ff5555", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=10)
        tk.Button(avg_ctrl_frame, text="RUN SIMULATION", command=self.run_simulation, bg="#bd93f9", fg="white", font=("Arial", 10, "bold"), padx=20).pack(side="right", padx=10)

    def toggle_extra_inputs(self, event=None):
        """Hides/Shows inputs based on selection"""
        algo = self.algo_var.get()
        # Hide everything first
        self.prio_frame.grid_forget()
        self.quantum_frame.grid_forget()

        if algo == "Priority (Non-Preemptive)":
            self.prio_frame.grid(row=0, column=5, padx=5)
        elif algo == "Round Robin":
            self.quantum_frame.grid(row=0, column=5, padx=5)

    def add_process(self):
        try:
            pid = len(self.processes) + 1
            at = int(self.arrival_entry.get())
            bt = int(self.burst_entry.get())
            # Default priority to 1 if hidden
            pr = int(self.priority_entry.get()) if self.algo_var.get() == "Priority (Non-Preemptive)" else 1
            
            self.processes.append({'id': pid, 'at': at, 'bt': bt, 'pr': pr, 'color': self.colors[(pid-1) % len(self.colors)]})
            self.input_tree.insert("", "end", values=(f"P{pid}", at, bt, pr))
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")

    def run_simulation(self):
        if not self.processes: return
        self.canvas.delete("all")
        algo = self.algo_var.get()
        if algo == "FCFS": schedule = self.solve_fcfs()
        elif algo == "SJF (Non-Preemptive)": schedule = self.solve_sjf()
        elif algo == "Priority (Non-Preemptive)": schedule = self.solve_priority()
        else: schedule = self.solve_rr()
        self.animate_gantt(schedule)
        self.display_results(schedule)

    def solve_fcfs(self):
        procs = sorted(self.processes, key=lambda x: x['at'])
        t, schedule = 0, []
        for p in procs:
            if t < p['at']: t = p['at']
            start = t; t += p['bt']
            schedule.append({'id': p['id'], 'start': start, 'end': t, 'color': p['color'], 'at': p['at'], 'bt': p['bt']})
        return schedule

    def solve_sjf(self):
        procs = sorted(self.processes, key=lambda x: x['at'])
        t, schedule, finished = 0, [], [False] * len(procs)
        while False in finished:
            available = [i for i, p in enumerate(procs) if not finished[i] and p['at'] <= t]
            if not available:
                t = min(p['at'] for i, p in enumerate(procs) if not finished[i]); continue
            idx = min(available, key=lambda i: procs[i]['bt'])
            p = procs[idx]
            schedule.append({'id': p['id'], 'start': t, 'end': t + p['bt'], 'color': p['color'], 'at': p['at'], 'bt': p['bt']})
            t += p['bt']; finished[idx] = True
        return schedule

    def solve_priority(self):
        procs = sorted(self.processes, key=lambda x: x['at'])
        t, schedule, finished = 0, [], [False] * len(procs)
        while False in finished:
            available = [i for i, p in enumerate(procs) if not finished[i] and p['at'] <= t]
            if not available:
                t = min(p['at'] for i, p in enumerate(procs) if not finished[i]); continue
            idx = min(available, key=lambda i: procs[i]['pr'])
            p = procs[idx]
            schedule.append({'id': p['id'], 'start': t, 'end': t + p['bt'], 'color': p['color'], 'at': p['at'], 'bt': p['bt']})
            t += p['bt']; finished[idx] = True
        return schedule

    def solve_rr(self):
        try:
            q = int(self.quantum_entry.get())
        except: q = 2
        procs = [p.copy() for p in sorted(self.processes, key=lambda x: x['at'])]
        for p in procs: p['rem'] = p['bt']
        t, schedule, queue, visited = 0, [], [], [False] * len(procs)
        def check():
            for i, p in enumerate(procs):
                if p['at'] <= t and not visited[i]:
                    queue.append(p); visited[i] = True
        check()
        while queue or any(not visited[i] for i in range(len(procs))):
            if not queue: t += 1; check(); continue
            p = queue.pop(0); exec_t = min(p['rem'], q)
            schedule.append({'id': p['id'], 'start': t, 'end': t + exec_t, 'color': p['color'], 'at': p['at'], 'bt': p['bt']})
            t += exec_t; p['rem'] -= exec_t; check()
            if p['rem'] > 0: queue.append(p)
        return schedule

    def display_results(self, schedule):
        completions = {}
        for task in schedule:
            completions[task['id']] = {'ct': task['end'], 'at': task['at'], 'bt': task['bt']}
        self.result_tree.delete(*self.result_tree.get_children())
        total_tat, total_wt = 0, 0
        for pid in sorted(completions.keys()):
            data = completions[pid]
            tat = data['ct'] - data['at']
            wt = tat - data['bt']
            total_tat += tat; total_wt += wt
            self.result_tree.insert("", "end", values=(f"P{pid}", data['at'], data['bt'], data['ct'], tat, wt))
        n = len(completions)
        self.avg_tat_lbl.config(text=f"Avg TAT: {total_tat/n:.2f}")
        self.avg_wt_lbl.config(text=f"Avg WT: {total_wt/n:.2f}")

    def animate_gantt(self, schedule):
        width = self.canvas.winfo_width() - 60
        if width <= 0: width = 1000 
        scale = width / schedule[-1]['end']
        for i, task in enumerate(schedule):
            x1, x2 = 30 + task['start'] * scale, 30 + task['end'] * scale
            self.root.after(i * 350, self.draw_block, x1, x2, task)

    def draw_block(self, x1, x2, task):
        self.canvas.create_rectangle(x1, 20, x2, 70, fill=task['color'], outline="white", width=2)
        self.canvas.create_text((x1+x2)/2, 45, text=f"P{task['id']}", fill="#282a36", font=("Arial", 10, "bold"))
        self.canvas.create_text(x1, 85, text=str(task['start']), fill="white", font=("Arial", 8, "bold"))
        self.canvas.create_text(x2, 85, text=str(task['end']), fill="white", font=("Arial", 8, "bold"))

    def reset_all(self):
        self.processes = []
        self.canvas.delete("all")
        self.input_tree.delete(*self.input_tree.get_children())
        self.result_tree.delete(*self.result_tree.get_children())
        self.avg_tat_lbl.config(text="Avg TAT: --")
        self.avg_wt_lbl.config(text="Avg WT: --")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerUI(root)
    root.mainloop()