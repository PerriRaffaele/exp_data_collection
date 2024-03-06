<template>
  <div v-if="!this.statingExperiment" class="personal-info-container">
    <h1>Personal Information</h1>
    <form @submit.prevent="submitForm">
      <!-- Demographics Questions -->
      <div class="form-group">
        <label for="age">Age:</label>
        <input type="number" id="age" v-model="participantData.age" required>
      </div>

      <div class="form-group">
        <label for="gender">Gender:</label>
        <select id="gender" v-model="participantData.gender" required>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Programming Experience (years):</label>
        <select id="gender" v-model="participantData.programmingExperience" required>
          <option value="Less than 1">Less than 1</option>
          <option value="3 to 5">3 to 5</option>
          <option value="More than 5">More than 5</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Which of the following programming languages are you most familiar with?</label>
        <select id="gender" v-model="participantData.familiarityProgrammingLanguage" required>
          <option value="Python">Python</option>
          <option value="Java">Java</option>
          <option value="C/C++">C/C++</option>
          <option value="Javascript">Javascript</option>
          <option value="PHP">PHP</option>
          <option value="Other">Other</option>
          <option value="None">None</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">How many lines of code do you have written until now?</label>
        <select id="gender" v-model="participantData.linesOfCode" required>
          <option value="Less than 1000">Less than 1000</option>
          <option value="1000 to 5000">1000 to 5000</option>
          <option value="5000 to 10000">5000 to 10000</option>
          <option value="10000 to 50000">10000 to 50000</option>
          <option value="More than 50000">More than 50000</option>
          <option value="None">None</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Have you ever use Pytamaro platform before?</label>
        <select id="gender" v-model="participantData.Pytamaro" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
  <div v-else class="experiment-container">
    <h1 class="experiment-title">Experiment</h1>
    <h2>EXAMPLES OF METHOD IN PYTAMARO</h2>
    <div class="experiment-description">
      <div>
      <div class="snippet">
        <pre>
          <code><span>public static Graphic circle(double radius) { </span>
            <span>return ellipse(radius, radius, red);</span>
            <span>&lt;/picture&gt;</span>
            <span></span>
            <span>show_graphic(circle(150))</span>
            <span></span>
            <span></span>
          </code>
            <img v-if="clickedOne" src="../../public/red_circle.PNG" alt="responsive image" />
        </pre>
      </div>
      <button @click="clickedOne = !clickedOne">
        <label v-if="!clickedOne">Run code</label>
        <label v-else>Close</label>
      </button>
      </div>
      <div>
      <div class="snippet">
        <pre>
           <code><span>public static Graphic square(double side) { </span>
            <span>return rectangle(side, side, blue);</span>
            <span>&lt;/picture&gt;</span>
             <span></span>
            <span>show_graphic(square(150))</span>
            <span></span>
            <span></span>
          </code>
            <img v-if="clickedTwo" src="../../public/blue_square.PNG" alt="responsive image" />
        </pre>
      </div>
      <button @click="clickedTwo = !clickedTwo">
        <label v-if="!clickedTwo">Run code</label>
        <label v-else>Close</label>
      </button>
    </div>
    </div>

    <h2>These are two output examples of two Pytamaro methods, circle and square.</h2>
    <!-- Example snippet -->


    <div class="button-container">
      <button v-if="!flagCountdown" class="start-button" @click="startExperimentUno">Start Exercise</button></div>

    <div v-if="flagCountdown" class="countdown">{{ countdown }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showStartButtonUno: false,
      participantData: {
        age: null,
        gender: null,
        programmingExperience: null,
        familiarityProgrammingLanguage: null,
        linesOfCode: null,
        Pytamaro: null,
      },
      statingExperiment: false,
      countdown: 3,
      flagCountdown: false,
      clickedOne: false,
      clickedTwo: false,
    };
  },
  methods: {
    submitForm() {
      console.log('Participant Data:', this.participantData);
      this.statingExperiment = true;
    },
    startExperimentUno() {
      // Show countdown
      this.flagCountdown = true;
      this.showCountdown();

      // Start experiment route after countdown
      setTimeout(() => {
        this.$router.push({
          name: 'ExperimentUno',
          params: {
            participantData: JSON.stringify(this.participantData),
          },
        });
      }, (this.countdown + 1) * 1000);
    },
    showCountdown() {
      let count = 3; // Set the initial countdown value

      const countdownInterval = setInterval(() => {
        this.countdown--;

        if (this.countdown < 0) {
          clearInterval(countdownInterval);
          this.countdown = 0;
        }
      }, 1000);
    },
  },
  mounted() {

  }
};
</script>

<style scoped>
pre {
  font-family: monospace;
  background-color: #fff;
  width: 100%;
  margin: 1em 1em;
  padding: 0.5em;
  border-radius: .25em;
  box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.45);
  line-height: 0;
  counter-reset: line;
}

pre img {
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
pre span {
  display: flex;
  line-height: 1.5rem;
}
pre span:before {
  counter-increment: line;
  content: counter(line);
  display: flex;
  border-right: 1px solid #ddd;
  padding: 0 .5em;
  margin-right: .5em;
  color: #888;
}

.personal-info-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #45a049;
}
.experiment-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;

}

.experiment-title {
  font-size: 60px;
  color: #333;
  margin-bottom: 10px;
}

.experiment-description {
  font-size: 25px;
  color: #555;
  margin-bottom: 20px;
  text-align: center; /* Add this line to center the content */
  justify-content: center;
  align-items: center;
}

.snippet {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-top: 20px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.start-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

.start-button:hover {
  background-color: #45a049;
}
.countdown {
  font-size: 32px;
  font-weight: bold;
  color: green;
  text-align: center;
  margin-top: 20px;
}
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.start-button {
  margin-right: 10px;
}

.experiment-title {
    color: #ffffff;
    font-size: 24px;
    margin-bottom: 10px;
}
.experiment-description {
    color: #666;
    font-size: 16px;
    line-height: 1.6;
  display: inline-flex;
  flex-direction: row;
}
.start-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    margin-top: 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}
.start-button:hover {
    background-color: #45a049;
}
</style>
