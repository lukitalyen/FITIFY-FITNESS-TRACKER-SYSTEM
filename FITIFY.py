#Alvarez, Allyza Marie L., Atienza, Dorothy Amor C., De Villa, Jan Allen C., Guico, Luis Daniel C., Onda, Joelar
#IT 2104 - FINAL PROJECT

import tkinter as tk
from tkinter import ttk, PhotoImage, Label
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import sv_ttk


host = "localhost"
user = "root"
database = "try2"

conn = mysql.connector.connect(
    host=host,
    user=user,
    database=database
)

class FitnessApp:
    def __init__(self, root):
        self.bmi = None
        self.images = { }
        self.root = root
        self.startup_page()
        self.root.title('Fitify')
        self.calculated_tdee = 0
        self.uploaded_pictures_directory = r"C:\Users\ally\Desktop\FPJ\UPP"
        os.makedirs(self.uploaded_pictures_directory, exist_ok=True)
        self.new_profile_picture_path = None

        
    #Functions for all
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #Functions for Startup
    def startup_page(self):
        self.clear_frame()
    
       #Logo and Labels Frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(padx=10, pady=250)

        #Frame for Logo
        logo_path = r"C:\Users\ally\Desktop\FPJ\logo-light.png"
        self.logo = tk.PhotoImage(file=logo_path)

        #Canvas for Logo
        logo_canvas = tk.Canvas(content_frame, width=self.logo.width(), height=self.logo.height(), highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        logo_canvas.create_image(0, 0, anchor=tk.NW, image=self.logo)

        #Frame for Labels, Entries, Buttons
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        #Username Label and Entry
        username_label = ttk.Label(left_frame, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(left_frame, font=('Arial', 12))
        username_entry.pack(pady=5)

        #PIN Label and Entry
        pin_label = ttk.Label(left_frame, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(left_frame, font=('Arial', 12), show='*')
        pin_entry.pack(pady=5)

        pin_warning_label = ttk.Label(left_frame, text='', font=('Arial', 12))
        pin_warning_label.pack(pady=5)

        #Log In and Sign Up Buttons
        login_button = ttk.Button(left_frame, text='Log In', command=lambda: self.authenticate_user(username_entry.get(), pin_entry.get(), pin_warning_label))
        login_button.pack(pady=10)

        signup_button = ttk.Button(left_frame, text='Sign Up', command=self.signup_page)
        signup_button.pack(pady=10)

    #Sign Up Page
    def signup_page(self):
        self.clear_frame()

        back_button = ttk.Button(self.root, text='Back to Startup', command=self.startup_page)
        back_button.pack(pady=10)

        label = ttk.Label(self.root, text='Sign Up Page', font=('Arial', 14))
        label.pack(pady=10)

        username_label = ttk.Label(self.root, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(self.root, font=('Arial', 12))
        username_entry.pack(pady=5)

        pin_label = ttk.Label(self.root, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(self.root, font=('Arial', 12), show='')  
        pin_entry.pack(pady=5)

        email_label = ttk.Label(self.root, text='Email:', font=('Arial', 12))
        email_label.pack(pady=5)

        email_entry = ttk.Entry(self.root, font=('Arial', 12))
        email_entry.pack(pady=5)

        initial_weight_label = ttk.Label(self.root, text='Initial Weight (kg):', font=('Arial', 12))
        initial_weight_label.pack(pady=5)

        initial_weight_entry = ttk.Entry(self.root, font=('Arial', 12))
        initial_weight_entry.pack(pady=5)

        username_warning_label = ttk.Label(self.root, text='', font=('Arial', 12), foreground='red')
        username_warning_label.pack(pady=10)

        signup_success_label = ttk.Label(self.root, text='', font=('Arial', 12, 'bold'), foreground='green')
        signup_success_label.pack(pady=10)

        signup_button = ttk.Button(self.root, text='Sign Up', command=lambda: self.validate_and_save_user(
            username_entry.get(), pin_entry.get(), email_entry.get(), initial_weight_entry.get(),
            username_warning_label, signup_success_label))
        signup_button.pack(pady=10)


    def validate_and_save_user(self, username, pin, email, initial_weight, username_warning_label, signup_success_label):
        # Validation checks
        if not username or not pin or not email or not initial_weight:
            username_warning_label.config(text='Invalid input. Please fill in all fields.')
            signup_success_label.config(text='')
            return
        
        if len(pin) != 4 or not pin.isdigit():
            username_warning_label.config(text='Invalid PIN. Please enter a 4-digit numeric PIN.')
            signup_success_label.config(text='')
            return

        self.save_user(username, pin, email, initial_weight, username_warning_label, signup_success_label)

    def save_user(self, username, pin, email, initial_weight, username_warning_label, signup_success_label):
        try:
            cursor = conn.cursor()
        
            check_user_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(check_user_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                username_warning_label.config(text='Username already exists. Please choose a different username.')
                signup_success_label.config(text='')
                return

            username_warning_label.config(text='')

            insert_user_query = "INSERT INTO users (username, pin, email, initial_weight) VALUES (%s, %s, %s, %s)"
            user_data = (username, pin, email, initial_weight)
            cursor.execute(insert_user_query, user_data)

            conn.commit()

            print("User saved successfully!")
            signup_success_label.config(text='Account created successfully!')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    #LogIn Page
    def login_page(self):
        self.clear_frame()

        back_button = ttk.Button(self.root, text='Back to Startup', command=self.startup_page)
        back_button.pack(pady=10)

        label = ttk.Label(self.root, text='Log In Page', font=('Arial', 14))
        label.pack(pady=10)

        username_label = ttk.Label(self.root, text='Username:', font=('Arial', 12))
        username_label.pack(pady=5)

        username_entry = ttk.Entry(self.root, font=('Arial', 12))
        username_entry.pack(pady=5)

        pin_label = ttk.Label(self.root, text='4-digit PIN:', font=('Arial', 12))
        pin_label.pack(pady=5)

        pin_entry = ttk.Entry(self.root, font=('Arial', 12), show='')  # Show '' for PIN
        pin_entry.pack(pady=5)

        login_button = ttk.Button(self.root, text='Log In', command=lambda: self.authenticate_user(username_entry.get(), pin_entry.get()))
        login_button.pack(pady=10)

    def authenticate_user(self, username, pin, pin_warning_label):
        try:
            cursor = conn.cursor()

            if not pin.isdigit() or len(pin) != 4:
                pin_warning_label.config(text='Invalid PIN. Please enter a 4-digit PIN.', foreground='red')
                return
        
            pin_warning_label.config(text=' Invalid PIN ', foreground='red')

            authenticate_query = "SELECT * FROM users WHERE username = %s AND pin = %s"
            user_data = (username, pin)
            cursor.execute(authenticate_query, user_data)

            result = cursor.fetchone()

            if result:
                print("Authentication successful!")
                self.main_menu(username)
            else:
                print("Authentication failed. Invalid username or PIN.")
                
                if pin_warning_label:
                    pin_warning_label.config(text='Invalid PIN. Please try again.', foreground='red')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def create_buttons(self, parent_frame, username):
        style = ttk.Style()
        style.configure('NoBorder.TButton', background='#F0F0F0', bd=0, foreground='#ffffff', font=('Arial', 12))

        profile_icon = Image.open(r"C:\Users\ally\Desktop\FPJ\menu-icons\1.png")
        dashboard_icon = Image.open(r"C:\Users\ally\Desktop\FPJ\menu-icons\2.png")
        workout_log_icon = Image.open(r"C:\Users\ally\Desktop\FPJ\menu-icons\3.png")
        health_metrics_icon = Image.open(r"C:\Users\ally\Desktop\FPJ\menu-icons\4.png")
        nutrition_icon = Image.open(r"C:\Users\ally\Desktop\FPJ\menu-icons\5.png")

        icon_size = (150, 105)
        profile_icon = profile_icon.resize(icon_size, Image.LANCZOS)
        dashboard_icon = dashboard_icon.resize(icon_size, Image.LANCZOS)
        workout_log_icon = workout_log_icon.resize(icon_size, Image.LANCZOS)
        health_metrics_icon = health_metrics_icon.resize(icon_size, Image.LANCZOS)
        nutrition_icon = nutrition_icon.resize(icon_size, Image.LANCZOS)

        profile_icon = ImageTk.PhotoImage(profile_icon)
        dashboard_icon = ImageTk.PhotoImage(dashboard_icon)
        workout_log_icon = ImageTk.PhotoImage(workout_log_icon)
        health_metrics_icon = ImageTk.PhotoImage(health_metrics_icon)
        nutrition_icon = ImageTk.PhotoImage(nutrition_icon)

        profile_button = ttk.Button(parent_frame, text='', image=profile_icon, compound=tk.LEFT,
                                    command=lambda: self.profile_page(username), style='NoBorder.TButton')
        profile_button.image = profile_icon 
        profile_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        dashboard_button = ttk.Button(parent_frame, text='', image=dashboard_icon, compound=tk.LEFT,
                                      command=lambda: self.dashboard_page(username), style='NoBorder.TButton')
        dashboard_button.image = dashboard_icon
        dashboard_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        workout_log_button = ttk.Button(parent_frame, text='', image=workout_log_icon, compound=tk.LEFT,
                                        command=lambda: self.workout_log_page(username), style='NoBorder.TButton')
        workout_log_button.image = workout_log_icon
        workout_log_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        health_metrics_button = ttk.Button(parent_frame, text='', image=health_metrics_icon, compound=tk.LEFT,
                                           command=lambda: self.health_metrics_page(username), style='NoBorder.TButton')
        health_metrics_button.image = health_metrics_icon
        health_metrics_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

        nutrition_button = ttk.Button(parent_frame, text='', image=nutrition_icon, compound=tk.LEFT,
                                      command=lambda: self.nutrition_page(username), style='NoBorder.TButton')
        nutrition_button.image = nutrition_icon
        nutrition_button.pack(pady=5, fill=tk.X, padx=10, ipady=10)

    #Main Functions
    def main_menu(self, username):
        self.clear_frame()

        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        #Sidebar Buttons
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\ally\Desktop\FPJ\headers\head.png").resize((1100, 200)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  
        profile_picture_label.pack()

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\ally\Desktop\FPJ\welcome.png").resize((1100, 100)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  
        profile_picture_label.pack()

        profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\ally\Desktop\FPJ\WHN.png").resize((1100, 475)))
        profile_picture_label = tk.Label(content_frame, image=profile_picture)
        profile_picture_label.image = profile_picture  
        profile_picture_label.pack()
    

    #Profile Page
    def profile_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)
        
        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\profile.png" 
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))  
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image  
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                #Display profile picture
                profile_picture_path = user_data[5]  
                if profile_picture_path and os.path.isfile(profile_picture_path):
                    profile_picture = ImageTk.PhotoImage(Image.open(profile_picture_path).resize((100, 100)))
                else:
                    #If no profile picture is set, display the placeholder
                    profile_picture = ImageTk.PhotoImage(Image.open(r"C:\Users\ally\Desktop\FPJ\placeholder.png").resize((100, 100)))
            
                profile_picture_label = tk.Label(self.root, image=profile_picture)
                profile_picture_label.image = profile_picture 
                profile_picture_label.pack(pady=10)


                #Display user information
                username_label = tk.Label(self.root, text=f'Username: {user_data[1]}', font=('Arial', 12))
                username_label.pack(pady=5)

                pin_label = tk.Label(self.root, text=f'4-digit PIN: {"*" * len(user_data[2])}', font=('Arial', 12))
                pin_label.pack(pady=5)

                email_label = tk.Label(self.root, text=f'Email: {user_data[3]}', font=('Arial', 12))
                email_label.pack(pady=5)

                initial_weight_label = tk.Label(self.root, text=f'Initial Weight: {user_data[4]}', font=('Arial', 12))
                initial_weight_label.pack(pady=5)

                #Buttons for editing profile picture and details
                edit_picture_button = ttk.Button(self.root, text='Edit Profile Picture', command=lambda: self.edit_profile_picture(username))
                edit_picture_button.pack(pady=10)

                edit_details_button = ttk.Button(self.root, text='Edit Profile Details', command=lambda: self.edit_profile_details(username))
                edit_details_button.pack(pady=10)
            else:
                print(f"Error: User {username} not found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def edit_profile_picture(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)
        
        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\profile.png" 
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100))) 
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image 
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT profile_picture_path FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            result = cursor.fetchone()

            if result and result[0]:
                current_image_path = result[0]
                current_profile_picture = ImageTk.PhotoImage(Image.open(current_image_path).resize((100, 100)))
                current_picture_label = tk.Label(self.root, image=current_profile_picture)
                current_picture_label.image = current_profile_picture 
                current_picture_label.pack(pady=5)
            else:
                #If no profile picture is set, display the placeholder
                placeholder_path = r"C:\Users\ally\Desktop\FPJ\placeholder.png"
                placeholder_photo = ImageTk.PhotoImage(Image.open(placeholder_path).resize((100, 100)))
                current_picture_label = tk.Label(self.root, image=placeholder_photo)
                current_picture_label.image = placeholder_photo 
                current_picture_label.pack(pady=5)

            #Button to upload a new profile picture
            upload_button = ttk.Button(self.root, text='Upload Picture', command=lambda: self.upload_picture(username, current_picture_label))
            upload_button.pack(pady=10)

            #Button to save changes
            save_button = ttk.Button(self.root, text='Save', command=lambda: self.save_profile_picture(username))
            save_button.pack(pady=10)

            remove_button = ttk.Button(self.root, text='Remove Picture', command=lambda: self.remove_profile_picture(username, current_picture_label))
            remove_button.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()


    def upload_picture(self, username, current_picture_label):
        file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path: 
            _, file_extension = os.path.splitext(file_path)
            new_filename = f"{username}_profile_picture{file_extension}"
            new_file_path = os.path.join(self.uploaded_pictures_directory, new_filename)
            os.rename(file_path, new_file_path)

            #Load and display the selected profile picture
            new_profile_picture = ImageTk.PhotoImage(Image.open(new_file_path).resize((100, 100)))
            current_picture_label.configure(image=new_profile_picture)
            current_picture_label.image = new_profile_picture 

            #Store the path of the newly selected profile picture
            self.new_profile_picture_path = new_file_path


    def save_profile_picture(self, username):
        try:
            cursor = conn.cursor()

            update_query = "UPDATE users SET profile_picture_path = %s WHERE username = %s"
            cursor.execute(update_query, (self.new_profile_picture_path, username))
            conn.commit()

            print("Profile picture saved successfully!")

            #Go back to the profile page
            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_image_path(self, username):
        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT profile_picture_path FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            result = cursor.fetchone()

            if result and result[0]:
                return result[0]

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

        return None

    def remove_profile_picture(self, username, current_picture_label):
        try:
            cursor = conn.cursor()

            #Update the database with NULL to remove the profile picture
            update_query = "UPDATE users SET profile_picture_path = NULL WHERE username = %s"
            cursor.execute(update_query, (username,))
            conn.commit()

            print("Profile picture removed successfully!")

            placeholder_path = r"C:\Users\ally\Desktop\FPJ\placeholder.png"
            placeholder_photo = ImageTk.PhotoImage(Image.open(placeholder_path).resize((100, 100)))
            current_picture_label.configure(image=placeholder_photo)
            current_picture_label.image = placeholder_photo  

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def edit_profile_details(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)
        
        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\profile.png" 
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))  
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image  
            header_label.pack()

        try:
            cursor = conn.cursor()
            select_profile_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(select_profile_query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                new_username_label = tk.Label(self.root, text='New Username:', font=('Arial', 12))
                new_username_label.pack(pady=5)

                new_username_entry = tk.Entry(self.root, font=('Arial', 12))
                new_username_entry.insert(0, user_data[1])  #Pre-fill with existing username
                new_username_entry.pack(pady=5)

                new_pin_label = tk.Label(self.root, text='New 4-digit PIN:', font=('Arial', 12))
                new_pin_label.pack(pady=5)

                new_pin_entry = tk.Entry(self.root, font=('Arial', 12), show='')  
                new_pin_entry.insert(0, user_data[2])  #Pre-fill with existing PIN
                new_pin_entry.pack(pady=5)

                new_email_label = tk.Label(self.root, text='New Email:', font=('Arial', 12))
                new_email_label.pack(pady=5)

                new_email_entry = tk.Entry(self.root, font=('Arial', 12))
                new_email_entry.insert(0, user_data[3])  #Pre-fill with existing email
                new_email_entry.pack(pady=5)

                #Buttons to save changes
                save_username_button = ttk.Button(self.root, text='Save Username', command=lambda: self.save_username(username, new_username_entry.get()))
                save_username_button.pack(pady=10)

                save_pin_button = ttk.Button(self.root, text='Save PIN', command=lambda: self.save_pin(username, new_pin_entry.get()))
                save_pin_button.pack(pady=10)

                save_email_button = ttk.Button(self.root, text='Save Email', command=lambda: self.save_email(username, new_email_entry.get()))
                save_email_button.pack(pady=10)
            else:
                print(f"Error: User {username} not found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_username(self, old_username, new_username):
        try:
            cursor = conn.cursor()

            #Update the database with the new username
            update_query = "UPDATE users SET username = %s WHERE username = %s"
            cursor.execute(update_query, (new_username, old_username))
            conn.commit()

            print("Username saved successfully!")

            #Go back to the profile page
            self.profile_page(new_username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_pin(self, username, new_pin):
        try:
            cursor = conn.cursor()

            #Update the database with the new PIN
            update_query = "UPDATE users SET pin = %s WHERE username = %s"
            cursor.execute(update_query, (new_pin, username))
            conn.commit()

            print("PIN saved successfully!")

            #Go back to the profile page
            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_email(self, username, new_email):
        try:
            cursor = conn.cursor()

            #Update the database with the new email
            update_query = "UPDATE users SET email = %s WHERE username = %s"
            cursor.execute(update_query, (new_email, username))
            conn.commit()

            print("Email saved successfully!")

            #Go back to the profile page
            self.profile_page(username)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    #Dashboard Page
    def dashboard_page(self, username):
        self.clear_frame()

        #Sidebar frame
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.profile_page(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\dashboard.png"  
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image 
            header_label.pack()

        #Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 2)) 
        
        #Display graphs in three columns
        self.display_workout_logs(username)
        self.display_weight_logs(username)
        self.display_sleep_logs(username)

        
    def display_logs(self, username, log_type):
        if log_type == 'workout':
             self.display_workout_logs(username)
        elif log_type == 'weight':
             self.display_weight_logs(username)
        elif log_type == 'sleep':
             self.display_sleep_logs(username)
        else:
              print(f"Error: User {username} not found.")
             
    def display_workout_logs(self, username):
        label = ttk.Label(self.root, text='Workout Logs', font=('Arial', 14))
        label.place(relx=0.28,rely=0.30)

        try:
            cursor = conn.cursor()
            select_workouts_query = "SELECT exercise_type, SUM(duration) FROM workouts WHERE username = %s GROUP BY exercise_type"
            cursor.execute(select_workouts_query, (username,))
            workout_data = cursor.fetchall()

            if workout_data:
                fig, ax = plt.subplots(figsize=(3, 2))
                workout_types = [entry[0] for entry in workout_data]
                durations = [entry[1] for entry in workout_data]

                ax.bar(workout_types, durations)
                ax.set_xlabel('Workout Types')
                ax.set_ylabel('Total Duration (minutes)')

                canvas = FigureCanvasTkAgg(fig, master=self.root)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.place(relx=0.20, rely=0.35)

            else:
                no_data_label = ttk.Label(self.root, text='No workout data available.', font=('Arial', 12))
                no_data_label.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def display_weight_logs(self, username):
        label = ttk.Label(self.root, text='Weight Logs', font=('Arial', 14))
        label.place(relx=0.54,rely=0.30)

        try:
            cursor = conn.cursor()
            select_weight_logs_query = "SELECT weight, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_weight_logs_query, (username,))
            weight_data = cursor.fetchall()

            if weight_data:
                unique_months = set(entry[1].strftime("%B") for entry in weight_data if entry[1] is not None)

                month_var = tk.StringVar()
                month_combobox = ttk.Combobox(self.root, textvariable=month_var, values=list(unique_months))
                month_combobox.place(relx=0.76, rely=0.61)

                filter_button = ttk.Button(self.root, text='Filter by Month',
                                           command=lambda: self.filter_weight_logs_by_selected_month(username, month_var.get(),
                                                                                                       weight_data))
                filter_button.place(relx=0.80,rely=0.66)

                fig, ax = plt.subplots(figsize=(3, 2))
                dates = [entry[1].strftime("%m/%d") if entry[1] is not None else None for entry in weight_data]
                weights = [entry[0] for entry in weight_data]

                valid_data = [(date, weight) for date, weight in zip(dates, weights) if date is not None and weight is not None]
                valid_dates, valid_weights = zip(*valid_data)

                ax.plot(valid_dates, valid_weights, marker='o', color='orange')
                ax.set_xlabel('Date')
                ax.set_ylabel('Weight')

                canvas = FigureCanvasTkAgg(fig, master=self.root)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.place(relx=0.46, rely=0.35)

            else:
                no_data_label = ttk.Label(self.root, text='No weight data available.', font=('Arial', 12))
                no_data_label.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()


    def filter_weight_logs_by_selected_month(self, username, selected_month, weight_data):
        #Filter weight logs by selected month
        filtered_data = [entry for entry in weight_data if entry[1] is not None and entry[1].strftime("%B") == selected_month]

        if filtered_data:
            #Display the filtered weight logs
            print(f"Weight Logs for {selected_month}:")
            for entry in filtered_data:
                print(f"{entry[1].strftime('%m/%d')}: Weight - {entry[0]} kg")
                 
        else:
            print(f"No weight data available for {selected_month}.")

    
    #Add similar functions for sleep logs
    def display_sleep_logs(self, username):

        label = ttk.Label(self.root, text='Sleep Logs', font=('Arial', 14))
        label.place(relx=0.80, rely=0.30)

        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT sleep_duration, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_sleep_logs_query, (username,))
            sleep_data = cursor.fetchall()

            filtered_sleep_data = [(entry[0], entry[1]) for entry in sleep_data if entry[0] is not None]

            dates = [entry[1].strftime("%m/%d") if entry[1] is not None else 'N/A' for entry in filtered_sleep_data]
            sleep_durations = [entry[0] for entry in filtered_sleep_data]

            if sleep_durations:
                fig, ax = plt.subplots(figsize=(3, 2))
                ax.bar(dates, sleep_durations, color='purple')
                ax.set_xlabel('Date')
                ax.set_ylabel('Sleep Duration (hours)')

                canvas = FigureCanvasTkAgg(fig, master=self.root)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.place(relx=0.72, rely=0.35) 

            else:
                no_data_label = ttk.Label(self.root, text='No sleep data available.', font=('Arial', 12))
                no_data_label.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_sleep_graph(self, dates, sleep_durations):


        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(dates, sleep_durations, color='purple')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sleep Duration (hours)')

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.72, rely=0.35)
        self.canvas.draw()  # Draw the new canvas
    
    def get_sleep_logs(self, username):
        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT sleep_duration, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_sleep_logs_query, (username,))
            sleep_data = cursor.fetchall()
            return sleep_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_user_workouts(self, username):
        try:
            cursor = conn.cursor()
            select_workouts_query = "SELECT exercise_type, SUM(duration) FROM workouts WHERE username = %s GROUP BY exercise_type"
            cursor.execute(select_workouts_query, (username,))
            workout_data = cursor.fetchall()
            return workout_data

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def average_sleep_per_week(self, username):
        try:
            cursor = conn.cursor()
            select_sleep_logs_query = "SELECT AVG(sleep_duration), WEEK(date) FROM sleep_logs WHERE username = %s GROUP BY WEEK(date)"
            cursor.execute(select_sleep_logs_query, (username,))
            average_sleep_data = cursor.fetchall()

            if average_sleep_data:
                #Display the average sleep duration per week
                print("Average Sleep Duration per Week:")
                for entry in average_sleep_data:
                    print(f"Week {entry[1]}: {entry[0]:.2f} hours")

            else:
                print("No sleep data available.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    #Workout Logging Page
    def workout_log_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\workout.png" 
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))  
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image  
            header_label.pack()

        #Container Frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')
    
        #Configure columns to center the input boxes
        form_frame.columnconfigure(0, weight=1)

        #Inside workout_log_page and health_metrics_page functions
        success_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='green')
        success_label.grid(row=16, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')  
    
        warning_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='red')
        warning_label.grid(row=9, column=0, padx=10, pady=5, sticky='nsew')

        date_label = ttk.Label(form_frame, text='Date:', font=('Helvetica', 14))
        date_label.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        date_entry = DateEntry(form_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

        exercise_label = ttk.Label(form_frame, text='Exercise Type:', font=('Helvetica', 14))
        exercise_label.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        exercise_types = self.get_exercise_types()

        exercise_var = tk.StringVar()
        exercise_combobox = ttk.Combobox(form_frame, textvariable=exercise_var, values=exercise_types, font=('Arial', 12), width=10)
        exercise_combobox.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')

        duration_label = ttk.Label(form_frame, text='Duration (minutes):', font=('Arial', 14))
        duration_label.grid(row=6, column=0, padx=10, pady=5, sticky='nsew')

        duration_entry = ttk.Entry(form_frame, font=('Helvetica', 12), width=20)
        duration_entry.grid(row=7, column=0, padx=10, pady=5, sticky='nsew')

        submit_button = ttk.Button(form_frame, text='Submit Workout', command=lambda: self.log_workout(username, exercise_combobox.get(), duration_entry.get(), date_entry.get(), warning_label, success_label))
        submit_button.grid(row=8, column=0, padx=10, pady=(20, 10), sticky='nsew')

        clear_button = ttk.Button(self.root, text='Clear Labels', command=self.clear_workout_form)
        clear_button.pack(pady=10)

    def get_exercise_types(self):
        exercise_types = ['Running', 'Cycling', 'Weightlifting', 'Yoga', 'Swimming', 'Other']
        return exercise_types

    def log_workout(self, username, exercise, duration, date, warning_label, success_label):
        try:
            cursor = conn.cursor()
            
            if not exercise or not duration or not date:
                warning_label.config(text='Invalid input. Please fill in all fields.')
                return
            
            if not duration.isdigit():
                warning_label.config(text='Invalid duration. Please enter a numeric value.')
                return

            #Convert the date format from 'mm/dd/yy' to 'yyyy-mm-dd'
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            insert_workout_query = "INSERT INTO workouts (username, exercise_type, duration, date) VALUES (%s, %s, %s, %s)"
            workout_data = (username, exercise, duration, formatted_date)
            cursor.execute(insert_workout_query, workout_data)

            conn.commit()

            print("Workout logged successfully!")
            success_label.config(text='Workout logged successfully!')
            
            warning_label.config(text='')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def clear_workout_form(self):
        form_frame = self.root.winfo_children()[1].winfo_children()[2]
        for widget in form_frame.winfo_children():
            if isinstance(widget, (ttk.Entry, tk.Entry)):
                widget.delete(0, 'end')
            elif isinstance(widget, ttk.Label):
                # Leave the labels unchanged
                pass


    #Health Metrics Page
    def health_metrics_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        #Header image
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\health.png"  
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))  
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image  
            header_label.pack()

        #Container Frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')

        form_frame.columnconfigure(0, weight=1)

        #Calendar for sleep routine
        date_label = tk.Label(form_frame, text='Date:', font=('Helvetica', 12))
        date_label.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

        weight_label = tk.Label(form_frame, text='Weight (kg):', font=('Helvetica', 12))
        weight_label.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')

        weight_entry = tk.Entry(form_frame, font=('Helvetica', 12))
        weight_entry.grid(row=6, column=0, padx=10, pady=5, sticky='nsew')

        #Activity level options
        activity_label = tk.Label(form_frame, text='Activity Level:', font=('Helvetica', 12))
        activity_label.grid(row=8, column=0, padx=10, pady=5, sticky='nsew')

        activity_levels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Highly Active']
        activity_var = tk.StringVar()
        activity_combobox = ttk.Combobox(form_frame, textvariable=activity_var, values=activity_levels)
        activity_combobox.grid(row=9, column=0, padx=10, pady=5, sticky='nsew')

        #Sleep duration entry
        sleep_label = tk.Label(form_frame, text='Sleep Duration (hours):', font=('Helvetica', 12))
        sleep_label.grid(row=11, column=0, padx=10, pady=5, sticky='nsew')

        sleep_entry = tk.Entry(form_frame, font=('Helvetica', 12))
        sleep_entry.grid(row=12, column=0, padx=10, pady=5, sticky='nsew')
        
        date_warning = ttk.Label(form_frame, text='', foreground='red')
        date_warning.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')

        #Add warning labels for each input field
        #Inside workout_log_page and health_metrics_page functions
        success_label = ttk.Label(form_frame, text='', font=('Arial', 12), foreground='green')
        success_label.grid(row=16, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')  

        weight_warning = ttk.Label(form_frame, text='', foreground='red')
        weight_warning.grid(row=6, column=1, padx=10, pady=5, sticky='nsew')

        activity_warning = ttk.Label(form_frame, text='', foreground='red')
        activity_warning.grid(row=9, column=1, padx=10, pady=5, sticky='nsew')

        sleep_warning = ttk.Label(form_frame, text='', foreground='red')
        sleep_warning.grid(row=12, column=1, padx=10, pady=5, sticky='nsew')

        general_warning = ttk.Label(form_frame, text='', foreground='red')
        general_warning.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')  

        submit_button = ttk.Button(form_frame, text='Submit Metrics', command=lambda: self.log_health_metrics(username, weight_entry.get(), date_entry.get(), activity_combobox.get(), sleep_entry.get(), weight_warning, date_warning, activity_warning, sleep_warning, general_warning, success_label))
        submit_button.grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')  

        form_frame.grid_rowconfigure(4, minsize=15)  # Empty row between Date and Weight
        form_frame.grid_rowconfigure(7, minsize=15)  # Empty row between Weight and Activity Level
        form_frame.grid_rowconfigure(10, minsize=15)  # Empty row between Activity Level and Sleep Duration
        form_frame.grid_rowconfigure(13, minsize=15)  # Empty row between Sleep Duration and Submit Metrics

    def filter_health_logs_by_month(self, username, selected_month):
        try:
            cursor = conn.cursor()
            select_health_logs_query = "SELECT weight, date FROM health_metrics WHERE username = %s"
            cursor.execute(select_health_logs_query, (username,))
            health_data = cursor.fetchall()

            if health_data:
                #Filter health logs by month
                filtered_data = [entry for entry in health_data if entry[1].strftime("%B") == selected_month]

                if filtered_data:
                    #Display the filtered health logs
                    print(f"Heath Metrics Logs for {selected_month}:")
                    for entry in filtered_data:
                        print(f"{entry[1].strftime('%m/%d')}: Weight - {entry[0]} kg")

                else:
                    print(f"No health data available for {selected_month}.")

            else:
                print("No health data available.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    def log_health_metrics(self, username, weight, date, activity_level, sleep_duration, weight_warning, date_warning, activity_warning, sleep_warning, general_warning, success_label):
        try:
            #Check if any field is empty
            if not weight or not date or not activity_level or not sleep_duration:
                general_warning.config(text='Please fill in all fields.')
                return  #Exit the function if any field is empty

            #Check if weight is empty or not numeric
            if not weight.replace('.', '', 1).isdigit():
                weight_warning.config(text='Invalid weight. Please enter a numeric value.')
            else:
                weight_warning.config(text='')

            #Check if date is in the correct format
            try:
                formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
                date_warning.config(text='')
            except ValueError:
                date_warning.config(text='Invalid date format. Please use mm/dd/yy.')

            #Check if activity level is selected
            if not activity_level:
                activity_warning.config(text='Please select an activity level.')
            else:
                activity_warning.config(text='')

            #Check if sleep duration is empty or not numeric
            if not sleep_duration.isdigit():
                sleep_warning.config(text='Invalid sleep duration. Please enter a numeric value.')
            else:
                sleep_warning.config(text='')

            #Convert sleep duration to integer
            int_sleep_duration = int(sleep_duration)

            cursor = conn.cursor()

            #Insert health metrics data into the database
            insert_health_metrics_query = "INSERT INTO health_metrics (username, weight, date, activity_level, sleep_duration) VALUES (%s, %s, %s, %s, %s)"
            health_metrics_data = (username, float(weight), formatted_date, activity_level, int(sleep_duration))
            cursor.execute(insert_health_metrics_query, health_metrics_data)

            conn.commit()

            print("Health Metrics logged successfully!")
            success_label.config(text='Health Metrics logged successfully!')
            general_warning.config(text='')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()

    #Nutrition Section
    def nutrition_page(self, username):
        self.clear_frame()
        sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        label = ttk.Frame(self.root, padding=20)
        label.pack(side=tk.LEFT, fill=tk.Y)

        buttons_frame = tk.Frame(sidebar_frame, bg='#F0F0F0')
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(sidebar_frame, username)

        sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
        sign_out_button.pack(pady=15, fill=tk.X)

        back_button = ttk.Button(self.root, text='Back', command=lambda: self.main_menu(username))
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        
        header_image_path = r"C:\Users\ally\Desktop\FPJ\headers\nutrition.png"  
        if os.path.isfile(header_image_path):
            header_image = ImageTk.PhotoImage(Image.open(header_image_path).resize((789, 100)))  
            header_label = tk.Label(self.root, image=header_image)
            header_label.image = header_image  
            header_label.pack()

        #Container Frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(expand=True, fill='both')

        #Single Section
        goal_label = ttk.Label(form_frame, text='Select Weight Goal:', font=('Helvetica', 12))
        goal_label.grid(row=2, column=0, pady=5, sticky='nsew')

        goal_options = ['Losing Weight', 'Maintaining Weight', 'Gaining Weight']
        goal_var = tk.StringVar()
        goal_combobox = ttk.Combobox(form_frame, textvariable=goal_var, values=goal_options)
        goal_combobox.grid(row=2, column=1, pady=5, padx=(0, 10), sticky='nsew')  

        weight_label = ttk.Label(form_frame, text='Weight (kg):', font=('Helvetica', 12))
        weight_label.grid(row=3, column=0, pady=5, sticky='nsew')

        weight_entry = ttk.Entry(form_frame, font=('Helvetica', 12))
        weight_entry.grid(row=3, column=1, pady=5, padx=(0, 10), sticky='nsew')  

        height_label = ttk.Label(form_frame, text='Height (cm):', font=('Helvetica', 12))
        height_label.grid(row=4, column=0, pady=5, sticky='nsew')

        height_entry = ttk.Entry(form_frame, font=('Helvetica', 12))
        height_entry.grid(row=4, column=1, pady=5, padx=(0, 10), sticky='nsew')  

        activity_label = ttk.Label(form_frame, text='Activity Level:', font=('Helvetica', 12))
        activity_label.grid(row=5, column=0, pady=5, sticky='nsew')

        activity_levels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Highly Active']
        activity_var = tk.StringVar()
        activity_combobox = ttk.Combobox(form_frame, textvariable=activity_var, values=activity_levels)
        activity_combobox.grid(row=5, column=1, pady=5, padx=(0, 10), sticky='w')  

        #Button below the entry boxes
        calculate_and_get_suggestions_button = ttk.Button(
            form_frame,
            text='Calculate Calories and Get Food Suggestions',
            command=lambda: self.show_combined_results(
                weight_entry.get(),
                height_entry.get(),
                activity_combobox.get(),
                goal_combobox.get(),
                username
            )
        )
        calculate_and_get_suggestions_button.grid(row=6, column=1, pady=10, padx=10, sticky='nsew')

        #Configure columns to expand
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

    def show_combined_results(self, weight, height, activity_level, goal, username):
        try:
            self.clear_frame()

            #Sidebar
            sidebar_frame = tk.Frame(self.root, width=400, bg='#22668D')
            sidebar_frame.grid(row=0, column=0, sticky='nsw')

            #Content
            content_frame = ttk.Frame(self.root, padding=20)
            content_frame.grid(row=0, column=1, sticky='nsew')
            content_frame.columnconfigure(0, weight=1)

            #Create buttons in the sidebar
            self.create_buttons(sidebar_frame, username)

            #Sign-out button
            sign_out_button = ttk.Button(sidebar_frame, text='Sign Out', command=self.startup_page, style='NoBorder.TButton')
            sign_out_button.pack(pady=15, fill=tk.X)

            #Back button
            back_button = ttk.Button(content_frame, text='Back', command=lambda: self.nutrition_page(username))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky='sw')

            #Convert weight and height to float
            weight = float(weight)
            height = float(height)

            #Calculate BMI
            bmi = self.calculate_bmi(weight, height)

            #Store BMI for later use
            self.bmi = bmi

            #Define the activity level multiplier based on Harris-Benedict equation
            activity_multipliers = {
                'Sedentary': 1.2,
                'Lightly Active': 1.375,
                'Moderately Active': 1.55,
                'Highly Active': 1.725
            }

            activity_multiplier = activity_multipliers.get(activity_level, 1.2)

            #Define calorie adjustment for different goals
            goal_calorie_adjustments = {
                'Losing Weight': -500,  # Aim for a deficit of 500 calories per day for weight loss
                'Maintaining Weight': 0,
                'Gaining Weight': 500  # Aim for a surplus of 500 calories per day for weight gain
            }

            #Choose the appropriate calorie adjustment based on the selected goal
            calorie_adjustment = goal_calorie_adjustments.get(goal, 0)

            #Calculate Total Daily Energy Expenditure (TDEE) using the Harris-Benedict equation
            #TDEE = BMR * Activity Multiplier + Calorie Adjustment
            bmr = 10 * weight + 6.25 * height - 5
            tdee = bmr * activity_multiplier + calorie_adjustment
            self.bmi = bmi  #Store BMI for later use

            # Display the calculated TDEE
            result_label = ttk.Label(content_frame, text=f'Total Daily Calories: {tdee:.2f} calories', font=('Helvetica', 18))
            result_label.grid(row=1, column=0, padx=10, pady=20, sticky='nsew')

            #Load images for each goal
            image_paths = {
                'Losing Weight': r'C:\Users\ally\Desktop\FPJ\losing.png',
                'Maintaining Weight': r'C:\Users\ally\Desktop\FPJ\maintain.png',
                'Gaining Weight': r'C:\Users\ally\Desktop\FPJ\gain.png',
            }
            self.images = {goal: PhotoImage(file=image_path) for goal, image_path in image_paths.items()}

            #Display the image for the selected goal
            img_label = Label(content_frame, image=self.images[goal])
            img_label.grid(row=2, column=0, padx=10, pady=20, sticky='nw')

        except ValueError:
            print("Error: Please enter valid numerical values for weight and height.")
        except Exception as e:
            print(f"Error: {e}")

    
    def calculate_bmi(self, weight_kg, height_cm):
        #Convert height from centimeters to meters
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)


    def classify_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
           return "Overweight"
        else:
          return "Obese"

if __name__ == '__main__':
    try:
        cursor = conn.cursor()
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            pin VARCHAR(4),
            email VARCHAR(100),
            initial_weight FLOAT,
            profile_picture_path VARCHAR(255) DEFAULT NULL
            )
            """
        

        cursor.execute(create_users_table_query)

        create_workouts_table_query = """
        CREATE TABLE IF NOT EXISTS workouts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            exercise_type VARCHAR(100),
            duration INT,
            date DATE
        )
        """
        cursor.execute(create_workouts_table_query)

        conn.commit()

        create_health_metrics_table_query = """
        CREATE TABLE IF NOT EXISTS health_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            weight DECIMAL(5, 2),
            date DATE,
            activity_level VARCHAR(20)
        )
        """
        cursor.execute(create_health_metrics_table_query)

        conn.commit()
        
        create_sleep_logs_table_query = """
        CREATE TABLE IF NOT EXISTS sleep_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            sleep_duration INT,
            date DATE
        )
        """
        cursor.execute(create_sleep_logs_table_query)

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()

    root = tk.Tk()
    style = ttk.Style(root)

    sv_ttk.set_theme("dark")
   
    root.geometry("1200x800")
    
    app = FitnessApp(root)
    root.mainloop()

    conn.close()
