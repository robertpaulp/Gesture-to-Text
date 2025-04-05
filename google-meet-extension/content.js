class GestureCaption {
    constructor() {
        this.captionBox = null;
        this.socket = null;
        this.initialize();
    }

    initialize() {
        // Create caption box
        this.createCaptionBox();
        // Connect WebSocket
        this.connectWebSocket();
    }

    createCaptionBox() {
        this.captionBox = document.createElement('div');
        this.captionBox.className = 'gesture-caption-box';
        this.captionBox.textContent = 'Waiting for gestures...';
        document.body.appendChild(this.captionBox);
    }

    connectWebSocket() {
        try {
            this.socket = new WebSocket('ws://localhost:8765');

            this.socket.onopen = () => {
                console.log('Connected to gesture recognition server');
                this.updateCaption('Connected to gesture recognition service');
            };

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.updateCaption(data.text);
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateCaption('Error connecting to gesture service');
            };

            this.socket.onclose = () => {
                console.log('WebSocket connection closed');
                this.updateCaption('Gesture service disconnected');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };
        } catch (error) {
            console.error('Failed to connect:', error);
        }
    }

    updateCaption(text) {
        if (this.captionBox) {
            this.captionBox.textContent = text;
        }
    }
}

// Initialize when the page loads
const gestureCaption = new GestureCaption();