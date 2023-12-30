// scripts for the templates
// so far just medication request has scrips
// Please oh please gods of coding guide me, I have gone beyond what I know and am making google assisted guesses

// Event listener and action url updater for changes to workflow selection
document.getElementById("select_workflow").addEventListener("change", configureWorkflow)
function configureWorkflow() {
        var selectedWorkflow = document.getElementById("select_workflow");
        var form = document.getElementById("enc_setup");
        form.action = `/encounter/${selectedWorkflow}`;
}


// For medication request, to confirm it after seeing issues
function confirmRequest() {
    alert('Confirmed Medication Request!');
    var provider = {{ provider }};
    window.location.href = "{{ url_for('setup_encounter', user_name=provider) }}";
}

// For medication request, to unlock form for editing and submitting a new medication request
function redoRequest() {
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('confirmBtn').classList.add('hidden');
    document.getElementById('redoBtn').classList.add('hidden');
}

// Listener to form submissions, locks form and unhides 2 buttons - Confirm, Redo
document.getElementById('submitBtn').addEventListener('click', function () {
    this.disabled = true;
    document.getElementById('confirmBtn').classList.remove('hidden');
    document.getElementById('redoBtn').classList.remove('hidden');
});