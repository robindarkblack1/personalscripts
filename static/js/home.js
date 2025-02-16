
    window.addEventListener("load", function() {
        document.getElementById("preloader").style.display = "none"; // Hide preloader
        document.body.classList.add("loaded"); // Enable scrolling
    });




// Show context menu
function showContextMenu(event, appName) {
    event.preventDefault(); // Prevent default right-click menu

    const contextMenu = document.getElementById("context-menu");
    contextMenu.style.display = "block";
    contextMenu.style.left = `${event.pageX}px`;
    contextMenu.style.top = `${event.pageY}px`;

    // Store the selected app
    contextMenu.dataset.app = appName;
}

// Hide context menu on click elsewhere
document.addEventListener("click", () => {
    document.getElementById("context-menu").style.display = "none";
});

// Open App Info
function openAppInfo() {
    const appName = document.getElementById("context-menu").dataset.app;
    document.getElementById("app-info-details").textContent = `App: ${appName}`;
    document.getElementById("app-info-modal").style.display = "block";
}

// Close App Info
function closeAppInfo() {
    document.getElementById("app-info-modal").style.display = "none";
}

// Uninstall App (Hide & Store in Local Storage)
function uninstallApp() {
    const appName = document.getElementById("context-menu").dataset.app;
    const icon = document.querySelector(`[data-app="${appName}"]`);
    
    if (icon) {
        icon.style.display = "none"; // Hide icon
        localStorage.setItem(`hidden_${appName}`, "true"); // Store in localStorage
    }
}

// Restore Hidden Icons on Page Load
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".icon-container").forEach(icon => {
        const appName = icon.dataset.app;
        if (localStorage.getItem(`hidden_${appName}`) === "true") {
            icon.style.display = "none";
        }
    });
});


// Restore all hidden icons
function restoreApps() {
    document.querySelectorAll(".icon-container").forEach(icon => {
        const appName = icon.dataset.app;
        localStorage.removeItem(`hidden_${appName}`); // Remove from storage
        icon.style.display = "flex"; // Show icon again
    });
}



function toggleSettings() {
    const settingsMenu = document.getElementById("settings-card");

    if (settingsMenu.classList.contains("show")) {
        // Close Animation (Shrink Back)
        settingsMenu.classList.remove("show");
        setTimeout(() => {
            settingsMenu.style.display = "none";
        }, 400); // Matches transition timing
    } else {
        // Ensure Display Before Animation Starts
        settingsMenu.style.display = "flex";
        requestAnimationFrame(() => {
            settingsMenu.classList.add("show");
        });
    }
}



// Open specific submenu
function openSubmenu(menuId) {
    const menu = document.getElementById(menuId + "-menu");
    menu.style.display = "flex";
    setTimeout(() => {
        menu.classList.add("show");
    }, 10);
}

// Close submenu with animation
function closeSubmenu(menuId) {
    const menu = document.getElementById(menuId);
    const button = document.querySelector('.close-btn .arrow');

    if (menu.classList.contains("show")) {
        // Animate closing
        menu.classList.remove("show");
        button.innerHTML = "→"; // Change to forward arrow
        setTimeout(() => {
            menu.style.display = "none";
        }, 400); // Match animation duration
    } else {
        // Animate opening
        menu.style.display = "block";
        setTimeout(() => {
            menu.classList.add("show");
            button.innerHTML = "←"; // Change to back arrow
        }, 10); // Short delay for smoother effect
    }
}


// Load Wallpaper on Start
window.onload = function () {
    const savedWallpaper = localStorage.getItem("wallpaper");
    if (savedWallpaper) {
        document.body.style.backgroundImage = `url('${savedWallpaper}')`;
    }
};


