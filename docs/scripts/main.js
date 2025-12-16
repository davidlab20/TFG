// Wait for the scene content to load completely
document.addEventListener('DOMContentLoaded', () => {
	// Frequently accessed elements
	const labelInfo = document.getElementById('labelInfo')
	const textLabel = document.getElementById('textLabel')

	// Offsets
	const OFFSETS = {
		PLAIN_Y: 2.25,
        PLAIN_Z: 1.1,
    };

	// Display information about the element
	function displayInfo(event) {
		const targetElement = event.target;

	    const objectPosition = new THREE.Vector3();
		objectPosition.setFromMatrixPosition(targetElement.object3D.matrixWorld);

	    event.target.setAttribute('scale', '1.1 1.1 1.1');  // Size the scale up

	    const labelInfoPos = {
            x: objectPosition.x,
            y: objectPosition.y + OFFSETS.PLAIN_Y,
            z: objectPosition.z + OFFSETS.PLAIN_Z
        };

        const value = event.target.getAttribute('id')

		// Update label info attributes
        labelInfo.setAttribute('position', labelInfoPos);
        labelInfo.setAttribute('visible', 'true')

	    // Update text label attributes
        textLabel.setAttribute('value', value);
	}

	// Set the element to its original state
	function returnToOriginal(event) {
	    event.target.setAttribute('scale', '1 1 1');
	    labelInfo.setAttribute('visible', 'false');  // Hide label info
	}

    const interactiveElements = document.querySelectorAll('a-box, a-cylinder, a-sphere');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', displayInfo);
        element.addEventListener('mouseleave', returnToOriginal);
    });
});