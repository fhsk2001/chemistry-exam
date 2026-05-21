let currentQuiz = [];
let currentQuestionIndex = 0;
let score = 0;
let quizInProgress = false;

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    loadPeriodicTable();
    setupNavigation();
    setupCharts();
});

// Навигация между секциите
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const contents = document.querySelectorAll('.content');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.dataset.section;

            // Премахни активния клас от всички
            navButtons.forEach(btn => btn.classList.remove('active'));
            contents.forEach(content => content.classList.remove('active'));

            // Добави активния клас
            this.classList.add('active');
            document.getElementById(section).classList.add('active');

            // Обнови графиките когато отиде на graphics
            if (section === 'graphics') {
                setTimeout(() => {
                    if (atomicNumberChart) atomicNumberChart.resize();
                    if (atomicMassChart) atomicMassChart.resize();
                }, 100);
            }
        });
    });
}

// Зареди периодичната таблица
async function loadPeriodicTable() {
    try {
        const response = await fetch('/api/elements');
        const elements = await response.json();

        const table = document.getElementById('periodicTable');
        table.innerHTML = '';

        Object.entries(elements).forEach(([symbol, data]) => {
            const element = document.createElement('div');
            element.className = 'element';
            element.style.background = data.color;
            element.innerHTML = `
                <div class="element-symbol">${symbol}</div>
                <div class="element-name">${data.name}</div>
            `;

            element.addEventListener('click', () => showElementDetails(symbol, data));
            table.appendChild(element);
        });
    } catch (error) {
        console.error('Грешка при зареждане на елементите:', error);
    }
}

// Покажи детайли на елемент
function showElementDetails(symbol, data) {
    document.getElementById('elementDetails').style.display = 'block';
    document.getElementById('elementName').textContent = data.name;
    document.getElementById('elementSymbol').textContent = symbol;
    document.getElementById('elementNumber').textContent = data.atomic_number;
    document.getElementById('elementMass').textContent = data.mass;
}

// Начало на тест
async function startQuiz() {
    try {
        const response = await fetch('/api/quiz');
        currentQuiz = await response.json();
        currentQuestionIndex = 0;
        score = 0;
        quizInProgress = true;

        document.getElementById('resultsContainer').innerHTML = '';
        showQuestion();
    } catch (error) {
        console.error('Грешка при зареждане на теста:', error);
        alert('Грешка при зареждане на теста!');
    }
}

// Покажи въпрос
function showQuestion() {
    if (currentQuestionIndex >= currentQuiz.length) {
        showResults();
        return;
    }

    const question = currentQuiz[currentQuestionIndex];
    const container = document.getElementById('resultsContainer');

    let html = `
        <div class="question-card">
            <div class="question-number">Въпрос ${currentQuestionIndex + 1} от ${currentQuiz.length}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${((currentQuestionIndex + 1) / currentQuiz.length) * 100}%"></div>
            </div>
            <div class="question-text">${question.question}</div>
            <div class="options" id="optionsContainer">
    `;

    question.options.forEach((option, index) => {
        html += `
            <div class="option" onclick="selectAnswer(${index})">${option}</div>
        `;
    });

    html += `
            </div>
            <button class="btn" onclick="nextQuestion()" style="display: none;" id="nextBtn">Следващ въпрос</button>
        </div>
    `;

    container.innerHTML = html;
}

// Избери отговор
async function selectAnswer(index) {
    const question = currentQuiz[currentQuestionIndex];
    const options = document.querySelectorAll('.option');

    options.forEach(option => option.style.pointerEvents = 'none');

    try {
        const response = await fetch('/api/check-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question_id: question.id,
                answer: index
            })
        });

        const result = await response.json();

        // Покажи отговор
        options[index].classList.add(result.correct ? 'correct' : 'incorrect');
        options[result.correct_answer].classList.add('correct');

        if (result.correct) {
            score++;
        }

        // Покажи обяснение
        const quizCard = document.querySelector('.question-card');
        const explanation = document.createElement('div');
        explanation.className = 'explanation';
        explanation.textContent = result.explanation;
        quizCard.appendChild(explanation);

        // Покажи бутона за следващ въпрос
        document.getElementById('nextBtn').style.display = 'block';
    } catch (error) {
        console.error('Грешка при проверка на отговора:', error);
    }
}

// Следващ въпрос
function nextQuestion() {
    currentQuestionIndex++;
    showQuestion();
}

// Покажи резултати
function showResults() {
    const container = document.getElementById('resultsContainer');
    const percentage = Math.round((score / currentQuiz.length) * 100);
    let message = '';
    let emoji = '';

    if (percentage === 100) {
        message = 'Отличен! Перфектен резултат!';
        emoji = '🏆';
    } else if (percentage >= 80) {
        message = 'Много добре! Браво!';
        emoji = '🎉';
    } else if (percentage >= 60) {
        message = 'Добре! Добра работа!';
        emoji = '👍';
    } else {
        message = 'Опитай се отново и ще го направиш по-добре!';
        emoji = '💪';
    }

    container.innerHTML = `
        <div class="results">
            <div style="font-size: 3em; margin-bottom: 20px;">${emoji}</div>
            <div class="score">${score}/${currentQuiz.length}</div>
            <div style="font-size: 1.5em; margin-bottom: 20px;">${percentage}%</div>
            <div class="results-text">${message}</div>
            <button class="btn" onclick="startQuiz()">Опитай отново</button>
        </div>
    `;

    quizInProgress = false;
}

// Графики
let atomicNumberChart, atomicMassChart;

function setupCharts() {
    // График на атомните номера
    const atomicCtx = document.getElementById('atomicNumberChart');
    atomicNumberChart = new Chart(atomicCtx, {
        type: 'bar',
        data: {
            labels: ['H', 'C', 'N', 'O', 'Na', 'Mg', 'Al', 'Si', 'S', 'Cl', 'K', 'Ca', 'Fe', 'Cu'],
            datasets: [{
                label: 'Атомно число',
                data: [1, 6, 7, 8, 11, 12, 13, 14, 16, 17, 19, 20, 26, 29],
                backgroundColor: [
                    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#FFD93D',
                    '#6BCB77', '#C7CEEA', '#B19CD9', '#FFFD38', '#90EE90',
                    '#FFB6C1', '#DDA0DD', '#A9A9A9', '#B87333'
                ],
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 14 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Атомно число'
                    }
                }
            }
        }
    });

    // График на атомните маси
    const massCtx = document.getElementById('atomicMassChart');
    atomicMassChart = new Chart(massCtx, {
        type: 'line',
        data: {
            labels: ['H', 'C', 'N', 'O', 'Na', 'Mg', 'Al', 'Si', 'S', 'Cl', 'K', 'Ca', 'Fe', 'Cu'],
            datasets: [{
                label: 'Атомна маса',
                data: [1, 12, 14, 16, 23, 24, 27, 28, 32, 35.5, 39, 40, 56, 64],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 14 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Атомна маса'
                    }
                }
            }
        }
    });
}
