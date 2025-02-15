 
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




async function openWindow(type) {
    let title = document.getElementById("window-title");
    let content = document.getElementById("window-content");

    try {
        let response = await fetch("data.json");
        let jsonData = await response.json();

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
    } catch (error) {
        console.error("Error loading data:", error);
    }
}

function closeWindow() {
    let windowDiv = document.getElementById("small-window");
    windowDiv.classList.remove("show");
    windowDiv.classList.add("hide");

    setTimeout(() => {
        windowDiv.style.display = "none";
        windowDiv.classList.remove("hide");
    }, 600);
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
