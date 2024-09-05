const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// MongoDB connection string
const mongoURI = "mongodb+srv://petwhiz8:VNs3DXlFys93zAzE@cluster1.tdxh1k7.mongodb.net/?retryWrites=true&w=majority";

// Connect to MongoDB
mongoose.connect(mongoURI)
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Could not connect to MongoDB', err));

// Define a schema for the user collection
const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String
});

// Create a model based on the schema
const User = mongoose.model('User', userSchema, 'usersdata');

// Middleware to parse JSON request bodies
app.use(bodyParser.json());

// Enable CORS for all origins
app.use(cors());


// Route to handle user registration
app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;

    try {
        // Check if the email is already registered
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ error: 'Email is already registered' });
        }

        // Create a new user instance
        const newUser = new User({
            username,
            email,
            password
        });

        // Save the user to the database
        await newUser.save();

        // Retrieve the user from the database to ensure all fields are included
        const registeredUser = await User.findById(newUser._id);

        res.status(201).json({ message: 'User registered successfully', user: registeredUser });
    } catch (error) {
        console.error('Error registering user:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Route to handle user login
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        // Find the user by username
        const user = await User.findOne({ username });
        if (!user) {
            return res.status(401).json({ error: 'Invalid username or password' });
        }

        // Check if the password matches
        if (user.password !== password) {
            return res.status(401).json({ error: 'Invalid username or password' });
        }

        // Successfully logged in
        res.status(200).json({ message: 'Login successful' });
    } catch (error) {
        console.error('Error logging in user:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});


// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
