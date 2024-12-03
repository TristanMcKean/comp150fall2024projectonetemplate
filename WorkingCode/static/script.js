let currentEnemies = [
    { name: 'Loki', health: 100, attackPower: 10 },
    { name: 'Ultron', health: 100, attackPower: 15 },
    { name: 'Hela', health: 150, attackPower: 20 }
];

let heroes = [
    { name: 'Iron Man', health: 100, energy: 100 },
    { name: 'Captain America', health: 120, energy: 100 },
    { name: 'Thor', health: 150, energy: 100 },
    { name: 'Spider-Man', health: 200, energy: 150 },
    { name: 'Black Widow', health: 95, energy: 110 }
];

let battleOver = false;
let thanosDefeated = false;

// Define random phrases for attack actions
const attackPhrases = [
    "{hero} strikes {enemy} with a powerful blow for {damage} damage!",
    "{hero} unleashes a mighty attack on {enemy}, causing {damage} damage!",
    "{hero} lands a fierce strike on {enemy}, dealing {damage} damage!",
    "{hero} delivers a crushing blow to {enemy}, inflicting {damage} damage!",
    "{hero} hits {enemy} with an unstoppable punch for {damage} damage!",
    "{hero} launches an intense strike at {enemy}, dealing {damage} damage!",
    "{hero} throws a devastating punch at {enemy}, causing {damage} damage!",
    "{hero} smashes {enemy} with a powerful hit for {damage} damage!"
];


// Define phrases for when enemies are defeated
const enemyDefeatPhrases = [
    " {enemy} has been defeated! Good job, hero!",
    " {enemy} is no more! You've won this round!",
    " Victory! {enemy} has fallen!"
];

// Helper function to replace placeholders with actual values
function randomPhrase(phrases, heroName, enemyName = '', damage = 0) {
    const randomIndex = Math.floor(Math.random() * phrases.length);
    return phrases[randomIndex]
        .replace("{hero}", heroName)
        .replace("{enemy}", enemyName)
        .replace("{damage}", damage);
}

// Start the battle
function startBattle() {
    displayHeroes();
    displayEnemies();
    updateDropdowns();
}

function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    if (!heroesList) return; // Prevent errors if element is missing
    heroesList.innerHTML = '';
    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}, Energy: ${hero.energy}`;
        heroesList.appendChild(li);
    });
}

function displayEnemies() {
    let enemiesList = document.getElementById('enemies-list');
    if (!enemiesList) return; // Prevent errors if element is missing
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
    if (!heroSelect || !enemySelect) return; // Prevent errors if elements are missing

    // Clear existing dropdowns
    heroSelect.innerHTML = '';
    enemySelect.innerHTML = '';

    // Populate hero dropdown
    heroes.forEach((hero, index) => {
        let option = document.createElement('option');
        option.value = index;
        option.textContent = hero.name;
        heroSelect.appendChild(option);
    });

    // Populate enemy dropdown
    currentEnemies.forEach((enemy, index) => {
        let option = document.createElement('option');
        option.value = index;
        option.textContent = enemy.name;
        enemySelect.appendChild(option);
    });
}

function performAction(action) {
    // Stop all actions if the game is over
    if (battleOver) return;

    let heroIndex = parseInt(document.getElementById('hero-select').value);
    let enemyIndex = parseInt(document.getElementById('enemy-select').value);

    let hero = heroes[heroIndex];
    let enemy = currentEnemies[enemyIndex];

    if (action === 'attack') {
        attackEnemy(hero, enemy);
    } else if (action === 'special') {
        useSpecialMove(hero, enemy);
    }
}

function attackEnemy(hero, enemy) {
    // 15% chance to miss the attack
    if (Math.random() < 0.15) {
        updateBattleStatus(randomPhrase(["{hero} attacks {enemy} but misses!"], hero.name, enemy.name));
        let counterStatus = enemyCounterAttack(hero);
        updateBattleStatus(counterStatus, true); // Append counter-attack result
        checkHeroesHealth();
        return; // End the function early
    }

    let damage = getRandomDamage(15, 25);
    enemy.health -= damage;

    // Generate attack phrase with hero, enemy, and damage
    let battleStatus = randomPhrase(attackPhrases, hero.name, enemy.name, damage);

    if (enemy.health <= 0) {
        battleStatus += handleEnemyDefeat(enemy);
    }

    let counterStatus = enemyCounterAttack(hero);
    updateBattleStatus(`${battleStatus} ${counterStatus}`);
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

    // Generate special attack phrase with hero, enemy, and damage
    let battleStatus = `${hero.name} uses a special move on ${enemy.name} for ${damage} damage!`;

    if (enemy.health <= 0) {
        battleStatus += handleEnemyDefeat(enemy);
    }

    let counterStatus = enemyCounterAttack(hero);
    updateBattleStatus(`${battleStatus} ${counterStatus}`);
    checkHeroesHealth();
    displayEnemies();
    displayHeroes();
}

function handleEnemyDefeat(enemy) {
    currentEnemies.splice(currentEnemies.indexOf(enemy), 1);

    // Check if Thanos is defeated
    if (enemy.name === 'Thanos') {
        thanosDefeated = true;
        battleOver = true; // Mark battle as over
        showWinScreen(); // Show victory screen
        return `\n${enemy.name} has been defeated! You have won the battle!`;
    }

    // If all other enemies are defeated and Thanos hasn't appeared yet
    if (currentEnemies.length === 0 && !thanosDefeated) {
        currentEnemies.push({ name: 'Thanos', health: 250, attackPower: 50 });
        updateDropdowns();
        return `\n${enemy.name} has been defeated! All enemies defeated! Thanos appears!`;
    }

    return randomPhrase(enemyDefeatPhrases, '', enemy.name);
}

function enemyCounterAttack(hero) {
    if (currentEnemies.length === 0) {
        return "No enemies left to counter-attack!";
    }

    let enemy = currentEnemies[Math.floor(Math.random() * currentEnemies.length)];
    let damage = getRandomDamage(enemy.attackPower - 5, enemy.attackPower + 5);
    hero.health -= damage;

    let counterStatus = `${enemy.name} counter-attacks ${hero.name} for ${damage} damage!`;

    if (hero.health <= 0) {
        counterStatus += `\n${hero.name} has been defeated!`;
        heroes.splice(heroes.indexOf(hero), 1);
        updateDropdowns(); // Ensure dropdowns reflect the updated heroes
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
    if (!battleStatusElement) return; // Prevent errors if element is missing

    // Do not update status if the game is over
    if (battleOver) return;

    battleStatusElement.textContent = statusText;
}

function showWinScreen() {
    // Hide all game elements
    hideGameElements();

    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>Victory Achieved!</h2>
        <p>Thanos has been vanquished, and the universe is safe once more.</p>
        <p>The forces of evil have been defeated!</p>
        <button onclick="restartGame()">Play Again</button>
    `;
}

function showGameOverScreen(message) {
    // Hide all game elements
    hideGameElements();

    let battleStatus = document.getElementById('battle-status');
    battleStatus.innerHTML = `
        <h2>${message}</h2>
        <button onclick="restartGame()">Try Again</button>
    `;
}

function hideGameElements() {
    // Hide the action controls (dropdowns and buttons)
    document.getElementById('actions').style.display = 'none';

    // Hide the heroes and enemies list
    document.getElementById('hero-stats').style.display = 'none';
    document.getElementById('enemy-stats').style.display = 'none';

}

function restartGame() {
    location.reload();
}

window.onload = function () {
    startBattle();
};
