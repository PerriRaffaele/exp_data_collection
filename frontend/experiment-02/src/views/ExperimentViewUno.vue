<template>
  <div>
    <h1>Experiment {{ this.currentExercise }}</h1>
    <div v-if="currentExercise <= totalExercises" class="exercise-page">
      <h2>FOLLOW THE LINK, SOLVE THE EXERCISE AND UPLOAD THE PYTHON FILE</h2>
      <a :href="exercises.exercises[this.currentExercise -1]" target="_blank">Exercise Link</a>

      <!-- File upload input -->
      <div>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".py" />
      </div>

      <!-- Button to trigger file upload and submission -->
      <button @click="submitAnswerData">Upload & Submit</button>
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

export default {
  data() {
    return {
      totalExercises: 3,
      currentExercise: 1,
      counter: 0,
      startTime: null,
      attempt:0,
      exercises: {  exercises:[] },
      uploadedFile: null,
    };
  },
  methods: {
    async fetchBoxWords() {
      try {
        this.startTime = performance.now();
        const response = await axios.get('https://exp-data-collection-api.vercel.app/exercises');
        this.exercises = response.data;
        console.log('Fetched exercises:', this.exercises);

        if (this.counter === this.totalExercises) {
          // Redirect to a new page after 10 experiments
          this.$router.push({name: 'EndPoll'});
        }
      } catch (error) {
        console.error('Error fetching exercises:', error);
      }
    },
    handleFileUpload() {
      // Get the uploaded file from the input
      // check taht the file is a .py file
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

        const formData = new FormData();
        formData.append('file', this.uploadedFile);
        formData.append('userId', this.exercises.user_id);

        const uploadResponse = await axios.post('https://exp-data-collection-api.vercel.app/upload-file', formData);
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
        const response = await axios.post('https://exp-data-collection-api.vercel.app/submit-and-export', answerData);
        console.log('Submitted answer data:', response.data);

        this.uploadedFile = this.$refs.fileInput.value = null; // Reset the uploaded file
        // Check if it's time to export to CSV (e.g., after n experiments)
        this.currentExercise++; // Move to the next exercise
        if (this.currentExercise > this.totalExercises) {
          // Make a GET request to trigger CSV export
          const exportResponse = await axios.get('https://exp-data-collection-api.vercel.app/submit-and-export');
          console.log('Exported answer data to CSV:', exportResponse.data);

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
      }
    },
  },
  computed: {
  },
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
