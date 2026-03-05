AFRAME.registerComponent('drag-controls', {
    schema: {
        mode: { type: 'string', default: 'cursor' }  // Options: cursor / vr
    },

    init: function () {
        this.grabbed = null;
        this.offset = new THREE.Vector3();
        this.distance = 0;

        const el = this.el;  // Controller

        const startGrab = (evt) => {
            const raycaster = el.components.raycaster;
            if (!raycaster) return;

            const hits = raycaster.intersections;
            if (!hits.length) return;

            // Grab the parent with attribute 'movable'
            let grabbedEl = hits[0].object.el;
            while (grabbedEl && !grabbedEl.hasAttribute('movable')) {
                grabbedEl = grabbedEl.parentEl;
            }
            if (!grabbedEl) return;

            this.grabbed = grabbedEl;
            this.distance = hits[0].distance;

            const hitPoint = hits[0].point;
            const objPos = this.grabbed.object3D.position;
            this.offset.copy(objPos).sub(hitPoint);
        };

        const stopGrab = () => {
            this.grabbed = null;
        };

        if (this.data.mode === 'cursor') {  // Desktop
            el.addEventListener('mousedown', startGrab);
            el.addEventListener('mouseup', stopGrab);
        }

        if (this.data.mode === 'vr') {  // VR controls
            el.addEventListener('gripdown', startGrab);
            el.addEventListener('gripup', stopGrab);
        }
    },

    tick: function () {
        if (!this.grabbed) return;

        const ray = this.el.components.raycaster.raycaster.ray;
        const pos = new THREE.Vector3();
        pos.copy(ray.origin);
        pos.add(ray.direction.clone().multiplyScalar(this.distance));  // position = origin + direction * distance
        pos.add(this.offset);

        this.grabbed.object3D.position.copy(pos);  // Move the object in the new position
    }
});

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
	    targetElement.setAttribute('scale', '1.1 1.1 1');  // Size the scale up
        const value = targetElement.getAttribute('info');
        if (!value) return;  // Return if the target element has not attribute 'info' (for movable objects)

        const camera = document.getElementById('camera');
        targetElement.object3D.updateMatrixWorld();
        camera.object3D.updateMatrixWorld();

        const position = new THREE.Vector3();
        targetElement.object3D.getWorldPosition(position);

		let y_offset = 0;
        let z_offset = 0;
        if (targetElement.tagName.toLowerCase() === 'a-box') {  // Bars chart
            let height = parseFloat(targetElement.getAttribute('height'));
            let depth = parseFloat(targetElement.getAttribute('depth'));
            y_offset = height / 2;
            z_offset = depth / 2;
        } else if (targetElement.tagName.toLowerCase() === 'a-sphere') {  // Point chart
            let radius = parseFloat(targetElement.getAttribute('radius'));
            y_offset = radius;
            z_offset = radius;
        } else if (targetElement.tagName.toLowerCase() === 'a-cylinder') {  // Pie chart
            let radius = parseFloat(targetElement.getAttribute('radius'));
            let depth = parseFloat(targetElement.getAttribute('height'));  // Using height, slices are rotated cylinders
            y_offset = radius;
            z_offset = depth / 2;
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

	    // Update HUD text attributes
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
	    if (!paramName) return;
	    const groupName = paramName.split('__')[0]  // Format is {groupName}__{values}

	    // Initialize group if not existing
	    if (!activeSubcharts[groupName]) {
            activeSubcharts[groupName] = [];
        }

	    activeSubcharts[groupName].forEach(chart => {
            chart.setAttribute('visible', 'false');

            // Remove raycastable for every children of the subchart
            const children = chart.querySelectorAll(interactiveAframeElements);
            children.forEach(child => child.removeAttribute('raycastable'));
        });

        activeSubcharts[groupName] = [];  // Clean actual group subcharts

        const targetCharts = document.querySelectorAll(`[param-name='${paramName}']`);
        targetCharts.forEach(chart => {
            chart.setAttribute('visible', 'true');

            // Add raycastable for every children of the subchart
            const children = chart.querySelectorAll(interactiveAframeElements);
            children.forEach(child => child.setAttribute('raycastable', ''));

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