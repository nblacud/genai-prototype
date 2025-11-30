import os
#from google import genai
from google.genai import types
from dotenv import load_dotenv # Only needed if using the .env file method
import streamlit as st
import re
import pandas as pd

# da la respuesta anterior si es que ya se hizo la misma consulta
# ayuda a la rapidez y que no se gasten muchos tokens. 
@st.cache_data 
def get_response(user_prompt, temperature):
     response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature, # lower = more deterministic, higher = more creative
                #max_output_tokens=1000, # optional, just an example
            ),)
     return response
 
# Helper function to clean text
def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Helper function to get dataset path
def get_dataset_path():
    
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return csv_path

# If using the .env file method, load the variables
load_dotenv() 

try:
    # The client will automatically use the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    st.title("HOLA GENAI")
    st.write("Esta es la primera app que hago de ai")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Ingest Dataset"): # The if runs only if the button is clicked
            try:
                csv_path = get_dataset_path()
                st.session_state["df"] = pd.read_csv(csv_path)
    # Stores the DataFrame in Streamlit's session state under the key "df"
    #st.session_state is a dictionary-like object that persists data across reruns
    # Without session state, the DataFrame would be lost on each rerun
                st.success("Los datos se cargaron exitosamente")
            except:
                st.error("Los datos no se encontraron. Revisa el path del archivo")
    
    with col2:
        if st.button("🧹 Parse Reviews"):
            if "df" in st.session_state: #Si se ha cargado
                st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
                st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")
        
    # Display the dataset if it exists
    if "df" in st.session_state:
        # Product filter dropdown
        st.subheader("🔍 Filter by Product")
        product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
        st.subheader(f"📁 Reviews for {product}")

        if product != "All Products":
            filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
        else:
            filtered_df = st.session_state["df"]
        st.dataframe(filtered_df)    
        
        st.subheader("Análisis de sentimiento por puntaje")
        agrupado = st.session_state["df"].groupby(["PRODUCT"])["SENTIMENT_SCORE"].mean()
        st.bar_chart(agrupado) 
    
    
    # Un text box para ingresar el prompt
    user_prompt = st.text_input("Ingresa tu consulta", "Explica una roca sedimentaria en una oracion")
    
    #Add a slider rule
    temperature = st.slider("Temperatura del Modelo",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01,
        help="Controla la Aletoreidad: 0 = deterministico, 1=muy creativo")
    
    # Simple model query
    #with st.spinner("la IA esta trabajando"):
     #   response = get_response(user_prompt,temperature)
    
        #respuesta del modelo
      #  st.write(response.text)
    

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check if your API key is correct and the environment variable is set.")