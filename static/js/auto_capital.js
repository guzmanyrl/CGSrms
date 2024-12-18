function capitalizeFirstLetter(event) {
    const input = event.target;
    const value = input.value;

    // Auto-capitalize the first letter as soon as the user types
    if (value.length === 1) {
        input.value = value.charAt(0).toUpperCase();
    }
}

// Add event listeners to each input field
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.input-box input');
    inputs.forEach(input => {
        // Capitalize on input for auto-updating
        input.addEventListener('input', capitalizeFirstLetter);

        // Listen for 'keydown' to detect user intent
        input.addEventListener('keydown', function (event) {
            const isShiftPressed = event.shiftKey;
            const isCapsLockOn = event.getModifierState && event.getModifierState('CapsLock');

            // Respect user intent for lowercase if Shift or Caps Lock is used
            if (isShiftPressed || isCapsLockOn) {
                // Do nothing, let the user control the case
                return;
            }
        });
    });
});
