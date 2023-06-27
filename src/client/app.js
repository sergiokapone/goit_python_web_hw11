// Функція для завантаження контактів і оновлення таблиці
function loadContacts() {
  axios.get('http://localhost:8000/contacts/')
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
    const response = await axios.post('http://localhost:8000/contacts/', newContact);
    console.log(response);

  
    createContactForm.reset();


    // Завантаження оновленого списку контактів
    loadContacts();
  } catch (error) {
    console.log(error);
  }
}

const createContactForm = document.getElementById('createContactForm');
createContactForm.addEventListener('submit', createContact);





// Функція для видалення контакту
async function deleteContact(contactId) {
  try {
    const response = await fetch(`http://localhost:8000/contacts/${contactId}`, {
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
async function editContact(contactId) {

}

// завантаження контактів під час завантаження сторінки
window.addEventListener('load', () => {
  loadContacts();
});
