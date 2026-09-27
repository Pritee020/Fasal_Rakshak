import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
from gtts import gTTS
import io

# Page setup
st.set_page_config(page_title="FasalRakshak", page_icon="🌾")
st.title("🌾 FasalRakshak - Crop Disease Detector")
st.write("Apne crop ki leaf ki photo upload karo, hum disease detect karenge.")

# Load model and class names (cached so it loads only once)
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('crop_disease_model.h5')
    with open('class_names.json', 'r') as f:
        class_names = json.load(f)
    return model, class_names

model, class_names = load_model()

# Simple disease-solution database

solutions = {
    "Apple___Apple_scab": {
        "cause": "Fungal disease (Venturia inaequalis) jo thandi, gili spring weather mein failta hai. Sankramit patte zameen par gire rehte hain aur agle saal bhi infection failate hain.",
        "solution": "Neem oil ya Mancozeb spray karein 7-10 din ke antaral par. Girhi hui patti hata dein aur jala dein.",
        "recovery_chance": "70-80% (agar early treatment ho)"
    },
    "Apple___Black_rot": {
        "cause": "Fungal disease jo purani, kamzor lakdi ya ghaav se paudhe mein pravesh karta hai. Garmi aur namी ismein madad karti hai.",
        "solution": "Sankramit shakhaon ko kaat kar hata dein. Copper-based fungicide spray karein.",
        "recovery_chance": "60-70%"
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Yeh fungus do mezban paudhon (apple aur cedar tree) ke beech cycle complete karta hai. Cedar tree paas hone se infection zyada hota hai.",
        "solution": "Fungicide (Myclobutanil) spray karein bud break se pehle. Aas-paas ke cedar trees hatayein agar sambhav ho.",
        "recovery_chance": "65-75%"
    },
    "Apple___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein - paani, dhoop aur nutrients sahi matra mein dein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Blueberry___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "cause": "Fungal disease jo garmi aur sookhi jalvayu mein, khaaskar dense planting me tezi se failta hai.",
        "solution": "Sulfur ya Potassium bicarbonate spray karein. Paudhon ke beech hawa aane ki jagah rakhein.",
        "recovery_chance": "70-80%"
    },
    "Cherry_(including_sour)___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungal disease jo garam, gili jalvayu mein failta hai. Ek hi khet mein baar-baar corn lagane se badhta hai.",
        "solution": "Fungicide (Azoxystrobin) spray karein. Fasal chakra apnayein (crop rotation).",
        "recovery_chance": "55-65%"
    },
    "Corn_(maize)___Common_rust_": {
        "cause": "Fungal spores hawa se failte hain, thandi raat aur gili subah mein zyada hota hai.",
        "solution": "Rust-resistant beej istemal karein. Fungicide spray karein agar zyada phaila ho.",
        "recovery_chance": "65-75%"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "cause": "Yeh fungal disease (Exserohilum turcicum) namी aur thandi jalvayu mein tezi se failta hai. Zyada barish ya paani jamaav, kam hawa ka aana-jana, aur sankramit beej iske mukhya kaaran hain.",
        "solution": "Fungicide (Propiconazole) spray karein. Sankramit patton ko hata kar jala dein. Agli baar resistant variety lagayein.",
        "recovery_chance": "70-80% (agar jaldi ilaj shuru ho)"
    },
    "Corn_(maize)___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Grape___Black_rot": {
        "cause": "Fungal disease jo garam, gili jalvayu mein failta hai. Purane sankramit patte agle saal bhi infection ka source bante hain.",
        "solution": "Sankramit patte aur phal hata dein. Mancozeb ya Myclobutanil spray karein.",
        "recovery_chance": "60-70%"
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal disease jo purani lakdi ke ghaav se pravesh karta hai. Iska ilaj mushkil hai kyunki fungus lakdi ke andar rehta hai.",
        "solution": "Sankramit lakdi ko kaat kar hata dein. Ghaav par fungicide paste lagayein.",
        "recovery_chance": "40-50%"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungal disease jo gili, garam jalvayu mein failta hai, khaaskar jab patton ke beech hawa nahi aati.",
        "solution": "Copper-based fungicide spray karein. Patton ke beech hawa ka aana-jana sunishchit karein.",
        "recovery_chance": "65-75%"
    },
    "Grape___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Yeh bacterial disease Asian citrus psyllid naamak keede se failta hai. Iska koi ilaj nahi hai.",
        "solution": "Sankramit ped ko turant hata dein - iska ilaj nahi hai. Psyllid keede ko niyantrit karein taaki phailav rukey.",
        "recovery_chance": "5-10% (bahut kam, ped hatana hi behtar hai)"
    },
    "Peach___Bacterial_spot": {
        "cause": "Bacterial disease jo gili, garam jalvayu mein failta hai. Barish ke chheenten iss bacteria ko ek patti se doosri patti tak le jaati hain.",
        "solution": "Copper-based spray karein sardi ke mausam mein. Resistant variety lagayein agla baar.",
        "recovery_chance": "60-70%"
    },
    "Peach___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterial disease jo sankramit beej ya paani ke chheenton se failta hai. Upar se paani dene se badhta hai.",
        "solution": "Copper spray karein. Pani upar se na dein, jadd mein dein. Sankramit beej na istemal karein.",
        "recovery_chance": "55-65%"
    },
    "Pepper,_bell___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Potato___Early_blight": {
        "cause": "Fungal disease (Alternaria solani) jo purane, neeche ki pattiyon se shuru hokar upar failta hai. Zyada namी, kam nutrients, aur paudhe ka stress isse badhata hai.",
        "solution": "Chlorothalonil ya Mancozeb fungicide spray karein. Fasal chakra apnayein, 2-3 saal tak potato na lagayein usi jagah.",
        "recovery_chance": "75-85% (agar early stage mein pakda jaye)"
    },
    "Potato___Late_blight": {
        "cause": "Yeh fungal disease (Phytophthora infestans) thandi, gili jalvayu mein bahut tezi se failta hai - khaaskar barsaat ke mausam mein. Sankramit beej aalu ya hawa ke through failta hai.",
        "solution": "Turant Metalaxyl ya Mancozeb spray karein - yeh tezi se failta hai. Sankramit paudhe ukhaad kar jala dein.",
        "recovery_chance": "40-50% (agar turant control na kiya jaye to poori fasal barbaad ho sakti hai)"
    },
    "Potato___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Raspberry___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Soybean___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Squash___Powdery_mildew": {
        "cause": "Fungal disease jo garam, sookhi din aur namІ raat wale jalvayu mein tezi se failta hai. Dense planting bhi iski wajah hai.",
        "solution": "Sulfur spray karein. Neem oil bhi effective hai. Paudhon ke beech achhi doori rakhein.",
        "recovery_chance": "70-80%"
    },
    "Strawberry___Leaf_scorch": {
        "cause": "Fungal disease jo gili jalvayu mein failta hai, khaaskar jab patte lambe samay tak gile rehte hain.",
        "solution": "Sankramit patte hata dein. Captan ya Myclobutanil fungicide spray karein.",
        "recovery_chance": "65-75%"
    },
    "Strawberry___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacterial disease jo gili jalvayu aur upar se paani dene se failta hai. Sankramit beej bhi iska source ho sakte hain.",
        "solution": "Copper-based spray karein. Upar se pani na dein. Sankramit paudhe hata dein.",
        "recovery_chance": "55-65%"
    },
    "Tomato___Early_blight": {
        "cause": "Fungal disease jo purane, neeche ki pattiyon se shuru hota hai. Zyada namІ aur paudhe ka stress ismein madad karta hai.",
        "solution": "Chlorothalonil ya Mancozeb spray karein har 7-10 din mein. Neeche ki sookhi patti hata dein.",
        "recovery_chance": "75-85% (agar early stage mein pakda jaye)"
    },
    "Tomato___Late_blight": {
        "cause": "Bahut tezi se failne wala fungal disease, thandi-gili jalvayu mein khaaskar khatarnak. Poori fasal chand dino mein barbaad ho sakti hai.",
        "solution": "Turant fungicide (Metalaxyl) spray karein - yeh bahut tezi se failta hai. Sankramit paudhe turant hata dein.",
        "recovery_chance": "35-45% (bahut tezi se failta hai)"
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungal disease jo greenhouse ya kam hawa wali jagah mein zyada namІ ki wajah se failta hai.",
        "solution": "Greenhouse mein hawa ka aana-jana badhayein. Chlorothalonil spray karein.",
        "recovery_chance": "70-80%"
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungal disease jo neeche ki purani pattiyon se shuru hokar upar failta hai, gili jalvayu mein tezi se badhta hai.",
        "solution": "Sankramit neeche ki patti hata dein. Chlorothalonil ya Copper spray karein.",
        "recovery_chance": "65-75%"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Yeh keede (mites) garam, sookhe mausam mein tezi se badhte hain. Yeh disease nahi, pest infestation hai.",
        "solution": "Neem oil ya Insecticidal soap spray karein. Paudhon par pani ka chhidkav karein (mites sookhe mausam mein badhte hain).",
        "recovery_chance": "75-85%"
    },
    "Tomato___Target_Spot": {
        "cause": "Fungal disease jo garam, gili jalvayu mein failta hai. Zyada patte hone se hawa kam aati hai jo isse badhata hai.",
        "solution": "Fungicide (Azoxystrobin) spray karein. Sankramit patte hata dein.",
        "recovery_chance": "65-75%"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Yeh viral disease whitefly (safed makkhi) ke through failta hai. Iska koi direct ilaj nahi hai.",
        "solution": "Iska koi ilaj nahi hai - sankramit paudhe ukhaad kar jala dein. Whitefly (safed makkhi) ko niyantrit karein jo isse failati hai.",
        "recovery_chance": "10-15% (bahut kam, prevention hi behtar hai)"
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Yeh virus haathon, tools, ya sankramit beej se failta hai. Ek baar lagne pe iska ilaj nahi hai.",
        "solution": "Iska koi ilaj nahi hai - sankramit paudhe hata dein. Haath dhoke hi paudhon ko chhuein, tools ko bhi saaf rakhein.",
        "recovery_chance": "10-15% (bahut kam, prevention hi behtar hai)"
    },
    "Tomato___healthy": {
        "cause": "Koi disease nahi - paudha swasth hai.",
        "solution": "Niyamit dekhbhal jaari rakhein.",
        "recovery_chance": "100% (already healthy)"
    },
    "default": {
        "cause": "Iska specific kaaran alag-alag ho sakta hai - fungal, bacterial, ya viral infection.",
        "solution": "Iske baare mein zyada jaankari ke liye apne nazdeeki krishi vigyan kendra se sampark karein.",
        "recovery_chance": "Nirdharit nahi - visheshagya se sampark karein"
    }
}
def generate_audio(text):
    tts = gTTS(text=text, lang='hi')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes    


# File uploader
uploaded_file = st.file_uploader("Leaf ki photo upload karo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Preprocess
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    

    disease_info = solutions.get(predicted_class, solutions["default"])

    st.success(f"**Disease Detected:** {predicted_class}")
    st.write(f"**Confidence:** {confidence:.2f}%")

    st.warning(f"**Kyun hua (Cause):** {disease_info['cause']}")
    st.info(f"**Solution:** {disease_info['solution']}")
    st.write(f"**Recovery Chances:** {disease_info['recovery_chance']}")
    full_text = f"Aapke paudhe mein {predicted_class.replace('___', ' ').replace('_', ' ')} disease hai. {disease_info['solution']}"

    if st.button("🔊 Solution Suniye (Awaaz mein)"):
        with st.spinner("Audio taiyar ho raha hai..."):
            audio_data = generate_audio(full_text)
            st.audio(audio_data, format='audio/mp3')