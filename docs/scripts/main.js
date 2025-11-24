// Wait for the scene content to load completely
document.addEventListener('DOMContentLoaded', () => {
	// Frequently accessed elements
	const plainLabel = document.getElementById('plainLabel')
	const textLabel = document.getElementById('label')

	// Offsets
	const OFFSETS = {
        PLAIN_Y: 2.25,
        PLAIN_Z: 1.1,
        LABEL_X_REL: -1.1, // Relative X offset from the plainLabel position
        LABEL_Y_REL: 0.25   // Relative Y offset from the plainLabel position
    };

	// Display information about the element
	function displayInfo(event) {
		const targetElement = event.target;

	    const objectPosition = new THREE.Vector3();
		objectPosition.setFromMatrixPosition(targetElement.object3D.matrixWorld);

	    event.target.setAttribute('scale', '1.1 1.1 1.1');  // Size the scale up

	    const plainPos = {
            x: objectPosition.x,
            y: objectPosition.y + OFFSETS.PLAIN_Y,
            z: objectPosition.z + OFFSETS.PLAIN_Z
        };

        const labelPos = {
            x: plainPos.x + OFFSETS.LABEL_X_REL,
            y: plainPos.y + OFFSETS.LABEL_Y_REL,
            z: plainPos.z
        };

	    const value = event.target.getAttribute('id')

		// Update plain label attributes
        plainLabel.setAttribute('position', plainPos);
        plainLabel.setAttribute('visible', 'true');

	    // Update text label attributes
        textLabel.setAttribute('position', labelPos);
        textLabel.setAttribute('value', value);
        textLabel.setAttribute('visible', 'true');
	}

	// Set the element to its original state
	function returnToOriginal(event) {
	    event.target.setAttribute('scale', '1 1 1');
	    plainLabel.setAttribute('visible', 'false');  // Hide plain
	    textLabel.setAttribute('visible', 'false');  // Hide text
	}

    const interactiveElements = document.querySelectorAll('a-box, a-cylinder, a-sphere');

    // Asignar eventos en un solo bucle
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', displayInfo);
        element.addEventListener('mouseleave', returnToOriginal);
    });
});