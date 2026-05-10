let sections = [

  {
    title: "Arrival in Paris",
    description:
      "Flight to Paris, hotel check-in and evening at leisure near Eiffel Tower.",
    startDate: "2026-06-10",
    endDate: "2026-06-14",
    budget: 800,
    location: "Paris, France"
  },

  {
    title: "Explore Rome",
    description:
      "Visit major attractions, Colosseum tour and local food experience.",
    startDate: "2026-06-15",
    endDate: "2026-06-20",
    budget: 1200,
    location: "Rome, Italy"
  },

  {
    title: "Venice Getaway",
    description:
      "Enjoy gondola rides, canals and Murano island tour.",
    startDate: "2026-06-21",
    endDate: "2026-06-24",
    budget: 900,
    location: "Venice, Italy"
  }

];

let currentEditIndex = null;

function renderSections(){

  const container =
    document.getElementById("sectionsContainer");

  container.innerHTML = "";

  sections.forEach((section, index) => {

    container.innerHTML += `

      <div class="section-card">

        <div class="section-top">

          <div class="left-section">

            <div class="number">
              ${index + 1}
            </div>

            <div class="section-content">

              <h2>
                Section ${index + 1}: ${section.title}
              </h2>

              <p>
                ${section.description}
              </p>

            </div>

          </div>

          <div class="actions">

            <button class="icon-btn"
              onclick="editSection(${index})">

              <i class="fa-solid fa-pen"></i>

            </button>

            <button class="icon-btn delete"
              onclick="deleteSection(${index})">

              <i class="fa-regular fa-trash-can"></i>

            </button>

          </div>

        </div>

        <div class="info-row">

          <div class="info-box">

            <i class="fa-regular fa-calendar"></i>

            <div>

              <div class="info-label">
                Date Range
              </div>

              <div class="info-value">

                ${formatDate(section.startDate)}
                -
                ${formatDate(section.endDate)}

              </div>

            </div>

          </div>

          <div class="info-box">

            <i class="fa-solid fa-wallet"></i>

            <div>

              <div class="info-label">
                Budget of this section
              </div>

              <div class="info-value">
                $ ${section.budget}
              </div>

            </div>

          </div>

        </div>

      </div>
    `;
  });
}

function formatDate(dateString){

  const date = new Date(dateString);

  return date.toLocaleDateString("en-GB", {
    day:"2-digit",
    month:"short",
    year:"numeric"
  });
}

function openModal(){

  document.getElementById("modal")
    .style.display = "flex";
}

function closeModal(){

  document.getElementById("modal")
    .style.display = "none";
}

function editSection(index){

  currentEditIndex = index;

  const section = sections[index];

  document.getElementById("titleInput")
    .value = section.title;

  document.getElementById("descriptionInput")
    .value = section.description;

  document.getElementById("startDateInput")
    .value = section.startDate;

  document.getElementById("endDateInput")
    .value = section.endDate;

  document.getElementById("budgetInput")
    .value = section.budget;

  document.getElementById("locationInput")
    .value = section.location;

  openModal();
}

function saveChanges(){

  sections[currentEditIndex].title =
    document.getElementById("titleInput").value;

  sections[currentEditIndex].description =
    document.getElementById("descriptionInput").value;

  sections[currentEditIndex].startDate =
    document.getElementById("startDateInput").value;

  sections[currentEditIndex].endDate =
    document.getElementById("endDateInput").value;

  sections[currentEditIndex].budget =
    document.getElementById("budgetInput").value;

  sections[currentEditIndex].location =
    document.getElementById("locationInput").value;

  renderSections();

  closeModal();
}

function deleteSection(index){

  const confirmDelete =
    confirm("Delete this section?");

  if(confirmDelete){

    sections.splice(index, 1);

    renderSections();

    closeModal();
  }
}

function addSection(){

  sections.push({

    title:"New Section",

    description:
      "Add your trip details here.",

    startDate:"2026-07-01",

    endDate:"2026-07-05",

    budget:500,

    location:"New Destination"
  });

  renderSections();
}

window.onclick = function(e){

  const modal =
    document.getElementById("modal");

  if(e.target === modal){

    closeModal();
  }
};

renderSections();