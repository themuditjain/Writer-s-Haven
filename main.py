import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import codecs
import os

current_folder = None

def fill_tree_view(folder_path):
    tree_view.delete(*tree_view.get_children())
    tree_view.heading('#0', text=folder_path, anchor='w')
    # process_folder(folder_path, "")

def process_folder(folder_path, parent_item):
    # Get all files and folders in the folder
    for item in os.scandir(folder_path):
        if item.is_file():
            # Add file to the tree view
            file_name = item.name
            file_path = os.path.join(folder_path, file_name)
            tree_view.insert(parent_item, "end", text=file_name, open=False, tags=("file", file_path))
            # node = tree_view.insert(parent_item, "end", text=file_name, open=False, tags=("file", file_path))
            # process_folder(file_path, node)
        elif item.is_dir():
            # Add sub-folder to the tree view
            folder_name = item.name
            folder_item = tree_view.insert(parent_item, "end", text=folder_name, open=False, tags=("folder",))
            sub_folder_path = os.path.join(folder_path, folder_name)
            process_folder(sub_folder_path, folder_item)


def open_folder():
    global current_folder
    folder_path = filedialog.askdirectory()
    if folder_path:
        current_folder = folder_path
        # Clear the existing tree view
        tree_view.delete(*tree_view.get_children())
        # clear_tree_view()
        fill_tree_view(folder_path)
        # Get all files and folders in the selected folder
        process_folder(folder_path, "")
        
        if not tree_view.get_children():
            messagebox.showwarning("No Files", "The selected folder does not contain any files.")
    else:
        messagebox.showwarning("No Folder Selected", "Please select a folder.")


def open_file():
    selected_item = tree_view.selection()
    if selected_item:
        item_tags = tree_view.item(selected_item)["tags"]
        if "file" in item_tags:
            file_path = item_tags[1]
            open_file_path(file_path)
        elif "folder" in item_tags:
            tree_view.item(selected_item, open=not tree_view.item(selected_item, "open"))

def open_single_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        tree_view.insert("", "end", text=file_name, open=False, tags=("file", file_path))
        open_file_path(file_path)

def show_submenu(event):
    open_submenu.post(event.x_root, event.y_root)

def hide_submenu(event):
    open_submenu.unpost()


def open_file_path(file_path):
    global current_folder
    # selected_item = tree_view.focus()
    encodings = ["utf-8-sig", "utf-8", "latin-1"]
    content = None
    for encoding in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                break
        except UnicodeDecodeError:
            continue
    if current_folder and not os.path.isabs(file_path):
        file_path = os.path.join(current_folder, file_path)
    if content is not None:
        text_editor.delete(1.0, tk.END)  # Clear the existing text
        text_editor.insert(tk.END, content)  # Insert file content into the text editor
        sidebar_label.config(text=os.path.basename(file_path))
        update_side_panel(file_path)
    else:
        messagebox.showerror("Error", "Failed to open the file.")


def update_side_panel(file_path):
    file_name = file_path.split("/")[-1]

def save_file(event=None):
    selected_item = tree_view.selection()
    if selected_item:
        item_tags = tree_view.item(selected_item)["tags"]
        if "file" in item_tags:
            encodings = ["utf-8-sig", "utf-8", "latin-1"]
            file_path = item_tags[1]
            for encoding in encodings:
                try:
                    with codecs.open(file_path, "w", encoding) as file:
                        content = text_editor.get("1.0", "end")
                        file.write(content)
                        messagebox.showinfo("Success", "File saved successfully.")
                        break
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save the file: {e}")
                    break
    else:
        messagebox.showwarning("No File Selected", "Please select a file to save.")

