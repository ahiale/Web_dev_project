// let login = document.querySelector(".login-form");

/*document.querySelector("#login-btn").onclick = () =>{
    login.classList.toggle('active');
    navbar.classList.remove('active');
}*/

let navbar = document.querySelector(".navbar");

// document.querySelector('#menu-btn').onclick = () =>{
//     login.classList.remove('active');
//     navbar.classList.toggle('active');
// }

window.onscroll = () =>{
    // login.classList.remove('active');
    navbar.classList.remove('active');
}

// var swiper = new Swiper(".gallery-slider", {
//     grabCursor:true,
//     loop:true,
//     centeredSlides:true,
//     spaceBetween:20,
//     navigation: {
//         nextEl: ".swiper-button-next",
//         prevEl: ".swiper-button-prev",
//     },
//     breakpoints: {
//         0:{
//             slidesPerView:1,
//         },
//         700:{
//             slidesPerView:2,
//         },
//     }
// }) 

// URL de l'API
const API_URL = 'http://127.0.0.1:8000/biome/biomes'; 

const biomesContainer = document.querySelector('.biomes-container');

// Fonction pour récupérer et afficher les biomes
async function fetchAndDisplayBiomes() {
    try {
        const response = await fetch(API_URL);
        const biomes = await response.json();

        biomes.forEach(biome => {
            const biomeCard = document.createElement('div');
            biomeCard.className = 'biome-card';
            biomeCard.style.backgroundColor = biome.color; 
            biomeCard.textContent = biome.name;

            // Rediriger vers la page des enclos lorsque le biome est cliqué
            biomeCard.addEventListener('click', () => {
                window.location.href = `enclos.html?biomeId=${biome.id}`; // Passer l'ID du biome dans l'URL
            });

            biomesContainer.appendChild(biomeCard);
        });
    } catch (error) {
        console.error('Erreur lors de la récupération des biomes:', error);
    }
}

window.addEventListener('DOMContentLoaded', fetchAndDisplayBiomes);

document.addEventListener('DOMContentLoaded', function () {
    const userSection = document.getElementById('userSection');
    const userName = document.getElementById('userName');
    const logoutBtn = document.getElementById('logoutBtn');
    const registerLink = document.getElementById('registerLink');
    const loginLink = document.getElementById('loginLink');

    // Vérifier si l'utilisateur est connecté
    const prenom = localStorage.getItem('prenom');

    if (prenom) {
        // Afficher le prénom et masquer les liens "sign up" et "login"
        userName.textContent = `hey, ${prenom}`;
        userSection.classList.remove('hidden');
        registerLink.classList.add('hidden');
        loginLink.classList.add('hidden');

        // Ajouter un événement pour le bouton de déconnexion
        logoutBtn.addEventListener('click', function () {
            // Effacer le localStorage
            localStorage.clear();

            // Recharger la page pour revenir à l'état non connecté
            window.location.reload();
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const pricingLink = document.querySelector('a[href="ticket.html"]'); 
    const token = localStorage.getItem('token'); 
    
    pricingLink.addEventListener('click', (event) => {
        if (!token) { 
            event.preventDefault(); 
            window.location.href = 'login.html'; 
        }
    });
});

function openModal(service) {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modal-content');
  
    const routes = {
      "Restroom": "From the main entrance, follow the signs to the central area.",
      "Water Point": "Follow the main path to the fountain marked with green signs.",
      "Snack Bar": "Head towards the cafeteria near the large lake.",
      "Cafe": "Take the main trail to the beverage kiosk.",
      "Restaurant": "Cross the central area to reach the main cafeteria.",
      "Hut": "Walk towards the central beach with wooden parasols.",
      "Shop": "Follow the signs to the souvenir center.",
      "Picnic Area": "Follow the path to the shaded tables at the back of the park.",
      "Parking": "Park in the main entrance parking area.",
      "Playground": "Walk towards the playground with colorful swings.",
      "Scenic Viewpoint": "Follow the elevated trail to the viewpoint."
    };
  
    modalContent.innerText = routes[service];
    modal.classList.remove('hidden');
  }
  
  function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.add('hidden');
  }