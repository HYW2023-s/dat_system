/**
 * DAT System - API Client
 * Handles authentication, API calls, and token management.
 */

const API_BASE = "/api";

// --- Token Management ---

function getToken() {
  return localStorage.getItem("dat_token");
}

function setToken(token) {
  localStorage.setItem("dat_token", token);
}

function clearToken() {
  localStorage.removeItem("dat_token");
  localStorage.removeItem("dat_username");
  localStorage.removeItem("dat_is_superuser");
}

function isLoggedIn() {
  return !!getToken();
}

function getUserInfo() {
  return {
    username: localStorage.getItem("dat_username"),
    isSuperuser: localStorage.getItem("dat_is_superuser") === "true",
  };
}

function setUserInfo(username, isSuperuser) {
  localStorage.setItem("dat_username", username);
  localStorage.setItem("dat_is_superuser", String(isSuperuser));
}

// --- API Calls ---

async function api(method, path, data = null) {
  const url = API_BASE + path;
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };

  const token = getToken();
  if (token) {
    opts.headers["Authorization"] = `Bearer ${token}`;
  }

  if (data && method !== "GET") {
    opts.body = JSON.stringify(data);
  }

  const response = await fetch(url, opts);

  if (response.status === 401) {
    clearToken();
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (response.status === 403) {
    throw new Error("Forbidden");
  }

  // Handle file downloads
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("text/csv") || contentType.includes("spreadsheetml")) {
    const blob = await response.blob();
    const disposition = response.headers.get("content-disposition") || "";
    const match = disposition.match(/filename=(.+)/);
    const filename = match ? match[1] : "export.csv";
    downloadBlob(blob, filename);
    return { _downloaded: true, filename };
  }

  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.detail || "Request failed");
  }
  return json;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// --- Convenience Methods ---

const apiGet = (path) => api("GET", path);
const apiPost = (path, data) => api("POST", path, data);
const apiPut = (path, data) => api("PUT", path, data);

// --- Auth ---

async function login(username, password) {
  const result = await apiPost("/auth/login", { username, password });
  setToken(result.access_token);
  setUserInfo(result.username, result.is_superuser);
  return result;
}

function logout() {
  clearToken();
  window.location.href = "/login";
}

// --- Navigation Guard ---

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "/login";
    return false;
  }
  return true;
}

function requireAdmin() {
  if (!requireAuth()) return false;
  const user = getUserInfo();
  if (!user.isSuperuser) {
    window.location.href = "/test";
    return false;
  }
  return true;
}

// --- Toast Notifications ---

function showToast(message, type = "info") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.2s";
    setTimeout(() => toast.remove(), 200);
  }, 3000);
}

// --- Navbar Rendering ---

function renderNavbar(activePage = "") {
  const user = getUserInfo();
  const nav = document.getElementById("navbar");
  if (!nav) return;

  const isAdmin = user.isSuperuser;

  let adminLinks = "";
  if (isAdmin) {
    adminLinks = `
      <a href="/analysis" class="${activePage === "analysis" ? "active" : ""}">
        <i class="ph ph-chart-bar"></i> 数据分析
      </a>
      <a href="/admin" class="${activePage === "admin" ? "active" : ""}">
        <i class="ph ph-gear"></i> 管理
      </a>
    `;
  }

  nav.innerHTML = `
    <a href="/introduction" class="navbar-brand">
      <i class="ph ph-brain"></i> DAT System
    </a>
    <ul class="navbar-nav">
      <li><a href="/introduction" class="${activePage === "introduction" ? "active" : ""}">
        <i class="ph ph-book-open"></i> 任务介绍
      </a></li>
      <li><a href="/test" class="${activePage === "test" ? "active" : ""}">
        <i class="ph ph-pencil-line"></i> 开始测试
      </a></li>
      <li><a href="/results" class="${activePage === "results" ? "active" : ""}">
        <i class="ph ph-list-numbers"></i> 结果查询
      </a></li>
      ${adminLinks}
    </ul>
    <div class="navbar-user">
      <span><i class="ph ph-user"></i> ${user.username || ""}</span>
      <button class="btn-logout" onclick="logout()">退出</button>
    </div>
  `;
}
