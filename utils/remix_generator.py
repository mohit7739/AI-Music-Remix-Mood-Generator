def generate_remix_ideas(genre_choice, base_tempo):
    """
    Generates remix ideas based on selected genre and original tempo.
    """
    remixes = {
        "EDM Remix": {
            "description": "A high-energy electronic dance music track suitable for clubs and festivals.",
            "tempo_recommendation": f"{max(128, base_tempo + 10)} BPM",
            "instruments": ["Synthesizer", "Drum Machine (909)", "Sub Bass", "Vocal Chops"],
            "beat_pattern": "Four-on-the-floor kick, claps on 2 and 4, syncopated hi-hats.",
            "production_notes": "Use sidechain compression on the bass and synths triggered by the kick drum. Add risers and drops for impact."
        },
        "Lo-fi Remix": {
            "description": "A relaxed, nostalgic, and chilled-out beat ideal for studying or relaxing.",
            "tempo_recommendation": f"{min(85, base_tempo - 15)} BPM",
            "instruments": ["Electric Piano (Rhodes)", "Vinyl Crackle", "Sampled Upright Bass", "Muted Drums"],
            "beat_pattern": "Dilla-style swing, off-grid hi-hats, soft kick and rimshot.",
            "production_notes": "Apply tape saturation, EQ out the high frequencies, and use subtle bitcrushing to achieve a vintage sound."
        },
        "Chill Remix": {
            "description": "Atmospheric, smooth, and spacious music with emotional undertones.",
            "tempo_recommendation": f"{min(100, base_tempo - 5)} BPM",
            "instruments": ["Pads", "Acoustic Guitar", "Reese Bass", "Foley Percussion"],
            "beat_pattern": "Spacious, half-time feel with organic percussion hits.",
            "production_notes": "Use long, lush reverbs (Valhalla-style) and wide stereo imaging for the pads."
        },
        "Rock Remix": {
            "description": "A driving, guitar-heavy track with a live band feel.",
            "tempo_recommendation": f"{base_tempo + 5} BPM",
            "instruments": ["Overdriven Electric Guitar", "Live Drum Kit", "Electric Bass", "Hammond Organ"],
            "beat_pattern": "Driving 8th notes, heavy crash on the 1, syncopated snare fills.",
            "production_notes": "Layer multiple guitar takes panned hard left and right. Compress the drum bus heavily for punch."
        },
        "Classical Remix": {
            "description": "An orchestral arrangement bringing grandeur and emotion.",
            "tempo_recommendation": f"{base_tempo} BPM",
            "instruments": ["String Section (Violins, Cellos)", "Grand Piano", "Timpani", "French Horns"],
            "beat_pattern": "Flowing, expressive timing (rubato) rather than strict grid.",
            "production_notes": "Focus on dynamics (pianissimo to fortissimo). Use convolution reverb to simulate a concert hall."
        },
        "Synthwave Remix": {
            "description": "An 80s-inspired electronic track with neon aesthetics.",
            "tempo_recommendation": f"{max(110, base_tempo)} BPM",
            "instruments": ["Analog Synths (Juno/Jupiter)", "LinnDrum", "Synth Bass (Rolling 16ths)", "Arpeggiator"],
            "beat_pattern": "Straight 4/4 with strong backbeat snare and continuous 16th note bass.",
            "production_notes": "Use chorus effects on synths, gated reverb on the snare drum."
        }
    }
    return remixes.get(genre_choice, remixes["EDM Remix"])

def generate_ai_prompt(genre_choice, mood, base_tempo):
    """
    Generates detailed prompts for AI music generators.
    """
    remix_data = generate_remix_ideas(genre_choice, base_tempo)
    instruments_str = ", ".join(remix_data["instruments"])
    
    prompt = f"Create a {mood.lower()}, {genre_choice.lower()} track at {remix_data['tempo_recommendation']}. "
    prompt += f"Feature {instruments_str}. "
    prompt += f"The beat should have {remix_data['beat_pattern'].lower()} "
    prompt += f"Atmosphere/Production: {remix_data['production_notes']} "
    
    return prompt
