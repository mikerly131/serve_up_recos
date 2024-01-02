// scripts for the templates
// so far just medication request has scrips
// Please oh please gods of coding guide me, I have gone beyond what I know and am making google assisted guesses
// Emptying this garbage, too many failed attempts.

var medicationSelect = document.getElementById('new_medication')
var brandSelect = document.getElementById('new_market_med')
var brandSelectName = document.getElementById('brand_name')

function loadBrands() {

    const selectedMedication = medicationSelect.value

    brandSelect.innerHTML = '<option value="">Select Brand</option>'

    fetch(`/get_brand_names/${selectedMedication}`)
        .then(response => response.json())
        .then(data => {
            const brands = data.brand_names;
            brands.forEach(brand => {
                const option = document.createElement('option')
                option.value = brand.id
                option.textContent = brand.brand_name
                brandSelect.appendChild(option)
            })
        })
    .catch(error => console.error('Error loading brands:', error))
}

// Add event listener to the brandSelect dropdown to update the hidden input
brandSelect.addEventListener('change', function () {
    var selectedBrandName = brandSelect.options[brandSelect.selectedIndex];
    brandSelectName.value = selectedBrandName.textContent;
});


document.addEventListener('DOMContentLoaded', function () {
    // This function will be called once the DOM is ready
    loadBrands();
});





