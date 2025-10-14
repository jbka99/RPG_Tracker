fetch("/character")
  .then(response => response.json())
  .then(data => {
    renderCharacter(data);
    renderStats(data);
  });

function renderStats(data) {
  document.getElementById('stats').innerHTML = `
  <p><b>Stats:</b></p>${Object.entries(data.stats)}</p>
      <p>
      <button id="stat_synt_up">+</button>
      <button id="stat_synt_down">-</button>
      </p>
  `;
  document.getElementById('stat_synt_up').addEventListener('click', () => updateStat(true));
  document.getElementById('stat_synt_down').addEventListener('click', () => updateStat(false));
}

function renderCharacter(data) {
  document.getElementById('character').innerHTML = `
    <p><b>Name:</b></p><p>${data.name}</p>
    <p><b>Class:</b></p><p>${data.rank}</p>
    <p><b>Level:</b></p><p>${data.level}</p>
      <p>
      <button id="level-up">+</button>
      <button id="level-down">-</button>
      </p>
    <p><b>Age:</b></p><p>${data.age}</p>
      
  `;
  document.getElementById('level-up').addEventListener('click', () => updateLevel(true));
  document.getElementById('level-down').addEventListener('click', () => updateLevel(false));
}

function updateLevel(up) {
  fetch('/character', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(up ? { level_up: true } : { level_down: true })
  })
  .then(res => res.json())
  .then(data => renderCharacter(data));
}
  
function updateStat(up) {
  fetch('/character', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(up ? { stat_synt_up: true } : { stat_synt_down: true })
  })
  .then(res => res.json())
  .then(data => renderCharacter(data));
}

fetch('/create', {
  method: 'POST',
  body: JSON.stringify({
    name: InputValue
  })
})

fetch('/delete', {
  method: 'POST',
  name
})