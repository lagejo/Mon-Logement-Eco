function showForm(formId) {
    // Hide all forms
    const forms = ['capteurForm', 'pieceForm', 'logementForm', 'suppressionForm'];
    forms.forEach(id => {
        const form = document.getElementById(id);
        if (form) {
            form.style.display = 'none';
        }
    });

    // Show the selected form
    const selectedForm = document.getElementById(formId);
    if (selectedForm) {
        selectedForm.style.display = 'block';
    }
}

