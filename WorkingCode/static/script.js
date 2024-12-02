let currentEnemies = [
    { name: 'Loki', health: 100, attackPower: 10 },
    { name: 'Ultron', health: 100, attackPower: 15 },
    { name: 'Hela', health: 150, attackPower: 20 } // New enemy: Hela
];

let heroes = [
    { name: 'Iron Man', health: 100, energy: 100 },
    { name: 'Captain America', health: 120, energy: 100 },
    { name: 'Thor', health: 150, energy: 100 },
    { name: 'Spider-Man', health: 90, energy: 100 }, // Added Spider-Man
    { name: 'Black Widow', health: 80, energy: 100 } // Added Black Widow
];

function displayEnemies() {
    let enemiesList = document.getElementById('enemies-list');
    if (!enemiesList) return;
    enemiesList.innerHTML = '';

    currentEnemies.forEach(enemy => {
        let li = document.createElement('li');
        li.textContent = `${enemy.name} - HP: ${enemy.health}`;
        enemiesList.appendChild(li);
    });
}

function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    if (!heroesList) return;
    heroesList.innerHTML = '';

    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}, Energy: ${hero.energy}`;
        heroesList.appendChild(li);
    });
}

function updateStats(totalHp, level) {
    // Update stats dynamically on the page
    let totalHpElement = document.getElementById('total-hp');
    let levelElement = document.getElementById('level');

    if (totalHpElement) totalHpElement.textContent = totalHp;
    if (levelElement) levelElement.textContent = level;

    // Save stats to the backend
    saveProgress(totalHp, level);
}

function saveProgress(totalHp, level) {
    // Send updated stats to the backend
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ total_hp: totalHp, level: level })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log(data.message); // Log success message
            } else {
                console.error(data.error); // Log error if any
            }
        })
        .catch(err => console.error('Error saving progress:', err));
}

function startBattle() {
    displayHeroes();
    displayEnemies();
    updateDropdowns();

    // Simulate a stat update for demonstration
    setTimeout(() => {
        // Example: Update total_hp and level
        const newTotalHp = 200; // Replace with actual calculations
        const newLevel = 3; // Replace with actual calculations
        updateStats(newTotalHp, newLevel);
    }, 3000); // Delay to simulate battle progression
}

function updateDropdowns() {
    let heroSelect = document.getElementById('hero-select');
    let enemySelect = document.getElementById('enemy-select');
    if (!heroSelect || !enemySelect) return;

    heroSelect.innerHTML = '';
    enemySelect.innerHTML = '';

    heroes.forEach((hero, index) => {
        if (hero.health > 0) {
            let option = document.createElement('option');
            option.value = index;
            option.textContent = hero.name;
            heroSelect.appendChild(option);
        }
    });

    currentEnemies.forEach((enemy, index) => {
        if (enemy.health > 0) {
            let option = document.createElement('option');
            option.value = index;
            option.textContent = enemy.name;
            enemySelect.appendChild(option);
        }
    });
}

window.onload = function () {
    startBattle();
};