// Toggle Dark Mode (Affects Only App Cards & Settings Card)
function toggleDarkMode() {
    let darkModeEnabled = document.body.classList.toggle("dark-mode");

    // Save dark mode state
    localStorage.setItem("darkMode", darkModeEnabled ? "enabled" : "disabled");

    // Change text and icon dynamically
    let darkModeIcon = document.getElementById("dark-mode-icon");
    let darkModeText = document.getElementById("dark-mode-text");

    if (darkModeEnabled) {
        darkModeIcon.classList.replace("bi-moon", "bi-sun");
        darkModeText.innerText = "Light Mode";
    } else {
        darkModeIcon.classList.replace("bi-sun", "bi-moon");
        darkModeText.innerText = "Dark Mode";
    }

    // Apply dark mode to all app cards
    document.querySelectorAll(".icon-container").forEach(card => {
        card.classList.toggle("dark-mode-app", darkModeEnabled);
    });

    // Force settings card to apply the correct theme
    let settingsCard = document.querySelector(".settings-card");
    if (darkModeEnabled) {
        settingsCard.classList.add("dark-mode");
        settingsCard.style.background = "#111"; // Dark mode background
        settingsCard.style.color = "#fff"; // Dark mode text color
    } else {
        settingsCard.classList.remove("dark-mode");
        settingsCard.style.background = "#fff"; // Light mode background
        settingsCard.style.color = "#000"; // Light mode text color
    }
}

// Restore Dark Mode on Load (Force Manual Preference)
function applySavedDarkMode() {
    let darkModeEnabled = localStorage.getItem("darkMode") === "enabled";

    if (darkModeEnabled) {
        document.body.classList.add("dark-mode");
        document.getElementById("dark-mode-icon").classList.replace("bi-moon", "bi-sun");
        document.getElementById("dark-mode-text").innerText = "Light Mode";

        document.querySelectorAll(".icon-container").forEach(card => {
            card.classList.add("dark-mode-app");
        });

        let settingsCard = document.querySelector(".settings-card");
        settingsCard.classList.add("dark-mode");
        settingsCard.style.background = "#111";
        settingsCard.style.color = "#fff";
    } else {
        document.body.classList.remove("dark-mode");
        document.getElementById("dark-mode-icon").classList.replace("bi-sun", "bi-moon");
        document.getElementById("dark-mode-text").innerText = "Dark Mode";

        document.querySelectorAll(".icon-container").forEach(card => {
            card.classList.remove("dark-mode-app");
        });

        let settingsCard = document.querySelector(".settings-card");
        settingsCard.classList.remove("dark-mode");
        settingsCard.style.background = "#fff";
        settingsCard.style.color = "#000";
    }
}

// Apply saved mode on load
applySavedDarkMode();





// Function to handle wallpaper change and store it in local storage
function changeWallpaper(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imageData = e.target.result;
            localStorage.setItem("customWallpaper", imageData);
            document.body.style.backgroundImage = `url('${imageData}')`;
        };
        reader.readAsDataURL(file);
    }
}

// Open file picker when "Change Wallpaper" is clicked
function openWallpaperUpload() {
    document.getElementById("wallpaper-upload").click();
}

// Reset wallpaper to default
function resetWallpaper() {
    localStorage.removeItem("customWallpaper");  // Remove from local storage
    document.body.style.backgroundImage = "url('../static/img/vivobg.png')"; // Default wallpaper
}

// Load stored wallpaper on page load
document.addEventListener("DOMContentLoaded", function () {
    const savedWallpaper = localStorage.getItem("customWallpaper");
    if (savedWallpaper) {
        document.body.style.backgroundImage = `url('${savedWallpaper}')`;
    } else {
        document.body.style.backgroundImage = "url('../static/img/vivobg.png')";
    }
});



// Toggle Notifications
function toggleNotifications() {
    alert("Notifications settings are not available yet!");
}

// Toggle Wi-Fi
function toggleWifi() {
    let wifiStatus = document.getElementById("wifi-status");
    if (wifiStatus.innerText === "On") {
        wifiStatus.innerText = "Off";
        wifiStatus.style.color = "red";
    } else {
        wifiStatus.innerText = "On";
        wifiStatus.style.color = "green";
    }
}

// Toggle Bluetooth
function toggleBluetooth() {
    let bluetoothStatus = document.getElementById("bluetooth-status");
    if (bluetoothStatus.innerText === "Off") {
        bluetoothStatus.innerText = "On";
        bluetoothStatus.style.color = "blue";
    } else {
        bluetoothStatus.innerText = "Off";
        bluetoothStatus.style.color = "gray";
    }
}

