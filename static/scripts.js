const video = document.getElementById('camera');

    async function setupCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (error) {
            console.error('Error accessing the camera:', error);
            alert('Camera access is required to take the test.');
        }
    }

    // Load BlazeFace model for face detection
    let model;
    async function loadModel() {
        model = await blazeface.load();
    }

    // Detect inappropriate movements
    async function detectInappropriateMovements() {
        if (!model) return;

        const predictions = await model.estimateFaces(video, false);
        if (predictions.length === 0) {
            // No face detected (user is not looking at the screen)
            handleTestFailure('No face detected.');
        } else if (predictions.length > 1) {
            // Multiple faces detected (potential cheating)
            handleTestFailure('Multiple faces detected.');
        }
    }

    // Handle test failure
    function handleTestFailure(reason) {
        alert(`Test failed: ${reason}`);
        document.querySelector('.test-form').submit(); // Automatically submit the test
    }

    // Start monitoring
    async function startMonitoring() {
        await setupCamera();
        await loadModel();
        setInterval(detectInappropriateMovements, 1000); // Check every second
    }

    // Start monitoring when the page loads
    startMonitoring();