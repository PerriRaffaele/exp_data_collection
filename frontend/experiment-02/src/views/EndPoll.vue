<template>
  <div id="container">
    <h1>End of Poll</h1>
    <p>Thank you for participating in the experiments!</p>

    <form @submit.prevent="submitFeedback">
      <label for="feedback">Your Feedback:</label>
      <textarea v-model="feedback" id="feedback" rows="4" cols="50" required></textarea>

      <button type="submit">Submit Feedback</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import config from './config';
export default {
  data() {
    return {
      feedback: "",
    };
  },
  methods: {
    async submitFeedback() {
      try {
        const feedbackData = {
          user_id: this.participantData.user_id,
          feedback: this.feedback,
        };
        console.log('Submitting feedback:', feedbackData);
        const response = await axios.post(`${config.production_backend}/submit-feedback`, feedbackData);
        console.log('Feedback submitted:', response.data);

        this.$router.push('/end-view')
      } catch (error) {
        console.error('Error submitting feedback:', error);
      }
    },
  },
  created() {
    const participantData = this.$route.params.participantData;
    if (participantData) {
      this.participantData = JSON.parse(participantData);
    }
  }
};
</script>

<style scoped>
#container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h1 {
  text-align: center;
  position: absolute;
  top: 20%;
  left: 45%;
}

p {
  text-align: center;
  position: absolute;
  top: 30%;
}

form {
  max-width: 600px;
  margin: 20px auto;
  position: absolute;
  top: 40%;
}

label {
  display: block;
  margin-bottom: 5px;
}

textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 15%;
  resize: vertical;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