// Change Language
function changeLanguage() {
    let selectedLanguage = document.getElementById("language-select").value;
    alert("Language changed to: " + selectedLanguage);
}

// Save Security PIN
function savePin() {
    let pin = document.getElementById("pin-input").value;
    if (pin.length >= 4) {
        localStorage.setItem("userPIN", pin);
        alert("PIN saved successfully!");
    } else {
        alert("PIN must be at least 4 digits.");
    }
}

// Logout Function
function logout() {
    alert("Logging out...");
    location.reload();
}
function showAppMenu(menuId) {
    console.log("Opening app details:", menuId);

    // Close all other app submenus before opening a new one
    document.querySelectorAll(".app-submenu").forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove("visible");
        }
    });

    // Open the selected app submenu
    let menu = document.getElementById(menuId);
    if (menu) {
        menu.classList.add("visible");

        // Make sure the menu is draggable
        makeDraggable(menu);
    }
}

function hideAppMenu(menuId) {
    let menu = document.getElementById(menuId);
    if (menu) {
        menu.classList.remove("visible");
    }
}

// Function to make submenus draggable
function makeDraggable(menu) {
    let isDragging = false;
    let offsetX = 0, offsetY = 0;

    // Set default positioning
    menu.style.position = "absolute";
    menu.style.zIndex = "1000"; // Ensure it's above other elements

    menu.onmousedown = (event) => {
        isDragging = true;
        
        // Get the initial cursor position relative to the menu
        offsetX = event.clientX - menu.getBoundingClientRect().left;
        offsetY = event.clientY - menu.getBoundingClientRect().top;

        // Move the menu on mouse move
        document.onmousemove = (e) => {
            if (isDragging) {
                menu.style.left = `${e.clientX - offsetX}px`;
                menu.style.top = `${e.clientY - offsetY}px`;
            }
        };

        // Stop dragging on mouse up
        document.onmouseup = () => {
            isDragging = false;
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };

    // Prevent text selection while dragging
    menu.ondragstart = () => false;
}


document.addEventListener("DOMContentLoaded", function () {
    restoreAppStates(); // Restore states on page load
});



document.addEventListener("DOMContentLoaded", function () {
    restoreAppStates(); // Restore app visibility on page load
});

function toggleButton(buttonId) {
    let button = document.getElementById(buttonId);
    let appName = buttonId.replace('-btn', ''); // Extract app name from button ID
    let appIcon = document.querySelector(`.icon-container[data-app="${appName}"]`);

    let isDisabled = localStorage.getItem(appName) === "disabled"; // Check if disabled

    if (isDisabled) {
        // Enable the app
        button.innerText = "Disable";
        button.style.background = "red";
        localStorage.setItem(appName, "enabled"); // Store state
        if (appIcon) appIcon.style.display = "flex"; // Show app icon
    } else {
        // Disable the app
        button.innerText = "Enable";
        button.style.background = "";
        localStorage.setItem(appName, "disabled"); // Store state
        if (appIcon) appIcon.style.display = "none"; // Hide app icon
    }
}

// Restore app states on page load
function restoreAppStates() {
    let buttons = document.querySelectorAll(".app-info button");

    buttons.forEach(button => {
        let appName = button.id.replace('-btn', ''); // Extract app name
        let appIcon = document.querySelector(`.icon-container[data-app="${appName}"]`);
        let isDisabled = localStorage.getItem(appName) === "disabled"; // Check if disabled

        if (isDisabled) {
            button.innerText = "Enable";
            button.style.background = "";
            if (appIcon) appIcon.style.display = "none"; // Hide app icon
        } else {
            button.innerText = "Disable";
            button.style.background = "red";
            if (appIcon) appIcon.style.display = "flex"; // Show app icon
        }
    });
}













let lastScrollTop = 0;
const notificationCard = document.querySelector(".notification-card");
const smallWindow = document.getElementById("small-window");

// **Disable pull-to-refresh (for mobile)**
document.addEventListener("touchmove", function (event) {
let isInsideSmallWindow = event.target.closest(".small-window"); // Check if inside small window
if (!isInsideSmallWindow) {
    event.preventDefault(); // Prevent scrolling only outside the small window
}
}, { passive: false });

// **Scroll Detection (Laptop/Desktop)**
window.addEventListener("scroll", function () {
let scrollTop = window.scrollY || document.documentElement.scrollTop;

// Prevent triggering notification card if `.small-window` is open
if (smallWindow && smallWindow.style.display === "block") return;  

if (scrollTop > lastScrollTop + 20) { // Scroll down
    notificationCard.classList.add("show");
} else if (scrollTop < lastScrollTop - 20) { // Scroll up
    notificationCard.classList.remove("show");
}

lastScrollTop = scrollTop;
}, { passive: true });

// **Touch Detection (Mobile) - Prevent Notification Swipe in Small Window**
let startY = 0;

document.addEventListener("touchstart", (event) => {
startY = event.touches[0].clientY; // Get initial touch position
}, { passive: true });

document.addEventListener("touchend", (event) => {
let endY = event.changedTouches[0].clientY; // Get touch end position
let diffY = endY - startY;

// Prevent notification from appearing if `.small-window` is open
if (smallWindow && smallWindow.style.display === "block") return;  

if (diffY > 30) { // Swipe Down (Show Notification)
    notificationCard.classList.add("show");
} else if (diffY < -30) { // Swipe Up (Hide Notification)
    notificationCard.classList.remove("show");
}
});

// **Close Small Window Function (If needed)**
function closeWindow() {
smallWindow.style.display = "none"; // Hide the small window
}



    const brightnessSlider = document.getElementById("brightness-slider");

brightnessSlider.addEventListener("input", function() {
let brightness = this.value;
document.body.style.filter = `brightness(${brightness}%)`;
});


document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        let notification = document.getElementById("iphone-notification");
        notification.classList.add("show");

        setTimeout(() => {
            notification.classList.add("hide");
        }, 2000); // Hide after 4 seconds
    }, 3000); // Show after 5 seconds
});

