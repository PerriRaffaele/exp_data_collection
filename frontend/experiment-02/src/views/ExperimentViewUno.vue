<template>
  <div>
    <h1>Experiment {{ this.currentExercise }}</h1>
    <h2>FOLLOW THE LINK, SOLVE THE EXERCISE AND UPLOAD THE PYTHON FILE</h2>
    <div v-if="currentExercise <= totalExercises" class="exercise-page">
      <a v-if="exercises.exercises.length > 0" :href="exercises.exercises[this.currentExercise -1]" target="_blank">Exercise Link</a>

      <!-- File upload input -->
      <div id="upload-file">
      <div class="file-input">
        <input
          type="file"
          name="file-input"
          id="file-input"
          class="file-input__input"
          ref="fileInput" 
          @change="handleFileUpload" 
          accept=".py"
        />
        <label class="file-input__label" for="file-input">
          <svg
            aria-hidden="true"
            focusable="false"
            data-prefix="fas"
            data-icon="upload"
            class="svg-inline--fa fa-upload fa-w-16"
            role="img"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
          >
            <path
              fill="currentColor"
              d="M296 384h-80c-13.3 0-24-10.7-24-24V192h-87.7c-17.8 0-26.7-21.5-14.1-34.1L242.3 5.7c7.5-7.5 19.8-7.5 27.3 0l152.2 152.2c12.6 12.6 3.7 34.1-14.1 34.1H320v168c0 13.3-10.7 24-24 24zm216-8v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h136v8c0 30.9 25.1 56 56 56h80c30.9 0 56-25.1 56-56v-8h136c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z"
            ></path>
          </svg>
          <span>Upload file</span>
        </label>
      </div>

      <!-- Display uploaded file name -->
      <div v-if="uploadedFileName" class="uploaded-file-name">
        Uploaded File: {{ uploadedFileName }}
      </div>
    </div>
      <!-- Button to trigger file upload and submission -->
    </div>
    <div>
        <button v-if="uploadedFileName" @click="submitAnswerData" :disabled="uploading">Upload & Submit</button>
        <div v-if="uploading">
          <!-- You can replace this with any loading animation or text -->
          <p>Uploading...</p>
        </div>
      </div>
  </div>
   <!-- Button to quit -->
   <button id="quit-button" @click="quitExperiment">Quit</button>
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
      attempt:0,
      exercises: {  exercises:[] },
      uploadedFile: null,
      uploading: false,
      uploadedFileName: null, // New property to store the uploaded file name
      feedback: "",
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
          this.$router.push({name: 'EndPoll'});
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
        this.uploadedFileName = this.uploadedFile.name; // Set uploaded file name
      } else {
        this.uploadedFile = this.$refs.fileInput.value = null;
        this.uploadedFileName = null;
        alert('Please upload a .py file');
      }
    },
    async submitAnswerData() {
      try {
        if (!this.uploadedFile) {
          console.error('No file uploaded');
          return;
        }
        
        this.uploading = true;

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
        this.uploadedFileName = null; // Reset the uploaded file name
        // Check if it's time to export to CSV (e.g., after n experiments)
        this.currentExercise++; // Move to the next exercise
        if (this.currentExercise > this.totalExercises) {
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
        this.uploading = false;
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
    quitExperiment() {
      if (this.currentExercise <= this.totalExercises) {
        for (let i = this.currentExercise; i <= this.totalExercises; i++) {
          this.submitNofFinishedData(i);
        }
        for (let i = 1; i <= this.totalExercises; i++) {
          this.submitEmptyFeedback();
        }
      }
      this.$router.push('/end-view');
    },
    async submitNofFinishedData(currentExercise) {
      try {
        const timeTaken = 0;
        const fileContent = "not finished because the user quit the experiment";
        const formData = new FormData();
        formData.append('fileContent', fileContent);
        formData.append('userId', this.exercises.user_id);

        const uploadResponse = await axios.post(`${config.production_backend}/upload-file`, formData);

        let answerData = {
          ex: currentExercise,
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
    } catch (error) {
      console.error('Error submitting answer data:', error);
    }
  },
  async submitEmptyFeedback() {
    try {
      const feedbackData = {
        user_id: this.exercises.user_id,
        feedback: "not finished because the user quit the experiment",
      };
      console.log('Submitting feedback:', feedbackData);
      const response = await axios.post(`${config.production_backend}/submit-feedback`, feedbackData);
      console.log('Feedback submitted:', response.data);
    } catch (error) {
      console.error('Error submitting feedback:', error);
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
  position: absolute;
  top: 15%;
  left: 42%;
}

h2 {
  margin-bottom: 20%;
}

a {
  margin-bottom: 0%;
  font-size: 1.3em;
  text-align: center;
  padding: 10px;
  justify-content: center;
  border: 2px solid transparent;
}

a:hover {
  /* i want the transition to be smooth */
  transition: 0.3s;
  border: 2px solid;
  border-radius: 5px;
  cursor: pointer;
}

input[type="file"] {
  margin-bottom: 20%;
}

.exercise-page {
  display: grid;
  grid-template-rows: 1fr 1fr;
  grid-template-columns: 1fr 1fr;
  align-items: center;
}

.file-input {
  margin-left: 15%;
  margin-right: 15%;
}

.file-input__input {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
  
}

.file-input__label {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  border-radius: 4px;
  font-size: 1.5em;
  font-weight: 600;
  color: #fff;
  font-size: 20px;
  padding: 10px 12px;
  box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.25);
  border: 2px solid tansparent;
}

.file-input__label svg {
  height: 26px;
  margin-right: 4px;
}

.file-input__label:hover {
  transition: 0.3s;
  border: 2px solid #4245a8;
  cursor: pointer;
}

.uploaded-file-name {
  margin-top: 10px;
}

button {
  font-size: 1.3em;
}

#upload-file {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-left: 10%;
  margin-right: 10%;
}

#quit-button {
  border: 3px solid #f1f1f1;
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  font-size: 1.5em;
  cursor: pointer;
  border-radius: 5px;
  display: block; /* Make the button a block-level element */
  margin: 20px auto; /* Center the button horizontally by setting margin-left and margin-right to 'auto' */
  position: absolute;
  top: 90%;
  left: 90%;
}

#quit-button:hover {
  transition: 0.3s;
  background-color: #f1f1f1;
  border: 3px solid #f44336;
  color: #f44336;
}
</style>
