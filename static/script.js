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

// Flag to track if the battle is over
let battleOver = false;
let thanosDefeated = false;  // Flag to track if Thanos has been defeated

// Start the battle and display heroes and enemies
function startBattle() {
    displayHeroes();
    displayEnemies();
}

// Display heroes on the page
function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    heroesList.innerHTML = '';  // Clear current heroes list

    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}`;
        heroesList.appendChild(li);
    });
}

// Display enemies on the page
function displayEnemies() {
    let enemiesList = document.getElementById('enemies-list');
    enemiesList.innerHTML = '';  // Clear current enemies list

    currentEnemies.forEach(enemy => {
        let li = document.createElement('li');
        li.textContent = `${enemy.name} - HP: ${enemy.health}`;
        enemiesList.appendChild(li);
    });
}

// Perform action (attack or special)
function performAction(action) {
    if (battleOver) return; // Prevent actions if the battle is over

    let actionType = action;
    // Simulate action results
    if (actionType === 'attack') {
        attackEnemy();
    } else if (actionType === 'special') {
        useSpecialMove();
    }
}

// Hero attacks the enemy
function attackEnemy() {
    let enemy = currentEnemies[0];  // Target the first enemy (you could improve this)
    let hero = heroes[0];  // For now, target the first hero

    // Randomize damage dealt by hero
    let heroAttackDamage = getRandomDamage(15, 25);  // Hero's attack damage between 15 and 25
    enemy.health -= heroAttackDamage;  // Apply damage to enemy

    let battleStatus = `${hero.name} attacks ${enemy.name} for ${heroAttackDamage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;
        currentEnemies.shift();  // Remove defeated enemy

        if (currentEnemies.length === 0 && !thanosDefeated) {
            battleStatus += "\nYou've defeated all enemies! Thanos appears!";
            // Add Thanos as the final boss only if he has not been defeated
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
        }
    }
    
    // Enemy counter-attacks
    enemyCounterAttack(hero);

    displayEnemies();  // Update enemy list
    displayHeroes();   // Update heroes list

    // Update the battle status area
    updateBattleStatus(battleStatus);

    // Check if any heroes are dead
    checkHeroesHealth();
}

// Use a special move
function useSpecialMove() {
    let enemy = currentEnemies[0];  // Target first enemy
    let hero = heroes[0];  // Target first hero

    let battleStatus = `${hero.name} uses a special move against ${enemy.name}!`;

    // Randomize damage dealt by special move
    let specialMoveDamage = getRandomDamage(40, 60);  // Special move damage between 40 and 60
    enemy.health -= specialMoveDamage;

    battleStatus += `\n${enemy.name} takes ${specialMoveDamage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += `\n${enemy.name} has been defeated!`;
        currentEnemies.shift();  // Remove defeated enemy
        if (currentEnemies.length === 0 && !thanosDefeated) {
            battleStatus += "\nYou've defeated all enemies! Thanos appears!";
            // Add Thanos as the final boss only if he has not been defeated
            currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
        }
    }

    // Enemy counter-attacks
    enemyCounterAttack(hero);

    displayEnemies();  // Update enemy list
    displayHeroes();   // Update heroes list

    // Update the battle status area
    updateBattleStatus(battleStatus);

    // Check if any heroes are dead
    checkHeroesHealth();
}

// Update battle status text
function updateBattleStatus(statusText) {
    let battleStatusElement = document.getElementById('battle-status');
    battleStatusElement.textContent = statusText;
}

// Enemy counter-attack logic (randomized damage)
function enemyCounterAttack(hero) {
    // Randomize damage dealt by enemy counter-attack
    let enemy = currentEnemies[0];  // The enemy that is currently targeted
    let counterAttackDamage = getRandomDamage(enemy.attackPower - 5, enemy.attackPower + 5);  // Random range based on enemy's attack power
    hero.health -= counterAttackDamage;  // Reduce hero's health by enemy's counter-attack damage

    let battleStatus = `${enemy.name} counter-attacks ${hero.name} for ${counterAttackDamage} damage!`;

    if (hero.health <= 0) {
        battleStatus += `\n${hero.name} has been defeated!`;
        // Remove the hero from the list of heroes
        heroes = heroes.filter(h => h !== hero);
    }

    // Update the battle status area
    updateBattleStatus(battleStatus);
}

// Check if any heroes are dead after each action
function checkHeroesHealth() {
    heroes.forEach(hero => {
        if (hero.health <= 0) {
            alert(`${hero.name} has been defeated!`);
            // Remove the hero from the list if they are defeated
            heroes = heroes.filter(h => h !== hero);
        }
    });

    // If there are no heroes left, game over
    if (heroes.length === 0) {
        updateBattleStatus("Game Over! All heroes are defeated.");
        showGameOverScreen("Sorry, you lost! Better luck next time.");
    }
}

// Function to get random damage within a specified range
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

// Check if Thanos has been defeated
function checkForThanosDefeat() {
    let thanos = currentEnemies.find(enemy => enemy.name === 'Thanos');
    if (thanos && thanos.health <= 0) {
        thanosDefeated = true;  // Mark Thanos as defeated
        currentEnemies = currentEnemies.filter(enemy => enemy.name !== 'Thanos');  // Remove Thanos permanently
        showWinScreen();
    }
}

// Ensure Thanos only appears if he hasn't been defeated yet
function addThanosIfNecessary() {
    if (currentEnemies.length === 0 && !thanosDefeated) {
        currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
    }
}

// Start the battle on page load
window.onload = function() {
    startBattle();
};
