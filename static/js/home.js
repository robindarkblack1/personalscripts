// =================================================== //
// ================ GLOBAL SETUP ===================== //
// =================================================== //

window.addEventListener("load", function() {
    if(document.getElementById("preloader")) {
        document.getElementById("preloader").style.display = "none";
    }
    document.body.classList.add("loaded");
});

// This is the main entry point. It decides whether to run
// the desktop or mobile experience based on screen width.
document.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth >= 768) {
        initializeDesktopUI();
    } else {
        initializeMobileListeners();
    }
});


// =================================================== //
// ============ DESKTOP UI INITIALIZATION ============ //
// =================================================== //

function initializeDesktopUI() {
    const apps = [
        { id: 'bio', name: 'My Bio', type: 'json', content: 'bio', icon: 'bi-person-badge' },
        { id: 'projects', name: 'Projects', type: 'json', content: 'projects', icon: 'bi-grid-fill' },
        { id: 'todo', name: 'Todo App', type: 'iframe', content: '/dashboard', icon: 'bi-journal-plus' },
        { id: 'chat', name: 'Click-Chat', type: 'iframe', content: 'https://chat.clickearn.me', icon: 'bi-chat-dots' },
        { id: 'downloader', name: 'Downloader', type: 'iframe', content: 'https://clickearn.me/Youtube-video-download', icon: 'bi-cloud-arrow-down' },
        { id: 'instagram', name: 'Instagram', type: 'iframe', content: 'https://www.instagram.com', icon: 'bi-instagram', proxy: 'instagram' },
        { id: 'linkedin', name: 'LinkedIn', type: 'iframe', content: 'https://www.linkedin.com/in/prdeep-verma-4a1364257/', icon: 'bi-linkedin' },
        { id: 'github', name: 'GitHub', type: 'iframe', content: 'https://github.com/robindarkblack1', icon: 'bi-github', proxy: true },
        { id: 'activities', name: 'Activities', type: 'json', content: 'activities', icon: 'bi-lightning-charge-fill' },
        { id: 'settings', name: 'Settings', type: 'html-clone', content: '#settings-card', icon: 'bi-gear-fill' },
    ];

    const desktopIconsContainer = document.getElementById('desktop-icons');
    const startMenuAppsContainer = document.getElementById('start-menu-apps');
    const startButton = document.getElementById('start-button');
    const startMenu = document.getElementById('start-menu');
    const desktopTime = document.getElementById('desktop-time');

    apps.forEach(app => {
        const desktopIcon = document.createElement('div');
        desktopIcon.className = 'desktop-icon';
        desktopIcon.innerHTML = `<div class="icon-image-wrapper"><i class="bi ${app.icon}"></i></div><div class="icon-label">${app.name}</div>`;
        desktopIcon.addEventListener('dblclick', () => createWindow(app));
        desktopIconsContainer.appendChild(desktopIcon);

        const startMenuItem = document.createElement('div');
        startMenuItem.className = 'start-menu-app';
        startMenuItem.innerHTML = `<i class="bi ${app.icon}" style="font-size: 24px;"></i> <span>${app.name}</span>`;
        startMenuItem.addEventListener('click', () => {
            createWindow(app);
            if(startMenu) startMenu.style.display = 'none';
        });
        startMenuAppsContainer.appendChild(startMenuItem);
    });

    if(startButton) startButton.addEventListener('click', (e) => {
        e.stopPropagation();
        if(startMenu) startMenu.style.display = startMenu.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', () => {
        if(startMenu) startMenu.style.display = 'none';
    });
    
    if(startMenu) startMenu.addEventListener('click', e => e.stopPropagation());

    function updateClock() {
        const now = new Date();
        if(desktopTime) desktopTime.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    setInterval(updateClock, 1000);
    updateClock();
}


// =================================================== //
// ================ WINDOW MANAGEMENT ================ //
// =================================================== //

let zIndexCounter = 100;
let openWindows = {};

async function createWindow(app) {
    if (openWindows[app.id]) {
        focusWindow(openWindows[app.id].element);
        return;
    }

    const windowEl = document.createElement('div');
    windowEl.id = `window-${app.id}`;
    windowEl.className = 'app-window';
    windowEl.style.zIndex = zIndexCounter++;
    windowEl.style.top = `${Math.random() * 15 + 5}%`;
    windowEl.style.left = `${Math.random() * 25 + 15}%`;

    windowEl.innerHTML = `
        <div class="window-header">
            <span class="window-title">${app.name}</span>
            <div class="window-controls">
                <button class="window-control-btn minimize-btn">-</button>
                <button class="window-control-btn maximize-btn">□</button>
                <button class="window-control-btn close-btn">×</button>
            </div>
        </div>
        <div class="window-body"><div class="loader"></div></div>
    `;
    document.getElementById('desktop-view').appendChild(windowEl);

    const windowBody = windowEl.querySelector('.window-body');
    const loader = windowBody.querySelector('.loader');

    if (app.type === 'iframe') {
        const iframe = document.createElement('iframe');
        if (app.proxy === true) {
            iframe.src = `/proxy?url=${encodeURIComponent(app.content)}`;
        } else if (app.proxy === 'instagram') {
            iframe.src = `/instagram-proxy?url=${encodeURIComponent(app.content)}`;
        } else {
            iframe.src = app.content;
        }
        iframe.onload = () => { if(loader) loader.style.display = 'none'; };
        windowBody.appendChild(iframe);
    } else if (app.type === 'json') {
        const data = await getJsonData();
        const contentHtml = data[app.content] ? data[app.content].content : '<p>Content not found.</p>';
        const contentDiv = document.createElement('div');
        contentDiv.className = 'window-body-content';
        contentDiv.innerHTML = contentHtml;
        if(loader) loader.remove();
        windowBody.appendChild(contentDiv);

        // **FIX:** Make icons inside the window open new windows
        contentDiv.querySelectorAll('.icon-container[onclick]').forEach(icon => {
            const onclickAttr = icon.getAttribute('onclick');
            icon.removeAttribute('onclick'); // Prevent original behavior
            icon.addEventListener('click', () => {
                const browserMatch = onclickAttr.match(/openBrowser\(['"](.*?)['"]\)/);
                const instaMatch = onclickAttr.match(/openInstagram\(['"](.*?)['"]\)/);
                
                let url, appName, needsProxy, needsInstaProxy;

                if (browserMatch && browserMatch[1]) {
                    url = browserMatch[1];
                    appName = icon.querySelector('.icon-label')?.textContent || 'Browser';
                    needsProxy = true;
                } else if (instaMatch && instaMatch[1]) {
                    url = instaMatch[1];
                    appName = icon.querySelector('.icon-label')?.textContent || 'Instagram';
                    needsInstaProxy = true;
                }

                if (url) {
                    const newApp = {
                        id: `browser-${Date.now()}`,
                        name: appName,
                        type: 'iframe',
                        content: url,
                        icon: 'bi-browser-chrome',
                        proxy: needsProxy,
                        proxyInsta: needsInstaProxy
                    };
                    createWindow(newApp);
                }
            });
        });
    } else if (app.type === 'html-clone') {
        const sourceElement = document.querySelector(app.content);
        if (sourceElement) {
            const clonedElement = sourceElement.cloneNode(true);
            clonedElement.style.cssText = 'display:flex; width:100%; height:100%; position:relative; transform:none; top:auto; left:auto;';
            if(loader) loader.remove();
            windowBody.appendChild(clonedElement);
            initializeClonedSettings(clonedElement);
        }
    }

    const taskbarIcon = document.createElement('div');
    taskbarIcon.id = `taskbar-${app.id}`;
    taskbarIcon.className = 'taskbar-app-icon active';
    taskbarIcon.innerHTML = `<i class="bi ${app.icon}"></i> <span>${app.name}</span>`;
    document.getElementById('taskbar-apps').appendChild(taskbarIcon);
    
    openWindows[app.id] = { element: windowEl, taskbarIcon: taskbarIcon, minimized: false };

    makeDraggable(windowEl);
    setupWindowControls(app.id);
    windowEl.addEventListener('mousedown', () => focusWindow(windowEl));
    taskbarIcon.addEventListener('click', () => handleTaskbarClick(app.id));
    focusWindow(windowEl);
}

function setupWindowControls(appId) {
    const windowEl = openWindows[appId].element;
    const closeBtn = windowEl.querySelector('.close-btn');
    const maximizeBtn = windowEl.querySelector('.maximize-btn');
    const minimizeBtn = windowEl.querySelector('.minimize-btn');

    closeBtn.addEventListener('click', (e) => { e.stopPropagation(); closeWindow(appId); });
    maximizeBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleMaximize(appId); });
    minimizeBtn.addEventListener('click', (e) => { e.stopPropagation(); minimizeWindow(appId); });
}

function closeWindow(appId) {
    if (openWindows[appId]) {
        openWindows[appId].element.remove();
        openWindows[appId].taskbarIcon.remove();
        delete openWindows[appId];
    }
}

function toggleMaximize(appId) {
    openWindows[appId].element.classList.toggle('maximized');
}

function minimizeWindow(appId) {
    const win = openWindows[appId];
    win.element.style.display = 'none';
    win.taskbarIcon.classList.add('minimized');
    win.taskbarIcon.classList.remove('active');
    win.minimized = true;
}

function handleTaskbarClick(appId) {
    const win = openWindows[appId];
    if (win.minimized) {
        win.element.style.display = 'flex';
        win.minimized = false;
        focusWindow(win.element);
    } else {
        win.taskbarIcon.classList.contains('active') ? minimizeWindow(appId) : focusWindow(win.element);
    }
}

function focusWindow(windowEl) {
    windowEl.style.zIndex = zIndexCounter++;
    Object.values(openWindows).forEach(win => {
        const isActive = win.element === windowEl;
        win.taskbarIcon.classList.toggle('active', isActive);
        if(isActive) {
            win.taskbarIcon.classList.remove('minimized');
            win.minimized = false;
        }
    });
}

function makeDraggable(el) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    const header = el.querySelector(".window-header");
    if (header) header.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        if (e.target.classList.contains('window-control-btn')) {
            return;
        }
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        window.onmouseup = closeDragElement;
        window.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();
        if (el.classList.contains('maximized')) return;
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        el.style.top = (el.offsetTop - pos2) + "px";
        el.style.left = (el.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        window.onmouseup = null;
        window.onmousemove = null;
    }
}

let jsonData = {};
async function getJsonData() {
    if (Object.keys(jsonData).length === 0) {
        try {
            let response = await fetch("static/js/data.json");
            jsonData = await response.json();
        } catch (error) { console.error("Error loading data.json:", error); }
    }
    return jsonData;
}

function initializeClonedSettings(clonedElement) {
    const submenus = clonedElement.querySelectorAll('.settings-submenu');
    clonedElement.querySelectorAll('.settings-item[onclick]').forEach(item => {
        const onclickAttr = item.getAttribute('onclick');
        item.onclick = null; // Remove original to prevent conflicts
        
        const submenuMatch = onclickAttr.match(/openSubmenu\(['"](.*?)['"]\)/);
        if (submenuMatch && submenuMatch[1]) {
            item.addEventListener('click', () => {
                const targetSubmenu = clonedElement.querySelector(`#${submenuMatch[1]}-menu`);
                submenus.forEach(sm => sm.classList.remove('show'));
                if (targetSubmenu) targetSubmenu.classList.add('show');
            });
        } else {
            // For other buttons like dark mode, etc.
            item.addEventListener('click', () => {
                try { eval(onclickAttr); } catch(e) { console.error("Error in cloned settings:", e); }
            });
        }
    });

    submenus.forEach(submenu => {
        const closeBtn = submenu.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.onclick = null;
            closeBtn.addEventListener('click', () => submenu.classList.remove('show'));
        }
    });
}

// =================================================== //
// =========== ORIGINAL MOBILE-ONLY SCRIPT =========== //
// =================================================== //

function initializeMobileListeners() {
    document.addEventListener("click", () => {
        const contextMenu = document.getElementById("context-menu");
        if (contextMenu) contextMenu.style.display = "none";
    });

    document.querySelectorAll(".icon-container").forEach(icon => {
        const appName = icon.dataset.app;
        if (localStorage.getItem(`hidden_${appName}`) === "true") icon.style.display = "none";
    });
    
    const tempSpan = document.querySelector('.time .small-text:last-child');
    if (tempSpan && tempSpan.textContent.trim().startsWith('°c')) {
        tempSpan.style.display = 'none';
    }

    preloadData();
    applySavedDarkMode();
    restoreAppStates();
    
    const savedWallpaper = localStorage.getItem("customWallpaper");
    document.body.style.backgroundImage = savedWallpaper ? `url('${savedWallpaper}')` : "url('../static/img/vivobg.png')";
}

function showContextMenu(event, appName) {
    event.preventDefault();
    event.stopPropagation();
    const contextMenu = document.getElementById("context-menu");
    contextMenu.style.display = "block";
    contextMenu.style.left = `${event.pageX}px`;
    contextMenu.style.top = `${event.pageY}px`;
    contextMenu.dataset.app = appName;
}

function uninstallApp() {
    const appName = document.getElementById("context-menu").dataset.app;
    const icon = document.querySelector(`.mobile-view [data-app="${appName}"]`);
    if (icon) {
        icon.style.display = "none";
        localStorage.setItem(`hidden_${appName}`, "true");
    }
}

function toggleSettings() {
    const settingsMenu = document.getElementById("settings-card");
    settingsMenu.style.display = "flex";
    requestAnimationFrame(() => settingsMenu.classList.toggle("show"));
}

function openSubmenu(menuId) {
    const menu = document.getElementById(menuId + "-menu");
    if(menu) {
        menu.style.display = "flex";
        setTimeout(() => menu.classList.add("show"), 10);
    }
}

function closeSubmenu(menuId) {
    const menu = document.getElementById(menuId);
    if(menu) {
        menu.classList.remove("show");
        setTimeout(() => { menu.style.display = "none"; }, 400);
    }
}

function toggleDarkMode() {
    let darkModeEnabled = document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", darkModeEnabled ? "enabled" : "disabled");
    applySavedDarkMode();
}

function applySavedDarkMode() {
    let darkModeEnabled = localStorage.getItem("darkMode") === "enabled";
    document.body.classList.toggle("dark-mode", darkModeEnabled);
    const darkModeIcon = document.getElementById("dark-mode-icon");
    const darkModeText = document.getElementById("dark-mode-text");
    if (darkModeIcon) darkModeIcon.className = darkModeEnabled ? "bi bi-sun" : "bi bi-moon";
    if (darkModeText) darkModeText.innerText = darkModeEnabled ? "Light Mode" : "Dark Mode";
}

function changeWallpaper(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            localStorage.setItem("customWallpaper", e.target.result);
            document.body.style.backgroundImage = `url('${e.target.result}')`;
        };
        reader.readAsDataURL(file);
    }
}

function openWallpaperUpload() { document.getElementById("wallpaper-upload").click(); }
function resetWallpaper() {
    localStorage.removeItem("customWallpaper");
    document.body.style.backgroundImage = "url('../static/img/vivobg.png')";
}

async function openWindow(type) {
    const title = document.getElementById("window-title");
    const content = document.getElementById("window-content");
    const data = await getJsonData();
    if (data[type]) {
        title.innerText = data[type].title;
        content.innerHTML = data[type].content;
    }
    let windowDiv = document.getElementById("small-window");
    windowDiv.style.display = "block";  
    setTimeout(() => { windowDiv.classList.add("show"); }, 10);
}

function closeWindow() { // Renamed from closeMobileWindow to avoid confusion
    let windowDiv = document.getElementById("small-window");
    windowDiv.classList.remove("show");
    setTimeout(() => { windowDiv.style.display = "none"; }, 600);
}

function openBrowser(url) {
    const browserCard = document.getElementById("browser-card");
    const browserFrame = document.getElementById("browser-frame");
    const browserLoader = document.getElementById("browser-loader");
    if(browserLoader) browserLoader.style.display = "block";
    if(browserCard) browserCard.style.display = "block";
    setTimeout(() => browserCard.classList.add("active"), 10);
    if(browserFrame) {
        browserFrame.src = `/proxy?url=${encodeURIComponent(url)}`;
        browserFrame.onload = () => { if(browserLoader) browserLoader.style.display = "none"; };
    }
}

function openInstagram(url) {
    const browserCard = document.getElementById("browser-card");
    const browserFrame = document.getElementById("browser-frame");
    const browserLoader = document.getElementById("browser-loader");
    if(browserLoader) browserLoader.style.display = "block";
    if(browserCard) browserCard.style.display = "block";
    setTimeout(() => browserCard.classList.add("active"), 10);
    if(browserFrame) {
        browserFrame.src = `/instagram-proxy?url=${encodeURIComponent(url)}`;
        browserFrame.onload = () => { if(browserLoader) browserLoader.style.display = "none"; };
    }
}

function closeBrowser() {
    const browserCard = document.getElementById("browser-card");
    browserCard.classList.remove("active");
    setTimeout(() => {
        browserCard.style.display = "none";
        document.getElementById("browser-frame").src = "about:blank";
    }, 300);
}

function openFeedback() {
    let feedbackCard = document.getElementById('feedback-card');
    if(feedbackCard) feedbackCard.style.display = 'block';
}

function closeFeedback() {
    let feedbackCard = document.getElementById('feedback-card');
    if(feedbackCard) feedbackCard.style.display = 'none';
}

function restoreAppStates() {
    document.querySelectorAll(".app-info button").forEach(button => {
        let appName = button.id.replace('-btn', '');
        let appIcon = document.querySelector(`.icon-container[data-app="${appName}"]`);
        let isDisabled = localStorage.getItem(appName) === "disabled";
        button.innerText = isDisabled ? "Enable" : "Disable";
        if (appIcon) appIcon.style.display = isDisabled ? "none" : "flex";
    });
}
