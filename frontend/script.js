const imageInput = document.getElementById("plantImage");
const analyzeBtn = document.getElementById("analyzeBtn");

const previewContainer = document.getElementById("previewContainer");
const plantName = document.getElementById("plantName");
const diseaseName = document.getElementById("diseaseName");
const confidence = document.getElementById("confidence");

const cause = document.getElementById("cause");
const solution = document.getElementById("solution");
const recovery = document.getElementById("recovery");

let currentLanguage = "en";
let lastResult = null;


// ================= LANGUAGE TEXT =================

const translations = {
    en: {
        home: "Home",
        analysis: "Plant Analysis",
        about: "About",
        heroTitle: "Protect Your Crops with AI",
        heroText: "Detect plant diseases early and get smart solutions for healthier crops.",
        uploadTitle: "Upload Plant Image",
        uploadText: "Upload a clear image of your crop leaf",
        analyze: "🔍 Analyze Plant",
        resultTitle: "Plant Analysis",
        preview: "Image preview will appear here",
        confidence: "Confidence",
        problem: "Problem & Solution",
        causeTitle: "🔍 Why did this happen?",
        solutionTitle: "💡 What should you do?",
        recoveryTitle: "🌱 Recovery",
        audioTitle: "🔊 Audio Analysis",
        audioText: "Listen to the disease information and solution.",
        playAudio: "🔊 Play Audio",
        analyzing: "Analyzing...",
        noImage: "Please upload a plant image first.",
        noResult: "No result",
        unavailable: "Information not available.",
        aboutTitle: "About Fasal Rakshak",
        aboutText:
            "Fasal Rakshak is an AI-powered crop disease detection system that helps farmers identify plant diseases and get useful solutions."
    },

    hi: {
        home: "होम",
        analysis: "पौधे का विश्लेषण",
        about: "हमारे बारे में",
        heroTitle: "AI के साथ अपनी फसलों की रक्षा करें",
        heroText: "पौधों की बीमारी का जल्दी पता लगाएं और स्वस्थ फसलों के लिए स्मार्ट समाधान पाएं।",
        uploadTitle: "पौधे की तस्वीर अपलोड करें",
        uploadText: "अपने फसल के पत्ते की साफ तस्वीर अपलोड करें",
        analyze: "🔍 पौधे का विश्लेषण करें",
        resultTitle: "पौधे का विश्लेषण",
        preview: "तस्वीर का प्रीव्यू यहां दिखाई देगा",
        confidence: "विश्वास स्तर",
        problem: "समस्या और समाधान",
        causeTitle: "🔍 यह क्यों हुआ?",
        solutionTitle: "💡 आपको क्या करना चाहिए?",
        recoveryTitle: "🌱 रिकवरी",
        audioTitle: "🔊 ऑडियो विश्लेषण",
        audioText: "बीमारी की जानकारी और समाधान सुनें।",
        playAudio: "🔊 ऑडियो चलाएं",
        analyzing: "विश्लेषण हो रहा है...",
        noImage: "कृपया पहले पौधे की तस्वीर अपलोड करें।",
        noResult: "कोई परिणाम नहीं",
        unavailable: "जानकारी उपलब्ध नहीं है।",
        aboutTitle: "फसल रक्षक के बारे में",
        aboutText:
            "फसल रक्षक एक AI आधारित फसल रोग पहचान प्रणाली है जो किसानों को पौधों की बीमारी पहचानने और उपयोगी समाधान प्राप्त करने में मदद करती है।"
    }
};


// ================= CREATE ABOUT SECTION =================

if (!document.getElementById("about")) {

    const aboutSection = document.createElement("section");

    aboutSection.id = "about";
    aboutSection.className = "card";
    aboutSection.style.marginTop = "25px";
    aboutSection.style.textAlign = "center";

    aboutSection.innerHTML = `
        <h2 id="aboutTitle"></h2>
        <p id="aboutText" style="line-height:1.7;"></p>
    `;

    document.querySelector("main").appendChild(aboutSection);
}


// ================= CREATE AUDIO BUTTON =================

const audioSection = document.querySelector(".audio-section");

let audioButton = document.getElementById("playAudioBtn");

if (!audioButton && audioSection) {

    audioButton = document.createElement("button");

    audioButton.id = "playAudioBtn";
    audioButton.style.marginTop = "10px";
    audioButton.style.padding = "12px 20px";
    audioButton.style.border = "none";
    audioButton.style.borderRadius = "10px";
    audioButton.style.cursor = "pointer";
    audioButton.style.background = "#25834a";
    audioButton.style.color = "white";
    audioButton.style.fontSize = "15px";

    audioSection.appendChild(audioButton);
}


// ================= LANGUAGE BUTTONS =================

const languageButton = document.querySelector(".language-btn");

if (languageButton) {

    languageButton.innerHTML = `
        <span id="englishBtn" style="cursor:pointer;">English</span>
        <span> | </span>
        <span id="hindiBtn" style="cursor:pointer;">हिंदी</span>
    `;

    document.getElementById("englishBtn").addEventListener("click", () => {
        setLanguage("en");
    });

    document.getElementById("hindiBtn").addEventListener("click", () => {
        setLanguage("hi");
    });
}


// ================= NAVIGATION =================

const navLinks = document.querySelectorAll(".navbar nav a");

