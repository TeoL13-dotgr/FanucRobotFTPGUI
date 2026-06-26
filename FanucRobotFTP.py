import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog


class FtpLibrary:
    def ftp_connect(self, ip, user, pwd):
        return f"Connected to {ip}"

    def ftp_list(self):
        return ["PROGRAM1.TP", "PROGRAM2.TP", "BACKUP.TP"]

    def ftp_put(self, local_path, robot_path):
        return f"Uploaded {local_path} to {robot_path}"
# ──────────────────────────────────────────────────────────────────

def on_robot_select(event):
    choice = robot_select.get()

    # Predefined robot IPs
    robot_ips = {
        "Robot 1": "192.168.1.10",
        "Robot 2": "192.168.1.11",
        "Robot 3": "192.168.1.12",
        "Robot 4": "192.168.1.13"
    }

    if choice in robot_ips:
        ip_entry.config(state="normal")
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, robot_ips[choice])
        ip_entry.config(state="disabled")   # lock the field
    else:
        ip_entry.config(state="normal")     # allow typing for Custom

def connect_to_robot():
    ip = ip_entry.get()
    user = username_entry.get()
    pwd = password_entry.get()

    try:
        result = ftp.ftp_connect(ip, user, pwd)
        status_label.config(text=f"Connected to {ip}", fg="green")
        print(result)
    except Exception as e:
        status_label.config(text=f"Connection failed: {e}", fg="red")

def list_directory():
    try:
        # Get file list from robot
        result = ftp.ftp_list()

        # Clear previous entries
        for item in file_tree.get_children():
            file_tree.delete(item)

        # Insert new entries
        for filename in result:
            file_tree.insert("", "end", values=(filename, "/md/"))

        status_label.config(text="Directory listed successfully", fg="green")

    except Exception as e:
        status_label.config(text=f"List failed: {e}", fg="red")

def choose_file():
    global selected_file_path

    selected_file_path = filedialog.askopenfilename(
        title="Select TP program",
        filetypes=[("TP files", "*.TP"), ("All files", "*.*")]
    )

    if selected_file_path:
        filename = selected_file_path.split("/")[-1]
        selected_file_label.config(text=filename, fg="black")
    else:
        selected_file_label.config(text="No file selected", fg="gray")

def upload_file():
    try:
        # Check if a file was selected
        if not selected_file_path:
            status_label.config(text="No file selected", fg="red")
            return

        # Get destination folder
        dest_folder = dest_select.get()

        # Extract filename
        filename = selected_file_path.split("/")[-1]

        # Build full robot path
        robot_path = dest_folder + filename

        # Upload
        ftp.ftp_put(selected_file_path, robot_path)

        status_label.config(text=f"Uploaded to {robot_path}", fg="green")

    except Exception as e:
        status_label.config(text=f"Upload failed: {e}", fg="red")

def main():
    global ip_entry, robot_select, username_entry, password_entry

    root = tk.Tk()
    root.title("Fanuc FTP Client")
    root.geometry("600x600")

    # --- Logo frame ---
    logo_frame = tk.Frame(root)
    logo_frame.pack(anchor="w", pady=0, padx=0)

    tk.Label(root, text="Fanuc FTP Client", font=("Arial", 16)).pack(pady=0)

    # --- Dropdown frame ---
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=0)

    tk.Label(dropdown_frame, text="Select Robot:").grid(row=0, column=0, padx=5)

    robot_select = ttk.Combobox(dropdown_frame, values=[
        "Robot 1", "Robot 2", "Robot 3", "Robot 4", "Custom"
    ], state="readonly", width=15)

    robot_select.grid(row=0, column=1, padx=5)
    robot_select.bind("<<ComboboxSelected>>", on_robot_select)
    robot_select.set("Custom")  # default

    # --- IP row ---
    ip_frame = tk.Frame(root)
    ip_frame.pack(pady=10)

    tk.Label(ip_frame, text="Robot IP:").grid(row=0, column=0, padx=5)

    ip_entry = tk.Entry(ip_frame, width=20)
    ip_entry.grid(row=0, column=1, padx=5)

    tk.Button(ip_frame, text="Connect", command=connect_to_robot).grid(row=0, column=2, padx=5)

        # --- Username row ---
    user_frame = tk.Frame(root)
    user_frame.pack(pady=5)

    tk.Label(user_frame, text="Username:").grid(row=0, column=0, padx=5)
    username_entry = tk.Entry(user_frame, width=20)
    username_entry.grid(row=0, column=1, padx=5)

    # --- Password row ---
    pass_frame = tk.Frame(root)
    pass_frame.pack(pady=5)

    tk.Label(pass_frame, text="Password:").grid(row=0, column=0, padx=5)
    password_entry = tk.Entry(pass_frame, width=20, show="*")
    password_entry.grid(row=0, column=1, padx=5)

        # --- Status label ---
    global status_label
    status_label = tk.Label(root, text="", font=("Arial", 10))
    status_label.pack(pady=5)

    global ftp
    ftp = FtpLibrary()

        # --- List Directory row ---
    list_frame = tk.Frame(root)
    list_frame.pack(pady=5)

    tk.Button(list_frame, text="List Directory", command=list_directory).pack()

        # --- File selection row ---
    file_frame = tk.Frame(root)
    file_frame.pack(pady=5)

    tk.Button(file_frame, text="Choose .TP File", command=choose_file).grid(row=0, column=0, padx=5)

    global selected_file_label
    selected_file_label = tk.Label(file_frame, text="No file selected", fg="gray")
    selected_file_label.grid(row=0, column=1, padx=5)

        # --- Destination folder row ---
    dest_frame = tk.Frame(root)
    dest_frame.pack(pady=5)

    tk.Label(dest_frame, text="Destination Folder:").grid(row=0, column=0, padx=5)

    global dest_select
    dest_select = ttk.Combobox(dest_frame, values=[
        "/md/",
        "/fr/",
        "/mc/",
        "/ud1/",
        "/md/backup/"
    ], state="readonly", width=15)

    dest_select.grid(row=0, column=1, padx=5)
    dest_select.set("/md/")  # default

        # --- Upload button ---
    upload_frame = tk.Frame(root)
    upload_frame.pack(pady=5)

    tk.Button(upload_frame, text="Upload File", command=upload_file).pack()

        # --- Robot File Browser (Treeview) ---
    browser_frame = tk.Frame(root)
    browser_frame.pack(pady=10)

    global file_tree
    file_tree = ttk.Treeview(browser_frame, columns=("Name", "Path"), show="headings", height=10)

    file_tree.heading("Name", text="Name")
    file_tree.heading("Path", text="Path")

    file_tree.column("Name", width=200)
    file_tree.column("Path", width=100)

    file_tree.pack()




    root.mainloop()

if __name__ == "__main__":
    main()
