// Wait for the scene content to load completely
document.addEventListener('DOMContentLoaded', (event) => {

	// Size up the scale of the element
	function getBigger(event) {
	    event.target.setAttribute('scale', '1.1 1.1 1.1');
	}

	// Set the scale of the element to its original value
	function originalScale(event) {
	    event.target.setAttribute('scale', '1 1 1');
	}

	const boxes = document.querySelectorAll('a-box');
	const spheres = document.querySelectorAll('a-sphere')

	// Events for boxes
	boxes.forEach(box => {
		box.addEventListener('mouseenter', getBigger);
		box.addEventListener('mouseleave', originalScale);
	})

	// Events for spheres
	spheres.forEach(sphere => {
		sphere.addEventListener('mouseenter', getBigger);
		sphere.addEventListener('mouseleave', originalScale);
	})
});