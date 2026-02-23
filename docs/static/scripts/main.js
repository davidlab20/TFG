// Wait for the scene content to load completely
document.addEventListener('DOMContentLoaded', () => {
	// Frequently accessed elements
	let activeSubcharts = {};
	const HUD = document.getElementById('HUD');
	const HUDText = document.getElementById('HUD-text');
	const interactiveAframeElements = 'a-box, a-cylinder, a-sphere'

	// Display information about the element
	function displayInfo(event) {
		const targetElement = event.target;
        const camera = document.getElementById('camera');
        targetElement.object3D.updateMatrixWorld();
        camera.object3D.updateMatrixWorld();

        const position = new THREE.Vector3();
        targetElement.object3D.getWorldPosition(position);

		let y_offset = 0;
        let z_offset = 0;
        if (targetElement.tagName.toLowerCase() === 'a-box') {  // Bars chart
            let height = parseFloat(targetElement.getAttribute('height'));
            const depth = parseFloat(targetElement.getAttribute('depth'));
            y_offset = height / 2;
            z_offset = depth / 2;
        } else if (targetElement.tagName.toLowerCase() === 'a-sphere') {  // Point chart
            let radius = parseFloat(targetElement.getAttribute('radius'));
            y_offset = radius;
            z_offset = radius;
        } else if (targetElement.tagName.toLowerCase() === 'a-cylinder') {  // Pie chart
            let radius = parseFloat(targetElement.getAttribute('radius'));
            y_offset = radius;
            z_offset = 0;
        }

		// Update HUD attributes
		HUD.setAttribute('position', {
            x: position.x,
            y: position.y + y_offset + 1,
            z: position.z + z_offset + 0.1
        });
        HUD.setAttribute('visible', 'true');
        const cameraPos = new THREE.Vector3();
        camera.object3D.getWorldPosition(cameraPos);
        HUD.object3D.lookAt(cameraPos);

	    targetElement.setAttribute('scale', '1.1 1.1 1');  // Size the scale up

	    // Update HUD text attributes
        const value = targetElement.getAttribute('info');
        HUDText.setAttribute('value', value);
	}

	// Set the element to its original state
	function returnToOriginal(event) {
	    event.target.setAttribute('scale', '1 1 1');
	    HUD.setAttribute('visible', 'false');  // Hide HUD display
	}

	// Subcharts
	function displaySubchart(event) {
	    const paramName = event.target.getAttribute('activates-param');
	    const groupName = paramName.split('__')[0]  // Format is {groupName}__{values}

	    // Initialize group if not existing
	    if (!activeSubcharts[groupName]) {
            activeSubcharts[groupName] = [];
        }

	    activeSubcharts[groupName].forEach(chart => {
            chart.setAttribute('visible', 'false');

            // Remove data-raycastable for every children of the subchart
            const children = chart.querySelectorAll(interactiveAframeElements);
            children.forEach(child => child.removeAttribute('data-raycastable'));
        });

        activeSubcharts[groupName] = [];  // Clean actual group subcharts

        const targetCharts = document.querySelectorAll(`[param-name='${paramName}']`);
        targetCharts.forEach(chart => {
            chart.setAttribute('visible', 'true');

            // Add data-raycastable for every children of the subchart
            const children = chart.querySelectorAll(interactiveAframeElements);
            children.forEach(child => child.setAttribute('data-raycastable', ''));

            activeSubcharts[groupName].push(chart);
        });
	}

    const interactiveElements = document.querySelectorAll(interactiveAframeElements);
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', displayInfo);
        element.addEventListener('mouseleave', returnToOriginal);
        element.addEventListener('click', displaySubchart);
    });
});