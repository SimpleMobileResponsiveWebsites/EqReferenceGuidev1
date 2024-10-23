import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Magic Frequencies - EQ Reference", layout="wide")
    
    st.title("🎵 Magic Frequencies - EQ Reference Guide")
    st.write("An interactive guide for finding the sweet spots in audio equalization")

    # Create the data
    data = {
        "Instrument": [
            "Bass guitar", "Kick drum", "Snare", "Toms", "Floor tom",
            "Hi-hat and cymbals", "Electric guitar", "Acoustic guitar",
            "Organ", "Piano", "Horns", "Voice", "Strings", "Conga"
        ],
        "Magic Frequencies": [
            "Bottom at 50 to 80Hz, attack at 700Hz, snap at 2.5kHz",
            "Bottom at 80 to 100Hz, hollowness at 400Hz, point at 3 to 5kHz",
            "Fatness at 120 to 240Hz, point at 900Hz, crispness at 5kHz, snap at 10kHz",
            "Fullness at 240 to 500Hz, attack at 5 to 7kHz",
            "Fullness at 80Hz, attack at 5kHz",
            "Clang at 200Hz, sparkle at 8 to 10kHz",
            "Fullness at 240 to 500Hz, presence at 1.5 to 2.5kHz, attenuate at 1kHz for 4x12 cabinet sound",
            "Fullness at 80Hz, body at 240Hz, presence at 2 to 5kHz",
            "Fullness at 80Hz, body at 240Hz, presence at 2 to 5kHz",
            "Fullness at 80Hz, presence at 3 to 5kHz, honky-tonk at 2.5kHz",
            "Fullness at 120Hz, piercing at 5kHz",
            "Fullness at 120Hz, boomy at 240Hz, presence at 5kHz, sibilance at 4 to 7kHz, air at 10 to 15kHz",
            "Fullness at 240Hz, scratchy at 7 to 10kHz",
            "Ring at 200Hz, slap at 5kHz"
        ]
    }
    
    df = pd.DataFrame(data)

    # Create instrument filter
    instrument_types = {
        "Percussion": ["Kick drum", "Snare", "Toms", "Floor tom", "Hi-hat and cymbals", "Conga"],
        "String": ["Bass guitar", "Electric guitar", "Acoustic guitar", "Piano", "Strings"],
        "Wind": ["Horns"],
        "Voice": ["Voice"],
        "Other": ["Organ"]
    }

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_type = st.sidebar.selectbox(
        "Instrument Type",
        ["All"] + list(instrument_types.keys())
    )

    # Filter the dataframe based on selection
    if selected_type != "All":
        filtered_instruments = instrument_types[selected_type]
        df = df[df["Instrument"].isin(filtered_instruments)]

    # Frequency range slider for additional filtering
    st.sidebar.header("Frequency Range")
    freq_range = st.sidebar.slider(
        "Filter by frequency (Hz)",
        min_value=0,
        max_value=15000,
        value=(0, 15000),
        step=100
    )

    # Function to check if a frequency description contains frequencies in the selected range
    def contains_frequency_in_range(freq_desc, range_min, range_max):
        freq_numbers = [int(n) for n in ''.join(c if c.isdigit() or c.isspace() else ' ' for c in freq_desc).split()]
        return any(range_min <= f <= range_max for f in freq_numbers)

    # Apply frequency range filter
    df = df[df["Magic Frequencies"].apply(
        lambda x: contains_frequency_in_range(x, freq_range[0], freq_range[1])
    )]

    # Display the main content
    st.subheader("EQ Reference Chart")
    
    # Create columns for each instrument
    for idx, row in df.iterrows():
        with st.expander(f"🎵 {row['Instrument']}", expanded=True):
            frequencies = row["Magic Frequencies"].split(", ")
            
            # Create a more visual representation of frequencies
            for freq in frequencies:
                if "Hz" in freq:
                    st.write(f"• {freq}")
                    
                    # Extract the frequency value for visualization
                    try:
                        freq_val = int(''.join(filter(str.isdigit, freq.split()[0])))
                        if freq_val <= 15000:  # Only show visualization for frequencies in human hearing range
                            progress_val = freq_val / 15000  # Normalize to 0-1 range
                            st.progress(progress_val)
                    except ValueError:
                        pass

    # Add helpful tips at the bottom
    st.markdown("---")
    st.markdown("""
    ### Tips for Using This Guide
    - These frequencies are approximate and may need adjustment based on:
        - The specific instrument
        - The player's style
        - The recording environment
        - The overall mix context
    - Use your ears as the final judge
    - Make subtle adjustments rather than dramatic ones
    """)

if __name__ == "__main__":
    main()
