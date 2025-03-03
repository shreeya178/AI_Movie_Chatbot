# AI_Movie_Chatbot
# AI Movie Recommendation Chatbot

This is an AI-powered chatbot built using Python and Tkinter. The chatbot helps users discover Bollywood movies based on their preferences, such as genre, romance and action levels, and family-friendliness. It also provides movie details and a YouTube link to watch trailers.

## Features

- **Interactive Chat**: Engages the user in a conversation to understand their movie preferences.
- **Personalized Recommendations**: Suggests movies based on user inputs like genre, action/romance levels, and family-friendliness.
- **Movie Details**: Provides a description and a clickable YouTube link for each recommended movie.
- **Responsive UI**: Built using Tkinter, the GUI offers a clean and interactive design.

## Technologies Used

- **Python 3.x**
- **Tkinter**: For the graphical user interface.
- **Pandas**: For managing and filtering movie data.
- **Pillow (PIL)**: For handling images.

## How to Use

1. **Launch the Application**:
   - Run `chatbot.py` using Python.
   - The welcome screen will appear with a "Get Started" button.

2. **Enter Preferences**:
   - The chatbot will ask for your preferred movie genre.
   - Specify action/romance levels on a scale of 1 to 5.
   - Indicate whether you want family-friendly movies.

3. **View Recommendations**:
   - The chatbot will display movies matching your preferences.
   - Click on a movie image for detailed information and a YouTube trailer link.

4. **Exit the Chat**:
   - Type `exit` or `quit` in the input field to close the application. A farewell message will appear before the application exits.

## Project Structure

- `chatbot.py`: The main Python script for the chatbot.
- `images/`: Contains images for movies and the welcome screen.
- `movie_data.xlsx`: An Excel file with movie data used for filtering recommendations.

## Movie Data

The application uses an internal dataset with the following fields:
- Movie name
- Genre
- Romance and action levels (1-5 scale)
- Family-friendly indicator (yes/no)
- Path to the movie image

## Prerequisites

1. Install Python 3.x.
2. Install the required libraries:
   ```bash
   pip install pandas pillow

