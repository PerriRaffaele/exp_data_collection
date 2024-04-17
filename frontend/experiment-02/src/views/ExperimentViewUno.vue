<template>
  <div>
    <h1>Experiment {{ this.currentExercise }}</h1>
    <div v-if="currentExercise <= totalExercises" class="exercise-page">
      <h2>FOLLOW THE LINK, SOLVE THE EXERCISE AND UPLOAD THE PYTHON FILE</h2>
      <a v-if="exercises.exercises.length > 0" :href="exercises.exercises[this.currentExercise - 1]" target="_blank">Exercise Link</a>

      <!-- File upload input -->
      <div>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".py" />
      </div>

      <!-- Button to trigger file upload and submission -->
      <button @click="submitAnswerData" :disabled="uploading">Upload & Submit</button>

      <!-- Loading indicator -->
      <div v-if="uploading">
        <!-- You can replace this with any loading animation or text -->
        <p>Loading...</p>
      </div>
    </div>
    <div v-else>
      <p>Experiments completed. Redirecting...</p>
      <!-- You can add a loading spinner or any other content here -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import EndPoll from "./EndPoll.vue";
import config from './config';

export default {
  data() {
    return {
      totalExercises: 3,
      currentExercise: 1,
      counter: 0,
      startTime: null,
      attempt: 0,
      exercises: { exercises: [] },
      uploadedFile: null,
      uploading: false, // Add a boolean variable to track upload status
    };
  },
  methods: {
    async fetchBoxWords() {
      try {
        this.startTime = performance.now();
        const response = await axios.get(`${config.production_backend}/exercises`);
        this.exercises = response.data;
        console.log('Fetched exercises:', this.exercises);

        if (this.counter === this.totalExercises) {
          // Redirect to a new page after 10 experiments
          this.$router.push({ name: 'EndPoll' });
        }
      } catch (error) {
        console.error('Error fetching exercises:', error);
      }
    },
    handleFileUpload() {
      // Get the uploaded file from the input
      // check that the file is a .py file
      if (this.$refs.fileInput.files.length > 0 && this.$refs.fileInput.files[0].name.split('.').pop() === 'py') {
        this.uploadedFile = this.$refs.fileInput.files[0];
      } else {
        this.uploadedFile = this.$refs.fileInput.value = null;
        alert('Please upload a .py file');
      }
    },
    async submitAnswerData() {
      try {
        if (!this.uploadedFile) {
          console.error('No file uploaded');
          return;
        }

        this.uploading = true; // Set uploading status to true

        const fileContent = await this.readFileContent(this.uploadedFile);

        const formData = new FormData();
        formData.append('fileContent', fileContent);
        formData.append('userId', this.exercises.user_id);

        const uploadResponse = await axios.post(`${config.production_backend}/upload-file`, formData);
        console.log('File uploaded:', uploadResponse.data);

        const timeTaken = performance.now() - this.startTime;
        // Make a POST request to the combined endpoint
        let answerData = {
          ex: this.currentExercise,
          user_id: this.exercises.user_id,
          age: this.participantData.age,
          gender: this.participantData.gender,
          programming_experience: this.participantData.programmingExperience,
          programming_language_familiarity: this.participantData.familiarityProgrammingLanguage,
          lines_of_code: this.participantData.linesOfCode,
          pytamaro: this.participantData.Pytamaro,
          timeTaken 
        };
        const response = await axios.post(`${config.production_backend}/submit-and-export`, answerData);
        console.log('Submitted answer data:', response.data);

        this.uploadedFile = this.$refs.fileInput.value = null; // Reset the uploaded file
        // Check if it's time to export to CSV (e.g., after n experiments)
        this.currentExercise++; // Move to the next exercise
        if (this.currentExercise > this.totalExercises) {
          // Make a GET request to trigger CSV export

          // Optionally, you can redirect to a new page after exporting to CSV
          this.$router.push({
            name: 'EndPoll',
            params: {
              participantData: JSON.stringify(answerData),
            }
          });
        }
      } catch (error) {
        console.error('Error submitting answer data:', error);
      } finally {
        this.uploading = false; // Set uploading status to false after upload completes
      }
    },
    async readFileContent(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
          resolve(event.target.result);
        };
        reader.onerror = (error) => {
          reject(error);
        };
        reader.readAsText(file);
      });
    },
  },
  computed: {},
  mounted() {
    axios.defaults.withCredentials = true;
    this.fetchBoxWords();
    //   clean the input for the file
    this.$refs.fileInput.value = null;
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

.box {
  margin-top: 20px;
  background-color: transparent;
  border: 1px solid #e0e0e0;
  padding: 10px;
  font-size: 20px;
  width: calc(90%); /* Adjust the width to account for margin and border */
}

.clickable-box {
  margin-top: 10px;
  margin-right: 10px;
  background-color: transparent;
  border: 1px solid #e0e0e0;
  padding: 10px;
  cursor: pointer;
  display: flex;
  width: calc(48% - 20px); /* Adjust the width to account for margin and border */
  height: 100px;
  box-sizing: border-box;
  transition: transform 0.3s; /* Smooth transition for the transform property */
  text-align: center;
  font-size: 20px;
  align-items: center;
  justify-content: center;
}

.boxes {
  display: flex;
  flex-wrap: wrap;
}
.correct-box {
  background-color: green; /* Set the background color for the correct answer */
}

.incorrect-box {
  background-color: red; /* Set the background color for the incorrect answer */
}

.clickable-box:hover {
  transform: scale(1.1); /* Increase the size on hover */
}
</style>
