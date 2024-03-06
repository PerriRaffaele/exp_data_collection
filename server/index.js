const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const fs = require('fs');


const app = express();
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', 'https://exp-data-collection-frontend.vercel.app');
    res.header('Access-Control-Allow-Methods', 'GET, POST');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.header('Access-Control-Allow-Credentials', true);
    next();
});

app.use(express.json());

mongoose.connect('mongodb+srv://raffaeleperri70:8qjAf3IHD4sBSxEi@cluster0.i7s1sfm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

// Mongoose model for answer data
const AnswerData = mongoose.model('AnswerData', {
    user_id: String,
    ex: String,
    age: Number,
    gender: String,
    programming_experience: String,
    programming_language_familiarity: String,
    lines_of_code: Number,
    pytamaro: String,
    timeTaken: Number
});

// Mongoose model for feedback data
const FeedbackData = mongoose.model('FeedbackData', {
    user_id: String,
    feedback: String
});

// Multer storage configuration
const storage = multer.diskStorage({
    destination: 'uploads',
    filename: (req, file, cb) => {
        const user_id = req.body.userId;
        const filename = `${user_id}_${file.originalname}`;
        cb(null, filename);
    }
});

// Multer upload configuration
const upload = multer({ storage: storage });

// Route for getting exercises
app.get('/exercises', (req, res) => {
    const user_id = Math.random().toString(36).substring(7);

    const exercise_links_list = [
        "https://pytamaro.si.usi.ch/activities/luce/color-flower/de/v2",
        "https://pytamaro.si.usi.ch/activities/luce/four-petal-flower/en/v3",
        "https://pytamaro.si.usi.ch/activities/luce/swiss-flag/en/v2"
    ];

    const response_data = {
        'user_id': user_id,
        'exercises': exercise_links_list
    };
    res.json(response_data);
});

// Route for uploading a file
app.post('/upload-file', upload.single('file'), (req, res) => {
    try {
        const user_id = req.body.userId;

        if (!req.file || !user_id) {
            return res.json({ "error": "Invalid request. Missing file or user ID." });
        }

        return res.json({ "message": "File uploaded successfully" });
    } catch (error) {
        console.error(error);
        return res.json({ "error": "Internal Server Error" });
    }
});

// Route for submitting and exporting answer data
app.post('/submit-and-export', async (req, res) => {
    try {
        const answer_data = req.body;
        await AnswerData.create(answer_data);
        return res.json({ "message": "Answer data submitted successfully" });
    } catch (error) {
        console.error(error);
        return res.json({ "error": "Internal Server Error" });
    }
});

// Route for submitting feedback
app.post('/submit-feedback', async (req, res) => {
    try {
        const feedback_data = req.body;
        await FeedbackData.create(feedback_data);
        return res.json({ "message": "Feedback submitted successfully" });
    } catch (error) {
        console.error(error);
        return res.json({ "error": "Internal Server Error" });
    }
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});