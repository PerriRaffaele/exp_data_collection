<template>
  <div>
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
        const response = await axios.post('exp-data-collection-api.vercel.app/submit-feedback', feedbackData);
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
/* Add component styles here */
h1 {
  text-align: center;
  margin-top: 20%;
}

form {
  max-width: 600px;
  margin: 20px auto;
}

label {
  display: block;
  margin-bottom: 5px;
}

textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
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
