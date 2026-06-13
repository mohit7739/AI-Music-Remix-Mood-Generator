# AI Music Remix & Mood Generator

A Streamlit-based web application that allows users to upload music, detect its mood and genre, visualize audio features, generate remix ideas with AI prompts, apply basic audio effects, and consult an AI music production assistant.

## Features
- **Music Upload:** Support for MP3 and WAV files.
- **AI Mood & Genre Detection:** Analyzes tempo, energy, and other audio features to predict the mood and genre.
- **Visual Analytics:** Interactive Waveforms, Mel Spectrograms, Mood Radar charts, and Genre Probabilities.
- **Remix & AI Prompt Generator:** Suggests instruments, beat patterns, production notes, and generates detailed prompts for tools like Suno AI and MusicGen.
- **Audio Effects:** Apply simple effects like Speed Up, Slow Down, and Bass Boost directly in the browser.
- **AI Assistant:** Chat with an AI music producer for tips and guidance (Requires Hugging Face API key).

## Screenshots
*(Add screenshots here)*
- [Dashboard Screenshot](#)
- [Remix Generator Screenshot](#)

## Installation

### Prerequisites
- Python 3.8+
- `ffmpeg` (Required by `pydub` for audio processing)
  - **Mac:** `brew install ffmpeg`
  - **Ubuntu:** `sudo apt install ffmpeg`
  - **Windows:** Download from the [official site](https://ffmpeg.org/download.html) and add to PATH.

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI-Music-Generator
   ```

2. Create a virtual environment (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Deployment
This app is ready to be deployed on **Streamlit Community Cloud**.
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in.
3. Click "New App", select your repository, branch, and set the Main file path to `app.py`.
4. Add your Hugging Face API key in the Streamlit Secrets (optional, for the chatbot feature to work without manual input).
5. Click "Deploy".

## Data
A sample `sample.wav` file is included in the `data/` folder for testing.

## Technologies Used
- Streamlit
- Librosa
- Pydub
- Plotly & Matplotlib
- Hugging Face Inference API
