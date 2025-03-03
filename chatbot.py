import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import pandas as pd
import os
import time

# Function to navigate from welcome page to chatbot page
def start_chatbot():
    welcome_frame.pack_forget()
    chatbot_frame.pack(fill="both", expand=True)

# Function to handle exit/quit command
def exit_chatbot():
    chat_history.insert(tk.END, "\nSys: Thank you for visiting AI movie chatbot!\n", 'sys')
    chat_history.update()  # Ensure the message is displayed immediately
    root.after(5000, root.destroy)  # Close the application after 5 seconds

# Function to send chatbot messages
def send_message(event=None):
    global step, preferences
    user_input = entry.get().strip().lower()
    
    if user_input in ["exit", "quit"]:
        exit_chatbot()
        return
    
    if step == 0:
        chat_history.insert(tk.END, "Sys: Welcome to the Bollywood Movie Recommendation Assistant!\n", 'sys')
        chat_history.insert(tk.END, "Sys: What genre of movie do you prefer? (Romantic, Action, Comedy, Drama, Thriller, Historical, Musical, Sci-Fi)\n", 'sys')
        step += 1
    elif step == 1:
        preferences['genre'] = user_input
        chat_history.insert(tk.END, f"You: {user_input}\n", 'user')
        chat_history.insert(tk.END, "Sys: On a scale of 1 to 5, how much romance do you enjoy? (1 being least, 5 being most)\n", 'sys')
        step += 1
    elif step == 2:
        preferences['romance_level'] = int(user_input)
        chat_history.insert(tk.END, f"You: {user_input}\n", 'user')
        chat_history.insert(tk.END, "Sys: On a scale of 1 to 5, how much action do you enjoy? (1 being least, 5 being most)\n", 'sys')
        step += 1
    elif step == 3:
        preferences['action_level'] = int(user_input)
        chat_history.insert(tk.END, f"You: {user_input}\n", 'user')
        chat_history.insert(tk.END, "Sys: Are you looking for family-friendly movies? (Yes/No)\n", 'sys')
        step += 1
    elif step == 4:
        preferences['family_friendly'] = user_input
        chat_history.insert(tk.END, f"You: {user_input}\n", 'user')
        recommendations = get_movie_recommendation(preferences)
        chat_history.insert(tk.END, "Sys: Based on your preferences, here are some recommendations:\n", 'sys')
        display_recommendations(recommendations)
        step = 0  # Reset the step for a new interaction
    entry.delete(0, tk.END)


# Function to get movie recommendations based on preferences
def get_movie_recommendation(preferences):
    # Load movie data from Excel file
    movie_data = pd.DataFrame({
        'movie Names': ['3 Idiots', 'War', 'Sholay','Aashiqui 2','Hera Pheri','Lagaan','Kahaani','Bajirao Mastani','Kabhi Khushi Kabhi Ghum','Koi Mil Gaya','Kabir Singh','Drishyam'],
        'genre': ['comedy', 'action', 'action','romantic','comedy','drama','thriller','historical', 'musical', 'sci-fi', 'romantic', 'thriller'],
        'romance_level': [2, 1, 1, 5, 2, 1, 3, 5, 5, 3, 5, 3],
        'action_level': [3, 5, 5, 2, 4, 3, 4, 5, 1, 2, 5, 4],
        'family_friendly': ['yes', 'yes', 'yes','no', 'yes','yes', 'no', 'no', 'yes', 'yes', 'no', 'no'],
        'image_path': ['movie11.jpeg', 'movie10.jpeg', 'movie2.jpeg', 'movie1.jpeg', 'movie3.jpeg', 'movie4.jpeg', 'movie5.jpeg', 'movie6.jpeg', 'movie7.jpeg', 'movie8.jpeg', 'movie9.jpeg', 'movie12.jpeg']
    })
    # Filtering movies based on user preferences
    filtered_movies = movie_data[
        (movie_data['genre'].str.lower() == preferences['genre']) &
        (movie_data['romance_level'] <= preferences['romance_level']) &
        (movie_data['action_level'] <= preferences['action_level']) &
        (movie_data['family_friendly'].str.lower() == preferences['family_friendly'])
    ]
    return filtered_movies

