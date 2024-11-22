let currentEnemies = [
    { name: 'Loki', health: 100, attackPower: 10 },
    { name: 'Ultron', health: 100, attackPower: 15 },
    { name: 'Hela', health: 150, attackPower: 20 } // New enemy: Hela
];

let heroes = [
    { name: 'Iron Man', health: 100, energy: 100 },
    { name: 'Captain America', health: 120, energy: 100 },
    { name: 'Thor', health: 150, energy: 100 },
    { name: 'Spider-Man', health: 90, energy: 120 }, // Added Spider-Man
    { name: 'Black Widow', health: 80, energy: 110 } // Added Black Widow
];

let battleOver = false;
let thanosDefeated = false;

// Start the battle
function startBattle() {
    displayHeroes();
    displayEnemies();
    updateDropdowns();
}

function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    heroesList.innerHTML = '';
    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}, Energy: ${hero.energy}`;
        heroesList.appendChild(li);
    });
}

function displayEnemies() {
    let enemiesList = document.getElementById('enemies-list');
    enemiesList.innerHTML = '';
    currentEnemies.forEach(enemy => {
        let li = document.createElement('li');
        li.textContent = `${enemy.name} - HP: ${enemy.health}`;
        enemiesList.appendChild(li);
    });
}

function updateDropdowns() {
    let heroSelect = document.getElementById('hero-select');
    let enemySelect = document.getElementById('enemy-select');
    heroSelect.innerHTML = '';
    enemySelect.innerHTML = '';

    heroes.forEach((hero, index) => {
        let option = document.createElement('option');
        option.value = index;
        option.textContent = hero.name;
        heroSelect.appendChild(option);
    });

    currentEnemies.forEach((enemy, index) => {
        let option = document.createElement('option');
        option.value = index;
        option.textContent = enemy.name;
        enemySelect.appendChild(option);
    });
}

function performAction(action) {
    if (battleOver) return;

    let heroIndex = document.getElementById('hero-select').value;
    let enemyIndex = document.getElementById('enemy-select').value;

    let hero = heroes[heroIndex];
    let enemy = currentEnemies[enemyIndex];

    if (action === 'attack') {
        attackEnemy(hero, enemy);
    } else if (action === 'special') {
        useSpecialMove(hero, enemy);
    }
}

function attackEnemy(hero, enemy) {
    let damage = getRandomDamage(15, 25);
    enemy.health -= damage;

    let battleStatus = `${hero.name} attacks ${enemy.name} for ${damage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;
        currentEnemies.splice(currentEnemies.indexOf(enemy), 1); // Remove defeated enemy

        // Check if all enemies are defeated and Thanos hasn't been added yet
        if (currentEnemies.length === 0 && !thanosDefeated) {
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
            battleStatus += "\nAll enemies defeated! Thanos appears!";
            updateDropdowns();  // Update the dropdowns to include Thanos
        }
    }

    let counterStatus = enemyCounterAttack(hero);
    updateBattleStatus(`${battleStatus}\n${counterStatus}`);
    checkHeroesHealth();
    displayEnemies();
    displayHeroes();
}

function useSpecialMove(hero, enemy) {
    if (hero.energy < 50) {
        updateBattleStatus(`${hero.name} doesn't have enough energy to use a special move!`);
        return;
    }

    let damage = getRandomDamage(40, 60);
    enemy.health -= damage;
    hero.energy -= 50;

    let battleStatus = `${hero.name} uses a special move on ${enemy.name} for ${damage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;
        currentEnemies.splice(currentEnemies.indexOf(enemy), 1); // Remove defeated enemy

        // Check if all enemies are defeated and Thanos hasn't been added yet
        if (currentEnemies.length === 0 && !thanosDefeated) {
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
            battleStatus += "\nAll enemies defeated! Thanos appears!";
            updateDropdowns();  // Update the dropdowns to include Thanos
        }
    }

    let counterStatus = enemyCounterAttack(hero);
    updateBattleStatus(`${battleStatus}\n${counterStatus}`);
    checkHeroesHealth();
    displayEnemies();
    displayHeroes();
}

function enemyCounterAttack(hero) {
    let enemy = currentEnemies[Math.floor(Math.random() * currentEnemies.length)];
    let damage = getRandomDamage(enemy.attackPower - 5, enemy.attackPower + 5);
    hero.health -= damage;

    let counterStatus = `${enemy.name} counter-attacks ${hero.name} for ${damage} damage!`;

    if (hero.health <= 0) {
        counterStatus += `\n${hero.name} has been defeated!`;
        heroes.splice(heroes.indexOf(hero), 1);
    }

    return counterStatus;
}

function checkHeroesHealth() {
    if (heroes.length === 0) {
        updateBattleStatus("Game Over! All heroes have been defeated.");
        showGameOverScreen("You lost! Better luck next time.");
        battleOver = true;
    }
}

function getRandomDamage(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function updateBattleStatus(statusText) {
    let battleStatusElement = document.getElementById('battle-status');
    battleStatusElement.textContent = statusText;
}

function showWinScreen() {
    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>Congratulations!</h2>
        <p>You defeated Thanos and saved the day!</p>
        <button onclick="restartGame()">Play Again</button>
    `;
}

function showGameOverScreen(message) {
    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>${message}</h2>
        <button onclick="restartGame()">Try Again</button>
    `;
}

function restartGame() {
    location.reload();
}

window.onload = function () {
    startBattle();
};