function openNotification(type) {
    let title = "";
    let message = "";
    let url = "";

    switch (type) {
        case 'instagram':
            title = "Instagram";
            message = "Opening Instagram... 📷";
            url = "https://www.instagram.com";
            break;
        case 'github':
            title = "GitHub";
            message = "Opening GitHub... 🛠️";
            url = "https://github.com/robindarkblack1";
            break;
        case 'errors':
            title = "Site Errors";
            message = "Checking for site errors... 🔍";
            break;
        case 'feedback':
            title = "Feedback Alert";
            message = "The Army of Bugs has breached our defenses! 🐞🔥 Pages are crashing, buttons are broken, and chaos is spreading fast! 😱 We sent our best developer to the frontlines… but they vanished without a trace. Only an ominous .'Syntax Error' remained. 👀💀 Now, the fate of our code rests in your hands! 💻⚔️ Will you rise as a hero, or let the bugs claim victory? 😈🐛";
            break;
        default:
            console.log("Unknown notification clicked");
            return;
    }

    // Show the notification card
    showNotification(title, message, url);
}

// Function to display a notification card
function showNotification(title, message, url = "") {
    let notificationCard = document.createElement("div");
    notificationCard.classList.add("custom-notification");

    notificationCard.innerHTML = `
        <div class="notification-icon"><i class="bi bi-bell-fill"></i></div>
        <div class="notification-content">
            <span class="notification-title">${title}</span>
            <p class="notification-message">${message}</p>
        </div>
    `;

    // Add click event to open URL if provided
    if (url) {
        notificationCard.addEventListener("click", function () {
            window.open(url, "_blank");
        });
    }

    // Append to body and show notification
    document.body.appendChild(notificationCard);
    setTimeout(() => {
        notificationCard.classList.add("show");
    }, 100);

    // Auto-hide after 3 seconds
    setTimeout(() => {
        notificationCard.classList.remove("show");
        setTimeout(() => notificationCard.remove(), 500);
    }, 10000);
}




















let jsonData = {};  // Global variable to store JSON data

// Preload JSON data when home.html loads
async function preloadData() {
    try {
        let response = await fetch("static/js/data.json");
        jsonData = await response.json();
    } catch (error) {
        console.error("Error preloading data:", error);
    }
}

