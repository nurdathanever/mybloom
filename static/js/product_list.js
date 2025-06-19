document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.querySelector(".overlay");
    const body = document.body;
    const filterContent = document.getElementById("filterContent");
    const filterSections = document.querySelectorAll(".filter-section");
    const filterOptions = document.querySelectorAll(".filter-options");

    window.toggleFilter = function () {
        const isOpen = filterContent.style.display === "block";
        filterContent.style.display = isOpen ? "none" : "block";
        overlay.style.display = isOpen ? "none" : "block";
        body.classList.toggle("no-scroll", !isOpen);
    };

    // Close filter when clicking overlay
    overlay.addEventListener("click", toggleFilter);

    // Toggle individual filter sections
    window.toggleFilterSection = function (sectionId, event) {
        filterOptions.forEach(option => {
            option.style.display = "none"; // hide all sections
        });
        document.getElementById(sectionId).style.display = "grid"; // show selected

        filterSections.forEach(sec => sec.classList.remove("active")); // remove active class
        if (event) event.target.classList.add("active"); // set active on clicked
    };

    // Initialize first section (Flower Type)
    toggleFilterSection("flower_ingredients");

    // Apply filters and redirect with query params
    window.applyFilters = function () {
        const params = new URLSearchParams();

        // Flower ingredients
        document.querySelectorAll('#flower_ingredients input:checked').forEach(cb => {
            params.append('flower_ingredients', cb.value);
        });

        // Size
        document.querySelectorAll('#bouquet-size input:checked').forEach(cb => {
            params.append('size', cb.value);
        });

        // Seasonality
        document.querySelectorAll('#seasonality input:checked').forEach(cb => {
            params.append('seasonality', cb.value);
        });

        // Style
        document.querySelectorAll('#bouquet-style input:checked').forEach(cb => {
            params.append('style', cb.value);
        });

        // Sort By
        document.querySelectorAll('#sort-by input:checked').forEach(cb => {
            params.append('sort', cb.value);
        });

        // Price Range (custom logic: low, medium, high)
        let priceRanges = [];
        if (document.getElementById('low-price') && document.getElementById('low-price').checked) priceRanges.push('low');
        if (document.getElementById('medium-price') && document.getElementById('medium-price').checked) priceRanges.push('medium');
        if (document.getElementById('high-price') && document.getElementById('high-price').checked) priceRanges.push('high');
        priceRanges.forEach(pr => params.append('price_range', pr));

        window.location.search = params.toString(); // Redirect with query parameters
    };
});


function showBouquetDetails(name, description, price, imageUrl, ingredients, size, seasonality, style) {
    document.getElementById('modalName').innerText = name;
    document.getElementById('modalDescription').innerText = description;
    document.getElementById('modalPrice').innerText = price + ' ₸';
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('modalIngredients').innerText = "Flowers: " + ingredients;
    document.getElementById('bouquetModal').style.display = 'block';
    document.getElementById('modalSize').innerText = size;
    document.getElementById('modalSeasonality').innerText = seasonality;
    document.getElementById('modalStyle').innerText = style;
}

function closeModal() {
    document.getElementById('bouquetModal').style.display = 'none';
}