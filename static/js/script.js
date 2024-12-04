function showForm(formId) {
    // Hide all forms
    document.getElementById('capteurForm').style.display = 'none';
    document.getElementById('pieceForm').style.display = 'none';
    document.getElementById('logementForm').style.display = 'none';

    // Show the selected form
    document.getElementById(formId).style.display = 'block';
}