// Call the function to preload JSON data when the page loads
window.addEventListener("DOMContentLoaded", preloadData);

// Function to open a window using preloaded data
async function openWindow(type) {
    let title = document.getElementById("window-title");
    let content = document.getElementById("window-content");

    if (jsonData[type]) {
        title.innerText = jsonData[type].title;
        content.innerHTML = jsonData[type].content;
    } else {
        title.innerText = "Not Found";
        content.innerHTML = "<p>No content available.</p>";
    }

    let windowDiv = document.getElementById("small-window");
    windowDiv.style.display = "block";  
    setTimeout(() => {
        windowDiv.classList.add("show");
        windowDiv.classList.remove("hide");
    }, 10);
}

function closeWindow() {
let windowDiv = document.getElementById("small-window");
windowDiv.classList.remove("show");
windowDiv.classList.add("hide");

setTimeout(() => {
    windowDiv.style.display = "none";
    windowDiv.classList.remove("hide");  // Reset for next open
}, 600); // Matches CSS transition duration
}


function openBrowser(url) {
    let browserFrame = document.getElementById("browser-frame");
    let browserLoader = document.getElementById("browser-loader");
    let browserCard = document.getElementById("browser-card");

    console.log("🔄 Attempting to open URL:", url);

    // Show loader
    browserLoader.style.display = "block";

    // Set display to block first, then trigger animation
    browserCard.style.display = "block";
    setTimeout(() => {
        browserCard.classList.add("active"); // Apply animation
    }, 10);

    // Load website through Flask proxy
    browserFrame.src = `/proxy?url=${encodeURIComponent(url)}`;

    // Debug iframe load success
    browserFrame.onload = function () {
        browserLoader.style.display = "none";
        console.log("✅ Iframe loaded successfully:", browserFrame.src);
    };

    // Debug iframe errors
    browserFrame.onerror = function () {
        browserLoader.style.display = "none";
        console.error("❌ Error loading iframe:", browserFrame.src);
    };
}


function openInstagram(url) {
    let browserFrame = document.getElementById("browser-frame");
    let browserLoader = document.getElementById("browser-loader");
    let browserCard = document.getElementById("browser-card");

    console.log("🔄 Attempting to open Instagram:", url);

    // Show loader
    browserLoader.style.display = "block";

    // Set display to block first, then trigger animation
    browserCard.style.display = "block";
    setTimeout(() => {
        browserCard.classList.add("active"); // Apply animation
    }, 10);

    // Load Instagram through proxy
    browserFrame.src = `/instagram-proxy?url=${encodeURIComponent(url)}`;

    // Debug iframe load success
    browserFrame.onload = function () {
        browserLoader.style.display = "none";
        console.log("✅ Instagram loaded successfully:", browserFrame.src);
    };

    // Debug iframe errors
    browserFrame.onerror = function () {
        browserLoader.style.display = "none";
        console.error("❌ Error loading Instagram:", browserFrame.src);
    };
}



function openDirectBrowser(url) {
    let browserFrame = document.getElementById("browser-frame");
    let browserLoader = document.getElementById("browser-loader");
    let browserCard = document.getElementById("browser-card");

    if (!browserFrame || !browserLoader || !browserCard) {
        console.error("Required elements not found!");
        return;
    }

    // Show loader & open browser card smoothly
    browserLoader.style.display = "block";
    browserCard.style.display = "block";
    browserCard.classList.add("active");

    // Directly load the website
    browserFrame.src = url;

    // Hide loader when the iframe loads successfully
    browserFrame.onload = () => {
        browserLoader.style.display = "none";
    };

    // Handle iframe errors properly
    browserFrame.onerror = () => {
        browserLoader.style.display = "none";
        console.error("Error loading website:", url);
    };
}



function closeBrowser() {
    let browserCard = document.getElementById("browser-card");

    // Remove animation class
    browserCard.classList.remove("active");

    // Wait for animation to finish before hiding
    setTimeout(() => {
        browserCard.style.display = "none";
        document.getElementById("browser-frame").src = ""; // Clear iframe for fresh load
    }, 300); // Matches CSS transition duration
}