# Function to display recommendations with images
def display_recommendations(recommendations):
    for widget in recommendation_frame.winfo_children():
        widget.destroy()

    if not recommendations.empty:
        row = 0
        col = 0
        for i, row_data in recommendations.iterrows():
            # Movie frame to group the image and title
            movie_frame = tk.Frame(recommendation_frame, bg="#2C2F33")
            movie_frame.grid(row=row, column=col, padx=10, pady=10)

            # Movie title
            movie_label = tk.Label(
                movie_frame,
                text=row_data['movie Names'],
                font=("Arial", 14, "bold"),
                bg="#2C2F33",
                fg="white"
            )
            movie_label.pack(side="top", pady=5)

            # Dynamically construct image path
            image_path = os.path.join("C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python311\\images", row_data['image_path'])
            try:
                movie_image = Image.open(image_path)
                movie_image = movie_image.resize((150, 200), Image.Resampling.LANCZOS)
                movie_photo = ImageTk.PhotoImage(movie_image)

                image_label = tk.Label(movie_frame, image=movie_photo, bg="#2C2F33")
                image_label.image = movie_photo
                image_label.pack(pady=5)

                # Make the image clickable
                image_label.bind("<Button-1>", lambda e, movie=row_data['movie Names']: open_movie_details(movie))

            except Exception as e:
                print(f"Error loading image for {row_data['movie Names']}: {e}")

            col += 1
            if col > 2:  # Adjust number of columns per row here
                col = 0
                row += 1
    else:
        no_result_label = tk.Label(
            recommendation_frame,
            text="Sorry, no movies match your preferences.",
            font=("Arial", 14),
            bg="#2C2F33",
            fg="white"
        )
        no_result_label.pack(pady=5)