def create_new_file():
    global current_folder
    if current_folder:
        new_file_path = filedialog.asksaveasfilename(initialdir=current_folder, title="Create New File",  defaultextension=".txt")
        if new_file_path:
            # file_name = os.path.basename(new_file_path)
            file_path = os.path.join(current_folder, new_file_path)
            with open(file_path, 'w') as file:
                file.write('')
            fill_tree_view(current_folder)
            process_folder(current_folder,"")
            
            open_file_path(file_path)  # Open the newly created file
            text_editor.delete("1.0", "end")  # Clear the text editor content
            # tree_view.insert("", "end", text=file_name, open=False, tags=("file", new_file_path))
            # Automatically select the newly created file in the tree view
            selected_item = tree_view.selection()
            if selected_item:
                tree_view.selection_remove(selected_item)
            tree_view.select(file_path)  # Select the newly created file
            tree_view.focus(file_path)
    else:
        new_file_path = filedialog.asksaveasfilename(initialdir='~', title="Create New File", defaultextension=".txt")
        if new_file_path:
            try:
                with open(new_file_path, 'w'):
                    pass
                file_name = os.path.basename(new_file_path)
                tree_view.insert("", "end", text=file_name, open=False, tags=("file", new_file_path))
                open_file_path(new_file_path)
            except IOError:
                messagebox.showerror("Error", "Failed to create the new file.")
        
            # file_name = os.path.basename(new_file_path)
            # tree_view.insert("", "end", text=file_name, open=False, tags=("file", new_file_path))
            # text_editor.delete("1.0", "end")  # Clear the text editor content
            # open_file_path(new_file_path)

# def save_file():
#     file_path = filedialog.asksaveasfilename(defaultextension=".txt")
#     if file_path:
#         content = text_editor.get(1.0, tk.END)
#         with open(file_path, 'w') as file:
#             file.write(content)

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()


# Create the main window
root = tk.Tk()
root.title("Writer's Haven")

# Set window dimensions
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Set the icon for the window
root.iconbitmap("paper_plane.ico")

# Configure the application style
root.style = ttk.Style()
root.style.theme_use('clam')
root.style.configure('TButton', font=('Arial', 10), background="#f2f2f2", foreground="#333333")

# Create a frame to contain the side panel and text editor
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

#create the sidebar
sidebar_frame = tk.Frame(main_frame, width=150)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

sidebar_label = tk.Label(sidebar_frame, text="Explore Yourself", font=("Arial", 12))
sidebar_label.pack(padx=5, pady=5)

# Create a tree view widget for displaying folders and files
tree_view = ttk.Treeview(sidebar_frame)
tree_view.pack(side=tk.LEFT, fill=tk.Y, expand=True)
# tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Bind double click event on tree view items
tree_view.bind("<<TreeviewSelect>>", lambda event: open_file())

# Bind the double-click event on the "New File" item to the create_new_file function
# tree_view.bind("<Double-1>", lambda event: create_new_file())

# Create a scrollbar for the tree view
tree_scroll = ttk.Scrollbar(sidebar_frame, orient="vertical", command=tree_view.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree_view.configure(yscrollcommand=tree_scroll.set)

# Bind right click event on tree view items
tree_view.bind("<Button-3>", show_submenu)
tree_view.bind("<Button-1>", hide_submenu)

# Create a frame to hold the text editor and scrollbars
editor_frame = tk.Frame(main_frame)
editor_frame.pack(fill="both", expand=True)

# Create a text editor widget
text_editor = scrolledtext.ScrolledText(editor_frame, font=("Arial", 12), undo=True, wrap=tk.WORD)
text_editor.pack(expand=True, fill="both")

# Sidebar label
sidebar_label = ttk.Label(editor_frame, text="No File Opened")
sidebar_label.pack(side=tk.BOTTOM, pady=5)


#Adding Control S feature
root.bind("<Control-s>", save_file) # Bind Control S feature
# root.protocol("WM_DELETE_WINDOW", save_file) # save fiile on window destroy

# Add a context menu to the text editor
text_editor_menu = tk.Menu(text_editor, tearoff=0)
text_editor_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: text_editor.event_generate("<<Cut>>"))
text_editor_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: text_editor.event_generate("<<Copy>>"))
text_editor_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: text_editor.event_generate("<<Paste>>"))
text_editor_menu.add_separator()
text_editor_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: text_editor.event_generate("<<Undo>>"))
text_editor_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: text_editor.event_generate("<<Redo>>"))

def show_text_editor_menu(event):
    text_editor_menu.post(event.x_root, event.y_root)

def hide_text_editor_menu(event):
    text_editor_menu.unpost()

text_editor.bind("<Button-3>", show_text_editor_menu)
text_editor.bind("<Button-1>", hide_text_editor_menu)


# #Create the vertical scrollbar for the text editor
# vertical_scrollbar = tk.Scrollbar(editor_frame, command=text_editor.yview)
# vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# text_editor.config(yscrollcommand=vertical_scrollbar.set)

# #Create the horizontal scrollbar for the text editor
# horizontal_scrollbar = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=text_editor.xview)
# horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
# text_editor.config(xscrollcommand=horizontal_scrollbar.set)


