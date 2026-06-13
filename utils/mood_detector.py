import numpy as np

def predict_mood(features):
    """
    Predicts mood based on heuristic analysis of audio features.
    Moods: Happy, Sad, Energetic, Calm, Romantic, Motivational
    """
    tempo = features.get('tempo', 120)
    energy = features.get('energy', 0.1)
    
    # Simple heuristic-based mapping for MVP
    # In a real scenario, a trained scikit-learn model would be loaded and used here.
    
    mood_scores = {
        'Happy': 0.0,
        'Sad': 0.0,
        'Energetic': 0.0,
        'Calm': 0.0,
        'Romantic': 0.0,
        'Motivational': 0.0
    }
    
    # Analyze tempo
    if tempo > 130:
        mood_scores['Energetic'] += 0.4
        mood_scores['Happy'] += 0.2
        mood_scores['Motivational'] += 0.2
    elif tempo < 90:
        mood_scores['Calm'] += 0.4
        mood_scores['Sad'] += 0.3
        mood_scores['Romantic'] += 0.2
    else:
        mood_scores['Happy'] += 0.2
        mood_scores['Romantic'] += 0.1
        mood_scores['Motivational'] += 0.1

    # Analyze energy
    if energy > 0.15:
        mood_scores['Energetic'] += 0.4
        mood_scores['Motivational'] += 0.3
        mood_scores['Happy'] += 0.1
    elif energy < 0.05:
        mood_scores['Calm'] += 0.4
        mood_scores['Sad'] += 0.3
        mood_scores['Romantic'] += 0.2
    
    # Normalize scores to look like probabilities
    total = sum(mood_scores.values())
    if total > 0:
        mood_scores = {k: v / total for k, v in mood_scores.items()}
    else:
        mood_scores = {k: 1/len(mood_scores) for k in mood_scores}
        
    # Get top mood
    top_mood = max(mood_scores, key=mood_scores.get)
    
    return top_mood, mood_scores

def predict_genre(features):
    """
    Predicts genre based on heuristics.
    Genres: Pop, Rock, Classical, EDM, Lo-fi, Hip-Hop
    """
    tempo = features.get('tempo', 120)
    energy = features.get('energy', 0.1)
    
    genre_scores = {
        'Pop': 0.0,
        'Rock': 0.0,
        'Classical': 0.0,
        'EDM': 0.0,
        'Lo-fi': 0.0,
        'Hip-Hop': 0.0
    }
    
    # EDM/Rock are usually high energy
    if energy > 0.15:
        genre_scores['EDM'] += 0.4
        genre_scores['Rock'] += 0.3
        if tempo > 120:
            genre_scores['EDM'] += 0.2
    
    # Classical/Lo-fi are usually lower energy
    elif energy < 0.08:
        genre_scores['Classical'] += 0.4
        genre_scores['Lo-fi'] += 0.4
        if tempo < 90:
            genre_scores['Lo-fi'] += 0.2
            
    # Pop/Hip-hop are usually mid tempo
    if 80 <= tempo <= 120:
        genre_scores['Pop'] += 0.3
        genre_scores['Hip-Hop'] += 0.3

    # Normalize
    total = sum(genre_scores.values())
    if total > 0:
        genre_scores = {k: v / total for k, v in genre_scores.items()}
    else:
        genre_scores = {k: 1/len(genre_scores) for k in genre_scores}
        
    # Sort genres by score
    sorted_genres = dict(sorted(genre_scores.items(), key=lambda item: item[1], reverse=True))
    return sorted_genres
