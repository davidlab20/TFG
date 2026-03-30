AFRAME.registerComponent('drag-controls', {
    schema: {
        mode: { type: 'string', default: 'cursor' }  // Options: 'cursor' or 'vr'
    },

    init: function () {
        this.grabbed = null;
        this.offset = new THREE.Vector3();
        this.distance = 0;

        const el = this.el;  // Controller entity

        const startGrab = (evt) => {
            const raycaster = el.components.raycaster;
            if (!raycaster) return;

            const hits = raycaster.intersections;
            if (!hits.length) return;

            // Find the parent entity with the 'movable' attribute
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

AFRAME.registerComponent('look-at-camera-on-ar', {
  tick: function () {
    if (!this.el.sceneEl.is('ar-mode')) return;

    const cameraEl = this.el.sceneEl.camera.el;
    if (!cameraEl) return;

    const objectPos = new THREE.Vector3();
    const cameraPos = new THREE.Vector3();

    this.el.object3D.getWorldPosition(objectPos);
    cameraEl.object3D.getWorldPosition(cameraPos);

    // Only Y-axis rotation
    const target = new THREE.Vector3(cameraPos.x, objectPos.y, cameraPos.z);
    this.el.object3D.lookAt(target);
  }
});

AFRAME.registerComponent('scale-on-enter-ar', {
    schema: {
        scale: { type: 'string', default: '0.1 0.1 0.1' }
    },
    init: function () {
        const el = this.el;
        const scene = el.sceneEl;

        scene.addEventListener('enter-vr', () => {
            if (scene.is('ar-mode')) {
                el.setAttribute('scale', this.data.scale);

                // Update ar-hit-test mesh's scale
                const hitTest = scene.components['ar-hit-test'];
                if (hitTest) hitTest.bboxNeedsUpdate = true;
            }
        });

        scene.addEventListener('exit-vr', () => {
            el.setAttribute('scale', '1 1 1');
        });
    }
});

AFRAME.registerComponent('show-on-enter-ar', {
  init: function () {
    const scene = this.el.sceneEl;

    const update = () => {
      this.el.object3D.visible = scene.is('ar-mode');
    };

    scene.addEventListener('enter-vr', update);
    scene.addEventListener('exit-vr', update);

    update();
  }
});

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
	// Frequently accessed elements
	let activeSubcharts = {};
	const HUD = document.querySelector('#HUD');
	const HUDPlane = document.querySelector('#HUD-plane')
	const HUDTextsEntity = document.querySelector('#HUD-texts');
	const interactiveAframeElements = 'a-box, a-cylinder, a-sphere';
	const scene = document.querySelector("a-scene");
	const sceneChartsContainer = document.querySelector('#charts');

	// Display information about the element
	function displayInfo(event) {
	    if (!event.detail || !event.detail.intersection) {
            return;
        }

		const targetElement = event.target;
        targetElement.setAttribute('scale', '1.1 1.1 1');

        const HUDInfo = targetElement.getAttribute('info');
        if (!HUDInfo) return;
        const HUDTexts = HUDInfo.split(';');

        const camera = document.querySelector('#camera');
        const cameraPos = new THREE.Vector3();
        camera.object3D.getWorldPosition(cameraPos);

        // Object's bounding box
        const bbox = new THREE.Box3().setFromObject(targetElement.object3D);
        const objectCenter = new THREE.Vector3();
        bbox.getCenter(objectCenter);

        const objectSize = new THREE.Vector3();
        bbox.getSize(objectSize);

        // HUD's bounding box
        const HUDHeightPerElement = 0.3;
        const HUDHeight = HUDHeightPerElement * HUDTexts.length;
        HUDPlane.setAttribute('height', HUDHeight);

        const hudBBox = new THREE.Box3().setFromObject(HUD.object3D);
        const hudSize = new THREE.Vector3();
        hudBBox.getSize(hudSize);

        const dirToCamera = new THREE.Vector3().subVectors(cameraPos, objectCenter).normalize();

        const distance = (objectSize.z / 2) + (hudSize.z / 2);

        // Final HUD's position
        const hudPos = objectCenter.clone().add(dirToCamera.multiplyScalar(distance));
        hudPos.y = bbox.max.y + (hudSize.y / 2);

        HUD.object3D.position.copy(hudPos);
        HUD.object3D.lookAt(cameraPos);
        HUD.setAttribute('visible', 'true');

        // Clean the previous HUD content
        while (HUDTextsEntity.firstChild) {
			HUDTextsEntity.removeChild(HUDTextsEntity.firstChild);
		}

		// Add the new HUD content
		let yOffset = HUDHeight / 2 - HUDHeightPerElement / 2;
        HUDTexts.forEach(text => {
        	const textEntity = document.createElement('a-text');
        	textEntity.setAttribute('value', text);
        	textEntity.setAttribute('position', `0 ${yOffset} 0`);
        	textEntity.setAttribute('scale', '0.7 0.7 0.7');
        	textEntity.setAttribute('align', 'center');
        	HUDTextsEntity.appendChild(textEntity);

        	yOffset -= HUDHeightPerElement;
        });
    }

	// Set the element to its original state
	function returnToOriginal(event) {
	    event.target.setAttribute('scale', '1 1 1');
	    HUD.setAttribute('visible', 'false');  // Hide the HUD
	}

	// Subcharts
	function displaySubchart(event) {
	    const paramName = event.target.getAttribute('activates-param');
	    if (!paramName) return;
	    const groupName = paramName.split('__')[0];  // Format is {groupName}__{values}

	    // Initialize group if not existing
	    if (!activeSubcharts[groupName]) {
            activeSubcharts[groupName] = [];
        }

	    activeSubcharts[groupName].forEach(chart => {
            chart.setAttribute('visible', 'false');

            // Remove 'raycastable' from all children of the subchart
            const children = chart.querySelectorAll(interactiveAframeElements);
            children.forEach(child => child.removeAttribute('raycastable'));
        });

        activeSubcharts[groupName] = [];  // Clear the current group's subcharts

        const targetCharts = document.querySelectorAll(`[param-name='${paramName}']`);
        targetCharts.forEach(chart => {
            chart.setAttribute('visible', 'true');

            // Add 'raycastable' to all children of the subchart
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

    scene.addEventListener("exit-vr", () => {
        sceneChartsContainer.object3D.position.set(0,0,0);
        sceneChartsContainer.object3D.rotation.set(0,0,0);
    });

    scene.addEventListener("ar-hit-test-select", () => {
        const hitTest = scene.components["ar-hit-test"];
        if (hitTest) {
            hitTest.data.enabled = false;  // Deactivates ar-hit-test
            hitTest.hitTest = null;

            if (hitTest.bboxMesh) hitTest.bboxMesh.visible = false;  // Hides the reticle
        }
    });
});