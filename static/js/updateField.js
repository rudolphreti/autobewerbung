function updateField(index, field, value) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch('/update_field', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
          index: index,
          field: field,
          value: value,
      }),
  })
  .then((response) => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then((data) => {
      if (data.status !== 'success') {
          alert('Failed to update the field');
      }
  })
  .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while updating the field.');
  });
}
