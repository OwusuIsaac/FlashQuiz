// main.js
const flashcards = [
  {
    question: "What is the main purpose of photosynthesis?",
    options: [
      "To absorb nutrients from the soil",
      "To produce oxygen for animals",
      "To convert sunlight into chemical energy",
      "To cool down the plant during the day"
    ],
    answer: "To convert sunlight into chemical energy"
  },
  {
    question: "Which organelle is responsible for photosynthesis?",
    options: [
      "Mitochondria",
      "Chloroplast",
      "Nucleus",
      "Ribosome"
    ],
    answer: "Chloroplast"
  },
  {
    question: "Which gas is taken in by plants during photosynthesis?",
    options: [
      "Oxygen",
      "Nitrogen",
      "Carbon Dioxide",
      "Hydrogen"
    ],
    answer: "Carbon Dioxide"
  }
];

let currentIndex = 0;
let score = 0;
const missed = [];

document.addEventListener("DOMContentLoaded", () => {
  const questionEl = document.getElementById("question");
  const optionsEl = document.getElementById("options");
  const nextBtn = document.getElementById("next-btn");

  if (!questionEl || !optionsEl || !nextBtn) return; 

  function loadQuestion() {
    const current = flashcards[currentIndex];
    questionEl.textContent = current.question;
    optionsEl.innerHTML = "";
    nextBtn.disabled = true;

    current.options.forEach(opt => {
      const li = document.createElement("li");
      li.textContent = opt;
      li.classList.add("option");
      li.addEventListener("click", () => {
        document.querySelectorAll(".option").forEach(el => el.classList.remove("selected"));
        li.classList.add("selected");
        nextBtn.disabled = false;
      });
      optionsEl.appendChild(li);
    });
  }

  nextBtn.addEventListener("click", () => {
    const selected = document.querySelector(".option.selected");
    const answer = selected?.textContent;
    const correct = flashcards[currentIndex].answer;

    if (answer === correct) {
      score++;
    } else {
      missed.push(flashcards[currentIndex]);
    }

    currentIndex++;
    if (currentIndex < flashcards.length) {
      loadQuestion();
    } else {
      // Save results 
      sessionStorage.setItem("score", score);
      sessionStorage.setItem("total", flashcards.length);
      sessionStorage.setItem("missed", JSON.stringify(missed));

      // Save progress 
      const existingProgress = JSON.parse(localStorage.getItem("progress")) || [];
      const currentDate = new Date().toLocaleString();
      existingProgress.push({
        date: currentDate,
        score: score,
        total: flashcards.length
      });
      localStorage.setItem("progress", JSON.stringify(existingProgress));

      window.location.href = "results.html";
    }
  });

  loadQuestion();
});