if (navLinks.length >= 3) {

    navLinks[0].addEventListener("click", function (e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });

    navLinks[1].addEventListener("click", function (e) {
        e.preventDefault();

        document.querySelector(".dashboard").scrollIntoView({
            behavior: "smooth"
        });
    });

    navLinks[2].addEventListener("click", function (e) {
        e.preventDefault();

        document.getElementById("about").scrollIntoView({
            behavior: "smooth"
        });
    });
}


// ================= SET LANGUAGE =================

function setLanguage(language) {

    currentLanguage = language;

    const t = translations[language];

    const nav = document.querySelectorAll(".navbar nav a");

    if (nav.length >= 3) {
        nav[0].innerText = t.home;
        nav[1].innerText = t.analysis;
        nav[2].innerText = t.about;
    }

    document.querySelector(".hero h1").innerText = t.heroTitle;
    document.querySelector(".hero p").innerText = t.heroText;

    document.querySelector(".upload-card h2").innerText = t.uploadTitle;
    document.querySelector(".upload-box p").innerText = t.uploadText;

    document.querySelector(".result-card h2").innerText = t.resultTitle;

    document.querySelector(".solution-card h2").innerText = t.problem;

    const solutionHeadings =
        document.querySelectorAll(".solution-card h3");

    if (solutionHeadings.length >= 3) {
        solutionHeadings[0].innerText = t.causeTitle;
        solutionHeadings[1].innerText = t.solutionTitle;
        solutionHeadings[2].innerText = t.recoveryTitle;
    }

    document.querySelector(".audio-section h2").innerText = t.audioTitle;
    document.querySelector(".audio-section p").innerText = t.audioText;

    if (audioButton) {
        audioButton.innerText = t.playAudio;
    }

    document.getElementById("aboutTitle").innerText = t.aboutTitle;
    document.getElementById("aboutText").innerText = t.aboutText;

    const previewText = previewContainer.querySelector("span");

    if (previewText) {
        previewText.innerText = t.preview;
    }

    const confidenceLabel =
        document.querySelector(".confidence span");

    if (confidenceLabel) {
        confidenceLabel.innerText = t.confidence;
    }

    if (!lastResult) {
        diseaseName.innerText = t.noResult;
        cause.innerText = t.unavailable;
        solution.innerText = t.unavailable;
        recovery.innerText = t.unavailable;
    }

    analyzeBtn.innerText = t.analyze;
}


// ================= IMAGE PREVIEW =================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) return;

    const imageURL = URL.createObjectURL(file);

    previewContainer.innerHTML = `
        <img src="${imageURL}" 
             alt="Plant Image"
             style="width:100%; height:100%; object-fit:cover; border-radius:15px;">
    `;
});


// ================= ANALYZE =================

analyzeBtn.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        alert(translations[currentLanguage].noImage);
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerText = translations[currentLanguage].analyzing;

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || "Prediction failed");
        }

        lastResult = data;

        plantName.innerText =
            data.plant || data.plant_name || "Plant";

        diseaseName.innerText =
            data.disease || data.prediction ||
            translations[currentLanguage].noResult;

        confidence.innerText =
            data.confidence !== undefined
                ? data.confidence + "%"
                : "N/A";

        cause.innerText =
            data.cause ||
            translations[currentLanguage].unavailable;

        solution.innerText =
            data.solution ||
            data.treatment ||
            translations[currentLanguage].unavailable;

        recovery.innerText =
            data.recovery ||
            data.recommendation ||
            translations[currentLanguage].unavailable;

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect with the backend. Please start the Flask server."
        );

    }

    finally {

        analyzeBtn.disabled = false;
        analyzeBtn.innerText =
            translations[currentLanguage].analyze;
    }
});


// ================= AUDIO =================

if (audioButton) {

    audioButton.addEventListener("click", function () {

        if (!lastResult) {
            alert(
                currentLanguage === "hi"
                    ? "पहले पौधे की तस्वीर का विश्लेषण करें।"
                    : "Please analyze a plant image first."
            );
            return;
        }

        window.speechSynthesis.cancel();

        const t = translations[currentLanguage];

        let text = "";

        if (currentLanguage === "hi") {

            text =
                `पौधा ${lastResult.plant || "पौधा"} है। ` +
                `बीमारी ${lastResult.disease || "उपलब्ध नहीं"} है। ` +
                `विश्वास स्तर ${lastResult.confidence || 0} प्रतिशत है। ` +
                `कारण: ${lastResult.cause || "जानकारी उपलब्ध नहीं है"}। ` +
                `समाधान: ${lastResult.solution || "जानकारी उपलब्ध नहीं है"}। ` +
                `रिकवरी: ${lastResult.recovery || "जानकारी उपलब्ध नहीं है"}।`;

        } else {

            text =
                `The plant is ${lastResult.plant || "unknown"}. ` +
                `The detected disease is ${lastResult.disease || "not available"}. ` +
                `The confidence is ${lastResult.confidence || 0} percent. ` +
                `Cause: ${lastResult.cause || "Information not available"}. ` +
                `Solution: ${lastResult.solution || "Information not available"}. ` +
                `Recovery: ${lastResult.recovery || "Information not available"}.`;
        }

        const speech = new SpeechSynthesisUtterance(text);

        speech.lang =
            currentLanguage === "hi"
                ? "hi-IN"
                : "en-IN";

        speech.rate = 0.9;

        window.speechSynthesis.speak(speech);
    });
}


// ================= START IN ENGLISH =================

setLanguage("en");