# Create the menu bar
menu_bar = tk.Menu(root)
# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
# Create the "Open" submenu
open_submenu = tk.Menu(file_menu, tearoff=0)
open_submenu.add_command(label="Open File", command=open_single_file)
open_submenu.add_command(label="Open Folder", command=open_folder)
file_menu.add_command(label="New File", command=create_new_file)
# Update the "Open" menu to include the submenu
file_menu.insert_cascade(0, label="Open", menu=open_submenu)
# file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
root.config(menu=menu_bar)


# Function to handle stack selection
def show_stack_layout(stack_type):
    # Hide all stack frames
    for frame in stack_frames.values():
        frame.pack_forget()
    
    # Show the selected stack frame
    stack_frames[stack_type].pack(fill="both", expand=True)
    messagebox.showinfo("Stack Layout", f"This is {stack_type}")

# Function to handle theme selection
def change_theme(theme_name):
    if theme_name == "dark":
        set_custom_dark()
    elif theme_name == "light":
        set_custom_light()
    else:
        set_default_theme()

def set_default_theme():
    # Reset the color scheme to default values
    text_editor.configure(background='white', foreground='black')
    text_editor.tag_configure('keyword', foreground='blue')
    text_editor.tag_configure('string', foreground='green')
    # Add more tag configurations for different elements

    # Reset the font style to default values
    text_editor.configure(font=('Arial', 12, 'normal'))


def set_custom_dark():
    # Configure the color scheme
    text_editor.configure(background='#222222', foreground='#ffffff')
    text_editor.tag_configure('keyword', foreground='#ff0000')
    text_editor.tag_configure('string', foreground='#00ff00')
    # Add more tag configurations for different elements
    # Configure the font style
    text_editor.configure(font=('Times New Roman', 12))

def set_custom_light():
    # Configure the color scheme
    text_editor.configure(background='#ffffff', foreground='#000000')
    text_editor.tag_configure('keyword', foreground='#0000ff')
    text_editor.tag_configure('string', foreground='#008000')
    # Add more tag configurations for different elements
    # Configure the font style
    text_editor.configure(font=('Times New Roman', 12))

# Create the "Stacks" menu
stacks_menu = tk.Menu(file_menu, tearoff=0)
stacks_menu.add_command(label="Comstack", command=lambda: show_stack_layout("Comstack"))
stacks_menu.add_command(label="Diagstack", command=lambda: show_stack_layout("Diagstack"))
stacks_menu.add_command(label="Memstack", command=lambda: show_stack_layout("Memstack"))
stacks_menu.add_command(label="NVMstack", command=lambda: show_stack_layout("NVMstack"))
stacks_menu.add_command(label="IOStack", command=lambda: show_stack_layout("IOStack"))
stacks_menu.add_command(label="OSStack", command=lambda: show_stack_layout("OSStack"))
stacks_menu.add_command(label="EUStack", command=lambda: show_stack_layout("EUStack"))

def troubleshoot():
    messagebox.showinfo("Troubleshoot", "You clicked Troubleshoot!")

def contact_us():
    messagebox.showinfo("Contact Us", "You clicked Contact Us!")

# Add the "Stacks" menu to the "File" menu
# file_menu.insert_cascade(1, label="Stacks", menu=stacks_menu)

# Add the "File" menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the "View" menu
view_menu = tk.Menu(menu_bar, tearoff=0)


# Create the "Themes" menu
themes_menu = tk.Menu(view_menu, tearoff=0)
themes_menu.add_command(label="Default", command=set_default_theme)
themes_menu.add_command(label="Light", command=set_custom_light)
themes_menu.add_command(label="Dark", command=set_custom_dark)

# Add the "Themes" menu to the "View" menu
view_menu.add_cascade(label="Themes", menu=themes_menu)

# Add the "View" menu to the menu bar
menu_bar.add_cascade(label="View", menu=view_menu)

# Create the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Troubleshoot", command=troubleshoot)
help_menu.add_command(label="Contact Us", command=contact_us)

# Add the "Help" menu to the menu bar
menu_bar.add_cascade(label="Help", menu=help_menu)


# Create frames for each stack layout
stack_frames = {}
for stack_type in ["Comstack", "Diagstack", "Memstack", "NVMstack", "IOStack", "OSStack", "EUStack"]:
    frame = tk.Frame(root)
    stack_frames[stack_type] = frame

# Start the application
root.mainloop()