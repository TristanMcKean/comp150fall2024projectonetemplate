let currentEnemies = [
    { name: 'Loki', health: 100, attackPower: 10 },
    { name: 'Ultron', health: 100, attackPower: 15 }
];

let heroes = [
    { name: 'Iron Man', health: 100 },
    { name: 'Captain America', health: 120 },
    { name: 'Thor', health: 150 }
];

let battleOver = false;
let thanosDefeated = false;

function startBattle() {
    displayHeroes();
    displayEnemies();
}

function displayHeroes() {
    let heroesList = document.getElementById('heroes-list');
    heroesList.innerHTML = '';
    heroes.forEach(hero => {
        let li = document.createElement('li');
        li.textContent = `${hero.name} - HP: ${hero.health}`;
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

function performAction(action) {
    if (battleOver) return;
    if (action === 'attack') attackEnemy();
    else if (action === 'special') useSpecialMove();
}

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

    let counterStatus = enemyCounterAttack(hero);
    displayEnemies();
    displayHeroes();
    updateBattleStatus(`${battleStatus}\n${counterStatus}`);
    checkHeroesHealth();
}

function useSpecialMove() {
    let enemy = currentEnemies[0];
    let hero = heroes[0];

    let specialMoveDamage = getRandomDamage(40, 60);
    enemy.health -= specialMoveDamage;

    let battleStatus = `${hero.name} uses a special move against ${enemy.name}!`;
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

    let counterStatus = enemyCounterAttack(hero);
    displayEnemies();
    displayHeroes();
    updateBattleStatus(`${battleStatus}\n${counterStatus}`);
    checkHeroesHealth();
}

function updateBattleStatus(statusText) {
    let battleStatusElement = document.getElementById('battle-status');
    battleStatusElement.textContent = statusText;
}

function enemyCounterAttack(hero) {
    let enemy = currentEnemies[0];
    let counterAttackDamage = getRandomDamage(enemy.attackPower - 5, enemy.attackPower + 5);
    hero.health -= counterAttackDamage;

    let counterStatus = `${enemy.name} counter-attacks ${hero.name} for ${counterAttackDamage} damage!`;

    if (hero.health <= 0) {
        counterStatus += `\n${hero.name} has been defeated!`;
        heroes = heroes.filter(h => h !== hero);
    }

    return counterStatus;
}

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

function getRandomDamage(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
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

window.onload = function() {
    startBattle();
};