# Function to open a new window with movie details
def open_movie_details(movie_name):
    if movie_name == "3 Idiots":
        description = ("3 Idiots is a 2009 Indian Hindi-language coming-of-age comedy-drama film written, edited and "
                       "directed by Rajkumar Hirani, co-written by Abhijat Joshi and produced by Vidhu Vinod Chopra.")
        youtube_link = "https://www.youtube.com/watch?v=hC83OcBmFgE"

    elif movie_name == "War":
        description = ("War film is a film genre concerned with warfare, typically about naval, air, or land battles, "
                       "with combat scenes central to the drama. It has been strongly associated with the 20th century. "
                       "Themes explored include combat, survival and escape, camaraderie between soldiers, sacrifice, "
                       "and the effects of war on society.")
        youtube_link = "https://www.youtube.com/watch?v=30zwFQEWemQ"

    elif movie_name == "Sholay":
        description = ("Sholay, a classic Indian film, released in 1975, became a blockbuster hit after initial struggles, "
                       "featuring iconic actors and unforgettable dialogues, leaving a lasting impact on Indian cinema.")
        youtube_link = "https://www.youtube.com/watch?v=XniRA_lNLnI"
        
    elif movie_name == "Aashiqui 2":
        description = ("Aashiqui 2 (transl. Romance 2) is a 2013 Indian Hindi-language romantic musical drama film directed "
                       "by Mohit Suri and produced by Mukesh Bhatt, Mahesh Bhatt, Bhushan Kumar and Krishan Kumar under the "
                       "Vishesh Films and T-Series Films, with Mahesh Bhatt also serving as presenter")
        youtube_link = "https://www.youtube.com/watch?v=nIkZwqAHZfg&t=14s"

    elif movie_name == "Hera Pheri":
        description = (" Hera Pheri (transl. Foul Play) is a 2000 Indian Hindi-language comedy film directed by Priyadarshan "
                       "and written by Neeraj Vora, starring Akshay Kumar, Suniel Shetty, Paresh Rawal, Tabu, Om Puri and Gulshan Grover.")
        youtube_link = "https://www.youtube.com/watch?v=XniRA_lNLnI"

    elif movie_name == "Lagaan":
        description = ("Set in 1893, during the late Victorian period of British colonial rule in India, the film follows the inhabitants of"
                       "a village in Central India, who, burdened by high taxes and several years of drought, are challenged by an arrogant "
                       "British Indian Army officer to a game of cricket as a wager to avoid paying the taxes they owe.")
        youtube_link = "https://www.youtube.com/watch?v=gbX-3eZRzsI"

    elif movie_name == "Kahani":
        description = ("Kahaani (IPA: [kəˈɦaːni]; transl. Story) is a 2012 Indian Hindi-language thriller film co-written, co-produced, "
                       "and directed by Sujoy Ghosh. It stars Vidya Balan as Vidya Bagchi, a pregnant woman looking for her missing husband in Kolkata during the festival of "
                       "Durga Puja, assisted by Assist Sub-Inspector Satyoki Rana Sinha (Parambrata Chatterjee) and Inspector General A. Khan (Nawazuddin Siddiqui).")
        youtube_link = "https://www.youtube.com/watch?v=WWBhfdaRfro"


    elif movie_name == "Bajirao Mastani":
        description = ("Bajirao Mastani is a 2015 Indian Hindi-language epic historical tragedy film directed by Sanjay Leela Bhansali, "
                       "who co-produced it with Eros International and composed its soundtrack. The film stars Ranveer Singh, "
                       "Deepika Padukone and Priyanka Chopra with Tanvi Azmi, Vaibhav Tatwawaadi, Milind Soman, Mahesh Manjrekar and Aditya Pancholi in "
                       "supporting roles. Based on Nagnath S. Inamdar's Marathi novel Rau, Bajirao Mastani narrates the story of the Maratha Peshwa Bajirao I (1700–1740) "
                       "and his second wife, Mastani.")
        youtube_link = "https://www.youtube.com/watch?v=PNTOyPXPfmk"

    elif movie_name == "Kabhi Khushi Kabhi Ghum":
        description = ("Kabhi Khushi Kabhie Gham… (transl. Sometimes happiness, sometimes sadness), also known by the initials K3G,[3] "
                       "is a 2001 Indian Hindi-language family drama film written and directed by Karan Johar and produced by Yash Johar under his banner Dharma Productions."
                       "The film stars an ensemble cast of Amitabh Bachchan, Jaya Bachchan, Shah Rukh Khan, Kajol, Hrithik Roshan, "
                       "and Kareena Kapoor, with Rani Mukerji in an extended guest appearance.")
        youtube_link = "https://www.youtube.com/watch?v=YnLKDI8t-tA"

    elif movie_name == "Koi Mil Gaya":
        description = ("Koi... Mil Gaya (Hindi pronunciation: [ˈkoːi mɪl ɡəjaː] transl. Someone...Is Found) is a 2003 Indian science fiction action-drama"
                       "film directed and produced by Rakesh Roshan. It stars Hrithik Roshan, Preity Zinta and Rekha. In addition to writing the story, "
                       "Rakesh Roshan also wrote the screenplay with Sachin Bhowmick, Honey Irani, and Robin Bhatt. Koi... Mil Gaya focuses on Rohit Mehra,"
                       "a developmentally disabled man who contacts an extraterrestrial being later named Jadoo with his late father Sanjay's supercomputer. "
                       "The film follows his relationship with Nisha, Rohit's friend, who falls in love with him.")
        youtube_link = "https://www.youtube.com/watch?v=hjAKlCWBSco"

    elif movie_name == "Kabir Singh":
        description = ("Kabir Singh is a 2019 Indian Hindi-language romantic drama film[1] co-written, co-edited and directed by Sandeep Reddy Vanga"
                       "and jointly produced by Bhushan Kumar and Krishan Kumar under T-Series Films and Murad Khetani and Ashwin Varde under Cine1 Studios."
                       "A remake of Vanga's own Telugu film Arjun Reddy (2017), it stars Shahid Kapoor in the title role as a doctor who spirals into "
                       "self-destruction when his girlfriend, played by Kiara Advani, marries someone else.")
        youtube_link = "https://www.youtube.com/watch?v=eby-cH2QiOU"

    elif movie_name == "Drishyam":
        description = ("Drishyam is an Indian crime thriller film series, written and directed by Jeethu Joseph, produced by Antony "
                       "Perumbavoor under Aashirvad Cinemas. It stars Mohanlal, Meena, Ansiba Hassan and Esther Anil as Georgekutty, Rani George, Anju George and Anu George.")
        youtube_link = "https://www.youtube.com/watch?v=U1DpL_2IkFk"

    else:
        description = "No details available."
        youtube_link = "#"

    details_window = Toplevel(root)
    details_window.title(movie_name)
    details_window.geometry("400x300")
    details_window.configure(bg="#2C2F33")

    description_label = tk.Label(
        details_window,
        text=description,
        wraplength=350,
        justify="left",
        bg="#2C2F33",
        fg="white",
        font=("Arial", 12)
    )
    description_label.pack(pady=10, padx=10)

    link_button = tk.Button(
        details_window,
        text="Watch Movie Here !!!!",
        command=lambda: os.system(f"start {youtube_link}"),
        bg="#7289DA",
        fg="white",
        font=("Arial", 12, "bold")
    )
    link_button.pack(pady=10)

