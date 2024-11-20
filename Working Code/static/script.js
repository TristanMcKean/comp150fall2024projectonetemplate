let currentEnemies = [
    { name: 'Loki', health: 100, attackPower: 10 },
    { name: 'Ultron', health: 100, attackPower: 15 }
];

// Example heroes (can be dynamically generated from the backend)
let heroes = [
    { name: 'Iron Man', health: 100 },
    { name: 'Captain America', health: 120 },
    { name: 'Thor', health: 150 }
];

let battleOver = false;
let thanosDefeated = false;

// Start the battle and display heroes and enemies
function startBattle() {
    displayHeroes();
    displayEnemies();
}

// Display heroes on the page
function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    heroesList.innerHTML = '';
    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}`;
        heroesList.appendChild(li);
    });
}

// Display enemies on the page
function displayEnemies() {
    let enemiesList = document.getElementById('enemies-list');
    enemiesList.innerHTML = '';
    currentEnemies.forEach(enemy => {
        let li = document.createElement('li');
        li.textContent = `${enemy.name} - HP: ${enemy.health}`;
        enemiesList.appendChild(li);
    });
}

// Perform action (attack or special)
function performAction(action) {
    if (battleOver) return;
    if (action === 'attack') attackEnemy();
    else if (action === 'special') useSpecialMove();
}

// Hero attacks the enemy
function attackEnemy() {
    let enemy = currentEnemies[0];
    let hero = heroes[0];

    let heroAttackDamage = getRandomDamage(15, 25);
    enemy.health -= heroAttackDamage;

    let battleStatus = `${hero.name} attacks ${enemy.name} for ${heroAttackDamage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;

        if (enemy.name === 'Thanos') {
            thanosDefeated = true;
            currentEnemies = currentEnemies.filter(e => e.name !== 'Thanos');
            displayEnemies();
            updateBattleStatus("You defeated Thanos! The universe is saved!");
            showWinScreen();
            return;
        }

        currentEnemies.shift();
        if (currentEnemies.length === 0 && !thanosDefeated) {
            battleStatus += "\nYou've defeated all enemies! Thanos appears!";
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
        }
    }

    enemyCounterAttack(hero);
    displayEnemies();
    displayHeroes();
    updateBattleStatus(battleStatus);
    checkHeroesHealth();
}

// Use a special move
function useSpecialMove() {
    let enemy = currentEnemies[0];
    let hero = heroes[0];

    let battleStatus = `${hero.name} uses a special move against ${enemy.name}!`;
    let specialMoveDamage = getRandomDamage(40, 60);
    enemy.health -= specialMoveDamage;

    battleStatus += `\n${enemy.name} takes ${specialMoveDamage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;

        if (enemy.name === 'Thanos') {
            thanosDefeated = true;
            currentEnemies = currentEnemies.filter(e => e.name !== 'Thanos');
            displayEnemies();
            updateBattleStatus("You defeated Thanos! The universe is saved!");
            showWinScreen();
            return;
        }

        currentEnemies.shift();
        if (currentEnemies.length === 0 && !thanosDefeated) {
            battleStatus += "\nYou've defeated all enemies! Thanos appears!";
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
        }
    }

    enemyCounterAttack(hero);
    displayEnemies();
    displayHeroes();
    updateBattleStatus(battleStatus);
    checkHeroesHealth();
}

// Update battle status text
function updateBattleStatus(statusText) {
    let battleStatusElement = document.getElementById('battle-status');
    battleStatusElement.textContent = statusText;
}

// Enemy counter-attack logic
function enemyCounterAttack(hero) {
    let enemy = currentEnemies[0];
    let counterAttackDamage = getRandomDamage(enemy.attackPower - 5, enemy.attackPower + 5);
    hero.health -= counterAttackDamage;

    let battleStatus = `${enemy.name} counter-attacks ${hero.name} for ${counterAttackDamage} damage!`;

    if (hero.health <= 0) {
        battleStatus += `\n${hero.name} has been defeated!`;
        heroes = heroes.filter(h => h !== hero);
    }

    updateBattleStatus(battleStatus);
}

// Check if any heroes are dead
function checkHeroesHealth() {
    heroes.forEach(hero => {
        if (hero.health <= 0) {
            alert(`${hero.name} has been defeated!`);
            heroes = heroes.filter(h => h !== hero);
        }
    });

    if (heroes.length === 0) {
        updateBattleStatus("Game Over! All heroes are defeated.");
        showGameOverScreen("Sorry, you lost! Better luck next time.");
    }
}

// Function to get random damage within a range
function getRandomDamage(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Show win screen
function showWinScreen() {
    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>Congratulations!</h2>
        <p>You defeated Thanos and saved the day!</p>
        <button onclick="restartGame()">Play Again</button>
    `;
}

// Show game over screen
function showGameOverScreen(message) {
    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>${message}</h2>
        <button onclick="restartGame()">Try Again</button>
    `;
}

// Restart the game
function restartGame() {
    location.reload();
}

// Start the battle on page load
window.onload = function() {
    startBattle();
};
