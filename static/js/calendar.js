const daysContainer = document.getElementById("days");
const monthYear = document.getElementById("monthYear");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let date = new Date();

const markedDates = [
  { day: 29, month: 10, year: 2025 },  
];

/* No JavaScript, os meses começam do zero:
    janeiro: 0
    favereiro: 1
    ...
*/


function renderCalendar() {
  const year = date.getFullYear();
  const month = date.getMonth();

  const firstDay = new Date(year, month, 1).getDay();
  const totalDays = new Date(year, month + 1, 0).getDate();

  monthYear.textContent = date.toLocaleString("pt-BR", {
    month: "long",
    year: "numeric",
  });

  daysContainer.innerHTML = "";

  for (let i = 0; i < firstDay; i++) {
    daysContainer.innerHTML += `<div></div>`;
  }

  for (let day = 1; day <= totalDays; day++) {
    const isToday =
      day === new Date().getDate() &&
      month === new Date().getMonth() &&
      year === new Date().getFullYear();

    const isMarked = markedDates.some(d =>
      d.day === day && d.month === month && d.year === year
    );

    daysContainer.innerHTML += `
      <div class="
        ${isToday ? 'today' : ''} 
        ${isMarked ? 'marked' : ''}
      ">
        ${day}
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', () => {
    const resultadoStep = document.getElementById('resultado-step');
    const viewResultBtn = document.getElementById('viewResultBtn');

    if (resultadoStep && resultadoStep.classList.contains('active')) {
        viewResultBtn.classList.remove('disabled');
        viewResultBtn.onclick = () => {
            window.location.href = '/html/resultados.html';
        };
    }
});

prevBtn.onclick = () => {
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
};

nextBtn.onclick = () => {
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
};


renderCalendar();
