<!-- App.vue -->
<template>
<h1 class="welcome-heading">Welcome to the Pytamaro exercises session</h1>
  <div class="welcome-container">
    
    <p>
      Welcome to the Pytamaro Exercise Session! In this experimental section, you will be engaging in a series of Python programming exercises designed to assess and enhance your coding skills.
      <br>
      The exercises are structured to incrementally increase in difficulty, providing you with a progressive challenge.
    </p>

    <div class="section">
      <h2>Purpose of the Experiment:</h2>
      <p>
        The primary goal of this experiment is to collect valuable data on your problem-solving approach and coding proficiency across different levels of difficulty in order to get your timing for each exercise solved.
        <br>
        Your participation will help us gain insights into the learning and problem-solving processes, contributing to the improvement of programming education.
      </p>
    </div>

    <div class="section">
      <h2>Procedure:</h2>
      <ol>
        <li>You will be directed to the Pytamaro platform for each exercise. Follow the instructions carefully and write your code directly on the platform.</li>
        <li>As you progress, be mindful of the increasing difficulty of the exercises.</li>
        <li>Before starting with the exercises, you will be redirected to a set of questions regarding your programming background. All responses are completely anonymous.</li>
        <li>At the end of the session, you will be prompted to download your code. Ensure you submit the downloaded code to validate your timing and participation.</li>
      </ol>
    </div>


    <div class="section">
      <h2>Note:</h2>
      <p>
        Your feedback and performance are crucial for the success of this experiment.
        <br>
        Please approach each exercise with focus and dedication.
        <br>
        Remember, your responses are confidential, and your individual progress will contribute to a broader understanding of programming skill development.
      </p>
    </div>
    <router-link to="/personal-info">
      <button @click="startExperiment">Start Experiment</button>
    </router-link>
  </div>
</template>

<script>
import Button from '../components/Button.vue';

export default {
  components: {
    Button
  },
  data() {
    return {
      buttons: [],
      clickStartTime: null,
      clickTime: null
    };
  },
  mounted() {
  },
  methods: {
    startExperiment() {
      this.$router.push('/personal-info');
    },
  }
};
</script>

<style scoped>
.welcome-heading {
  text-align: center;
}
.welcome-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: justify;
}

.section {
  margin-bottom: 20px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  display: block; /* Make the button a block-level element */
  margin: 20px auto; /* Center the button horizontally by setting margin-left and margin-right to 'auto' */
}

button:hover {
  background-color: #45a049;
}
</style>