function afficherFenetreModale() {;
    var modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <p>Souhaitez-vous continuer le questionnaire?</p>
            <button onclick="continuerQuestionnaire()">Oui</button>
            <button onclick="retourAccueil()">Non</button>
        </div>
    `;
    document.body.appendChild(modal);
}

function continuerQuestionnaire() {
    var modal = document.querySelector('.modal');
    modal.parentNode.removeChild(modal);
    resetTimer();
}

var inactivityTimer;
var lastActivityTime = Date.now(); 

function resetTimer() {
    clearTimeout(inactivityTimer);
    lastActivityTime = Date.now(); 
    inactivityTimer = setTimeout(checkInactivity, 10000);
}

function checkInactivity() {
    var currentTime = Date.now();
    var timeSinceLastActivity = currentTime - lastActivityTime;
    if (timeSinceLastActivity >= 10000) {
        afficherFenetreModale();
    }
}

window.addEventListener('click', resetTimer);
window.addEventListener('mousemove', resetTimer);
window.addEventListener('keydown', resetTimer);

resetTimer(); 