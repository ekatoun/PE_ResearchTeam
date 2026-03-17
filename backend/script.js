/* ============================================
   QUESTIONNAIRE PRÉÉCLAMPSIE – script.js
   ============================================ */

/**
 * Calcule l'âge à partir de la date de naissance
 * et remplit automatiquement le champ "Âge actuel".
 */
function calcAge() {
  const dob = document.getElementById('dateNaissance').value;
  if (!dob) return;

  const d = new Date(dob);
  const now = new Date();
  let age = now.getFullYear() - d.getFullYear();
  const m = now.getMonth() - d.getMonth();

  if (m < 0 || (m === 0 && now.getDate() < d.getDate())) {
    age--;
  }

  document.getElementById('ageActuel').value = age > 0 ? age : '';
}

/**
 * Calcule l'IMC à partir du poids (kg) et de la taille (cm),
 * affiche la valeur et la catégorie correspondante.
 */
function calcIMC() {
  const p = parseFloat(document.getElementById('poids').value);
  const t = parseFloat(document.getElementById('taille').value);
  if (!p || !t) return;

  const imc = (p / ((t / 100) ** 2)).toFixed(1);
  document.getElementById('imcInput').value = imc;

  let cat = '';
  if      (imc < 18.5) cat = 'Insuffisance pondérale';
  else if (imc < 25)   cat = 'Poids normal';
  else if (imc < 30)   cat = 'Surpoids';
  else if (imc < 35)   cat = 'Obésité classe I';
  else if (imc < 40)   cat = 'Obésité classe II';
  else                 cat = 'Obésité classe III';

  document.getElementById('imcVal').textContent = imc + ' kg/m²';
  document.getElementById('imcCat').textContent = '– ' + cat;
  document.getElementById('imcCategorie').value = cat;
  document.getElementById('imcResult').classList.add('visible');

  updateProgress();
}

/**
 * Affiche ou masque un bloc conditionnel.
 * @param {string} id   - L'identifiant du bloc HTML
 * @param {boolean} show - true pour afficher, false pour masquer
 */
function toggle(id, show) {
  document.getElementById(id).classList.toggle('visible', show);
  updateProgress();
}

/**
 * Met à jour la barre de progression en fonction des champs remplis.
 */
function updateProgress() {
  const form = document.getElementById('mainForm');
  const inputs = form.querySelectorAll(
    'input[type="radio"][name], input[type="date"], input[type="number"]'
  );

  const names = new Set();
  inputs.forEach(el => names.add(el.name));

  let filled = 0;
  names.forEach(name => {
    const els = form.querySelectorAll(`[name="${name}"]`);
    const answered = Array.from(els).some(el => {
      if (el.type === 'radio' || el.type === 'checkbox') return el.checked;
      return el.value.trim() !== '';
    });
    if (answered) filled++;
  });

  const pct = Math.round((filled / names.size) * 100);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressPct').textContent = pct + '%';
}

/**
 * Collecte toutes les valeurs du formulaire dans un objet plat,
 * en gérant correctement les checkboxes multiples.
 */
function collectFormData() {
  const form = document.getElementById('mainForm');
  const data = {};
  const formData = new FormData(form);

  for (const [key, value] of formData.entries()) {
    const cleanKey = key.replace('[]', '');
    if (key.endsWith('[]')) {
      if (!data[cleanKey]) data[cleanKey] = [];
      data[cleanKey].push(value);
    } else {
      data[key] = value;
    }
  }
  return data;
}

/**
 * Affiche un toast de notification.
 */
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.style.background = type === 'error' ? '#a33057' : '#1a2640';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 4000);
}

/**
 * Gère la soumission du formulaire vers l'API PHP.
 * @param {Event} e
 */
async function handleSubmit(e) {
  e.preventDefault();

  const btn = document.querySelector('.btn-submit');
  btn.textContent = 'Envoi en cours…';
  btn.disabled = true;

  try {
    const data = collectFormData();

    const response = await fetch('/api/reponses/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.success) {
      showToast('✓ Questionnaire enregistré (ID #' + result.id + ')', 'success');
      document.getElementById('progressFill').style.width = '100%';
      document.getElementById('progressPct').textContent = '100%';
      setTimeout(() => {
        if (confirm('Réponse enregistrée. Réinitialiser le formulaire pour une nouvelle saisie ?')) {
          document.getElementById('mainForm').reset();
          document.getElementById('imcResult').classList.remove('visible');
          document.querySelectorAll('.conditional').forEach(el => el.classList.remove('visible'));
          document.getElementById('progressFill').style.width = '0%';
          document.getElementById('progressPct').textContent = '0%';
        }
      }, 1500);
    } else {
      const msgs = result.errors ? result.errors.join('\n') : result.error;
      showToast('⚠ Erreur : ' + msgs, 'error');
    }
  } catch (err) {
    showToast('⚠ Impossible de contacter le serveur.', 'error');
    console.error(err);
  } finally {
    btn.textContent = 'Soumettre le questionnaire';
    btn.disabled = false;
  }
}

/* ── Initialisation ────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('mainForm');
  form.addEventListener('change', updateProgress);
  form.addEventListener('input', updateProgress);
});
