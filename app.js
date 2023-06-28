const BASE_URL = "https://fastapi11-z9nc.onrender.com"

// Функція для завантаження контактів і оновлення таблиці
function loadContacts() {
  axios.get(`${BASE_URL}/contacts/`)
    .then(response => {
      const contacts = response.data;
      // Очищення таблиці
      const tableBody = document.getElementById('contactTableBody');
      tableBody.innerHTML = '';

      // Рядки таблиці для кожного контакту
      contacts.forEach(contact => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${contact.Contact.id}</td>
          <td>${contact.Contact.first_name}</td>
          <td>${contact.Contact.last_name}</td>
          <td>${contact.Contact.email}</td>
          <td>${contact.Contact.birthday}</td>
          <td>${contact.Contact.phone_number}</td>
          <td>${contact.Contact.additional_data ?? ""}</td>
          <td><button onclick="showUpdateModal(${contact.Contact.id})">Update</button></td>
          <td><button onclick="deleteContact(${contact.Contact.id})">Delete</button></td>
        `;
        tableBody.appendChild(row);
      });

    })
    .catch(error => {
      console.error('Failed to load contacts:', error);
    });
}

/// Функція для створення нового контакту
async function createContact(event) {
  event.preventDefault();

  const firstNameInput = document.getElementById('firstNameInput');
  const lastNameInput = document.getElementById('lastNameInput');
  const emailInput = document.getElementById('emailInput');
  const phoneNumberInput = document.getElementById('phoneNumberInput');
  const birthdayInput = document.getElementById('birthdayInput');
  const additionalDataInput = document.getElementById('additionalDataInput');

  const newContact = {
    first_name: firstNameInput.value,
    last_name: lastNameInput.value,
    email: emailInput.value,
    phone_number: phoneNumberInput.value,
    birthday: birthdayInput.value,
    additional_data: additionalDataInput.value,
  };

  try {
    const response = await axios.post(`${BASE_URL}/contacts/`, newContact);
    console.log(response);

    createContactForm.reset();
    createContactModal.hide();

    // Завантаження оновленого списку контактів
    loadContacts();
  } catch (error) {
    console.log(error);
  }
}

const createContactForm = document.getElementById('createContactForm');
createContactForm.addEventListener('submit', createContact);
const createContactModal = new bootstrap.Modal(document.getElementById('createContactModal'));

const updateContactForm = document.getElementById('updateContactForm');
updateContactForm.addEventListener('submit', showUpdateModal);
const updateContactModal = new bootstrap.Modal(document.getElementById('updateContactModal'));

// Функція для видалення контакту
async function deleteContact(contactId) {
  try {
    const response = await fetch(`${BASE_URL}/contacts/${contactId}`, {
      method: 'DELETE',
    });

    if (response.ok) {
      console.log('Contact deleted');
      loadContacts();
    } else {
      throw new Error('Failed to delete contact');
    }
  } catch (error) {
    console.error(error);
  }
}

// Функція для редагування контакту
async function updateContact(contactId) {
  try {
    const response = await axios.get(`${BASE_URL}/contacts/${contactId}`);
    const contact = response.data;

    const firstNameInput = document.getElementById('updateFirstNameInput');
    const lastNameInput = document.getElementById('updateLastNameInput');
    const emailInput = document.getElementById('updateEmailInput');
    const phoneNumberInput = document.getElementById('updatePhoneNumberInput');
    const birthdayInput = document.getElementById('updateBirthdayInput');
    const additionalDataInput = document.getElementById('updateAdditionalDataInput');

    firstNameInput.value = contact.first_name;
    lastNameInput.value = contact.last_name;
    emailInput.value = contact.email;
    phoneNumberInput.value = contact.phone_number;
    birthdayInput.value = contact.birthday;
    additionalDataInput.value = contact.additional_data ?? "";

    updateContactForm.onsubmit = async (event) => {
      event.preventDefault();

      const updatedContact = {
        first_name: firstNameInput.value,
        last_name: lastNameInput.value,
        email: emailInput.value,
        phone_number: phoneNumberInput.value,
        birthday: birthdayInput.value,
        additional_data: additionalDataInput.value,
      };

      try {
        const response = await axios.put(`${BASE_URL}/contacts/${contactId}`, updatedContact);
        console.log(response);

        updateContactForm.reset();
        updateContactModal.hide();

        // Завантаження оновленого списку контактів
        loadContacts();
      } catch (error) {
        console.log(error);
      }
    };

    updateContactModal.show();
  } catch (error) {
    console.log(error);
  }
}

function showUpdateModal(contactId) {
  updateContact(contactId);
  updateContactModal.show();
}

// Завантаження контактів під час завантаження сторінки
window.addEventListener('load', () => {
  loadContacts();
});
