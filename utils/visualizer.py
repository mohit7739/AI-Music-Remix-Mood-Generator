import matplotlib.pyplot as plt
import numpy as np
import librosa
import plotly.express as px
import plotly.graph_objects as go

def plot_waveform(y, sr):
    """Plots the audio waveform using matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 3))
    # Provide a dark theme look
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    librosa.display.waveshow(y, sr=sr, ax=ax, color='#1f77b4')
    ax.set(title='Audio Waveform')
    ax.title.set_color('white')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    return fig

def plot_spectrogram(y, sr):
    """Plots the Mel spectrogram."""
    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0e1117')
    
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax, cmap='magma')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel Spectrogram')
    ax.title.set_color('white')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    return fig

def plot_mood_chart(mood_scores):
    """Plots a radar/polar chart for mood scores using Plotly."""
    categories = list(mood_scores.keys())
    values = list(mood_scores.values())
    
    # Close the loop for radar chart
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='#00ffcc'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) + 0.1]
            )),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

def plot_genre_probabilities(genre_scores):
    """Plots a bar chart of genre probabilities."""
    genres = list(genre_scores.keys())
    probs = list(genre_scores.values())
    
    fig = px.bar(x=probs, y=genres, orientation='h', 
                 title="Genre Probabilities",
                 labels={'x': 'Probability', 'y': 'Genre'})
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig
