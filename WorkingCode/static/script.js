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

function startBattle() {
    displayHeroes();
    displayEnemies();
    updateDropdowns();
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
