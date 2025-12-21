// Wait for the scene content to load completely
document.addEventListener('DOMContentLoaded', () => {
	// Frequently accessed elements
	const HUD = document.getElementById('HUD')
	const HUDText = document.getElementById('HUD-text')

	// Display information about the element
	function displayInfo(event) {
		const targetElement = event.target;

	    event.target.setAttribute('scale', '1.1 1.1 1.1');  // Size the scale up

        const value = event.target.getAttribute('id')

		// Update HUD attributes
        HUD.setAttribute('visible', 'true')

	    // Update HUD text attributes
        HUDText.setAttribute('value', value);
	}

	// Set the element to its original state
	function returnToOriginal(event) {
	    event.target.setAttribute('scale', '1 1 1');
	    HUD.setAttribute('visible', 'false');  // Hide HUD display
	}

    const interactiveElements = document.querySelectorAll('a-box, a-cylinder, a-sphere');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', displayInfo);
        element.addEventListener('mouseleave', returnToOriginal);
    });
});