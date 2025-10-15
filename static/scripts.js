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
// Загрузка аватарки
document.getElementById('avatar-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatar-preview').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

// Создание персонажа
function createCharacter() {
    const name = document.getElementById('character-name').value;
    const avatar = document.getElementById('avatar-preview').src;
    
    if (!name) {
        alert('Please enter character name');
        return;
    }
    

    const newCharacter = document.createElement('div');
    newCharacter.id = 'block';
    newCharacter.innerHTML = `
        <div><img id="avatar" src="${avatar}"></div>
        <div>${name}</div>
        <div>Rename</div>
        <div>Delete</div>
    `;
    

    document.getElementById('panel').insertBefore(newCharacter, document.getElementById('panel').children[1]);
    

    document.getElementById('character-name').value = '';
    document.getElementById('avatar-preview').src = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPtCBdlq4hR6jNFFtkxEYrgJoOgnsMgKp3PQ&s';
    
    alert('Character created: ' + name);
}