# Initialize the GUI
root = tk.Tk()
root.title("Movie Assistant Chatbot")
root.geometry("800x800")
root.configure(bg="#2C2F33")


# Welcome Frame
welcome_frame = tk.Frame(root, bg="#2C2F33")
welcome_frame.pack(fill="both", expand=True)

# Load welcome image
welcome_image_path = "./images/welcome_image.jpeg"
welcome_image = Image.open(welcome_image_path)
welcome_image = welcome_image.resize((800, 600), Image.Resampling.LANCZOS)
welcome_photo = ImageTk.PhotoImage(welcome_image)

# Display welcome image
image_label = tk.Label(welcome_frame, image=welcome_photo, bg="#2C2F33")
image_label.pack(pady=20)

# Welcome text
welcome_text = tk.Label(
    welcome_frame, 
    text="Welcome to the Movie Chatbot!", 
    font=("Arial", 18, "bold"), 
    bg="#2C2F33", 
    fg="white"
)
welcome_text.pack(pady=10)

# Get Started Button
get_started_button = tk.Button(
    welcome_frame, 
    text="Get Started", 
    command=start_chatbot, 
    font=("Arial", 14, "bold"), 
    bg="#7289DA", 
    fg="white"
)
get_started_button.pack(pady=10)

# Chatbot Frame
chatbot_frame = tk.Frame(root, bg="#2C2F33")

# Chat history
chat_history = tk.Text(
    chatbot_frame, 
    wrap=tk.WORD, 
    height=20, 
    width=80, 
    bg="#99AAB5", 
    fg="#23272A", 
    relief=tk.FLAT,
    font=("Arial", 12)
)
chat_history.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Recommendation frame
recommendation_frame = tk.Frame(chatbot_frame, bg="#2C2F33")
recommendation_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# User input frame
input_frame = tk.Frame(chatbot_frame, bg="#2C2F33")
input_frame.pack(fill=tk.X, padx=20, pady=10)
entry = tk.Entry(
    input_frame, 
    width=50, 
    bg="#FFFFFF", 
    fg="#23272A", 
    font=("Arial", 12)
)
entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
send_button = tk.Button(
    input_frame, 
    text="Send", 
    command=send_message, 
    bg="#7289DA", 
    fg="white", 
    font=("Arial", 12, "bold")
)
send_button.pack(side=tk.LEFT, padx=5)

# Initialize variables
step = 0
preferences = {
    'genre': '',
    'romance_level': 0,
    'action_level': 0,
    'family_friendly': '',
}

# Bind Enter key
entry.bind('<Return>', send_message)

# Run the GUI
root.mainloop()
